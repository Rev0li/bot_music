"""
themes.py - Gestionnaire de thèmes moderne pour l'application
"""

import customtkinter as ctk
from typing import Dict, Any

class ThemeManager:
    """Gestionnaire de thèmes pour l'application."""
    
    def __init__(self):
        """Initialise le gestionnaire de thèmes."""
        self.current_theme = "dark"
        self.themes = {
            "dark": {
                "name": "Dark Theme",
                "ctk_theme": "dark-blue",
                "colors": {
                    "primary": "#4a90e2",      # Bleu plus doux
                    "secondary": "#5ba0f2",    # Bleu complémentaire
                    "success": "#7cb342",      # Vert plus doux
                    "warning": "#ffa726",      # Orange plus doux
                    "error": "#e57373",       # Rouge plus doux
                    "info": "#42a5f5",        # Bleu info doux
                    "bg_primary": "#2d2d2d",   # Gris foncé plus doux
                    "bg_secondary": "#3a3a3a", # Gris moyen
                    "text_primary": "#f5f5f5", # Blanc cassé
                    "text_secondary": "#c0c0c0", # Gris clair
                    "border": "#555555",       # Bordure douce
                    "hover": "#5ba0f2"         # Bleu hover doux
                }
            },
            "light": {
                "name": "Light Theme", 
                "ctk_theme": "blue",
                "colors": {
                    "primary": "#4a90e2",      # Bleu doux
                    "secondary": "#5ba0f2",    # Bleu complémentaire
                    "success": "#7cb342",      # Vert doux
                    "warning": "#ffa726",      # Orange doux
                    "error": "#e57373",       # Rouge doux
                    "info": "#42a5f5",        # Bleu info
                    "bg_primary": "#ffffff",   # Blanc pur
                    "bg_secondary": "#f8f9fa", # Gris très clair
                    "text_primary": "#2d2d2d", # Gris foncé
                    "text_secondary": "#6c757d", # Gris moyen
                    "border": "#e9ecef",       # Bordure claire
                    "hover": "#4a90e2"         # Bleu hover
                }
            },
            "soft": {
                "name": "Soft Theme",
                "ctk_theme": "dark-blue",
                "colors": {
                    "primary": "#6fa8d4",      # Bleu très doux
                    "secondary": "#8bb8d8",    # Bleu complémentaire doux
                    "success": "#8bc34a",      # Vert tendre
                    "warning": "#ffb74d",      # Orange tendre
                    "error": "#f48fb1",       # Rose tendre
                    "info": "#64b5f6",        # Bleu ciel
                    "bg_primary": "#f5f5f5",   # Gris très clair
                    "bg_secondary": "#eeeeee", # Gris clair
                    "text_primary": "#424242", # Gris foncé doux
                    "text_secondary": "#9e9e9e", # Gris moyen
                    "border": "#e0e0e0",       # Bordure très claire
                    "hover": "#8bb8d8"         # Hover doux
                }
            }
        }
    
    def apply_theme(self, theme_name: str = None):
        """
        Applique un thème à l'application.
        
        Args:
            theme_name (str): Nom du thème à appliquer
        """
        if theme_name:
            self.current_theme = theme_name
            
        theme = self.themes.get(self.current_theme, self.themes["dark"])
        
        # Appliquer le thème CustomTkinter
        ctk.set_appearance_mode("dark" if "dark" in theme["ctk_theme"] else "light")
        ctk.set_default_color_theme(theme["ctk_theme"])
    
    def get_color(self, color_name: str) -> str:
        """
        Récupère une couleur du thème actuel.
        
        Args:
            color_name (str): Nom de la couleur
            
        Returns:
            str: Code couleur hexadécimal
        """
        theme = self.themes.get(self.current_theme, self.themes["dark"])
        return theme["colors"].get(color_name, "#ffffff")
    
    def get_theme_list(self) -> list:
        """
        Récupère la liste des thèmes disponibles.
        
        Returns:
            list: Liste des noms de thèmes
        """
        return list(self.themes.keys())
    
    def get_theme_info(self, theme_name: str = None) -> Dict[str, Any]:
        """
        Récupère les informations d'un thème.
        
        Args:
            theme_name (str): Nom du thème
            
        Returns:
            dict: Informations du thème
        """
        if not theme_name:
            theme_name = self.current_theme
        return self.themes.get(theme_name, self.themes["dark"])

# Instance globale du gestionnaire de thèmes
theme_manager = ThemeManager()
