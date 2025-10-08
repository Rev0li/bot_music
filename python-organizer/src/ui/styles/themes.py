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
                    "primary": "#1f538d",
                    "secondary": "#14375e", 
                    "success": "#4CAF50",
                    "warning": "#FF9800",
                    "error": "#f44336",
                    "info": "#2196F3",
                    "bg_primary": "#212121",
                    "bg_secondary": "#2b2b2b",
                    "text_primary": "#ffffff",
                    "text_secondary": "#b0b0b0",
                    "border": "#404040",
                    "hover": "#1565C0"
                }
            },
            "light": {
                "name": "Light Theme", 
                "ctk_theme": "blue",
                "colors": {
                    "primary": "#1976D2",
                    "secondary": "#1565C0",
                    "success": "#4CAF50", 
                    "warning": "#FF9800",
                    "error": "#f44336",
                    "info": "#2196F3",
                    "bg_primary": "#ffffff",
                    "bg_secondary": "#f5f5f5",
                    "text_primary": "#212121",
                    "text_secondary": "#757575",
                    "border": "#e0e0e0",
                    "hover": "#1976D2"
                }
            },
            "music": {
                "name": "Music Theme",
                "ctk_theme": "dark-blue", 
                "colors": {
                    "primary": "#8e24aa",
                    "secondary": "#7b1fa2",
                    "success": "#4CAF50",
                    "warning": "#FF9800", 
                    "error": "#f44336",
                    "info": "#9c27b0",
                    "bg_primary": "#1a1a1a",
                    "bg_secondary": "#2d2d2d",
                    "text_primary": "#ffffff",
                    "text_secondary": "#b39ddb",
                    "border": "#4a148c",
                    "hover": "#9c27b0"
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
