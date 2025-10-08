"""
navigation.py - Système de navigation avec onglets pour les catégories
"""

import customtkinter as ctk
from typing import Dict, Any, Callable, Optional

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from core.utils.user_profile import get_user_profile
except ImportError:
    # Fallback
    def get_user_profile():
        class DummyProfile:
            def get(self, key, default=None):
                defaults = {
                    "music_folder": os.path.join(os.path.expanduser("~"), "Music", "itunes"),
                    "download_folder": os.path.join(os.path.expanduser("~"), "Downloads"),
                    "auto_save_enabled": True
                }
                return defaults.get(key, default)
        return DummyProfile()

class FallbackThemeManager:
    """Gestionnaire de thème de secours."""
    def get_color(self, color_name):
        colors = {
            "text_primary": "#2d2d2d",
            "text_secondary": "#6c757d",
            "success": "#4CAF50",
            "error": "#f44336",
            "bg_primary": "#ffffff",
            "bg_secondary": "#f8f9fa"
        }
        return colors.get(color_name, "#000000")

# Instance globale de secours
theme_manager = FallbackThemeManager()

class NavigationManager:
    """
    Gestionnaire de navigation avec onglets pour l'application.
    """
{{ ... }}
                    "music_folder": os.path.join(os.path.expanduser("~"), "Music", "itunes"),
                    "download_folder": os.path.join(os.path.expanduser("~"), "Downloads"),
                    "auto_save_enabled": True
                }
                return defaults.get(key, default)
        theme_manager = FallbackThemeManager()
    
    def __init__(self, parent, categories: Dict[str, Dict[str, Any]], services=None):
        """
        Initialise le gestionnaire de navigation.
        
        Args:
            parent: Widget parent
            categories (Dict[str, Dict[str, Any]]): Configuration des catégories
            services: Adaptateur de services (optionnel)
        """
        self.parent = parent
        self.categories = categories
        self.services = services
        self.current_category = None
        self.category_frames = {}
        self.callbacks = {}
        
        # Profil utilisateur
        self.profile = get_user_profile()
        
        # Créer l'interface de navigation
        self._create_navigation()
        self._create_content_area()
        
        # Sélectionner la première catégorie par défaut
        if self.categories:
            first_category = list(self.categories.keys())[0]
            self.switch_to_category(first_category)
    
    def _create_navigation(self):
        """Crée la barre de navigation."""
        self.nav_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Titre
        title_label = ctk.CTkLabel(
            self.nav_frame,
            text="🎵 Music Organizer Pro",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", pady=10)
        
        # Onglets de navigation
        self.tabs_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        self.tabs_frame.pack(side="right", pady=10)
        
        self.tab_buttons = {}
        
        for category_key, category_config in self.categories.items():
            # Bouton d'onglet
            tab_btn = ctk.CTkButton(
                self.tabs_frame,
                text=category_config["title"],
                command=lambda k=category_key: self.switch_to_category(k),
                font=ctk.CTkFont(size=12, weight="bold"),
                width=120,
                height=35,
                corner_radius=8
            )
            tab_btn.pack(side="left", padx=(0, 10))
            
            self.tab_buttons[category_key] = tab_btn
        
        # Séparateur
        separator = ctk.CTkFrame(self.nav_frame, height=2, fg_color="gray50")
        separator.pack(fill="x", pady=(0, 10))
    
    def _create_content_area(self):
        """Crée la zone de contenu principale."""
        self.content_frame = ctk.CTkFrame(
            self.parent,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Créer les frames pour chaque catégorie
        for category_key, category_config in self.categories.items():
            frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.category_frames[category_key] = frame
            
            # Créer le contenu de la catégorie
            if "create_func" in category_config:
                category_config["create_func"](frame, self)
    
    def switch_to_category(self, category_key: str):
        """
        Change de catégorie active.
        
        Args:
            category_key (str): Clé de la catégorie
        """
        if category_key not in self.categories:
            return
        
        # Masquer toutes les frames
        for key, frame in self.category_frames.items():
            if key == category_key:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()
        
        # Mettre à jour les boutons d'onglets
        for key, button in self.tab_buttons.items():
            if key == category_key:
                button.configure(
                    fg_color="#1f538d",
                    text_color="white"
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color="#666666"
                )
        
        # Mettre à jour la catégorie actuelle
        self.current_category = category_key
        
        # Callback de changement de catégorie
        if category_key in self.callbacks:
            self.callbacks[category_key]()
    
    def register_callback(self, category_key: str, callback: Callable):
        """
        Enregistre un callback pour une catégorie.
        
        Args:
            category_key (str): Clé de la catégorie
            callback (Callable): Fonction à appeler
        """
        self.callbacks[category_key] = callback
    
    def get_current_category(self) -> Optional[str]:
        """
        Récupère la catégorie actuelle.
        
        Returns:
            str: Clé de la catégorie actuelle
        """
        return self.current_category
    
    def get_category_frame(self, category_key: str):
        """
        Récupère le frame d'une catégorie.
        
        Args:
            category_key (str): Clé de la catégorie
            
        Returns:
            CTkFrame: Frame de la catégorie
        """
        return self.category_frames.get(category_key)

    # === Méthodes de gestion des fonctionnalités ===

    def start_monitoring(self):
        """Démarre le monitoring des téléchargements."""
        if hasattr(self, 'services'):
            success = self.services.start_monitoring()
            if success:
                # Mettre à jour l'interface
                download_frame = self.get_category_frame("download")
                if download_frame and hasattr(download_frame, 'status_label'):
                    download_frame.status_label.configure(
                        text="Monitoring: Actif",
                        text_color=theme_manager.get_color("success")
                    )
                    if hasattr(download_frame, 'start_btn'):
                        download_frame.start_btn.configure(state="disabled")
                    if hasattr(download_frame, 'stop_btn'):
                        download_frame.stop_btn.configure(state="normal")
            return success
        return False

    def stop_monitoring(self):
        """Arrête le monitoring des téléchargements."""
        if hasattr(self, 'services'):
            success = self.services.stop_monitoring()
            if success:
                # Mettre à jour l'interface
                download_frame = self.get_category_frame("download")
                if download_frame and hasattr(download_frame, 'status_label'):
                    download_frame.status_label.configure(
                        text="Monitoring: Arrêté",
                        text_color=theme_manager.get_color("error")
                    )
                    if hasattr(download_frame, 'start_btn'):
                        download_frame.start_btn.configure(state="normal")
                    if hasattr(download_frame, 'stop_btn'):
                        download_frame.stop_btn.configure(state="disabled")
            return success
        return False

    def set_auto_save(self, enabled: bool):
        """Active/désactive l'auto-save."""
        if hasattr(self, 'services'):
            self.services.set_auto_save(enabled)

    def browse_download_folder(self):
        """Ouvre le dialogue de sélection de dossier de téléchargement."""
        # TODO: Implémenter le dialogue de sélection
        print("Sélection du dossier de téléchargement...")

def create_download_category(parent, nav_manager):
    """
    Crée la catégorie de téléchargement avec fonctionnalités connectées.
    
    Args:
        parent: Frame parent
        nav_manager: Gestionnaire de navigation
    """
    # Récupérer le theme_manager depuis nav_manager ou utiliser le fallback
    theme_manager = getattr(nav_manager, 'theme_manager', None) or FallbackThemeManager()
    # Titre de la section
    title_label = ctk.CTkLabel(
        parent,
        text="Gestion des Téléchargements",
        font=ctk.CTkFont(size=16, weight="normal"),  # Police plus légère
        text_color=theme_manager.get_color("text_primary")
    )
    title_label.pack(pady=(20, 15))
    
    # Frame pour les contrôles
    controls_frame = ctk.CTkFrame(parent, fg_color="transparent")
    controls_frame.pack(fill="x", padx=20, pady=10)
    
    # Status du monitoring
    status_label = ctk.CTkLabel(
        controls_frame,
        text="Monitoring: Arrêté",
        font=ctk.CTkFont(size=11),
        text_color=theme_manager.get_color("text_secondary")
    )
    status_label.pack(pady=8)
    
    # Boutons de contrôle
    buttons_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
    buttons_frame.pack(pady=12)
    
    start_btn = ModernButton(
        buttons_frame,
        text="Démarrer",
        command=lambda: nav_manager.start_monitoring(),
        style="success"
    )
    start_btn.pack(side="left", padx=5)
    
    stop_btn = ModernButton(
        buttons_frame,
        text="Arrêter",
        command=lambda: nav_manager.stop_monitoring(),
        style="error"
    )
    stop_btn.pack(side="left", padx=5)
    
    # Switch Auto-Save
    auto_save_var = ctk.BooleanVar(value=True)
    auto_save_switch = ctk.CTkSwitch(
        controls_frame,
        text="Auto-Save",
        variable=auto_save_var,
        command=lambda: nav_manager.set_auto_save(auto_save_var.get()),
        font=ctk.CTkFont(size=10)
    )
    auto_save_switch.pack(pady=12)
    
    # Préférences de téléchargement
    prefs_frame = ctk.CTkFrame(parent, fg_color="transparent")
    prefs_frame.pack(fill="x", padx=20, pady=10)
    
    prefs_label = ctk.CTkLabel(
        prefs_frame,
        text="Préférences de Téléchargement",
        font=ctk.CTkFont(size=13, weight="normal"),
        text_color=theme_manager.get_color("text_primary")
    )
    prefs_label.pack(pady=8)
    
    # Dossier de téléchargement
    download_folder_frame = ctk.CTkFrame(prefs_frame, fg_color="transparent")
    download_folder_frame.pack(fill="x", pady=8)
    
    download_label = ctk.CTkLabel(
        download_folder_frame,
        text="Dossier de téléchargement:",
        font=ctk.CTkFont(size=10),
        text_color=theme_manager.get_color("text_secondary")
    )
    download_label.pack(side="left")
    
    download_entry = ctk.CTkEntry(
        download_folder_frame,
        placeholder_text="Sélectionnez le dossier...",
        width=280,
        font=ctk.CTkFont(size=10)
    )
    download_entry.pack(side="left", padx=10)
    
    download_btn = ModernButton(
        download_folder_frame,
        text="Parcourir",
        command=lambda: nav_manager.browse_download_folder(),
        style="secondary"
    )
    download_btn.pack(side="left")
    
    # Stocker les références pour les autres méthodes
    parent.status_label = status_label
    parent.start_btn = start_btn
    parent.stop_btn = stop_btn
    parent.auto_save_switch = auto_save_switch
    parent.download_entry = download_entry

def create_organize_category(parent, nav_manager):
    """
    Crée la catégorie d'organisation.
    
    Args:
        parent: Frame parent
        nav_manager: Gestionnaire de navigation
    """
    # Titre de la section
    title_label = ctk.CTkLabel(
        parent,
        text="📁 Organisation Musicale",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    title_label.pack(pady=(20, 10))
    
    # Frame pour les contrôles
    controls_frame = ctk.CTkFrame(parent, fg_color="transparent")
    controls_frame.pack(fill="x", padx=20, pady=10)
    
    # Sélection de dossier
    folder_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
    folder_frame.pack(fill="x", pady=10)
    
    folder_label = ctk.CTkLabel(
        folder_frame,
        text="📂 Dossier à organiser:",
        font=ctk.CTkFont(size=11)
    )
    folder_label.pack(side="left")
    
    folder_entry = ctk.CTkEntry(
        folder_frame,
        placeholder_text="Sélectionnez le dossier...",
        width=300
    )
    folder_entry.pack(side="left", padx=10)
    
    folder_btn = ctk.CTkButton(
        folder_frame,
        text="Parcourir",
        command=lambda: print("Sélection dossier organisation...")
    )
    folder_btn.pack(side="left")
    
    # Boutons d'action
    actions_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
    actions_frame.pack(fill="x", pady=20)
    
    scan_btn = ctk.CTkButton(
        actions_frame,
        text="🔍 Scanner",
        command=lambda: print("Scan des fichiers..."),
        width=150
    )
    scan_btn.pack(side="left", padx=5)
    
    organize_btn = ctk.CTkButton(
        actions_frame,
        text="📋 Organiser",
        command=lambda: print("Organisation des fichiers..."),
        width=150
    )
    organize_btn.pack(side="left", padx=5)
    
    # Statistiques
    stats_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
    stats_frame.pack(fill="x", pady=10)
    
    stats_label = ctk.CTkLabel(
        stats_frame,
        text="📊 Statistiques:",
        font=ctk.CTkFont(size=12, weight="bold")
    )
    stats_label.pack(anchor="w")
    
    # Frame pour les stats
    stats_values = ctk.CTkFrame(stats_frame, fg_color="transparent")
    stats_values.pack(fill="x", pady=5)
    
    total_label = ctk.CTkLabel(
        stats_values,
        text="Total: 0 fichiers",
        font=ctk.CTkFont(size=10)
    )
    total_label.pack(anchor="w")
    
    valid_label = ctk.CTkLabel(
        stats_values,
        text="Valides: 0 fichiers",
        font=ctk.CTkFont(size=10)
    )
    valid_label.pack(anchor="w")
    
    ignored_label = ctk.CTkLabel(
        stats_values,
        text="Ignorés: 0 fichiers",
        font=ctk.CTkFont(size=10)
    )
    ignored_label.pack(anchor="w")

def create_categories_config() -> Dict[str, Dict[str, Any]]:
    """
    Crée la configuration des catégories.
    
    Returns:
        Dict[str, Dict[str, Any]]: Configuration des catégories
    """
    return {
        "download": {
            "title": "📥 Téléchargements",
            "description": "Monitoring et sauvegarde automatique",
            "create_func": create_download_category
        },
        "organize": {
            "title": "📁 Organisation",
            "description": "Scan et organisation des fichiers",
            "create_func": create_organize_category
        }
    }
