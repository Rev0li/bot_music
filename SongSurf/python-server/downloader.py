#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
downloader.py - Module de téléchargement avec yt-dlp

FONCTIONNALITÉ:
  - Télécharge les vidéos YT en MP3 via yt-dlp
  - Gestion de la progression en temps réel
  - Conversion automatique en MP3 (via FFmpeg)
  - Gestion des erreurs robuste
"""

import yt_dlp
from pathlib import Path
import os
from datetime import datetime
import shutil


class DownloadProgress:
    """Classe pour suivre la progression du téléchargement"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.percent = 0
        self.downloaded = 0
        self.total = 0
        self.speed = "0 KB/s"
        self.eta = "0s"
        self.status = "idle"  # idle, downloading, processing, completed, error
    
    def update(self, d):
        """Callback appelé par yt-dlp pour mettre à jour la progression"""
        if d['status'] == 'downloading':
            self.status = 'downloading'
            self.downloaded = d.get('downloaded_bytes', 0)
            self.total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            
            if self.total > 0:
                self.percent = int((self.downloaded / self.total) * 100)
            
            # Vitesse et ETA
            speed = d.get('speed', 0)
            if speed:
                self.speed = f"{speed / 1024:.0f} KB/s"
            
            eta = d.get('eta', 0)
            if eta:
                self.eta = f"{eta}s"
                
        elif d['status'] == 'finished':
            self.status = 'processing'
            self.percent = 100
    
    def to_dict(self):
        return {
            'status': self.status,
            'percent': self.percent,
            'downloaded': self.downloaded,
            'total': self.total,
            'speed': self.speed,
            'eta': self.eta
        }


