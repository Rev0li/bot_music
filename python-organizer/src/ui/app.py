"""
app.py - Application principale moderne avec CustomTkinter
"""

import customtkinter as ctk
import tkinter as tk
from typing import Optional
import sys
import os

# Ajouter le chemin vers les modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from .styles.themes import theme_manager
from .pages.main_page import MainPage

class ModernMusicOrganizerApp:
    """Application principale moderne Music Organizer."""
    
    def __init__(self):
        """Initialise l'application."""
        
        # Configuration CustomTkinter
        self._setup_customtkinter()
        
        # Créer la fenêtre principale
        self._create_main_window()
        
        # Créer l'interface
        self._create_interface()
        
        # Appliquer le thème
        theme_manager.apply_theme("dark")
    
    def _setup_customtkinter(self):
        """Configure CustomTkinter."""
        # Mode d'apparence (dark/light)
        ctk.set_appearance_mode("dark")
        
        # Thème de couleur
        ctk.set_default_color_theme("dark-blue")
        
        # Configuration des widgets
        ctk.deactivate_automatic_dpi_awareness()  # Optionnel
    
    def _create_main_window(self):
        """Crée la fenêtre principale."""
        self.root = ctk.CTk()
        
        # Configuration de la fenêtre
        self.root.title("🎵 Music Organizer Pro - Modern Edition")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Icône (si disponible)
        try:
            # self.root.iconbitmap("assets/icon.ico")  # Décommentez si vous avez une icône
            pass
        except:
            pass
        
        # Configuration de la grille
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Centrer la fenêtre
        self._center_window()
        
        # Gestionnaire de fermeture
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran."""
        self.root.update_idletasks()
        
        # Dimensions de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Dimensions de la fenêtre
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Calculer la position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Positionner la fenêtre
        self.root.geometry(f"+{x}+{y}")
    
    def _create_interface(self):
        """Crée l'interface utilisateur."""
        # Container principal
        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Page principale
        self.main_page = MainPage(self.main_container)
        self.main_page.grid(row=0, column=0, sticky="nsew")
        
        # Barre de statut (optionnelle)
        self._create_status_bar()
    
    def _create_status_bar(self):
        """Crée une barre de statut en bas."""
        self.status_bar = ctk.CTkFrame(
            self.root,
            height=30,
            fg_color=theme_manager.get_color("bg_secondary")
        )
        self.status_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.status_bar.grid_propagate(False)
        
        # Label de statut
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Prêt",
            font=ctk.CTkFont(size=10),
            text_color=theme_manager.get_color("text_secondary")
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Version
        version_label = ctk.CTkLabel(
            self.status_bar,
            text="v2.0 Modern",
            font=ctk.CTkFont(size=10),
            text_color=theme_manager.get_color("text_secondary")
        )
        version_label.pack(side="right", padx=10, pady=5)
    
    def _on_closing(self):
        """Gestionnaire de fermeture de l'application."""
        try:
            # Arrêter le moniteur si actif
            if hasattr(self.main_page, 'monitor') and self.main_page.monitor:
                if self.main_page.monitor.is_active():
                    self.main_page.monitor.stop()
            
            # Fermer l'application
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            print(f"Erreur lors de la fermeture: {e}")
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
            self.main_page.log("Music Organizer Pro - Modern Edition")
            self.main_page.log("Interface moderne chargee avec CustomTkinter")
            self.main_page.log(f"Theme actuel: {theme_manager.current_theme}")
            
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
        # Créer et lancer l'application
        app = ModernMusicOrganizerApp()
        app.run()
        
    except Exception as e:
        print(f"Erreur lors du demarrage: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
