#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py - Serveur Flask pour GrabSong V3

FONCTIONNALITÉ:
  - Serveur HTTP qui reçoit les requêtes de l'extension Chrome
  - Télécharge les vidéos YouTube via yt-dlp
  - Organise automatiquement les fichiers MP3
  - Retourne le statut en temps réel
  
UTILISATION:
  python app.py
  
  Le serveur démarre sur http://localhost:5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from datetime import datetime
import threading
import time

# Import des modules
from downloader import YouTubeDownloader
from organizer import MusicOrganizer

# ============================================
# CONFIGURATION
# ============================================

app = Flask(__name__)
CORS(app)  # Permettre les requêtes depuis l'extension Chrome

# Dossiers
BASE_DIR = Path(__file__).parent.parent
TEMP_DIR = BASE_DIR / "temp"
MUSIC_DIR = BASE_DIR / "music"

# Créer les dossiers
TEMP_DIR.mkdir(exist_ok=True)
MUSIC_DIR.mkdir(exist_ok=True)

print(f"📁 Temp: {TEMP_DIR}")
print(f"📁 Music: {MUSIC_DIR}")

# Instances
downloader = YouTubeDownloader(TEMP_DIR, MUSIC_DIR)
organizer = MusicOrganizer(MUSIC_DIR)

# État global
download_status = {
    'in_progress': False,
    'current_download': None,
    'last_completed': None,
    'last_error': None,
    'progress': None
}

# Lock pour éviter les téléchargements simultanés
download_lock = threading.Lock()

# ============================================
# ROUTES
# ============================================

@app.route('/ping', methods=['GET'])
def ping():
    """Test de connexion"""
    return jsonify({
        'status': 'ok',
        'message': 'GrabSong V3 server is running',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/status', methods=['GET'])
def get_status():
    """Retourne le statut du téléchargement en cours"""
    status = download_status.copy()
    
    # Ajouter la progression si un téléchargement est en cours
    if status['in_progress']:
        status['progress'] = downloader.get_progress()
    
    return jsonify(status)


@app.route('/download', methods=['POST'])
def download():
    """
    Lance un téléchargement
    
    Body:
    {
        "url": "https://music.youtube.com/watch?v=...",
        "artist": "Artist Name",
        "album": "Album Name",
        "title": "Song Title",
        "year": "2024"
    }
    """
    # Vérifier si un téléchargement est déjà en cours
    if download_lock.locked():
        return jsonify({
            'success': False,
            'error': 'Un téléchargement est déjà en cours'
        }), 409
    
    try:
        data = request.get_json()
        
        # Valider les données
        if not data.get('url'):
            return jsonify({
                'success': False,
                'error': 'URL manquante'
            }), 400
        
        url = data['url']
        metadata = {
            'artist': data.get('artist', 'Unknown Artist'),
            'album': data.get('album', 'Unknown Album'),
            'title': data.get('title', 'Unknown Title'),
            'year': data.get('year', '')
        }
        
        print(f"\n{'='*60}")
        print(f"🎵 NOUVELLE REQUÊTE DE TÉLÉCHARGEMENT")
        print(f"{'='*60}")
        print(f"URL: {url}")
        print(f"Artiste: {metadata['artist']}")
        print(f"Album: {metadata['album']}")
        print(f"Titre: {metadata['title']}")
        print(f"Année: {metadata['year']}")
        print(f"{'='*60}\n")
        
        # Lancer le téléchargement dans un thread séparé
        download_thread = threading.Thread(
            target=process_download,
            args=(url, metadata)
        )
        download_thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Téléchargement démarré',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/cleanup', methods=['POST'])
def cleanup():
    """Nettoie le dossier temp/"""
    try:
        print("\n🧹 Nettoyage du dossier temp/...")
        
        deleted_files = []
        
        if TEMP_DIR.exists():
            for file in TEMP_DIR.iterdir():
                if file.is_file():
                    file.unlink()
                    deleted_files.append(file.name)
                    print(f"   🗑️ Supprimé: {file.name}")
        
        print(f"✅ Nettoyage terminé: {len(deleted_files)} fichier(s) supprimé(s)\n")
        
        # Reset le statut
        download_status['in_progress'] = False
        download_status['current_download'] = None
        download_status['last_error'] = None
        
        return jsonify({
            'success': True,
            'deleted_files': deleted_files
        })
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Retourne les statistiques de la bibliothèque musicale"""
    stats = organizer.get_stats()
    return jsonify(stats)


# ============================================
# FONCTIONS
# ============================================

def process_download(url, metadata):
    """
    Traite un téléchargement (télécharge + organise)
    Exécuté dans un thread séparé
    """
    with download_lock:
        try:
            # Marquer comme en cours
            download_status['in_progress'] = True
            download_status['current_download'] = {
                'url': url,
                'metadata': metadata,
                'started_at': datetime.now().isoformat()
            }
            download_status['last_error'] = None
            
            # Étape 1: Télécharger
            print("📥 Étape 1/2: Téléchargement...")
            download_result = downloader.download(url, metadata)
            
            if not download_result['success']:
                raise Exception(download_result.get('error', 'Erreur inconnue'))
            
            file_path = download_result['file_path']
            print(f"✅ Téléchargement terminé: {file_path}")
            
            # Étape 2: Organiser
            print("\n📁 Étape 2/2: Organisation...")
            organize_result = organizer.organize(file_path, metadata)
            
            if not organize_result['success']:
                raise Exception(organize_result.get('error', 'Erreur inconnue'))
            
            final_path = organize_result['final_path']
            print(f"✅ Organisation terminée: {final_path}")
            
            # Succès
            download_status['in_progress'] = False
            download_status['current_download'] = None
            download_status['last_completed'] = {
                'success': True,
                'file_path': final_path,
                'metadata': metadata,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"\n{'='*60}")
            print(f"✅ TÉLÉCHARGEMENT TERMINÉ AVEC SUCCÈS")
            print(f"{'='*60}")
            print(f"Fichier: {final_path}")
            print(f"{'='*60}\n")
            
        except Exception as e:
            # Erreur
            print(f"\n{'='*60}")
            print(f"❌ ERREUR LORS DU TÉLÉCHARGEMENT")
            print(f"{'='*60}")
            print(f"Erreur: {str(e)}")
            print(f"{'='*60}\n")
            
            download_status['in_progress'] = False
            download_status['current_download'] = None
            download_status['last_error'] = {
                'error': str(e),
                'metadata': metadata,
                'timestamp': datetime.now().isoformat()
            }


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎵 GrabSong V3 - Serveur Python")
    print("="*60)
    print(f"📁 Dossier temporaire: {TEMP_DIR}")
    print(f"📁 Bibliothèque musicale: {MUSIC_DIR}")
    print("="*60)
    print("🚀 Serveur démarré sur http://localhost:5000")
    print("="*60)
    print("\n💡 Endpoints disponibles:")
    print("   GET  /ping      → Test de connexion")
    print("   GET  /status    → Statut du téléchargement")
    print("   POST /download  → Lancer un téléchargement")
    print("   POST /cleanup   → Nettoyer le dossier temp/")
    print("   GET  /stats     → Statistiques de la bibliothèque")
    print("\n" + "="*60 + "\n")
    
    # Lancer le serveur
    app.run(
        host='localhost',
        port=5000,
        debug=True,
        use_reloader=False  # Éviter le double démarrage en mode debug
    )
