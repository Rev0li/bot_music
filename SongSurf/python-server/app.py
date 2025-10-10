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

# Fix pour l'encodage Windows
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from datetime import datetime
import threading
import time
import queue

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

# Système de queue
MAX_QUEUE_SIZE = 10
download_queue = queue.Queue(maxsize=MAX_QUEUE_SIZE)
queue_lock = threading.Lock()
cancel_flag = threading.Event()

# État global
download_status = {
    'in_progress': False,
    'current_download': None,
    'last_completed': None,
    'last_error': None,
    'progress': None,
    'queue_size': 0,
    'queue_position': 0
}

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
    with queue_lock:
        status = download_status.copy()
        status['queue_size'] = download_queue.qsize()
        
        # Ajouter la progression si un téléchargement est en cours
        if status['in_progress']:
            status['progress'] = downloader.get_progress()
        
        return jsonify(status)


@app.route('/download', methods=['POST'])
def download():
    """
    Ajoute un téléchargement à la queue
    
    Body:
    {
        "url": "https://music.youtube.com/watch?v=...",
        "artist": "Artist Name",
        "album": "Album Name",
        "title": "Song Title",
        "year": "2024"
    }
    """
    try:
        data = request.get_json()
        
        # Valider les données
        if not data.get('url'):
            return jsonify({
                'success': False,
                'error': 'URL manquante'
            }), 400
        
        # Vérifier si la queue est pleine
        if download_queue.full():
            return jsonify({
                'success': False,
                'error': f'Queue pleine (max {MAX_QUEUE_SIZE} téléchargements)'
            }), 429
        
        url = data['url']
        metadata = {
            'artist': data.get('artist', 'Unknown Artist'),
            'album': data.get('album', 'Unknown Album'),
            'title': data.get('title', 'Unknown Title'),
            'year': data.get('year', '')
        }
        
        # Ajouter à la queue
        download_queue.put({
            'url': url,
            'metadata': metadata,
            'added_at': datetime.now().isoformat()
        })
        
        queue_size = download_queue.qsize()
        
        print(f"\n{'='*60}")
        print(f"➕ AJOUTÉ À LA QUEUE (Position {queue_size}/{MAX_QUEUE_SIZE})")
        print(f"{'='*60}")
        print(f"URL: {url}")
        print(f"Artiste: {metadata['artist']}")
        print(f"Album: {metadata['album']}")
        print(f"Titre: {metadata['title']}")
        print(f"Année: {metadata['year']}")
        print(f"{'='*60}\n")
        
        return jsonify({
            'success': True,
            'message': 'Ajouté à la queue',
            'queue_position': queue_size,
            'queue_size': queue_size,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/cancel', methods=['POST'])
def cancel_download():
    """Annule le téléchargement en cours"""
    try:
        if not download_status['in_progress']:
            return jsonify({
                'success': False,
                'error': 'Aucun téléchargement en cours'
            }), 400
        
        print("\n🛑 ANNULATION DU TÉLÉCHARGEMENT EN COURS...")
        cancel_flag.set()
        
        return jsonify({
            'success': True,
            'message': 'Téléchargement annulé'
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

def queue_worker():
    """
    Worker qui traite la queue de téléchargements
    Tourne en boucle infinie dans un thread séparé
    """
    print("🔄 Queue worker démarré\n")
    
    while True:
        try:
            # Attendre un élément dans la queue (bloquant)
            item = download_queue.get()
            
            if item is None:  # Signal d'arrêt
                break
            
            url = item['url']
            metadata = item['metadata']
            
            # Réinitialiser le flag d'annulation
            cancel_flag.clear()
            
            # Marquer comme en cours
            with queue_lock:
                download_status['in_progress'] = True
                download_status['current_download'] = {
                    'url': url,
                    'metadata': metadata,
                    'started_at': datetime.now().isoformat()
                }
                download_status['last_error'] = None
            
            print(f"\n{'='*60}")
            print(f"🎵 DÉMARRAGE DU TÉLÉCHARGEMENT")
            print(f"{'='*60}")
            print(f"Queue restante: {download_queue.qsize()}")
            print(f"Artiste: {metadata['artist']}")
            print(f"Album: {metadata['album']}")
            print(f"Titre: {metadata['title']}")
            print(f"{'='*60}\n")
            
            try:
                # Étape 1: Télécharger
                print("📥 Étape 1/2: Téléchargement...")
                download_result = downloader.download(url, metadata)
                
                # Vérifier annulation
                if cancel_flag.is_set():
                    raise Exception("Téléchargement annulé par l'utilisateur")
                
                if not download_result['success']:
                    raise Exception(download_result.get('error', 'Erreur inconnue'))
                
                file_path = download_result['file_path']
                print(f"✅ Téléchargement terminé: {file_path}")
                
                # Vérifier annulation
                if cancel_flag.is_set():
                    raise Exception("Téléchargement annulé par l'utilisateur")
                
                # Étape 2: Organiser
                print("\n📁 Étape 2/2: Organisation...")
                organize_result = organizer.organize(file_path, metadata)
                
                if not organize_result['success']:
                    raise Exception(organize_result.get('error', 'Erreur inconnue'))
                
                final_path = organize_result['final_path']
                print(f"✅ Organisation terminée: {final_path}")
                
                # Succès
                with queue_lock:
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
                print(f"Queue restante: {download_queue.qsize()}")
                print(f"{'='*60}\n")
                
            except Exception as e:
                # Erreur
                print(f"\n{'='*60}")
                print(f"❌ ERREUR LORS DU TÉLÉCHARGEMENT")
                print(f"{'='*60}")
                print(f"Erreur: {str(e)}")
                print(f"{'='*60}\n")
                
                with queue_lock:
                    download_status['in_progress'] = False
                    download_status['current_download'] = None
                    download_status['last_error'] = {
                        'error': str(e),
                        'metadata': metadata,
                        'timestamp': datetime.now().isoformat()
                    }
            
            # Marquer la tâche comme terminée
            download_queue.task_done()
            
        except Exception as e:
            print(f"❌ Erreur dans le queue worker: {str(e)}")
            time.sleep(1)


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎵 SongSurf - Serveur Python avec Queue")
    print("="*60)
    print(f"📁 Dossier temporaire: {TEMP_DIR}")
    print(f"📁 Bibliothèque musicale: {MUSIC_DIR}")
    print(f"📊 Taille max de la queue: {MAX_QUEUE_SIZE}")
    print("="*60)
    print("🚀 Serveur démarré sur http://localhost:5000")
    print("="*60)
    print("\n💡 Endpoints disponibles:")
    print("   GET  /ping           → Test de connexion")
    print("   GET  /status         → Statut du téléchargement + queue")
    print("   POST /download       → Ajouter à la queue")
    print("   POST /cancel         → Annuler le téléchargement en cours")
    print("   POST /cleanup        → Nettoyer le dossier temp/")
    print("   GET  /stats          → Statistiques de la bibliothèque")
    print("\n" + "="*60 + "\n")
    
    # Démarrer le queue worker dans un thread séparé
    worker_thread = threading.Thread(target=queue_worker, daemon=True)
    worker_thread.start()
    print("✅ Queue worker démarré\n")
    
    # Lancer le serveur
    app.run(
        host='localhost',
        port=5000,
        debug=True,
        use_reloader=False  # Éviter le double démarrage en mode debug
    )
