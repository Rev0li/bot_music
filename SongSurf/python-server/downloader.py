#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
downloader.py - Module de téléchargement avec yt-dlp

FONCTIONNALITÉ:
  - Télécharge les vidéos YouTube en MP3 via yt-dlp
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


class YouTubeDownloader:
    """Téléchargeur YouTube avec yt-dlp"""
    
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
        Télécharge une vidéo YouTube en MP3
        
        Args:
            url (str): URL YouTube ou YouTube Music
            metadata (dict): {artist, album, title, year}
            
        Returns:
            dict: {success, file_path, error}
        """
        try:
            print(f"\n🎵 Téléchargement: {metadata.get('title', 'Unknown')}")
            print(f"   URL originale: {url}")
            
            # Convertir l'URL YouTube Music en URL YouTube classique
            if 'music.youtube.com' in url:
                # Extraire le video ID de l'URL YouTube Music
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
            
            # Configuration yt-dlp (optimisée pour YouTube Music)
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
    # Test avec une vidéo YouTube
    downloader = YouTubeDownloader('temp', 'music')
    
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
