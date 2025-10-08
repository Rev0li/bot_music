#!/usr/bin/env python3
"""
user_profile.py - Système de profil utilisateur avec préférences
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class UserProfile:
    """
    Gestionnaire de profil utilisateur avec préférences.
    Centralise tous les paramètres et chemins par défaut.
    """
    
    def __init__(self, profile_path: Optional[str] = None):
        """
        Initialise le profil utilisateur.
        
        Args:
            profile_path (str, optional): Chemin vers le fichier de profil
        """
        self.profile_path = profile_path or self._get_default_profile_path()
        self.preferences = self._load_defaults()
        self._load_profile()
    
    def _get_default_profile_path(self) -> str:
        """Récupère le chemin par défaut du profil."""
        app_data = os.path.expanduser("~")
        profile_dir = os.path.join(app_data, ".music_organizer")
        os.makedirs(profile_dir, exist_ok=True)
        return os.path.join(profile_dir, "profile.json")
    
    def _load_defaults(self) -> Dict[str, Any]:
        """Charge les préférences par défaut."""
        return {
            # Chemins par défaut
            "music_folder": os.path.join(os.path.expanduser("~"), "Music", "itunes"),
            "download_folder": os.path.join(os.path.expanduser("~"), "Downloads"),
            "temp_folder": os.path.join(os.path.expanduser("~"), "Music", "temp"),
            
            # Préférences générales
            "auto_save_enabled": True,
            "auto_paste_enabled": True,
            "debug_mode": False,
            "theme": "dark",
            
            # Préférences de scan
            "scan_recursive": True,
            "scan_extensions": [".mp3", ".m4a", ".flac"],
            "ignore_existing_tags": False,
            
            # Préférences d'organisation
            "organize_structure": "artist_album_title",  # artist_album_title, artist_title, etc.
            "update_tags": True,
            "create_playlists": False,
            
            # Préférences de téléchargement
            "monitor_enabled": True,
            "notification_enabled": True,
            "auto_click_save": False,
            
            # Statistiques
            "stats_downloads": 0,
            "stats_organized": 0,
            "last_scan_date": None,
            "last_download_date": None
        }
    
    def _load_profile(self):
        """Charge le profil depuis le fichier."""
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, 'r', encoding='utf-8') as f:
                    saved_preferences = json.load(f)
                
                # Fusionner avec les défauts
                self.preferences.update(saved_preferences)
                
            except Exception as e:
                print(f"Erreur chargement profil: {e}")
    
    def _save_profile(self):
        """Sauvegarde le profil dans le fichier."""
        try:
            os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
            
            with open(self.profile_path, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Erreur sauvegarde profil: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Récupère une préférence.
        
        Args:
            key (str): Clé de la préférence
            default (Any): Valeur par défaut si clé inexistante
            
        Returns:
            Any: Valeur de la préférence
        """
        return self.preferences.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Définit une préférence.
        
        Args:
            key (str): Clé de la préférence
            value (Any): Nouvelle valeur
        """
        self.preferences[key] = value
        self._save_profile()
    
    def update(self, preferences: Dict[str, Any]):
        """
        Met à jour plusieurs préférences.
        
        Args:
            preferences (Dict[str, Any]): Dictionnaire de préférences
        """
        self.preferences.update(preferences)
        self._save_profile()
    
    def reset_to_defaults(self):
        """Remet les préférences par défaut."""
        self.preferences = self._load_defaults()
        self._save_profile()
    
    def get_path(self, path_type: str) -> str:
        """
        Récupère un chemin selon son type.
        
        Args:
            path_type (str): Type de chemin (music_folder, download_folder, temp_folder)
            
        Returns:
            str: Chemin absolu
        """
        path = self.get(path_type, "")
        if not os.path.isabs(path):
            # Convertir en chemin absolu par rapport au home
            path = os.path.join(os.path.expanduser("~"), path)
        return path
    
    def set_path(self, path_type: str, path: str):
        """
        Définit un chemin.
        
        Args:
            path_type (str): Type de chemin
            path (str): Nouveau chemin
        """
        self.set(path_type, path)
    
    def increment_stat(self, stat_key: str):
        """
        Incrémente une statistique.
        
        Args:
            stat_key (str): Clé de la statistique
        """
        current = self.get(stat_key, 0)
        self.set(stat_key, current + 1)
    
    def update_last_action(self, action_type: str):
        """
        Met à jour la date de dernière action.
        
        Args:
            action_type (str): Type d'action (scan, download)
        """
        from datetime import datetime
        self.set(f"last_{action_type}_date", datetime.now().isoformat())
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques.
        
        Returns:
            Dict[str, Any]: Statistiques utilisateur
        """
        return {
            "downloads": self.get("stats_downloads", 0),
            "organized": self.get("stats_organized", 0),
            "last_scan": self.get("last_scan_date"),
            "last_download": self.get("last_download_date")
        }

# Instance globale du profil utilisateur
user_profile = UserProfile()

def get_user_profile() -> UserProfile:
    """Récupère l'instance globale du profil utilisateur."""
    return user_profile