class YTDownloader:
    """Téléchargeur YT avec yt-dlp"""
    
    def __init__(self, temp_dir, music_dir):
        self.temp_dir = Path(temp_dir)
        self.music_dir = Path(music_dir)
        self.progress = DownloadProgress()
        
        # Créer les dossiers
        self.temp_dir.mkdir(exist_ok=True, parents=True)
        self.music_dir.mkdir(exist_ok=True, parents=True)
        
        # Détecter FFmpeg
        self.ffmpeg_location = self._find_ffmpeg()
    
    def download(self, url, metadata):
        """
        Télécharge une vidéo YT en MP3
        
        Args:
            url (str): URL YT ou YT Music
            metadata (dict): {artist, album, title, year}
            
        Returns:
            dict: {success, file_path, error}
        """
        try:
            print(f"\n🎵 Téléchargement: {metadata.get('title', 'Unknown')}")
            print(f"   URL originale: {url}")
            
            # Convertir l'URL YT Music en URL YT classique
            if 'music.youtube.com' in url:
                # Extraire le video ID de l'URL YT Music
                import re
                video_id_match = re.search(r'[?&]v=([^&]+)', url)
                if video_id_match:
                    video_id = video_id_match.group(1)
                    url = f'https://www.youtube.com/watch?v={video_id}'
                    print(f"   🔄 Converti en: {url}")
            
            print(f"   📥 Téléchargement depuis: {url}")
            
            # Reset la progression
            self.progress.reset()
            self.progress.status = 'downloading'
            
            # Nom de fichier temporaire
            temp_filename = f"{metadata.get('artist', 'Unknown')} - {metadata.get('title', 'Unknown')}"
            
            # Configuration yt-dlp (optimisée pour YT Music)
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '0',  # Meilleure qualité (0-9)
                }],
                'outtmpl': str(self.temp_dir / f'{temp_filename}.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [self.progress.update],
                'noplaylist': True,  # Ne télécharger QUE la vidéo, pas la playlist
                'writethumbnail': True,  # Télécharger la pochette
                'nocheckcertificate': True,
            }
            
            # Ajouter le chemin FFmpeg si trouvé
            if self.ffmpeg_location:
                ydl_opts['ffmpeg_location'] = self.ffmpeg_location
                print(f"   🔧 FFmpeg trouvé: {self.ffmpeg_location}")
            
            # Télécharger
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("   ⏳ Téléchargement en cours...")
                info = ydl.extract_info(url, download=True)
                
                # Le fichier téléchargé (avec extension .mp3 après conversion)
                downloaded_file = self.temp_dir / f"{temp_filename}.mp3"
                
                if not downloaded_file.exists():
                    raise FileNotFoundError(f"Fichier non trouvé: {downloaded_file}")
                
                print(f"   ✅ Téléchargement terminé: {downloaded_file.name}")
                
                # Marquer comme terminé
                self.progress.status = 'completed'
                self.progress.percent = 100
                
                return {
                    'success': True,
                    'file_path': str(downloaded_file),
                    'metadata': metadata,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)}")
            self.progress.status = 'error'
            
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_progress(self):
        """Retourne la progression actuelle"""
        return self.progress.to_dict()
    
    def extract_metadata(self, url):
        """
        Extrait les métadonnées d'une vidéo YT sans la télécharger
        
        Args:
            url (str): URL YT ou YT Music
            
        Returns:
            dict: {success, metadata: {title, artist, album, year, thumbnail_url}, error}
        """
        try:
            print(f"\n🔍 Extraction des métadonnées: {url}")
            
            # Convertir l'URL YT Music en URL YT classique
            if 'music.youtube.com' in url:
                import re
                video_id_match = re.search(r'[?&]v=([^&]+)', url)
                if video_id_match:
                    video_id = video_id_match.group(1)
                    url = f'https://www.youtube.com/watch?v={video_id}'
                    print(f"   🔄 Converti en: {url}")
            
            # Configuration yt-dlp (extraction uniquement)
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,  # Ne pas télécharger
                'noplaylist': True,
            }
            
            # Extraire les infos
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Extraire les métadonnées pertinentes
                title = info.get('title', 'Unknown Title')
                uploader = info.get('uploader', 'Unknown Artist')
                artist = info.get('artist') or info.get('creator') or uploader
                album = info.get('album', 'Unknown Album')
                
                # Essayer d'extraire l'année
                release_date = info.get('release_date') or info.get('upload_date', '')
                year = release_date[:4] if len(release_date) >= 4 else ''
                
                # URL de la miniature
                thumbnail_url = info.get('thumbnail', '')
                
                # Nettoyer le titre (enlever " - Topic" de l'artiste si présent)
                if artist.endswith(' - Topic'):
                    artist = artist[:-8]
                
                metadata = {
                    'title': title,
                    'artist': artist,
                    'album': album,
                    'year': year,
                    'thumbnail_url': thumbnail_url,
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0)
                }
                
                print(f"   ✅ Métadonnées extraites:")
                print(f"      🎵 Titre: {title}")
                print(f"      🎤 Artiste: {artist}")
                print(f"      💿 Album: {album}")
                print(f"      📅 Année: {year}")
                
                return {
                    'success': True,
                    'metadata': metadata,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def extract_playlist_metadata(self, url):
        """
        Extrait les métadonnées d'un album ou playlist YT Music
        
        Args:
            url (str): URL de l'album ou playlist
            
        Returns:
            dict: {
                success: bool,
                type: 'album' | 'playlist',
                title: str,
                artist: str,
                songs: [{title, artist, url, duration}, ...],
                total_songs: int,
                total_duration: int
            }
        """
        try:
            print(f"\n💿 Extraction playlist/album: {url}")
            
            # Configuration yt-dlp pour extraire la playlist
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'extract_flat': 'in_playlist',  # Extraction avec plus de détails
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Vérifier si c'est une playlist
                if 'entries' not in info:
                    return {
                        'success': False,
                        'error': 'URL ne contient pas de playlist/album'
                    }
                
                # Type de playlist
                playlist_type = 'album' if 'browse' in url else 'playlist'
                
                # Infos générales - Amélioration de la détection de l'artiste
                playlist_title = info.get('title', 'Unknown Playlist')
                
                # Nettoyer le titre (enlever "Album - " si présent au début)
                if playlist_title.startswith('Album - '):
                    playlist_title = playlist_title[8:]  # Enlever "Album - "
                    print(f"   🧹 Titre nettoyé: {playlist_title}")
                
                # Essayer plusieurs sources pour l'artiste
                playlist_artist = (
                    info.get('artist') or 
                    info.get('creator') or 
                    info.get('uploader') or 
                    info.get('channel')
                )
                
                # Nettoyer l'artiste (enlever " - Topic" si présent)
                if playlist_artist and playlist_artist.endswith(' - Topic'):
                    playlist_artist = playlist_artist[:-8]
                
                # Si toujours pas d'artiste, extraire depuis la première chanson
                playlist_year = ''
                if not playlist_artist or playlist_artist == 'None' or str(playlist_artist).lower() == 'none':
                    print("   🔍 Artiste non trouvé, extraction depuis la première chanson...")
                    first_entry = info['entries'][0] if info['entries'] else None
                    
                    if first_entry and first_entry.get('id'):
                        try:
                            # Extraire les détails de la première chanson
                            first_song_url = f"https://www.youtube.com/watch?v={first_entry['id']}"
                            first_song_info = self.extract_metadata(first_song_url)
                            
                            if first_song_info['success']:
                                playlist_artist = first_song_info['metadata'].get('artist', 'Unknown Artist')
                                playlist_year = first_song_info['metadata'].get('year', '')
                                print(f"   ✅ Artiste trouvé via première chanson: {playlist_artist}")
                                if playlist_year:
                                    print(f"   📅 Année: {playlist_year}")
                        except Exception as e:
                            print(f"   ⚠️  Impossible d'extraire l'artiste: {e}")
                
                # Fallback: essayer d'extraire depuis le titre
                if not playlist_artist or playlist_artist == 'Unknown Artist':
                    # Format souvent : "Album - THE 25TH HOUR" ou "THE 25TH HOUR - Artist"
                    if ' - ' in playlist_title:
                        parts = playlist_title.split(' - ')
                        if len(parts) >= 2:
                            # Enlever "Album" du début si présent
                            if parts[0].strip().lower() == 'album':
                                # Le titre est parts[1], chercher l'artiste ailleurs
                                pass
                            else:
                                # Le dernier élément pourrait être l'artiste
                                potential_artist = parts[-1].strip()
                                if potential_artist and not potential_artist.lower().startswith('album'):
                                    playlist_artist = potential_artist
                
                # Dernier fallback
                if not playlist_artist:
                    playlist_artist = 'Unknown Artist'
                
                # Extraire les chansons
                songs = []
                total_duration = 0
                
                for entry in info['entries']:
                    if entry is None:
                        continue
                    
                    # Essayer d'extraire l'artiste de chaque chanson
                    song_artist = (
                        entry.get('artist') or
                        entry.get('creator') or
                        entry.get('uploader') or
                        playlist_artist
                    )
                    
                    # Nettoyer l'artiste de la chanson
                    if song_artist.endswith(' - Topic'):
                        song_artist = song_artist[:-8]
                    
                    song = {
                        'title': entry.get('title', 'Unknown'),
                        'artist': song_artist,
                        'url': entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}",
                        'id': entry.get('id'),
                        'duration': entry.get('duration', 0)
                    }
                    songs.append(song)
                    total_duration += song['duration']
                
                print(f"   ✅ {len(songs)} chansons trouvées")
                print(f"   📀 Titre: {playlist_title}")
                print(f"   🎤 Artiste: {playlist_artist}")
                print(f"   ⏱️  Durée totale: {total_duration // 60}min {total_duration % 60}s")
                
                return {
                    'success': True,
                    'type': playlist_type,
                    'title': playlist_title,
                    'artist': playlist_artist,
                    'year': playlist_year,
                    'songs': songs,
                    'total_songs': len(songs),
                    'total_duration': total_duration,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def download_playlist(self, url, playlist_metadata, progress_callback=None):
        """
        Télécharge toutes les chansons d'un album/playlist
        
        Args:
            url (str): URL de l'album/playlist
            playlist_metadata (dict): Métadonnées de la playlist
            progress_callback (function): Callback pour la progression (song_index, total_songs, song_info)
            
        Returns:
            dict: {
                success: bool,
                downloaded: int,
                failed: int,
                results: [...]
            }
        """
        try:
            print(f"\n💿 Téléchargement playlist: {playlist_metadata.get('title')}")
            
            songs = playlist_metadata.get('songs', [])
            total_songs = len(songs)
            
            results = []
            downloaded = 0
            failed = 0
            
            for index, song in enumerate(songs, 1):
                print(f"\n📥 [{index}/{total_songs}] {song['title']}")
                
                # Callback de progression
                if progress_callback:
                    progress_callback(index, total_songs, song)
                
                # Métadonnées pour cette chanson
                metadata = {
                    'artist': song.get('artist', playlist_metadata.get('artist', 'Unknown')),
                    'album': playlist_metadata.get('title', 'Unknown Album'),
                    'title': song['title'],
                    'year': ''
                }
                
                # Télécharger la chanson
                result = self.download(song['url'], metadata)
                
                if result['success']:
                    downloaded += 1
                    print(f"   ✅ Téléchargé: {song['title']}")
                else:
                    failed += 1
                    print(f"   ❌ Échec: {song['title']} - {result.get('error')}")
                
                results.append({
                    'song': song,
                    'result': result
                })
            
            print(f"\n📊 Résumé:")
            print(f"   ✅ Téléchargés: {downloaded}/{total_songs}")
            print(f"   ❌ Échecs: {failed}/{total_songs}")
            
            return {
                'success': True,
                'downloaded': downloaded,
                'failed': failed,
                'total': total_songs,
                'results': results,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _find_ffmpeg(self):
        """
        Détecte automatiquement le chemin de FFmpeg
        
        Returns:
            str: Chemin du dossier contenant ffmpeg.exe, ou None si non trouvé
        """
        # Vérifier si ffmpeg est dans le PATH
        ffmpeg_path = shutil.which('ffmpeg')
        if ffmpeg_path:
            # Retourner le dossier parent
            return str(Path(ffmpeg_path).parent)
        
        # Chemins courants sur Windows
        common_paths = [
            Path.home() / 'ffmpeg' / 'bin',
            Path.home() / '.local' / 'ffmpeg' / 'ffmpeg-7.0.2-amd64-static'  ,
            Path('C:/ffmpeg/bin'),
            Path('C:/Program Files/ffmpeg/bin'),
            Path.home() / 'Downloads' / 'ffmpeg-8.0' / 'bin',
            # Chemins winget (versions multiples possibles)
            Path.home() / 'AppData' / 'Local' / 'Microsoft' / 'WinGet' / 'Packages' / 'Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe' / 'ffmpeg-8.0-full_build' / 'bin',
            Path.home() / 'AppData' / 'Local' / 'Microsoft' / 'WinGet' / 'Packages' / 'Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe' / 'ffmpeg-7.1-full_build' / 'bin',
            # Ajoutez votre chemin ici si différent
        ]
        
        for path in common_paths:
            print(f"   🔍 Vérification: {path}")
            if path.exists():
                print(f"      ✓ Dossier existe")
                if (path / 'ffmpeg.exe').exists():
                    print(f"   ✅ FFmpeg détecté: {path}")
                    return str(path)
                else:
                    print(f"      ✗ ffmpeg.exe non trouvé dans ce dossier")
            else:
                print(f"      ✗ Dossier n'existe pas")
        
        print("\n   ⚠️ FFmpeg non trouvé automatiquement")
        print("   💡 Exécutez: where.exe ffmpeg")
        print("   💡 Ou ajoutez le chemin manuellement dans downloader.py ligne 182")
        return None


# Test du module
if __name__ == '__main__':
    # Test avec une vidéo YT
    downloader = YTDownloader('temp', 'music')
    
    result = downloader.download(
        url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        metadata={
            'artist': 'Rick Astley',
            'album': 'Whenever You Need Somebody',
            'title': 'Never Gonna Give You Up',
            'year': '1987'
        }
    )
    
    print("\n📊 Résultat:")
    print(result)
