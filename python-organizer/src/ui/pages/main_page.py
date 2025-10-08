"""
main_page.py - Page principale moderne de l'application
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from typing import Optional, Callable
import threading

from ..components.buttons import ModernButton, ToggleButton, IconButton, ActionButton
from ..components.frames import ModernFrame, CardFrame, StatusFrame, CollapsibleFrame, ProgressFrame
from ..styles.themes import theme_manager

# Import de l'adaptateur de services
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from core.services.service_adapter import get_service_adapter
except ImportError:
    # Fallback
    def get_service_adapter(log_callback=None):
        class DummyAdapter:
            def __init__(self, log_callback=None):
                self.log_callback = log_callback or print
                self.on_download_detected = None
                self.on_scan_progress = None
                self.on_scan_complete = None
                self.on_organize_progress = None
                self.on_organize_complete = None
            
            def start_monitoring(self): 
                self.log_callback("Mode demo - monitoring simule")
                return True
            def stop_monitoring(self): return True
            def set_auto_save(self, state): pass
            def test_paste(self): 
                self.log_callback("Mode demo - test simule")
                return True
            def toggle_debug(self): return False
            def scan_folder(self, path, progress_callback=None):
                return {"success": False, "error": "Mode demo"}
            def organize_songs(self, path, progress_callback=None):
                return {"success": False, "error": "Mode demo"}
            def get_status(self):
                return {"services_available": False}
        
        return DummyAdapter(log_callback)

class MainPage(ctk.CTkFrame):
    """Page principale de l'application Music Organizer."""
    
    def __init__(self, parent):
        """
        Initialise la page principale.
        
        Args:
            parent: Widget parent
        """
        super().__init__(parent, fg_color="transparent")
        
        # Variables d'état
        self.selected_folder = tk.StringVar()
        self.auto_save_enabled = tk.BooleanVar(value=True)
        self.detection_count = 0
        
        # Créer l'interface d'abord
        self._create_layout()
        
        # Puis initialiser les services
        self.services = get_service_adapter(log_callback=self.log)
        
        # Configurer les callbacks
        self._setup_service_callbacks()
    
    def _setup_service_callbacks(self):
        """Configure les callbacks pour les services."""
        # Callback pour les détections de téléchargement
        self.services.on_download_detected = self._on_download_detected
        
        # Callbacks pour le scan
        self.services.on_scan_progress = self._on_scan_progress
        self.services.on_scan_complete = self._on_scan_complete
        
        # Callbacks pour l'organisation
        self.services.on_organize_progress = self._on_organize_progress
        self.services.on_organize_complete = self._on_organize_complete
    
    def _create_layout(self):
        """Crée le layout principal."""
        # Titre principal
        self._create_header()
        
        # Container principal avec scroll
        self._create_main_container()
        
        # Sections
        self._create_folder_section()
        self._create_monitor_section()
        self._create_scanner_section()
        self._create_log_section()
    
    def _create_header(self):
        """Crée l'en-tête de l'application."""
        header_frame = ctk.CTkFrame(self, height=80, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Titre
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎵 Music Organizer Pro",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=theme_manager.get_color("primary")
        )
        title_label.pack(side="left", pady=20)
        
        # Boutons d'action rapide
        quick_actions = ctk.CTkFrame(header_frame, fg_color="transparent")
        quick_actions.pack(side="right", pady=20)
        
        # Bouton thème
        theme_btn = IconButton(
            quick_actions,
            icon="🎨",
            command=self._toggle_theme,
            tooltip="Changer de thème"
        )
        theme_btn.pack(side="right", padx=5)
        
        # Bouton paramètres
        settings_btn = IconButton(
            quick_actions,
            icon="⚙️",
            command=self._open_settings,
            tooltip="Paramètres"
        )
        settings_btn.pack(side="right", padx=5)
    
    def _create_main_container(self):
        """Crée le container principal avec scroll."""
        # Frame scrollable
        self.main_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=theme_manager.get_color("primary"),
            scrollbar_button_hover_color=theme_manager.get_color("hover")
        )
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)
    
    def _create_folder_section(self):
        """Crée la section de sélection de dossier."""
        folder_card = CardFrame(self.main_container, title="📁 Dossier de Musique")
        folder_card.pack(fill="x", pady=10)
        
        # Container pour le chemin et bouton
        path_frame = ctk.CTkFrame(folder_card, fg_color="transparent")
        path_frame.pack(fill="x", padx=15, pady=10)
        
        # Champ de chemin
        self.path_entry = ctk.CTkEntry(
            path_frame,
            textvariable=self.selected_folder,
            placeholder_text="Sélectionnez un dossier...",
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Bouton parcourir
        browse_btn = ModernButton(
            path_frame,
            text="Parcourir",
            command=self._browse_folder,
            icon="📂",
            style="secondary",
            width=120
        )
        browse_btn.pack(side="right")
    
    def _create_monitor_section(self):
        """Crée la section de monitoring des téléchargements."""
        monitor_card = CardFrame(self.main_container, title="🔍 Scanner de Téléchargement")
        monitor_card.pack(fill="x", pady=10)
        
        # Status et contrôles
        controls_frame = ctk.CTkFrame(monitor_card, fg_color="transparent")
        controls_frame.pack(fill="x", padx=15, pady=10)
        
        # Status du monitor
        self.monitor_status = StatusFrame(controls_frame)
        self.monitor_status.pack(side="left", fill="x", expand=True)
        
        self.monitor_status.add_status("status", "Statut:", "⭕ Arrêté", "error")
        self.monitor_status.add_status("detected", "Détections:", "0", "info")
        
        # Boutons de contrôle
        controls_buttons = ctk.CTkFrame(controls_frame, fg_color="transparent")
        controls_buttons.pack(side="right", padx=(10, 0))
        
        # Bouton start/stop
        self.monitor_btn = ToggleButton(
            controls_buttons,
            text="Scanner",
            initial_state=False,
            on_toggle=self._toggle_monitor
        )
        self.monitor_btn.pack(pady=2)
        
        # Switch Auto-Save
        self.auto_save_btn = ToggleButton(
            controls_buttons,
            text="Auto-Save",
            initial_state=True,
            on_toggle=self._toggle_auto_save
        )
        self.auto_save_btn.pack(pady=2)
        
        # Boutons de test
        test_frame = ctk.CTkFrame(monitor_card, fg_color="transparent")
        test_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        test_btn = ModernButton(
            test_frame,
            text="Test Collage",
            command=self._test_paste,
            icon="🎯",
            style="info",
            width=120
        )
        test_btn.pack(side="left", padx=(0, 10))
        
        debug_btn = ModernButton(
            test_frame,
            text="Debug",
            command=self._toggle_debug,
            icon="🐛",
            style="warning",
            width=100
        )
        debug_btn.pack(side="left")
    
    def _create_scanner_section(self):
        """Crée la section de scan et organisation."""
        scanner_card = CardFrame(self.main_container, title="🔍 Scanner et Organisateur")
        scanner_card.pack(fill="x", pady=10)
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(scanner_card, fg_color="transparent")
        actions_frame.pack(fill="x", padx=15, pady=10)
        
        # Bouton scan
        self.scan_btn = ActionButton(
            actions_frame,
            text="Scanner les Chansons",
            command=self._scan_songs,
            icon="🔍",
            style="primary"
        )
        self.scan_btn.pack(side="left", padx=(0, 10))
        
        # Bouton organisation
        self.organize_btn = ActionButton(
            actions_frame,
            text="Organiser",
            command=self._organize_songs,
            icon="📁",
            style="success"
        )
        self.organize_btn.pack(side="left")
        
        # Statistiques
        self.stats_frame = StatusFrame(scanner_card)
        self.stats_frame.pack(fill="x", padx=15, pady=10)
        
        self.stats_frame.add_status("total", "Total:", "0", "info")
        self.stats_frame.add_status("valid", "Valides:", "0", "success")
        self.stats_frame.add_status("ignored", "Ignorés:", "0", "warning")
        
        # Barre de progression
        self.progress_frame = ProgressFrame(scanner_card, title="Progression")
        self.progress_frame.pack(fill="x", padx=15, pady=10)
        self.progress_frame.pack_forget()  # Caché par défaut
    
    def _create_log_section(self):
        """Crée la section des logs."""
        # Frame pliable pour les logs
        self.log_collapsible = CollapsibleFrame(
            self.main_container,
            title="📋 Logs de l'Application",
            collapsed=False
        )
        self.log_collapsible.pack(fill="both", expand=True, pady=10)
        
        # Zone de texte pour les logs
        self.log_text = ctk.CTkTextbox(
            self.log_collapsible.content_frame,
            height=200,
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=theme_manager.get_color("success"),
            fg_color=theme_manager.get_color("bg_primary")
        )
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Boutons de contrôle des logs
        log_controls = ctk.CTkFrame(self.log_collapsible.content_frame, fg_color="transparent")
        log_controls.pack(fill="x", padx=5, pady=5)
        
        clear_btn = ModernButton(
            log_controls,
            text="Effacer",
            command=self._clear_logs,
            icon="🗑️",
            style="error",
            width=100
        )
        clear_btn.pack(side="right")
    
    # Méthode supprimée - remplacée par l'adaptateur de services
    
    # === Méthodes d'événements ===
    
    def _browse_folder(self):
        """Ouvre le dialogue de sélection de dossier."""
        folder = filedialog.askdirectory(
            title="Sélectionner le dossier de musique",
            initialdir=self.selected_folder.get() or os.path.expanduser("~/Music")
        )
        
        if folder:
            self.selected_folder.set(folder)
            self.log(f"📁 Dossier sélectionné: {folder}")
    
    def _toggle_monitor(self, state: bool):
        """Toggle le moniteur de téléchargements."""
        if state:
            success = self.services.start_monitoring()
            if success:
                self.monitor_status.update_status("status", "[ON] Actif", "success")
                self.log("Scanner de telechargement active")
            else:
                self.monitor_btn.set_state(False)
                self.log("Erreur: Impossible d'activer le scanner")
        else:
            success = self.services.stop_monitoring()
            if success:
                self.monitor_status.update_status("status", "[OFF] Arrete", "error")
                self.log("Scanner de telechargement arrete")
    
    def _toggle_auto_save(self, state: bool):
        """Toggle l'auto-save."""
        self.auto_save_enabled.set(state)
        self.services.set_auto_save(state)
        
        status = "active" if state else "desactive"
        self.log(f"Auto-Save {status}")
    
    def _test_paste(self):
        """Test le collage automatique."""
        self.log("Test de collage...")
        
        def test_thread():
            result = self.services.test_paste()
            if result:
                self.log("Test reussi!")
            else:
                self.log("Test echoue")
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    def _toggle_debug(self):
        """Toggle le mode debug."""
        debug_state = self.services.toggle_debug()
        status = "active" if debug_state else "desactive"
        self.log(f"Mode debug {status}")
    
    def _scan_songs(self):
        """Lance le scan des chansons."""
        if not self.selected_folder.get():
            messagebox.showwarning("Attention", "Veuillez selectionner un dossier")
            return
        
        self.log("Demarrage du scan...")
        self.progress_frame.pack(fill="x", padx=15, pady=10)
        
        def scan_thread():
            # Callback de progression
            def on_progress(current, total, filename):
                progress = current / total if total > 0 else 0
                self.progress_frame.update_progress(
                    progress, 
                    f"Scan {current}/{total}: {filename[:30]}..."
                )
            
            # Scanner via l'adaptateur de services
            result = self.services.scan_folder(
                self.selected_folder.get(),
                progress_callback=on_progress
            )
            
            if result["success"]:
                self.log(f"Scan termine: {result['total']} fichiers trouves")
                self.progress_frame.update_progress(1.0, "Scan termine")
            else:
                self.log(f"Erreur scan: {result.get('error', 'Erreur inconnue')}")
            
            # Cacher la barre de progression après 2 secondes
            self.after(2000, lambda: self.progress_frame.pack_forget())
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def _organize_songs(self):
        """Lance l'organisation des chansons."""
        if not self.selected_folder.get():
            messagebox.showwarning("Attention", "Veuillez selectionner un dossier")
            return
        
        # Vérifier qu'il y a des chansons à organiser
        status = self.services.get_status()
        if not status.get("last_scan_results") or not status["last_scan_results"].get("valid_songs"):
            messagebox.showwarning("Attention", "Aucune chanson a organiser. Lancez d'abord un scan.")
            return
        
        self.log("Organisation en cours...")
        self.progress_frame.pack(fill="x", padx=15, pady=10)
        
        def organize_thread():
            # Callback de progression
            def on_progress(current, total, filename):
                progress = current / total if total > 0 else 0
                self.progress_frame.update_progress(
                    progress, 
                    f"Organisation {current}/{total}: {filename[:30]}..."
                )
            
            # Organiser via l'adaptateur de services
            result = self.services.organize_songs(
                self.selected_folder.get(),
                progress_callback=on_progress
            )
            
            if result["success"]:
                self.log(f"Organisation terminee: {result['organized']} fichiers organises")
                if result["errors"] > 0:
                    self.log(f"Erreurs: {result['errors']} fichiers non organises")
                self.progress_frame.update_progress(1.0, "Organisation terminee")
            else:
                self.log(f"Erreur organisation: {result.get('error', 'Erreur inconnue')}")
            
            # Cacher la barre de progression après 2 secondes
            self.after(2000, lambda: self.progress_frame.pack_forget())
        
        threading.Thread(target=organize_thread, daemon=True).start()
    
    def _on_download_detected(self, window_title: str):
        """Callback appelé lors de la détection d'un téléchargement."""
        self.detection_count += 1
        self.monitor_status.update_status("detected", str(self.detection_count), "success")
        self.log(f"Telechargement detecte: {window_title}")
    
    def _on_scan_progress(self, current: int, total: int, filename: str):
        """Callback de progression du scan."""
        # Déjà géré dans _scan_songs
        pass
    
    def _on_scan_complete(self, results: dict):
        """Callback de completion du scan."""
        # Mettre à jour les statistiques
        self.stats_frame.update_status("total", str(results["total"]), "info")
        self.stats_frame.update_status("valid", str(results["valid"]), "success")
        self.stats_frame.update_status("ignored", str(results["ignored"]), "warning")
        
        self.log(f"Scan complete: {results['valid']} valides, {results['ignored']} ignores")
    
    def _on_organize_progress(self, current: int, total: int, filename: str):
        """Callback de progression de l'organisation."""
        # Déjà géré dans _organize_songs
        pass
    
    def _on_organize_complete(self, results: dict):
        """Callback de completion de l'organisation."""
        if results["errors"] > 0:
            self.log(f"Organisation terminee avec {results['errors']} erreurs")
        else:
            self.log("Organisation terminee avec succes")
    
    def _toggle_theme(self):
        """Change le thème de l'application."""
        current_theme = theme_manager.current_theme
        themes = theme_manager.get_theme_list()
        current_index = themes.index(current_theme)
        next_theme = themes[(current_index + 1) % len(themes)]
        
        theme_manager.apply_theme(next_theme)
        self.log(f"🎨 Thème changé: {next_theme}")
        
        # Redessiner l'interface (nécessite un redémarrage complet)
        messagebox.showinfo("Thème", f"Thème changé vers '{next_theme}'.\nRedémarrez l'application pour voir les changements.")
    
    def _open_settings(self):
        """Ouvre la fenêtre des paramètres."""
        self.log("⚙️ Ouverture des paramètres...")
        # TODO: Implémenter la fenêtre des paramètres
    
    def _clear_logs(self):
        """Efface les logs."""
        self.log_text.delete("1.0", tk.END)
    
    def log(self, message: str):
        """
        Ajoute un message aux logs.
        
        Args:
            message (str): Message à logger
        """
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
        # Limiter le nombre de lignes
        lines = self.log_text.get("1.0", tk.END).split('\n')
        if len(lines) > 1000:
            # Garder seulement les 800 dernières lignes
            self.log_text.delete("1.0", f"{len(lines)-800}.0")
