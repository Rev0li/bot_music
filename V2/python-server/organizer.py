"""
organizer.py - Organisation des fichiers MP3

Ce module gère:
- Le scan des fichiers MP3
- La mise à jour des tags ID3
- L'organisation en dossiers Artiste/Album/
- Le déplacement des fichiers
"""

import os
import shutil
from typing import List, Dict, Callable, Optional
from mutagen.easyid3 import EasyID3

from .parser import MetadataParser


class MusicOrganizer:
    """
    Organise les fichiers MP3 en structure Artiste/Album/.
    Met à jour les tags ID3 avec les métadonnées extraites.
    """
    
    def __init__(self, base_folder: str, log_callback: Optional[Callable] = None):
        """
        Initialise l'organisateur de musique.
        
        Args:
            base_folder (str): Dossier racine contenant les MP3
            log_callback (Callable, optional): Fonction pour logger les messages
        """
        self.base_folder = base_folder
        self.parser = MetadataParser()
        self.log_callback = log_callback or print
        self.songs_found = []
    
    def log(self, message: str):
        """
        Log un message via le callback.
        
        Args:
            message (str): Message à logger
        """
        if self.log_callback:
            self.log_callback(message)
    
    def scan(self) -> List[Dict]:
        """
        Scanne le dossier pour trouver les fichiers MP3 valides.
        
        Returns:
            List[Dict]: Liste des chansons trouvées avec leurs métadonnées
            
        Examples:
            >>> organizer = MusicOrganizer("/path/to/music")
            >>> songs = organizer.scan()
            >>> len(songs)
            42
        """
        self.log("\n🔍 Scan en cours...")
        self.songs_found = []
        
        for root, _, files in os.walk(self.base_folder):
            for file in files:
                if file.lower().endswith(".mp3"):
                    full_path = os.path.join(root, file)
                    self._process_file(file, full_path)
        
        count = len(self.songs_found)
        self.log(f"\n✅ Scan terminé: {count} chanson(s) trouvée(s)")
        
        return self.songs_found
    
    def _process_file(self, filename: str, full_path: str):
        """
        Traite un fichier MP3 individuel.
        
        Args:
            filename (str): Nom du fichier
            full_path (str): Chemin complet du fichier
        """
        artist, album, title, year = self.parser.parse(filename)
        
        if artist and title:
            self.songs_found.append({
                'path': full_path,
                'filename': filename,
                'artist': artist,
                'album': album,
                'title': title,
                'year': year
            })
            
            info = self.parser.get_info_string(filename)
            self.log(f"✅ Trouvé: {info}")
        else:
            self.log(f"⚠️  Ignoré (manque art= ou N=): {filename}")
    
    def organize(self, songs: Optional[List[Dict]] = None) -> tuple:
        """
        Organise les chansons trouvées.
        
        Args:
            songs (List[Dict], optional): Liste des chansons à organiser.
                                         Si None, utilise self.songs_found
        
        Returns:
            tuple: (success_count, error_count)
            
        Examples:
            >>> organizer = MusicOrganizer("/path/to/music")
            >>> organizer.scan()
            >>> success, errors = organizer.organize()
            >>> print(f"✅ {success} chansons organisées")
        """
        songs = songs or self.songs_found
        
        if not songs:
            self.log("❌ Aucune chanson à organiser")
            return 0, 0
        
        self.log("\n✨ Organisation en cours...\n")
        
        success = 0
        errors = 0
        total = len(songs)
        
        for i, song in enumerate(songs, 1):
            try:
                self._organize_song(song, i, total)
                success += 1
            except Exception as e:
                self.log(f"   ❌ Erreur: {str(e)}\n")
                errors += 1
        
        self._log_summary(success, errors)
        
        return success, errors
    
    def _organize_song(self, song: Dict, index: int, total: int):
        """
        Organise une chanson individuelle.
        
        Args:
            song (Dict): Dictionnaire contenant les infos de la chanson
            index (int): Index actuel
            total (int): Total de chansons
        """
        self.log(f"🎵 [{index}/{total}] {song['filename']}")
        self.log(f"   → Artiste: {song['artist']}")
        self.log(f"   → Album: {song['album']}")
        self.log(f"   → Titre: {song['title']}")
        self.log(f"   → Année: {song['year']}")
        
        # Mettre à jour les tags ID3
        self._update_id3_tags(song)
        
        # Créer la structure de dossiers
        new_path = self._create_folder_structure(song)
        
        # Déplacer le fichier
        shutil.move(song['path'], new_path)
        
        self.log(f"   ✅ Déplacé vers: {new_path}\n")
    
    def _update_id3_tags(self, song: Dict):
        """
        Met à jour les tags ID3 du fichier MP3.
        
        Args:
            song (Dict): Dictionnaire contenant les infos de la chanson
        """
        try:
            audio = EasyID3(song['path'])
        except Exception:
            audio = EasyID3()
        
        audio["artist"] = song['artist']
        audio["album"] = song['album']
        audio["title"] = song['title']
        audio["date"] = song['year']
        audio.save(song['path'])
    
    def _create_folder_structure(self, song: Dict) -> str:
        """
        Crée la structure de dossiers Artiste/Album/ et retourne le nouveau chemin.
        
        Args:
            song (Dict): Dictionnaire contenant les infos de la chanson
            
        Returns:
            str: Nouveau chemin complet du fichier
        """
        # Nettoyer les caractères invalides
        artist = self._clean_filename(song['artist'])
        album = self._clean_filename(song['album'])
        title = self._clean_filename(song['title'])
        
        # Créer les dossiers
        artist_folder = os.path.join(self.base_folder, artist)
        album_folder = os.path.join(artist_folder, album)
        os.makedirs(album_folder, exist_ok=True)
        
        # Nouveau chemin
        new_path = os.path.join(album_folder, f"{title}.mp3")
        
        return new_path
    
    def _clean_filename(self, filename: str) -> str:
        """
        Nettoie un nom de fichier en supprimant les caractères invalides.
        
        Args:
            filename (str): Nom à nettoyer
            
        Returns:
            str: Nom nettoyé
        """
        # Supprimer les caractères invalides pour Windows
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        
        return filename.strip()
    
    def _log_summary(self, success: int, errors: int):
        """
        Affiche un résumé de l'organisation.
        
        Args:
            success (int): Nombre de succès
            errors (int): Nombre d'erreurs
        """
        self.log(f"\n{'='*60}")
        self.log(f"🎉 Organisation terminée!")
        self.log(f"✅ Succès: {success}")
        if errors > 0:
            self.log(f"❌ Erreurs: {errors}")
        self.log(f"{'='*60}\n")
    
    def get_stats(self) -> Dict:
        """
        Retourne des statistiques sur les chansons trouvées.
        
        Returns:
            Dict: Statistiques (total, artistes uniques, albums uniques)
        """
        if not self.songs_found:
            return {'total': 0, 'artists': 0, 'albums': 0}
        
        artists = set(song['artist'] for song in self.songs_found)
        albums = set(song['album'] for song in self.songs_found)
        
        return {
            'total': len(self.songs_found),
            'artists': len(artists),
            'albums': len(albums)
        }
