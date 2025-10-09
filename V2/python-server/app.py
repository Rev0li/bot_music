#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py - Serveur Flask pour GrabSong

FONCTIONNALITÉ:
  - Serveur HTTP simple qui tourne en continu
  - Reçoit les données de l'extension via HTTP
  - Sauvegarde les métadonnées en JSON
  - Détecte la fenêtre "Save As" (à implémenter)
  
UTILISATION:
  python app.py
  
  Le serveur démarre sur http://localhost:5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from pathlib import Path
import threading
import time
from datetime import datetime

# Import du handler Save As
try:
    from save_as_handler import SaveAsHandler, PYWINAUTO_AVAILABLE
    from music_organizer import MusicOrganizer
    SAVE_AS_AVAILABLE = PYWINAUTO_AVAILABLE
except ImportError:
    SAVE_AS_AVAILABLE = False
    print("⚠️ save_as_handler non disponible (pywinauto non installé)")
# ============================================

app = Flask(__name__)
CORS(app)  # Permettre les requêtes depuis l'extension Chrome

# Dossiers
BASE_DIR = Path(__file__).parent.parent
TEMP_DIR = BASE_DIR / "temp"  # JSON + MP3 temporaires
MUSIC_DIR = BASE_DIR / "music"  # MP3 organisés (FINAL)

# Créer les dossiers
TEMP_DIR.mkdir(exist_ok=True)
MUSIC_DIR.mkdir(exist_ok=True)

print(f"📁 Temp: {TEMP_DIR}")
print(f"📁 Music: {MUSIC_DIR}")

# État global pour le statut de téléchargement
download_status = {
    'in_progress': False,
    'last_completed': None,
    'last_error': None
}

# ============================================
# ROUTES
# ============================================

