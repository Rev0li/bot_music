"""
frames.py - Composants de layout et conteneurs modernes
"""

import customtkinter as ctk
from typing import Optional, List, Dict, Any
from ..styles.themes import theme_manager

class ModernFrame(ctk.CTkFrame):
    """Frame moderne avec style personnalisé."""
    
    def __init__(self, parent, title: str = None, **kwargs):
        """
        Crée un frame moderne.
        
        Args:
            parent: Widget parent
            title (str): Titre optionnel du frame
        """
        
        default_config = {
            "corner_radius": 10,
            "border_width": 1,
            "border_color": theme_manager.get_color("border"),
            "fg_color": theme_manager.get_color("bg_secondary")
        }
        
        default_config.update(kwargs)
        super().__init__(parent, **default_config)
        
        if title:
            self._create_title(title)
    
    def _create_title(self, title: str):
        """Crée un titre pour le frame."""
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=theme_manager.get_color("text_primary")
        )
        title_label.pack(pady=(10, 5), padx=10, anchor="w")

class CardFrame(ModernFrame):
    """Frame en forme de carte avec ombre."""
    
    def __init__(self, parent, title: str = None, **kwargs):
        """
        Crée une carte moderne.
        
        Args:
            parent: Widget parent
            title (str): Titre de la carte
        """
        
        default_config = {
            "corner_radius": 12,
            "border_width": 0,
            "fg_color": theme_manager.get_color("bg_secondary")
        }
        
        default_config.update(kwargs)
        super().__init__(parent, title, **default_config)

class StatusFrame(ModernFrame):
    """Frame pour afficher des statuts."""
    
    def __init__(self, parent, **kwargs):
        """
        Crée un frame de statut.
        
        Args:
            parent: Widget parent
        """
        super().__init__(parent, **kwargs)
        
        self.status_items = {}
        self._create_layout()
    
    def _create_layout(self):
        """Crée le layout du frame de statut."""
        # Container pour les éléments de statut
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def add_status(self, key: str, label: str, value: str = "", 
                   status_type: str = "info"):
        """
        Ajoute un élément de statut.
        
        Args:
            key (str): Clé unique de l'élément
            label (str): Label de l'élément
            value (str): Valeur initiale
            status_type (str): Type de statut (info, success, warning, error)
        """
        
        # Couleurs selon le type
        color_map = {
            "info": theme_manager.get_color("info"),
            "success": theme_manager.get_color("success"),
            "warning": theme_manager.get_color("warning"),
            "error": theme_manager.get_color("error")
        }
        
        # Frame pour cet élément
        item_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        item_frame.pack(fill="x", pady=2)
        
        # Label
        label_widget = ctk.CTkLabel(
            item_frame,
            text=label,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=theme_manager.get_color("text_secondary")
        )
        label_widget.pack(side="left")
        
        # Valeur
        value_widget = ctk.CTkLabel(
            item_frame,
            text=value,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=color_map.get(status_type, color_map["info"])
        )
        value_widget.pack(side="right")
        
        self.status_items[key] = {
            "frame": item_frame,
            "label": label_widget,
            "value": value_widget,
            "type": status_type
        }
    
    def update_status(self, key: str, value: str, status_type: str = None):
        """
        Met à jour un élément de statut.
        
        Args:
            key (str): Clé de l'élément
            value (str): Nouvelle valeur
            status_type (str): Nouveau type de statut
        """
        if key not in self.status_items:
            return
        
        item = self.status_items[key]
        item["value"].configure(text=value)
        
        if status_type:
            color_map = {
                "info": theme_manager.get_color("info"),
                "success": theme_manager.get_color("success"),
                "warning": theme_manager.get_color("warning"),
                "error": theme_manager.get_color("error")
            }
            
            item["value"].configure(
                text_color=color_map.get(status_type, color_map["info"])
            )
            item["type"] = status_type

class CollapsibleFrame(ModernFrame):
    """Frame pliable/dépliable."""
    
    def __init__(self, parent, title: str, collapsed: bool = False, **kwargs):
        """
        Crée un frame pliable.
        
        Args:
            parent: Widget parent
            title (str): Titre du frame
            collapsed (bool): État initial (plié ou non)
        """
        super().__init__(parent, **kwargs)
        
        self.title = title
        self.collapsed = collapsed
        
        self._create_header()
        self._create_content()
        
        if collapsed:
            self._toggle_content()
    
    def _create_header(self):
        """Crée l'en-tête cliquable."""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=5, pady=5)
        
        # Bouton toggle
        self.toggle_btn = ctk.CTkButton(
            self.header_frame,
            text="▼" if not self.collapsed else "▶",
            width=30,
            height=30,
            command=self._toggle_content,
            fg_color="transparent",
            text_color=theme_manager.get_color("text_primary"),
            hover_color=theme_manager.get_color("hover"),
            font=ctk.CTkFont(size=12)
        )
        self.toggle_btn.pack(side="left")
        
        # Titre
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=self.title,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=theme_manager.get_color("text_primary")
        )
        self.title_label.pack(side="left", padx=(5, 0))
    
    def _create_content(self):
        """Crée la zone de contenu."""
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def _toggle_content(self):
        """Toggle l'affichage du contenu."""
        self.collapsed = not self.collapsed
        
        if self.collapsed:
            self.content_frame.pack_forget()
            self.toggle_btn.configure(text="▶")
        else:
            self.content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            self.toggle_btn.configure(text="▼")
    
    def add_content(self, widget):
        """
        Ajoute un widget au contenu.
        
        Args:
            widget: Widget à ajouter
        """
        widget.pack(in_=self.content_frame, fill="x", pady=2)

class ProgressFrame(ModernFrame):
    """Frame avec barre de progression."""
    
    def __init__(self, parent, title: str = "Progression", **kwargs):
        """
        Crée un frame avec barre de progression.
        
        Args:
            parent: Widget parent
            title (str): Titre du frame
        """
        super().__init__(parent, title, **kwargs)
        
        self._create_progress_bar()
        self._create_status_label()
    
    def _create_progress_bar(self):
        """Crée la barre de progression."""
        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=300,
            height=20,
            corner_radius=10,
            progress_color=theme_manager.get_color("primary")
        )
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.set(0)
    
    def _create_status_label(self):
        """Crée le label de statut."""
        self.status_label = ctk.CTkLabel(
            self,
            text="Prêt",
            font=ctk.CTkFont(size=11),
            text_color=theme_manager.get_color("text_secondary")
        )
        self.status_label.pack(pady=(0, 10))
    
    def update_progress(self, value: float, status: str = ""):
        """
        Met à jour la progression.
        
        Args:
            value (float): Valeur de 0.0 à 1.0
            status (str): Texte de statut
        """
        self.progress_bar.set(value)
        if status:
            self.status_label.configure(text=status)
