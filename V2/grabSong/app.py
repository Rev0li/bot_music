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
from datetime import datetime
import threading
import time

# Import du handler Save As
try:
    from save_as_handler import SaveAsHandler
    SAVE_AS_AVAILABLE = True
except ImportError:
    SAVE_AS_AVAILABLE = False
    print("⚠️ save_as_handler non disponible (pywinauto non installé)")

# ============================================
# CONFIGURATION
# ============================================

app = Flask(__name__)
CORS(app)  # Permettre les requêtes depuis l'extension Chrome

# Dossiers
BASE_DIR = Path(__file__).parent.parent
QUEUE_DIR = BASE_DIR / "queue"
A_TRIER_DIR = BASE_DIR / "a_trier"

# Créer les dossiers
QUEUE_DIR.mkdir(exist_ok=True)
A_TRIER_DIR.mkdir(exist_ok=True)

print(f"📁 Queue: {QUEUE_DIR}")
print(f"📁 A trier: {A_TRIER_DIR}")

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
        
        # Créer un dossier avec timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        song_folder = QUEUE_DIR / timestamp
        song_folder.mkdir(exist_ok=True)
        
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
            'path': str(song_folder.absolute()),  # Chemin complet du dossier
            'a_trier_path': str(A_TRIER_DIR.absolute()),  # Dossier de destination
        }
        
        # Sauvegarder en JSON
        json_path = song_folder / 'info.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Données sauvegardées: {json_path}")
        
        # Démarrer la surveillance de la fenêtre "Save As" en arrière-plan
        threading.Thread(
            target=watch_save_as_window,
            args=(metadata,),
            daemon=True
        ).start()
        
        return jsonify({
            'success': True,
            'message': 'Données sauvegardées',
            'folder': str(song_folder),
            'json_path': str(json_path),
            'timestamp': timestamp
        })
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================
# SURVEILLANCE FENÊTRE "SAVE AS"
# ============================================

def watch_save_as_window(metadata):
    """
    Surveille l'apparition de la fenêtre "Save As"
    
    Args:
        metadata (dict): Métadonnées de la chanson
    """
    print(f"\n🔍 Surveillance de la fenêtre 'Save As' démarrée...")
    print(f"   Fichier attendu: {metadata['filename']}")
    
    if not SAVE_AS_AVAILABLE:
        print("⚠️ pywinauto non disponible - Mode simulation")
        time.sleep(5)
        print("✅ Fenêtre 'Save As' détectée (simulé)")
        print("🎉 Téléchargement terminé (simulé)!\n")
        return
    
    try:
        # Utiliser le vrai handler
        handler = SaveAsHandler()
        
        success = handler.wait_and_fill(
            filename=metadata['filename'],
            target_folder=str(A_TRIER_DIR),
            timeout=120  # 2 minutes max
        )
        
        if success:
            print(f"🎉 Téléchargement terminé avec succès!")
            print(f"📁 Fichier sauvegardé: {A_TRIER_DIR / metadata['filename']}\n")
            
            # TODO: Envoyer notification à l'extension
            # send_download_complete(metadata)
        else:
            print(f"❌ Échec de l'automatisation")
            print(f"⚠️ Le fichier a peut-être été sauvegardé manuellement\n")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'automatisation: {e}\n")

# ============================================
# DÉMARRAGE
# ============================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🐍 Serveur Python GrabSong")
    print("="*50)
    print(f"🌐 URL: http://localhost:5000")
    print(f"📁 Queue: {QUEUE_DIR}")
    print(f"📁 A trier: {A_TRIER_DIR}")
    print("="*50)
    print("\n✅ Serveur démarré - En attente de requêtes...\n")
    
    # Démarrer le serveur
    app.run(
        host='localhost',
        port=5000,
        debug=True,
        use_reloader=False  # Éviter le double démarrage en mode debug
    )