@app.route('/ping', methods=['GET'])
def ping():
    """Test de connexion"""
    return jsonify({
        'status': 'ok',
        'message': 'Python server is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/status', methods=['GET'])
def get_status():
    """Retourne le statut du téléchargement en cours"""
    return jsonify(download_status)

@app.route('/cleanup', methods=['POST'])
def cleanup_temp():
    """
    Nettoie le dossier temp/ (JSON + MP3)
    Utile en cas d'erreur ou de blocage
    """
    try:
        print("\n🧹 Nettoyage du dossier temp/...")
        
        deleted_files = []
        
        # Supprimer tous les fichiers dans temp/
        if TEMP_DIR.exists():
            for file in TEMP_DIR.iterdir():
                if file.is_file():
                    file.unlink()
                    deleted_files.append(file.name)
                    print(f"   🗑️ Supprimé: {file.name}")
        
        print(f"✅ Nettoyage terminé: {len(deleted_files)} fichier(s) supprimé(s)\n")
        
        # Reset le statut
        download_status['in_progress'] = False
        download_status['last_completed'] = None
        download_status['last_error'] = None
        
        return jsonify({
            'success': True,
            'deleted_files': deleted_files,
            'count': len(deleted_files)
        })
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/save', methods=['POST'])
def save_song_data():
    """
    Reçoit et sauvegarde les données de la chanson
    """
    try:
        # Récupérer les données
        data = request.json
        print(f"\n📨 Données reçues:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Timestamp pour les métadonnées
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Préparer les métadonnées
        metadata = {
            'artist': data.get('artist', ''),
            'album': data.get('album', ''),
            'title': data.get('title', ''),
            'year': data.get('year', ''),
            'filename': data.get('filename', ''),
            'link': data.get('link', ''),
            'timestamp': timestamp,
            'created_at': datetime.now().isoformat(),
            'temp_path': str(TEMP_DIR.absolute()),  # Dossier temporaire
        }
        
        # Sauvegarder en JSON directement dans temp/ avec le même nom que le MP3
        json_filename = metadata['filename'].replace('.mp3', '.json')
        json_path = TEMP_DIR / json_filename
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Données sauvegardées: {json_path}")
        print(f"📝 Nom du JSON: {json_filename}")
        
        # Démarrer la surveillance de la fenêtre "Save As" en arrière-plan
        threading.Thread(
            target=watch_save_as_window,
            args=(metadata,),
            daemon=True
        ).start()
        
        return jsonify({
            'success': True,
            'message': 'Données sauvegardées',
            'json_path': str(json_path),
            'json_filename': json_filename,
            'timestamp': timestamp
        })
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# ORGANISATION AUTOMATIQUE
# ============================================

def organize_downloaded_file(file_info: dict, metadata: dict):
    """
    Organise automatiquement le fichier téléchargé dans music/
    
    Args:
        file_info: Infos du fichier téléchargé
        metadata: Métadonnées du JSON
    """
    try:
        print("\n" + "="*50)
        print("🎨 Organisation automatique")
        print("="*50)
        
        # Chemins
        mp3_path = Path(file_info['path']) / file_info['filename']
        json_filename = file_info['filename'].replace('.mp3', '.json')
        json_path = TEMP_DIR / json_filename
        
        # Vérifier que les fichiers existent
        if not mp3_path.exists():
            print(f"❌ MP3 introuvable: {mp3_path}")
            return
        
        if not json_path.exists():
            print(f"⚠️ JSON introuvable: {json_path}")
            # Continuer quand même avec les métadonnées en mémoire
        
        # Organiser
        organizer = MusicOrganizer(str(MUSIC_DIR))
        
        # Utiliser les métadonnées en mémoire si le JSON n'existe pas
        if json_path.exists():
            result = organizer.organize_file(str(mp3_path), str(json_path))
        else:
            # Créer un JSON temporaire
            temp_json = TEMP_DIR / f"temp_{json_filename}"
            with open(temp_json, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            result = organizer.organize_file(str(mp3_path), str(temp_json))
            temp_json.unlink()  # Supprimer le temp
        
        if result['success']:
            print(f"✅ Fichier organisé dans: {result['new_path']}")
            
            # Supprimer le JSON
            if json_path.exists():
                json_path.unlink()
                print(f"🗑️ JSON supprimé: {json_filename}")
        else:
            print(f"❌ Erreur d'organisation: {result.get('error')}")
        
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'organisation: {e}\n")

# ============================================
# SURVEILLANCE FENÊTRE "SAVE AS"
# ============================================

def watch_save_as_window(metadata):
    """
    Surveille l'apparition de la fenêtre "Save As"
    
    Args:
        metadata (dict): Métadonnées de la chanson
    """
    global download_status
    
    print(f"\n🔍 Surveillance de la fenêtre 'Save As' démarrée...")
    print(f"   Fichier attendu: {metadata['filename']}")
    
    # Marquer comme en cours
    download_status['in_progress'] = True
    download_status['last_completed'] = None
    download_status['last_error'] = None
    
    if not SAVE_AS_AVAILABLE:
        print("⚠️ pywinauto non disponible - Mode simulation")
        time.sleep(5)
        print("✅ Fenêtre 'Save As' détectée (simulé)")
        print("🎉 Téléchargement terminé (simulé)!\n")
        download_status['in_progress'] = False
        download_status['last_completed'] = metadata
        return
    
    try:
        # Utiliser le vrai handler
        handler = SaveAsHandler()
        
        file_info = handler.wait_and_fill(
            filename=metadata['filename'],
            target_folder=str(TEMP_DIR),
            timeout=120  # 2 minutes max pour la fenêtre Save As
        )
        
        if file_info:
            # Fichier réellement téléchargé et détecté !
            print(f"🎉 Téléchargement confirmé !")
            print(f"📁 Fichier réel: {file_info['filename']}")
            print(f"📂 Dossier: {file_info['path']}")
            print(f"📊 Taille: {file_info['size'] / 1024 / 1024:.2f} MB\n")
            
            # Organiser le fichier dans music/
            organize_downloaded_file(file_info, metadata)
            
            # Mettre à jour le statut avec les vraies infos
            download_status['in_progress'] = False
            download_status['last_completed'] = {
                'filename': file_info['filename'],
                'path': file_info['path'],
                'size': file_info['size'],
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"✅ Prêt pour un nouveau téléchargement\n")
        else:
            print(f"❌ Échec de l'automatisation ou timeout")
            print(f"⚠️ Le fichier n'a pas été détecté\n")
            
            # Mettre à jour le statut d'erreur
            download_status['in_progress'] = False
            download_status['last_error'] = 'Fichier non détecté après automatisation'
            
    except Exception as e:
        print(f"❌ Erreur lors de l'automatisation: {e}\n")
        download_status['in_progress'] = False
        download_status['last_error'] = str(e)

# ============================================
# DÉMARRAGE
# ============================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🐍 Serveur Python GrabSong")
    print("="*50)
    print(f"🌐 URL: http://localhost:5000")
    print(f"📁 Temp: {TEMP_DIR}")
    print(f"📁 Music: {MUSIC_DIR}")
    print("="*50)
    print("\n✅ Serveur démarré - En attente de requêtes...\n")
    
    # Démarrer le serveur
    app.run(
        host='localhost',
        port=5000,
        debug=True,
        use_reloader=False  # Éviter le double démarrage en mode debug
    )
