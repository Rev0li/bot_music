"""
music_organizer.py - Organisation automatique des MP3 téléchargés

Organise les fichiers MP3 depuis a_trier/ vers music/Artiste/Album/
en utilisant les métadonnées du JSON correspondant.
"""

import os
import json
import shutil
from pathlib import Path
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError


class MusicOrganizer:
    """
    Organise automatiquement les MP3 téléchargés.
    """
    
    def __init__(self, music_folder: str):
        """
        Args:
            music_folder: Dossier racine où organiser (ex: music/)
        """
        self.music_folder = Path(music_folder)
        self.music_folder.mkdir(exist_ok=True)
    
    def organize_file(self, mp3_path: str, json_path: str) -> dict:
        """
        Organise un fichier MP3 avec son JSON.
        
        Args:
            mp3_path: Chemin du fichier MP3
            json_path: Chemin du JSON avec métadonnées
            
        Returns:
            dict: Résultat avec 'success', 'new_path', etc.
        """
        try:
            # Lire les métadonnées du JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            artist = metadata.get('artist', 'Unknown Artist')
            album = metadata.get('album', 'Unknown Album')
            title = metadata.get('title', 'Unknown Title')
            year = metadata.get('year', '')
            
            print(f"\n📁 Organisation de: {Path(mp3_path).name}")
            print(f"   🎤 Artiste: {artist}")
            print(f"   💿 Album: {album}")
            print(f"   🎵 Titre: {title}")
            print(f"   📅 Année: {year}")
            
            # Mettre à jour les tags ID3
            self._update_id3_tags(mp3_path, metadata)
            
            # Créer la structure de dossiers
            new_path = self._create_folder_structure(mp3_path, metadata)
            
            # Déplacer le fichier
            shutil.move(mp3_path, new_path)
            
            print(f"   ✅ Déplacé vers: {new_path}")
            
            return {
                'success': True,
                'new_path': str(new_path),
                'artist': artist,
                'album': album,
                'title': title
            }
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _update_id3_tags(self, mp3_path: str, metadata: dict):
        """
        Met à jour les tags ID3 du fichier MP3.
        """
        try:
            try:
                audio = EasyID3(mp3_path)
            except ID3NoHeaderError:
                audio = EasyID3()
            
            audio["artist"] = metadata.get('artist', 'Unknown Artist')
            audio["album"] = metadata.get('album', 'Unknown Album')
            audio["title"] = metadata.get('title', 'Unknown Title')
            
            if metadata.get('year'):
                audio["date"] = metadata['year']
            
            audio.save(mp3_path)
            print(f"   ✅ Tags ID3 mis à jour")
            
        except Exception as e:
            print(f"   ⚠️ Erreur tags ID3: {e}")
    
    def _create_folder_structure(self, mp3_path: str, metadata: dict) -> Path:
        """
        Crée la structure Artiste/Album/ et retourne le nouveau chemin.
        """
        # Nettoyer les noms
        artist = self._clean_filename(metadata.get('artist', 'Unknown Artist'))
        album = self._clean_filename(metadata.get('album', 'Unknown Album'))
        title = self._clean_filename(metadata.get('title', 'Unknown Title'))
        
        # Créer les dossiers
        artist_folder = self.music_folder / artist
        album_folder = artist_folder / album
        album_folder.mkdir(parents=True, exist_ok=True)
        
        # Nouveau chemin
        new_path = album_folder / f"{title}.mp3"
        
        # Gérer les doublons
        if new_path.exists():
            counter = 1
            while new_path.exists():
                new_path = album_folder / f"{title} ({counter}).mp3"
                counter += 1
        
        return new_path
    
    def _clean_filename(self, filename: str) -> str:
        """
        Nettoie un nom de fichier en supprimant les caractères invalides.
        """
        # Supprimer les caractères invalides pour Windows
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        
        # Remplacer les espaces multiples
        filename = ' '.join(filename.split())
        
        return filename.strip() or 'Unknown'
