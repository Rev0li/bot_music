#!/usr/bin/env python3
"""
app_simple_navigation.py - Version simplifiée avec navigation qui fonctionne
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import sys
import os

# Configuration de base
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class SimpleNavigationApp:
    """Application simple avec navigation par catégories."""

    def __init__(self):
        """Initialise l'application."""
        self.root = ctk.CTk()
        self.root.title("Music Organizer Pro - Navigation")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # État de l'application
        self.current_category = "download"
        self.monitoring_active = False
        self.auto_save_enabled = True
        self.services = None
        self.organizer = None
        self.scan_results = None

        # Créer l'interface
        self.create_navigation()
        self.create_content_area()

        # Logs
        self.create_logs_section()

        # Initialiser les services (après l'interface)
        self._initialize_services()

        # Afficher la première catégorie
        self.show_category("download")

        # Messages de démarrage dans les logs
        self.log("Music Organizer Pro - Version Simple Navigation")
        self.log("Interface avec navigation par categories")
        self.log("Theme: Soft et leger")

    def create_logs_section(self):
        """Crée la section des logs."""
        # Frame pour les logs (partagé entre les deux catégories)
        self.logs_frame = ctk.CTkFrame(self.content_frame)

        # Titre
        logs_title = ctk.CTkLabel(
            self.logs_frame,
            text="📋 Logs de l'Application",
            font=ctk.CTkFont(size=14, weight="normal")
        )
        logs_title.pack(pady=(10, 5))

        # Zone de texte pour les logs
        self.logs_text = ctk.CTkTextbox(
            self.logs_frame,
            height=200,
            font=ctk.CTkFont(family="Consolas", size=9),
            fg_color="#1e1e1e",
            text_color="#00ff00"
        )
        self.logs_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Boutons de contrôle des logs
        logs_controls = ctk.CTkFrame(self.logs_frame)
        logs_controls.pack(fill="x", padx=10, pady=(0, 10))

        clear_btn = ctk.CTkButton(
            logs_controls,
            text="🗑️ Effacer",
            command=self.clear_logs,
            fg_color="#f44336",
            hover_color="#d32f2f",
            width=100
        )
        clear_btn.pack(side="right")

    def _initialize_services(self):
        """Initialise les services backend."""
        try:
            # Ajouter le chemin vers les modules backend
            current_dir = os.path.dirname(__file__)
            backend_path = os.path.join(current_dir, 'music_organizer')
            if backend_path not in sys.path:
                sys.path.insert(0, backend_path)

            # Importer les services
            from music_organizer.monitor import DownloadMonitor
            from music_organizer.process_activator import SimpleAutoSaver
            from music_organizer.organizer import MusicOrganizer

            # Créer l'auto-saver pour les tests
            self.auto_saver = SimpleAutoSaver(log_callback=self.log)

            # Créer le monitor
            self.monitor = DownloadMonitor(
                notification_callback=self._on_download_detected,
                log_callback=self.log,
                auto_paste=True,
                auto_save=self.auto_save_enabled
            )

            # Préparer l'organizer (sera créé lors du scan)
            self.organizer_class = MusicOrganizer

            self.log("[OK] Services initialises avec succes")
            self.services_available = True

        except ImportError as e:
            self.log(f"[WARN] Services non disponibles: {e}")
            self.log("[TIP] Utilisation du mode simulation")
            self.services_available = False
        except Exception as e:
            self.log(f"[ERROR] Erreur initialisation services: {e}")
            self.services_available = False

    def show_category(self, category):
        """Affiche une catégorie."""
        # Afficher la catégorie demandée
        if category == "download":
            self.download_frame.pack(fill="both", expand=True)
            self.current_category = "download"
            # Mettre à jour les couleurs des onglets
            self.download_tab.configure(fg_color="#1f538d", text_color="white")
            self.organize_tab.configure(fg_color="transparent", text_color="#666666")
        else:
            self.organize_frame.pack(fill="both", expand=True)
            self.current_category = "organize"
            # Mettre à jour les couleurs des onglets
            self.organize_tab.configure(fg_color="#1f538d", text_color="white")
            self.download_tab.configure(fg_color="transparent", text_color="#666666")

        # Forcer les logs à être en bas (après un petit délai pour laisser Tkinter organiser)
        self.root.after(10, self._ensure_logs_at_bottom)

    def _ensure_logs_at_bottom(self):
        """Force les logs à être en bas de l'interface."""
        try:
            # Masquer les logs temporairement
            self.logs_frame.pack_forget()

            # Les réafficher en dernier (donc en bas)
            self.logs_frame.pack(fill="x", pady=(10, 20))

            # Forcer la mise à jour de l'affichage
            self.root.update_idletasks()

        except Exception as e:
            # En cas d'erreur, ignorer silencieusement
            pass

    def log(self, message):
        """Ajoute un message aux logs."""
        self.logs_text.insert("end", f"{message}\n")
        self.logs_text.see("end")

        # Limiter le nombre de lignes
        lines = self.logs_text.get("1.0", "end").split('\n')
        if len(lines) > 1000:
            self.logs_text.delete("1.0", f"{len(lines)-800}.0")

    def clear_logs(self):
        """Efface les logs."""
        self.logs_text.delete("1.0", "end")

    def create_navigation(self):
        """Crée la barre de navigation."""
        self.nav_frame = ctk.CTkFrame(self.root, height=80)
        self.nav_frame.pack(fill="x", padx=20, pady=20)
        self.nav_frame.pack_propagate(False)

        # Titre
        title_label = ctk.CTkLabel(
            self.nav_frame,
            text="🎵 Music Organizer Pro",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", pady=20)

        # Onglets de navigation
        self.tabs_frame = ctk.CTkFrame(self.nav_frame)
        self.tabs_frame.pack(side="right", pady=20)

        # Onglet Téléchargements
        self.download_tab = ctk.CTkButton(
            self.tabs_frame,
            text="📥 Téléchargements",
            command=lambda: self.show_category("download"),
            font=ctk.CTkFont(size=12, weight="bold"),
            width=150,
            height=35,
            corner_radius=8
        )
        self.download_tab.pack(side="left", padx=5)

        # Onglet Organisation
        self.organize_tab = ctk.CTkButton(
            self.tabs_frame,
            text="📁 Organisation",
            command=lambda: self.show_category("organize"),
            font=ctk.CTkFont(size=12, weight="bold"),
            width=150,
            height=35,
            corner_radius=8
        )
        self.organize_tab.pack(side="left", padx=5)

    def create_content_area(self):
        """Crée la zone de contenu principale."""
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Créer les frames pour chaque catégorie
        self.create_download_category()
        self.create_organize_category()

    def create_download_category(self):
        """Crée la catégorie de téléchargement."""
        self.download_frame = ctk.CTkFrame(self.content_frame)

        # Titre
        title_label = ctk.CTkLabel(
            self.download_frame,
            text="📥 Gestion des Téléchargements",
            font=ctk.CTkFont(size=16, weight="normal")
        )
        title_label.pack(pady=(20, 15))

        # Contrôles
        controls_frame = ctk.CTkFrame(self.download_frame)
        controls_frame.pack(fill="x", padx=20, pady=10)

        # Status
        self.download_status = ctk.CTkLabel(
            controls_frame,
            text="Monitoring: Arrêté",
            font=ctk.CTkFont(size=11)
        )
        self.download_status.pack(pady=8)

        # Boutons
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(pady=12)

        self.start_btn = ctk.CTkButton(
            buttons_frame,
            text="▶️ Démarrer",
            command=self.start_monitoring,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ctk.CTkButton(
            buttons_frame,
            text="⏸️ Arrêter",
            command=self.stop_monitoring,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        self.stop_btn.pack(side="left", padx=5)

        # Switch Auto-Save
        self.auto_save_var = tk.BooleanVar(value=True)
        self.auto_save_switch = ctk.CTkSwitch(
            controls_frame,
            text="Auto-Save",
            variable=self.auto_save_var,
            command=self.toggle_auto_save,
            font=ctk.CTkFont(size=10)
        )
        self.auto_save_switch.pack(pady=12)

        # Boutons de test
        test_frame = ctk.CTkFrame(self.download_frame)
        test_frame.pack(fill="x", padx=20, pady=10)

        test_btn = ctk.CTkButton(
            test_frame,
            text="🎯 Test Collage",
            command=self.test_paste,
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        test_btn.pack(side="left")

    def create_organize_category(self):
        """Crée la catégorie d'organisation."""
        self.organize_frame = ctk.CTkFrame(self.content_frame)

        # Titre
        title_label = ctk.CTkLabel(
            self.organize_frame,
            text="📁 Organisation Musicale",
            font=ctk.CTkFont(size=16, weight="normal")
        )
        title_label.pack(pady=(20, 15))

        # Sélection de dossier
        folder_frame = ctk.CTkFrame(self.organize_frame)
        folder_frame.pack(fill="x", padx=20, pady=10)

        folder_label = ctk.CTkLabel(
            folder_frame,
            text="📂 Dossier à organiser:",
            font=ctk.CTkFont(size=11)
        )
        folder_label.pack(side="left")

        self.folder_entry = ctk.CTkEntry(
            folder_frame,
            placeholder_text="Sélectionnez le dossier...",
            width=400
        )
        self.folder_entry.pack(side="left", padx=10)

        folder_btn = ctk.CTkButton(
            folder_frame,
            text="Parcourir",
            command=self.browse_folder,
            fg_color="#9C27B0",
            hover_color="#7B1FA2"
        )
        folder_btn.pack(side="left")

        # Boutons d'action
        actions_frame = ctk.CTkFrame(self.organize_frame)
        actions_frame.pack(fill="x", padx=20, pady=20)

        self.scan_btn = ctk.CTkButton(
            actions_frame,
            text="🔍 Scanner",
            command=self.scan_folder,
            fg_color="#FF9800",
            hover_color="#F57C00",
            width=150
        )
        self.scan_btn.pack(side="left", padx=5)

        self.organize_btn = ctk.CTkButton(
            actions_frame,
            text="📋 Organiser",
            command=self.organize_folder,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=150
        )
        self.organize_btn.pack(side="left", padx=5)

        # Statistiques
        self.stats_frame = ctk.CTkFrame(self.organize_frame)
        self.stats_frame.pack(fill="x", padx=20, pady=10)

        stats_label = ctk.CTkLabel(
            self.stats_frame,
            text="📊 Statistiques:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        stats_label.pack(anchor="w")

        stats_values = ctk.CTkFrame(self.stats_frame)
        stats_values.pack(fill="x", pady=5)

        self.total_label = ctk.CTkLabel(
            stats_values,
            text="Total: 0 fichiers",
            font=ctk.CTkFont(size=10)
        )
        self.total_label.pack(anchor="w")

        self.valid_label = ctk.CTkLabel(
            stats_values,
            text="Valides: 0 fichiers",
            font=ctk.CTkFont(size=10)
        )
        self.valid_label.pack(anchor="w")

        self.ignored_label = ctk.CTkLabel(
            stats_values,
            text="Ignorés: 0 fichiers",
            font=ctk.CTkFont(size=10)
        )
        self.ignored_label.pack(anchor="w")

    def show_category(self, category):
        """Affiche une catégorie."""
        # Masquer tous les frames
        self.download_frame.pack_forget()
        self.organize_frame.pack_forget()

        # Afficher la catégorie demandée + logs
        if category == "download":
            self.download_frame.pack(fill="both", expand=True, pady=(0, 10))
            self.logs_frame.pack(fill="x", pady=(0, 20))
            self.current_category = "download"
            # Mettre à jour les couleurs des onglets
            self.download_tab.configure(fg_color="#1f538d", text_color="white")
            self.organize_tab.configure(fg_color="transparent", text_color="#666666")
        else:
            self.organize_frame.pack(fill="both", expand=True, pady=(0, 10))
            self.logs_frame.pack(fill="x", pady=(0, 20))
            self.current_category = "organize"
            # Mettre à jour les couleurs des onglets
            self.organize_tab.configure(fg_color="#1f538d", text_color="white")
            self.download_tab.configure(fg_color="transparent", text_color="#666666")

    # === Méthodes de téléchargement ===

    def start_monitoring(self):
        """Démarre le monitoring des téléchargements."""
        if not self.services_available or not self.monitor:
            self.log("[WARN] Services non disponibles - mode simulation")
            # Mode simulation
            self.monitoring_active = True
            self.download_status.configure(text="Monitoring: Actif (Simulation)", text_color="#4CAF50")
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.log("Monitoring demarre (simulation)")
            return

        try:
            success = self.monitor.start()
            if success:
                self.monitoring_active = True
                self.download_status.configure(text="Monitoring: Actif", text_color="#4CAF50")
                self.start_btn.configure(state="disabled")
                self.stop_btn.configure(state="normal")
                self.log("Monitoring demarre avec succes")
            else:
                self.log("[ERROR] Impossible de demarrer le monitoring")
        except Exception as e:
            self.log(f"[ERROR] Erreur demarrage monitoring: {e}")
            # Fallback vers le mode simulation
            self.monitoring_active = True
            self.download_status.configure(text="Monitoring: Actif (Fallback)", text_color="#4CAF50")
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")

    def stop_monitoring(self):
        """Arrête le monitoring des téléchargements."""
        if not self.services_available or not self.monitor:
            # Mode simulation
            self.monitoring_active = False
            self.download_status.configure(text="Monitoring: Arrêté", text_color="#f44336")
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.log("Monitoring arrete (simulation)")
            return

        try:
            success = self.monitor.stop()
            if success:
                self.monitoring_active = False
                self.download_status.configure(text="Monitoring: Arrêté", text_color="#f44336")
                self.start_btn.configure(state="normal")
                self.stop_btn.configure(state="disabled")
                self.log("Monitoring arrete avec succes")
            else:
                self.log("[ERROR] Impossible d'arreter le monitoring")
        except Exception as e:
            self.log(f"[ERROR] Erreur arret monitoring: {e}")

    def toggle_auto_save(self):
        """Toggle l'auto-save."""
        self.auto_save_enabled = self.auto_save_var.get()
        if self.monitor:
            self.monitor.auto_save = self.auto_save_enabled

        status = "active" if self.auto_save_enabled else "desactive"
        self.log(f"Auto-Save {status}")

    def test_paste(self):
        """Test le collage automatique."""
        if not self.services_available or not self.auto_saver:
            self.log("[WARN] AutoSaver non disponible - mode simulation")
            self.log("Test de collage simule...")
            return

        self.log("Test de collage...")
        try:
            result = self.auto_saver.simple_save(auto_click_save=self.auto_save_enabled)
            if result:
                self.log("Test de collage reussi!")
            else:
                self.log("[WARN] Test de collage echoue")
        except Exception as e:
            self.log(f"[ERROR] Erreur test collage: {e}")

    def _on_download_detected(self, window_title: str):
        """Callback appelé lors de la détection d'un téléchargement."""
        self.log(f"Telechargement detecte: {window_title}")
        # TODO: Mettre à jour un compteur de téléchargements

    # === Méthodes d'organisation ===

    def browse_folder(self):
        """Ouvre le dialogue de sélection de dossier."""
        folder = filedialog.askdirectory(
            title="Sélectionner le dossier de musique",
            initialdir=self.folder_entry.get() or os.path.expanduser("~/Music")
        )

        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
            self.log(f"Dossier selectionne: {folder}")

    def scan_folder(self):
        """Scanne le dossier."""
        folder = self.folder_entry.get()
        if not folder:
            messagebox.showwarning("Attention", "Veuillez sélectionner un dossier")
            return

        if not self.services_available or not self.organizer_class:
            self.log("[WARN] Services d'organisation non disponibles - mode simulation")
            # Mode simulation
            def scan_thread():
                import time
                time.sleep(2)
                total, valid, ignored = 15, 12, 3
                self.total_label.configure(text=f"Total: {total} fichiers")
                self.valid_label.configure(text=f"Valides: {valid} fichiers")
                self.ignored_label.configure(text=f"Ignorés: {ignored} fichiers")
                self.log(f"Scan termine: {total} fichiers trouves")

            threading.Thread(target=scan_thread, daemon=True).start()
            return

        self.log(f"Scan du dossier: {folder}")

        def scan_thread():
            try:
                # Créer l'organizer
                self.organizer = self.organizer_class(folder, log_callback=self.log)

                # Scanner
                songs = self.organizer.scan()

                # Analyser les résultats
                valid_songs = songs  # MusicOrganizer ne retourne que les valides
                ignored_songs = []   # Pas d'ignorés pour le moment

                total = len(songs)
                valid = len(valid_songs)
                ignored = len(ignored_songs)

                # Mettre à jour l'interface
                self.total_label.configure(text=f"Total: {total} fichiers")
                self.valid_label.configure(text=f"Valides: {valid} fichiers")
                self.ignored_label.configure(text=f"Ignorés: {ignored} fichiers")

                # Stocker les résultats
                self.scan_results = {
                    "songs": songs,
                    "valid_songs": valid_songs,
                    "total": total,
                    "valid": valid,
                    "ignored": ignored
                }

                self.log(f"[OK] Scan termine: {total} fichiers valides trouves")

            except Exception as e:
                self.log(f"[ERROR] Erreur scan: {e}")
                # Fallback vers le mode simulation
                total, valid, ignored = 15, 12, 3
                self.total_label.configure(text=f"Total: {total} fichiers")
                self.valid_label.configure(text=f"Valides: {valid} fichiers")
                self.ignored_label.configure(text=f"Ignorés: {ignored} fichiers")
                self.log("[WARN] Scan en mode simulation")

        threading.Thread(target=scan_thread, daemon=True).start()

    def organize_folder(self):
        """Organise le dossier."""
        folder = self.folder_entry.get()
        if not folder:
            messagebox.showwarning("Attention", "Veuillez sélectionner un dossier")
            return

        if not self.scan_results or not self.scan_results.get("valid_songs"):
            messagebox.showwarning("Attention", "Aucune chanson à organiser. Lancez d'abord un scan.")
            return

        if not self.services_available or not self.organizer:
            self.log("[WARN] Services d'organisation non disponibles - mode simulation")
            # Mode simulation
            def organize_thread():
                import time
                time.sleep(3)
                self.log("Organisation terminee (simulation)")

            threading.Thread(target=organize_thread, daemon=True).start()
            return

        self.log(f"Organisation du dossier: {folder}")

        def organize_thread():
            try:
                # Organiser les chansons trouvées
                success_count, error_count = self.organizer.organize()

                if success_count > 0:
                    self.log(f"[OK] Organisation terminee: {success_count} fichiers organises")
                if error_count > 0:
                    self.log(f"[WARN] {error_count} erreurs lors de l'organisation")

            except Exception as e:
                self.log(f"[ERROR] Erreur organisation: {e}")
                # Fallback vers le mode simulation
                import time
                time.sleep(3)
                self.log("Organisation terminee (simulation)")

        threading.Thread(target=organize_thread, daemon=True).start()

    def run(self):
        """Lance l'application."""
        self.root.mainloop()

def main():
    """Point d'entrée principal."""
    print("Lancement de Music Organizer Pro - Version Simple")
    print("Navigation avec 2 catégories principales")
    print("=" * 50)

    try:
        app = SimpleNavigationApp()
        app.run()
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
