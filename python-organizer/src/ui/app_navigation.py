"""
app_navigation.py - Application principale avec navigation par catégories
"""

import customtkinter as ctk
import tkinter as tk
from typing import Optional

# Ajouter le chemin vers les modules
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from .styles.themes import theme_manager
from .components.navigation import NavigationManager, create_categories_config
from .components.buttons import ModernButton, ToggleButton, IconButton

class NavigationApp:
    """Application principale avec navigation par catégories."""
    
    def __init__(self):
        """Initialise l'application."""
        
        # Profil utilisateur (en premier)
        self._load_user_profile()
        
        # Adaptateur de services
        self._initialize_services()
        
        # Configuration CustomTkinter
        self._setup_customtkinter()
        
        # Créer la fenêtre principale
        self._create_main_window()
        
        # Créer l'interface avec navigation
        self._create_interface()
        
        # Appliquer le thème par défaut (soft et léger)
        theme_manager.apply_theme("soft")
    
    def _setup_customtkinter(self):
        """Configure CustomTkinter."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        ctk.deactivate_automatic_dpi_awareness()
    def _create_main_window(self):
        """Crée la fenêtre principale."""
        self.root = ctk.CTk()
        
        # Configuration de la fenêtre
        self.root.title("Music Organizer Pro - Navigation Edition")
        self.root.geometry("1300x800")      # Légèrement plus petit
        self.root.minsize(900, 600)         # Minimum plus petit
        
        # Centrer la fenêtre
        self._center_window()
        
        # Gestionnaire de fermeture
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran."""
        self.root.update_idletasks()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"+{x}+{y}")
    
    def _create_interface(self):
        """Crée l'interface avec navigation."""
        # Container principal
        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
        # Configuration des catégories
        categories = create_categories_config()
        
        # Créer la navigation
        self.navigation = NavigationManager(self.main_container, categories, services=self.services)
        
        # Barre de statut
        self._create_status_bar()
    
    def _initialize_services(self):
        """Initialise l'adaptateur de services."""
        try:
            from ..core.services.service_adapter import get_service_adapter
            self.services = get_service_adapter(log_callback=self._log_to_ui)
            print("Services initialises avec succes")
        except ImportError as e:
            print(f"Erreur initialisation services: {e}")
            self.services = None
    
    def _log_to_ui(self, message: str):
        """Log un message dans l'interface."""
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)
    
    def _load_user_profile(self):
        """Charge le profil utilisateur."""
        try:
            from ..core.utils.user_profile import get_user_profile
            self.profile = get_user_profile()
            print(f"Profil utilisateur charge: {self.profile.get('music_folder', 'N/A')}")
        except ImportError:
            print("Profil utilisateur non disponible")
            self.profile = None
    
    def _on_closing(self):
        """Gestionnaire de fermeture."""
        try:
            # Sauvegarder le profil si disponible
            if self.profile:
                self.profile._save_profile()
        except:
            pass
        
        self.root.quit()
        self.root.destroy()
    
    def update_status(self, message: str):
        """
        Met à jour le message de statut.
        
        Args:
            message (str): Message de statut
        """
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)
    
    def run(self):
        """Lance l'application."""
        try:
            # Log de démarrage
            print("Music Organizer Pro - Navigation Edition")
            print("Interface avec navigation par categories")
            print(f"Theme actuel: {theme_manager.current_theme}")
            
            if self.profile:
                print(f"Profil: {self.profile.profile_path}")
            
            # Démarrer la boucle principale
            self.root.mainloop()
            
        except KeyboardInterrupt:
            print("\nArret demande par l'utilisateur")
            self._on_closing()
        except Exception as e:
            print(f"Erreur fatale: {e}")
            self._on_closing()

def main():
    """Point d'entrée principal."""
    try:
        app = NavigationApp()
        app.run()
    except Exception as e:
        print(f"Erreur demarrage: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
