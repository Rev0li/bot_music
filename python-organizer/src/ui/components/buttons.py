"""
buttons.py - Composants boutons modernes et stylisés
"""

import customtkinter as ctk
from typing import Callable, Optional
from ..styles.themes import theme_manager

class ModernButton(ctk.CTkButton):
    """Bouton moderne stylisé."""
    
    def __init__(self, parent, text: str, command: Callable = None, 
                 style: str = "primary", icon: str = None, **kwargs):
        """
        Crée un bouton moderne.
        
        Args:
            parent: Widget parent
            text (str): Texte du bouton
            command (Callable): Fonction à exécuter
            style (str): Style du bouton (primary, secondary, success, warning, error)
            icon (str): Icône du bouton (emoji ou texte)
        """
        
        # Récupérer les couleurs du thème
        color_map = {
            "primary": theme_manager.get_color("primary"),
            "secondary": theme_manager.get_color("secondary"), 
            "success": theme_manager.get_color("success"),
            "warning": theme_manager.get_color("warning"),
            "error": theme_manager.get_color("error"),
            "info": theme_manager.get_color("info")
        }
        
        # Texte avec icône si fournie
        display_text = f"{icon} {text}" if icon else text
        
        # Configuration par défaut
        default_config = {
            "text": display_text,
            "command": command,
            "fg_color": color_map.get(style, color_map["primary"]),
            "hover_color": theme_manager.get_color("hover"),
            "corner_radius": 10,           # Coins plus arrondis
            "font": ctk.CTkFont(size=11, weight="normal"), # Police moins épaisse
            "height": 32,                 # Plus petits
            "cursor": "hand2"
        }
        
        # Fusionner avec les kwargs personnalisés
        default_config.update(kwargs)
        
        super().__init__(parent, **default_config)

class ToggleButton(ctk.CTkButton):
    """Bouton toggle/switch moderne."""
    
    def __init__(self, parent, text: str, initial_state: bool = False, 
                 on_toggle: Callable = None, **kwargs):
        """
        Crée un bouton toggle.
        
        Args:
            parent: Widget parent
            text (str): Texte de base du bouton
            initial_state (bool): État initial
            on_toggle (Callable): Fonction appelée lors du toggle
        """
        self.base_text = text
        self.state = initial_state
        self.on_toggle = on_toggle
        
        # Configuration initiale
        initial_text = f"[{'ON' if initial_state else 'OFF'}] {text}"
        initial_color = theme_manager.get_color("success" if initial_state else "error")
        
        default_config = {
            "text": initial_text,
            "command": self._toggle,
            "corner_radius": 25,           # Très arrondi pour l'effet switch
            "font": ctk.CTkFont(size=10, weight="normal"), # Plus petit et léger
            "height": 28,                 # Plus petit
            "cursor": "hand2",
            "fg_color": initial_color
        }
        
        default_config.update(kwargs)
        super().__init__(parent, **default_config)
        
        # Appliquer l'apparence après l'initialisation complète
        self.after(10, self._update_appearance)
    
    def _toggle(self):
        """Toggle l'état du bouton."""
        self.state = not self.state
        self._update_appearance()
        
        if self.on_toggle:
            self.on_toggle(self.state)
    
    def _update_appearance(self):
        """Met à jour l'apparence selon l'état."""
        if self.state:
            text = f"[ON] {self.base_text}"
            color = theme_manager.get_color("success")
            hover = "#66bb6a"  # Vert plus doux pour hover
        else:
            text = f"[OFF] {self.base_text}"
            color = theme_manager.get_color("error")
            hover = "#ef5350"  # Rouge plus doux pour hover
        
        # Configurer après l'initialisation complète
        if hasattr(self, '_text_label'):
            self.configure(
                text=text,
                fg_color=color,
                hover_color=hover
            )
    
    def set_state(self, state: bool):
        """
        Définit l'état du bouton.
        
        Args:
            state (bool): Nouvel état
        """
        self.state = state
        self._update_appearance()

class IconButton(ctk.CTkButton):
    """Bouton avec icône uniquement."""
    
    def __init__(self, parent, icon: str, command: Callable = None, 
                 tooltip: str = None, **kwargs):
        """
        Crée un bouton icône.
        
        Args:
            parent: Widget parent
            icon (str): Icône (emoji ou texte)
            command (Callable): Fonction à exécuter
            tooltip (str): Texte d'aide au survol
        """
        
        default_config = {
            "text": icon,
            "command": command,
            "width": 40,
            "height": 40,
            "corner_radius": 20,
            "fg_color": theme_manager.get_color("secondary"),
            "hover_color": theme_manager.get_color("hover"),
            "font": ctk.CTkFont(size=16),
            "cursor": "hand2"
        }
        
        default_config.update(kwargs)
        super().__init__(parent, **default_config)
        
        # TODO: Ajouter tooltip si nécessaire

class ActionButton(ModernButton):
    """Bouton d'action avec état de chargement."""
    
    def __init__(self, parent, text: str, command: Callable = None, **kwargs):
        """
        Crée un bouton d'action.
        
        Args:
            parent: Widget parent
            text (str): Texte du bouton
            command (Callable): Fonction à exécuter
        """
        self.original_text = text
        self.original_command = command
        self.is_loading = False
        
        super().__init__(parent, text, self._handle_click, **kwargs)
    
    def _handle_click(self):
        """Gère le clic avec état de chargement."""
        if self.is_loading or not self.original_command:
            return
            
        self.set_loading(True)
        
        try:
            result = self.original_command()
            # Si c'est une coroutine, on pourrait l'awaiter ici
        except Exception as e:
            print(f"Erreur dans le bouton: {e}")
        finally:
            self.set_loading(False)
    
    def set_loading(self, loading: bool):
        """
        Définit l'état de chargement.
        
        Args:
            loading (bool): État de chargement
        """
        self.is_loading = loading
        
        if loading:
            self.configure(
                text="⏳ Chargement...",
                state="disabled"
            )
        else:
            self.configure(
                text=self.original_text,
                state="normal"
            )
