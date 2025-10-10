#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
organizer.py - Organisation des fichiers MP3

FONCTIONNALITÉ:
  - Organise les MP3 en structure Artist/Album/Title.mp3
  - Met à jour les tags ID3
  - Gère les doublons
"""

from pathlib import Path
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, APIC
import shutil
from datetime import datetime
import mimetypes


class MusicOrganizer:
    """Organisateur de fichiers musicaux"""
    
    def __init__(self, music_dir):
        self.music_dir = Path(music_dir)
        self.music_dir.mkdir(exist_ok=True, parents=True)
    
    def organize(self, file_path, metadata):
        """
        Organise un fichier MP3 dans la structure Artist/Album/Title.mp3
        
        Args:
            file_path (str): Chemin du fichier MP3 temporaire
            metadata (dict): {artist, album, title, year}
            
        Returns:
            dict: {success, final_path, error}
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"Fichier non trouvé: {file_path}")
            
            print(f"\n📁 Organisation du fichier: {file_path.name}")
            
            # Extraire les métadonnées
            artist = metadata.get('artist', 'Unknown Artist')
            album = metadata.get('album', 'Unknown Album')
            title = metadata.get('title', 'Unknown Title')
            year = metadata.get('year', '')
            
            # Nettoyer les noms (caractères interdits)
            artist = self._clean_filename(artist)
            album = self._clean_filename(album)
            title = self._clean_filename(title)
            
            print(f"   🎤 Artiste: {artist}")
            print(f"   💿 Album: {album}")
            print(f"   🎵 Titre: {title}")
            print(f"   📅 Année: {year}")
            
            # Créer la structure de dossiers
            artist_dir = self.music_dir / artist
            album_dir = artist_dir / album
            album_dir.mkdir(parents=True, exist_ok=True)
            
            # Chemin final
            final_path = album_dir / f"{title}.mp3"
            
            # Gérer les doublons
            if final_path.exists():
                print(f"   ⚠️ Fichier existant, ajout d'un suffixe...")
                counter = 1
                while final_path.exists():
                    final_path = album_dir / f"{title} ({counter}).mp3"
                    counter += 1
            
            # Copier le fichier
            print(f"   📋 Copie vers: {final_path}")
            shutil.copy2(file_path, final_path)
            
            # Chercher la pochette (image téléchargée par yt-dlp)
            thumbnail_path = self._find_thumbnail(file_path)
            
            # Mettre à jour les tags ID3
            print(f"   🏷️ Mise à jour des tags ID3...")
            self._update_tags(final_path, metadata, thumbnail_path)
            
            # Supprimer le fichier temporaire
            file_path.unlink()
            print(f"   🗑️ Fichier temporaire supprimé")
            
            # Supprimer la pochette temporaire si elle existe
            if thumbnail_path and thumbnail_path.exists():
                thumbnail_path.unlink()
                print(f"   🗑️ Pochette temporaire supprimée")
            
            print(f"   ✅ Organisation terminée!")
            
            return {
                'success': True,
                'final_path': str(final_path.relative_to(self.music_dir)),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _clean_filename(self, name):
        """Nettoie un nom de fichier (supprime les caractères interdits)"""
        # Caractères interdits sur Windows
        forbidden = '<>:"/\\|?*'
        for char in forbidden:
            name = name.replace(char, '')
        return name.strip()
    
    def _find_thumbnail(self, mp3_path):
        """Cherche la pochette téléchargée par yt-dlp"""
        mp3_path = Path(mp3_path)
        base_name = mp3_path.stem
        
        # Extensions d'images possibles
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        
        for ext in image_extensions:
            thumbnail = mp3_path.parent / f"{base_name}{ext}"
            if thumbnail.exists():
                print(f"   🖼️ Pochette trouvée: {thumbnail.name}")
                return thumbnail
        
        return None
    
    def _update_tags(self, file_path, metadata, thumbnail_path=None):
        """Met à jour les tags ID3 d'un fichier MP3 avec pochette"""
        try:
            # Charger le fichier MP3
            audio = MP3(file_path, ID3=ID3)
            
            # Ajouter les tags ID3 si ils n'existent pas
            try:
                audio.add_tags()
            except:
                pass
            
            # Mettre à jour les tags textuels
            audio.tags['TIT2'] = TIT2(encoding=3, text=metadata.get('title', ''))
            audio.tags['TPE1'] = TPE1(encoding=3, text=metadata.get('artist', ''))
            audio.tags['TALB'] = TALB(encoding=3, text=metadata.get('album', ''))
            
            if metadata.get('year'):
                audio.tags['TDRC'] = TDRC(encoding=3, text=metadata.get('year', ''))
            
            # Ajouter la pochette si disponible
            if thumbnail_path and thumbnail_path.exists():
                with open(thumbnail_path, 'rb') as img_file:
                    img_data = img_file.read()
                
                # Déterminer le type MIME
                mime_type = mimetypes.guess_type(str(thumbnail_path))[0]
                if not mime_type:
                    mime_type = 'image/jpeg'
                
                # Ajouter la pochette
                audio.tags['APIC'] = APIC(
                    encoding=3,
                    mime=mime_type,
                    type=3,  # Cover (front)
                    desc='Cover',
                    data=img_data
                )
                print(f"      🖼️ Pochette intégrée au MP3")
            
            # Sauvegarder
            audio.save()
            
            print(f"      ✅ Tags ID3 mis à jour")
            
        except Exception as e:
            print(f"      ⚠️ Erreur lors de la mise à jour des tags: {str(e)}")
    
    def get_stats(self):
        """Retourne les statistiques de la bibliothèque musicale"""
        try:
            artists = [d for d in self.music_dir.iterdir() if d.is_dir()]
            
            total_albums = 0
            total_songs = 0
            
            for artist_dir in artists:
                albums = [d for d in artist_dir.iterdir() if d.is_dir()]
                total_albums += len(albums)
                
                for album_dir in albums:
                    songs = list(album_dir.glob('*.mp3'))
                    total_songs += len(songs)
            
            return {
                'artists': len(artists),
                'albums': total_albums,
                'songs': total_songs
            }
        except Exception as e:
            return {
                'artists': 0,
                'albums': 0,
                'songs': 0,
                'error': str(e)
            }


# Test du module
if __name__ == '__main__':
    organizer = MusicOrganizer('music')
    
    # Simuler un fichier téléchargé
    # (créer un fichier de test)
    
    stats = organizer.get_stats()
    print(f"\n📊 Statistiques:")
    print(f"   Artistes: {stats['artists']}")
    print(f"   Albums: {stats['albums']}")
    print(f"   Chansons: {stats['songs']}")
