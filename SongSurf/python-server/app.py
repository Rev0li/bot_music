#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py - Serveur Flask pour GrabSong V3

FONCTIONNALITÉ:
  - Serveur HTTP qui reçoit les requêtes de l'extension Chrome
  - Télécharge les vidéos YT via yt-dlp
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

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pathlib import Path
from datetime import datetime
import threading
import time
import queue
from collections import deque

# Import des modules
from downloader import YTDownloader
from organizer import MusicOrganizer

# ============================================
# CONFIGURATION
# ============================================

app = Flask(__name__)
# Configuration CORS explicite pour éviter les blocages de navigateur (Brave, Chrome, etc.)
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# Dossiers
# Détecter si on est dans Docker (chemin /app) ou en local
if Path(__file__).parent == Path('/app'):
    # Docker: utiliser /data
    TEMP_DIR = Path('/data/temp')
    MUSIC_DIR = Path('/data/music')
else:
    # Local: utiliser ../temp et ../music
    BASE_DIR = Path(__file__).parent.parent
    TEMP_DIR = BASE_DIR / "temp"
    MUSIC_DIR = BASE_DIR / "music"

# Créer les dossiers s'ils n'existent pas
TEMP_DIR.mkdir(parents=True, exist_ok=True)
MUSIC_DIR.mkdir(parents=True, exist_ok=True)

# Dossier pour les photos d'artistes (dans le dossier music à la racine)
ARTIST_PHOTOS_DIR = MUSIC_DIR / "artist_photos"
ARTIST_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

print(f"📁 Temp: {TEMP_DIR}")
print(f"📁 Music: {MUSIC_DIR}")
print(f"📁 Artist Photos: {ARTIST_PHOTOS_DIR}")

# Instances
downloader = YTDownloader(TEMP_DIR, MUSIC_DIR)
organizer = MusicOrganizer(MUSIC_DIR)

# Système de queue
MAX_QUEUE_SIZE = 50  # Augmenté pour supporter les gros albums
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

# Logs simplifiés (console uniquement)
def log_message(level, message, data=None):
    """Affiche un message dans la console"""
    emoji = {'INFO': 'ℹ️', 'WARNING': '⚠️', 'ERROR': '❌', 'SUCCESS': '✅'}.get(level, '📝')
    print(f"{emoji} [{level}] {message}")
    if data:
        print(f"   Data: {data}")

# ============================================
# ROUTES
# ============================================

@app.route('/', methods=['GET'])
def dashboard():
    """Dashboard principal"""
    return render_template('dashboard.html')


