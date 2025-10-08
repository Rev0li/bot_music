"""
parser.py - Extraction des métadonnées depuis les noms de fichiers

Ce module parse les noms de fichiers au format:
    art=Artiste alb=Album N=Titre Y=Année.mp3

Seuls art= et N= sont obligatoires.
"""

import re
from typing import Tuple, Optional


class MetadataParser:
    """
    Parse les métadonnées depuis les noms de fichiers MP3.
    
    Format accepté: art=Artist alb=Album N=Title Y=Year.mp3
    Obligatoire: art= et N=
    Optionnel: alb= et Y=
    """
    
    def __init__(self):
        """Initialise le parser avec les patterns regex."""
        self.patterns = {
            'artist': r"art=([^=]+?)(?:\s+(?:alb|N|Y)=|\.mp3|$)",
            'album': r"alb=([^=]+?)(?:\s+(?:art|N|Y)=|\.mp3|$)",
            'title': r"N=([^=]+?)(?:\s+(?:art|alb|Y)=|\.mp3|$)",
            'year': r"Y=(\d{4})"
        }
    
    def parse(self, filename: str) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        """
        Parse un nom de fichier et extrait les métadonnées.
        
        Args:
            filename (str): Nom du fichier à parser
            
        Returns:
            Tuple[str, str, str, str]: (artist, album, title, year)
            - artist: Nom de l'artiste (obligatoire)
            - album: Nom de l'album (optionnel, défaut: "Unknown Album")
            - title: Titre de la chanson (obligatoire)
            - year: Année (optionnel, défaut: "Unknown")
            
        Examples:
            >>> parser = MetadataParser()
            >>> parser.parse("art=Drake alb=Views N=OneDance Y=2016.mp3")
            ('Drake', 'Views', 'OneDance', '2016')
            
            >>> parser.parse("art=Drake N=OneDance.mp3")
            ('Drake', 'Unknown Album', 'OneDance', 'Unknown')
        """
        # Extraire chaque champ
        artist = self._extract_field(filename, 'artist')
        album = self._extract_field(filename, 'album')
        title = self._extract_field(filename, 'title')
        year = self._extract_field(filename, 'year')
        
        # Vérifier les champs obligatoires
        if not artist or not title:
            return None, None, None, None
        
        # Valeurs par défaut pour les champs optionnels
        album = album or "Unknown Album"
        year = year or "Unknown"
        
        return artist, album, title, year
    
    def _extract_field(self, filename: str, field: str) -> Optional[str]:
        """
        Extrait un champ spécifique du nom de fichier.
        
        Args:
            filename (str): Nom du fichier
            field (str): Nom du champ ('artist', 'album', 'title', 'year')
            
        Returns:
            Optional[str]: Valeur du champ ou None si non trouvé
        """
        pattern = self.patterns.get(field)
        if not pattern:
            return None
        
        match = re.search(pattern, filename)
        if match:
            return match.group(1).strip()
        
        return None
    
    def is_valid(self, filename: str) -> bool:
        """
        Vérifie si un nom de fichier est valide (contient art= et N=).
        
        Args:
            filename (str): Nom du fichier à vérifier
            
        Returns:
            bool: True si valide, False sinon
            
        Examples:
            >>> parser = MetadataParser()
            >>> parser.is_valid("art=Drake N=OneDance.mp3")
            True
            >>> parser.is_valid("Drake - OneDance.mp3")
            False
        """
        artist, _, title, _ = self.parse(filename)
        return artist is not None and title is not None
    
    def get_info_string(self, filename: str) -> str:
        """
        Retourne une chaîne formatée avec les infos trouvées.
        
        Args:
            filename (str): Nom du fichier
            
        Returns:
            str: Chaîne formatée "art=... alb=... N=... Y=..."
            
        Examples:
            >>> parser = MetadataParser()
            >>> parser.get_info_string("art=Drake alb=Views N=OneDance Y=2016.mp3")
            'art=Drake alb=Views N=OneDance Y=2016'
        """
        artist, album, title, year = self.parse(filename)
        
        if not artist or not title:
            return "Format invalide"
        
        parts = [f"art={artist}", f"N={title}"]
        
        if album != "Unknown Album":
            parts.insert(1, f"alb={album}")
        
        if year != "Unknown":
            parts.append(f"Y={year}")
        
        return " ".join(parts)