@app.route('/ping', methods=['GET'])
def ping():
    """Test de connexion"""
    return jsonify({
        'status': 'ok',
        'message': 'GrabSong V3 server is running',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check pour Docker"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/status', methods=['GET'])
def get_status():
    """Retourne le statut du téléchargement en cours"""
    with queue_lock:
        status = download_status.copy()
        status['queue_size'] = download_queue.qsize()
        
        # Ajouter la progression si un téléchargement est en cours
        if status['in_progress']:
            status['progress'] = downloader.get_progress()
        
        # Ajouter les détails de la queue pour le dashboard
        status['queue'] = list(download_queue.queue)
        
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
        
        # Log
        log_message('INFO', f"Téléchargement ajouté à la queue: {metadata['title']} - {metadata['artist']}", {
            'url': url,
            'metadata': metadata,
            'queue_position': queue_size,
            'queue_size': queue_size
        })
        
        return jsonify({
            'success': True,
            'message': 'Ajouté à la queue',
            'queue_position': queue_size,
            'queue_size': queue_size,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        log_message('ERROR', f"Erreur lors de l'ajout à la queue: {str(e)}", {'error': str(e)})
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/cancel', methods=['POST'])
def cancel_download():
    """Annule le téléchargement en cours"""
    try:
        if not download_status['in_progress']:
            log_message('WARNING', 'Tentative d\'annulation sans téléchargement en cours')
            return jsonify({
                'success': False,
                'error': 'Aucun téléchargement en cours'
            }), 400
        
        print("\n🛑 ANNULATION DU TÉLÉCHARGEMENT EN COURS...")
        log_message('WARNING', 'Annulation du téléchargement en cours', {
            'download': download_status['current_download']
        })
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
        log_message('INFO', 'Démarrage du nettoyage du dossier temp/')
        
        deleted_files = []
        
        if TEMP_DIR.exists():
            for file in TEMP_DIR.iterdir():
                if file.is_file():
                    file.unlink()
                    deleted_files.append(file.name)
                    print(f"   🗑️ Supprimé: {file.name}")
        
        print(f"✅ Nettoyage terminé: {len(deleted_files)} fichier(s) supprimé(s)\n")
        log_message('SUCCESS', f'Nettoyage terminé: {len(deleted_files)} fichier(s) supprimé(s)', {
            'deleted_files': deleted_files
        })
        
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


@app.route('/api/library', methods=['GET'])
def get_library():
    """Retourne la structure complète de la bibliothèque"""
    structure = organizer.get_library_structure()
    return jsonify(structure)


@app.route('/api/album-cover/<path:artist>/<path:album>')
def get_album_cover(artist, album):
    """Retourne la pochette d'un album"""
    try:
        # Chercher le premier fichier MP3 dans l'album
        album_dir = organizer.music_dir / artist / album
        
        if not album_dir.exists():
            return '', 404
        
        mp3_files = list(album_dir.glob('*.mp3'))
        
        if not mp3_files:
            return '', 404
        
        # Extraire la pochette du premier fichier
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, APIC
        
        audio = MP3(mp3_files[0], ID3=ID3)
        
        # Chercher la pochette
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                return tag.data, 200, {'Content-Type': tag.mime}
        
        return '', 404
        
    except Exception as e:
        print(f"❌ Erreur récupération pochette: {e}")
        return '', 404


@app.route('/api/cover/<path:filename>')
def get_cover(filename):
    """Retourne la pochette d'un album par nom de fichier"""
    try:
        # Extraire artiste et album du filename
        # Format: Artist_Album.jpg
        parts = filename.replace('.jpg', '').split('_', 1)
        if len(parts) != 2:
            return '', 404
        
        artist, album = parts
        
        # Chercher le premier fichier MP3 dans l'album
        album_dir = organizer.music_dir / artist / album
        
        if not album_dir.exists():
            return '', 404
        
        mp3_files = list(album_dir.glob('*.mp3'))
        
        if not mp3_files:
            return '', 404
        
        # Extraire la pochette du premier fichier
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, APIC
        
        audio = MP3(mp3_files[0], ID3=ID3)
        
        # Chercher la pochette
        if audio.tags:
            for tag in audio.tags.values():
                if isinstance(tag, APIC):
                    return tag.data, 200, {'Content-Type': tag.mime}
        
        return '', 404
        
    except Exception as e:
        print(f"❌ Erreur récupération pochette: {e}")
        return '', 404


@app.route('/api/artist-photo/<artist_name>')
def get_artist_photo(artist_name):
    """Retourne la photo d'un artiste"""
    try:
        for ext in ['.jpg', '.jpeg', '.png', '.webp']:
            photo_path = ARTIST_PHOTOS_DIR / f"{artist_name}{ext}"
            if photo_path.exists():
                from flask import send_file
                return send_file(photo_path, mimetype=f'image/{ext[1:]}')
        
        return '', 404
    except Exception as e:
        print(f"❌ Erreur récupération photo: {e}")
        return '', 404


@app.route('/api/upload-artist-photo', methods=['POST'])
def upload_artist_photo():
    """Upload une photo pour un artiste"""
    try:
        if 'photo' not in request.files:
            return jsonify({'success': False, 'error': 'Aucun fichier fourni'}), 400
        
        file = request.files['photo']
        artist_name = request.form.get('artist_name')
        
        if not artist_name:
            return jsonify({'success': False, 'error': 'Nom d\'artiste manquant'}), 400
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Fichier vide'}), 400
        
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({'success': False, 'error': 'Format non supporté'}), 400
        
        for ext in allowed_extensions:
            old_photo = ARTIST_PHOTOS_DIR / f"{artist_name}{ext}"
            if old_photo.exists():
                old_photo.unlink()
        
        photo_path = ARTIST_PHOTOS_DIR / f"{artist_name}{file_ext}"
        file.save(str(photo_path))
        
        log_message('SUCCESS', f'Photo uploadée pour {artist_name}')
        
        return jsonify({
            'success': True,
            'message': f'Photo uploadée pour {artist_name}',
            'photo_url': f'/api/artist-photo/{artist_name}'
        })
        
    except Exception as e:
        log_message('ERROR', f'Erreur upload photo: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/extract-metadata', methods=['POST'])
def extract_metadata():
    """Extract metadata from YT URL using yt-dlp"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'success': False, 'error': 'URL manquante'})
        
        log_message('INFO', f'Extraction des métadonnées: {url}')
        
        # Détecter si c'est une playlist/album ou une musique simple
        if '/playlist?list=' in url or '/browse/' in url:
            # C'est une playlist ou un album
            result = downloader.extract_playlist_metadata(url)
            
            if result['success']:
                log_message('SUCCESS', f'✅ Playlist/Album extrait: {result["total_songs"]} chansons', {
                    'title': result['title'],
                    'artist': result['artist'],
                    'total_songs': result['total_songs']
                })
            else:
                log_message('ERROR', f'❌ Échec extraction playlist: {result.get("error")}')
            
            return jsonify(result)
        else:
            # C'est une musique simple
            result = downloader.extract_metadata(url)
            
            if result['success']:
                log_message('SUCCESS', f'✅ Métadonnées extraites', result['metadata'])
                return jsonify(result)
            else:
                log_message('ERROR', f'❌ Échec extraction: {result.get("error")}')
                return jsonify(result)
            
    except Exception as e:
        log_message('ERROR', f'Erreur extraction métadonnées: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/download-playlist', methods=['POST'])
def download_playlist():
    """
    Télécharge un album ou une playlist complète
    
    Body:
    {
        "url": "https://music.youtube.com/playlist?list=...",
        "playlist_metadata": {
            "title": "Album Name",
            "artist": "Artist Name",
            "songs": [...]
        }
    }
    """
    try:
        data = request.get_json()
        url = data.get('url')
        playlist_metadata = data.get('playlist_metadata')
        
        if not url or not playlist_metadata:
            return jsonify({'success': False, 'error': 'URL ou métadonnées manquantes'})
        
        total_songs = playlist_metadata.get('total_songs', 0)
        
        log_message('INFO', f'Téléchargement playlist: {playlist_metadata.get("title")} ({total_songs} chansons)')
        
        # Ajouter chaque chanson à la queue
        songs = playlist_metadata.get('songs', [])
        added = 0
        
        for song in songs:
            if download_queue.full():
                log_message('WARNING', f'Queue pleine, {len(songs) - added} chansons non ajoutées')
                break
            
            # Métadonnées pour cette chanson
            metadata = {
                'artist': song.get('artist', playlist_metadata.get('artist', 'Unknown')),
                'album': playlist_metadata.get('title', 'Unknown Album'),
                'title': song['title'],
                'year': playlist_metadata.get('year', '')
            }
            
            download_queue.put({
                'url': song['url'],
                'metadata': metadata,
                'added_at': datetime.now().isoformat(),
                'playlist_info': {
                    'playlist_title': playlist_metadata.get('title'),
                    'song_index': added + 1,
                    'total_songs': total_songs
                }
            })
            
            added += 1
        
        log_message('SUCCESS', f'✅ {added}/{total_songs} chansons ajoutées à la queue')
        
        return jsonify({
            'success': True,
            'message': f'{added} chansons ajoutées à la queue',
            'added': added,
            'total': total_songs,
            'queue_size': download_queue.qsize(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        log_message('ERROR', f'Erreur téléchargement playlist: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/move-song', methods=['POST'])
def move_song():
    """Déplace une chanson vers un autre artiste/album avec drag & drop"""
    try:
        data = request.get_json()
        song_path = data.get('song_path')  # Chemin relatif
        target_artist = data.get('target_artist')
        target_album = data.get('target_album')
        
        if not all([song_path, target_artist, target_album]):
            return jsonify({'success': False, 'error': 'Paramètres manquants'})
        
        log_message('INFO', f'Déplacement: {song_path} → {target_artist}/{target_album}')
        
        # Construire les chemins
        source_file = organizer.music_dir / song_path
        
        if not source_file.exists():
            return jsonify({'success': False, 'error': 'Fichier introuvable'})
        
        # Créer le dossier de destination
        target_dir = organizer.music_dir / target_artist / target_album
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Déplacer le fichier
        target_file = target_dir / source_file.name
        
        # Gérer les doublons
        if target_file.exists():
            counter = 1
            while target_file.exists():
                target_file = target_dir / f"{source_file.stem} ({counter}){source_file.suffix}"
                counter += 1
        
        import shutil
        shutil.move(str(source_file), str(target_file))
        
        # Nettoyer les dossiers vides
        organizer._cleanup_empty_dirs(source_file.parent)
        
        log_message('SUCCESS', f'✅ Déplacé: {source_file.name} → {target_artist}/{target_album}')
        
        return jsonify({
            'success': True,
            'new_path': str(target_file.relative_to(organizer.music_dir))
        })
        
    except Exception as e:
        log_message('ERROR', f'Erreur déplacement: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/rename-song', methods=['POST'])
def rename_song():
    """Renomme une chanson (fichier + métadonnées ID3)"""
    try:
        data = request.get_json()
        song_path = data.get('song_path')
        new_title = data.get('new_title')
        
        if not all([song_path, new_title]):
            return jsonify({'success': False, 'error': 'Paramètres manquants'})
        
        log_message('INFO', f'Renommage: {song_path} → {new_title}')
        
        # Construire le chemin
        source_file = organizer.music_dir / song_path
        
        if not source_file.exists():
            return jsonify({'success': False, 'error': 'Fichier introuvable'})
        
        # Nettoyer le nouveau titre
        clean_title = organizer._clean_filename(new_title)
        new_filename = f"{clean_title}.mp3"
        new_path = source_file.parent / new_filename
        
        # Vérifier si le fichier existe déjà
        if new_path.exists() and new_path != source_file:
            return jsonify({'success': False, 'error': 'Un fichier avec ce nom existe déjà'})
        
        # Mettre à jour les métadonnées ID3
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, TIT2
        
        audio = MP3(source_file, ID3=ID3)
        audio['TIT2'] = TIT2(encoding=3, text=new_title)
        audio.save()
        
        # Renommer le fichier
        import shutil
        shutil.move(str(source_file), str(new_path))
        
        log_message('SUCCESS', f'✅ Renommé: {source_file.name} → {new_filename}')
        
        return jsonify({
            'success': True,
            'new_path': str(new_path.relative_to(organizer.music_dir))
        })
        
    except Exception as e:
        log_message('ERROR', f'Erreur renommage: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/apply-corrections', methods=['POST'])
def apply_corrections():
    """Applique les corrections de feat (déplace et renomme les fichiers)"""
    try:
        data = request.get_json()
        corrections = data.get('corrections', [])
        
        if not corrections:
            return jsonify({'success': False, 'error': 'Aucune correction à appliquer'})
        
        log_message('INFO', f'Début de l\'application de {len(corrections)} correction(s)', {
            'count': len(corrections)
        })
        
        results = []
        for correction in corrections:
            song_path = correction.get('song_path')
            target_artist = correction.get('target_artist')
            feat_artist = correction.get('feat_artist')
            
            log_message('INFO', f'Correction: {song_path} → {target_artist} (feat. {feat_artist})')
            
            # Appeler la fonction de l'organizer pour déplacer le fichier
            result = organizer.move_and_rename_feat(song_path, target_artist, feat_artist)
            results.append(result)
            
            if result['success']:
                log_message('SUCCESS', f'✅ Correction appliquée: {result["new_path"]}')
            else:
                log_message('ERROR', f'❌ Échec: {result.get("error")}')
        
        # Compter les succès
        success_count = sum(1 for r in results if r['success'])
        
        log_message('INFO', f'Corrections terminées: {success_count}/{len(corrections)} réussies')
        
        return jsonify({
            'success': True,
            'results': results,
            'success_count': success_count,
            'total': len(corrections)
        })
        
    except Exception as e:
        log_message('ERROR', f'Erreur lors de l\'application des corrections: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})


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
            
            log_message('INFO', f"Démarrage du téléchargement: {metadata['title']} - {metadata['artist']}", {
                'url': url,
                'metadata': metadata,
                'queue_remaining': download_queue.qsize()
            })
            
            try:
                # Étape 1: Télécharger
                print("📥 Étape 1/2: Téléchargement...")
                log_message('INFO', '📥 Étape 1/2: Début du téléchargement via yt-dlp', {
                    'url': url,
                    'title': metadata['title'],
                    'artist': metadata['artist']
                })
                
                download_result = downloader.download(url, metadata)
                
                log_message('INFO', 'Résultat du téléchargement reçu', {
                    'success': download_result.get('success'),
                    'has_file_path': 'file_path' in download_result
                })
                
                # Vérifier annulation
                if cancel_flag.is_set():
                    log_message('WARNING', 'Téléchargement annulé par l\'utilisateur')
                    raise Exception("Téléchargement annulé par l'utilisateur")
                
                if not download_result['success']:
                    error_msg = download_result.get('error', 'Erreur inconnue')
                    log_message('ERROR', f'Échec du téléchargement: {error_msg}', download_result)
                    raise Exception(error_msg)
                
                file_path = download_result['file_path']
                print(f"✅ Téléchargement terminé: {file_path}")
                log_message('SUCCESS', '✅ Téléchargement terminé avec succès', {
                    'file_path': file_path,
                    'file_size': download_result.get('file_size', 'unknown')
                })
                
                # Vérifier annulation
                if cancel_flag.is_set():
                    log_message('WARNING', 'Annulation détectée avant organisation')
                    raise Exception("Téléchargement annulé par l'utilisateur")
                
                # Étape 2: Organiser
                print("\n📁 Étape 2/2: Organisation...")
                log_message('INFO', '📁 Étape 2/2: Début de l\'organisation du fichier', {
                    'file_path': file_path,
                    'target_artist': metadata['artist'],
                    'target_album': metadata['album']
                })
                
                organize_result = organizer.organize(file_path, metadata)
                
                log_message('INFO', 'Résultat de l\'organisation reçu', {
                    'success': organize_result.get('success'),
                    'has_final_path': 'final_path' in organize_result
                })
                
                if not organize_result['success']:
                    error_msg = organize_result.get('error', 'Erreur inconnue')
                    log_message('ERROR', f'Échec de l\'organisation: {error_msg}', organize_result)
                    raise Exception(error_msg)
                
                final_path = organize_result['final_path']
                print(f"✅ Organisation terminée: {final_path}")
                log_message('SUCCESS', '✅ Organisation terminée avec succès', {
                    'final_path': final_path,
                    'artist_folder': metadata['artist'],
                    'album_folder': metadata['album']
                })
                
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
                
                log_message('SUCCESS', f"Téléchargement complet: {metadata['title']} - {metadata['artist']}", {
                    'final_path': final_path,
                    'metadata': metadata,
                    'queue_remaining': download_queue.qsize()
                })
                
            except Exception as e:
                # Erreur
                print(f"\n{'='*60}")
                print(f"❌ ERREUR LORS DU TÉLÉCHARGEMENT")
                print(f"{'='*60}")
                print(f"Erreur: {str(e)}")
                print(f"{'='*60}\n")
                
                log_message('ERROR', f"Erreur lors du téléchargement: {str(e)}", {
                    'error': str(e),
                    'metadata': metadata,
                    'url': url
                })
                
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
    print("🚀 Serveur démarré sur http://localhost:8080")
    print("="*60)
    print("\n⚠️  IMPORTANT - Navigateurs:")
    print("   🛡️  Brave: Désactivez Shields pour YT Music")
    print("   🛡️  Chrome: Désactivez le bloqueur de pub si nécessaire")
    print("   ✅ CORS configuré pour accepter toutes les origines")
    print("="*60)
    print("\n💡 Endpoints disponibles:")
    print("   GET  /                → Dashboard principal")
    print("   GET  /ping           → Test de connexion")
    print("   GET  /status         → Statut du téléchargement + queue")
    print("   POST /download       → Ajouter à la queue")
    print("   POST /cancel         → Annuler le téléchargement en cours")
    print("   POST /cleanup        → Nettoyer le dossier temp/")
    print("   GET  /stats          → Statistiques de la bibliothèque")
    print("\n" + "="*60 + "\n")
    
    # Log de démarrage
    log_message('SUCCESS', 'Serveur SongSurf démarré', {
        'temp_dir': str(TEMP_DIR),
        'music_dir': str(MUSIC_DIR),
        'max_queue': MAX_QUEUE_SIZE
    })
    
    # Démarrer le queue worker dans un thread séparé
    worker_thread = threading.Thread(target=queue_worker, daemon=True)
    worker_thread.start()
    print("✅ Queue worker démarré\n")
    log_message('INFO', 'Queue worker démarré')
    
    # Lancer le serveur
    # En Docker, écouter sur 0.0.0.0 pour accepter les connexions externes
    host = '0.0.0.0' if Path(__file__).parent == Path('/app') else 'localhost'
    app.run(
        host=host,
        port=8080,
        debug=True,
        use_reloader=False  # Éviter le double démarrage en mode debug
    )