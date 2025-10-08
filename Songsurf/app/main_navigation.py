#!/usr/bin/env python3
"""
Songsurf - Application principale avec navigation EN HAUT
"""

import customtkinter as ctk
import sys
import os
import tkinter as tk
from threading import Thread

# Ajouter le répertoire racine au path
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

class NavigationManager:
    """Gestionnaire de navigation avec onglets"""

    def __init__(self, content_frame, parent_app):
        self.content_frame = content_frame
        self.parent = parent_app  # Référence à l'application principale
        self.current_tab = "download"

        # Organisateur de musique (sera créé quand un dossier sera sélectionné)
        # Créer le contenu des onglets D'ABORD
        self._create_tab_content()

        # Afficher l'onglet par défaut ENSUITE
        self.show_tab("download")

    def _download_content(self):
        """Crée le contenu de l'onglet Téléchargements"""
        # Titre de la section
        section_title = ctk.CTkLabel(
            self.download_frame,
            text="Gestionnaire de telechargement",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.pack(pady=(20, 15))

        # Contrôles du monitoring
        controls_frame = ctk.CTkFrame(self.download_frame)
        controls_frame.pack(fill="x", padx=20, pady=10)

        # Status
        self.download_status = ctk.CTkLabel(
            controls_frame,
            text="Monitoring: Arrêté",
            font=ctk.CTkFont(size=12)
        )
        self.download_status.pack(pady=8)

        # Boutons
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(pady=12)

        self.start_btn = ctk.CTkButton(
            buttons_frame,
            text="[PLAY] Démarrer",
            command=self._start_monitoring,
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=120
        )
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ctk.CTkButton(
            buttons_frame,
            text="[PAUSE] Arrêter",
            command=self._stop_monitoring,
            fg_color="#f44336",
            hover_color="#d32f2f",
            width=120
        )
        self.stop_btn.pack(side="left", padx=5)

        # Switch Auto-Save
        self.auto_save_var = tk.BooleanVar(value=True)
        self.auto_save_switch = ctk.CTkSwitch(
            controls_frame,
            text="Auto-Save",
            variable=self.auto_save_var,
            command=self._toggle_auto_save,
            font=ctk.CTkFont(size=11)
        )
        self.auto_save_switch.pack(pady=12)

        # Compteur de téléchargements
        self.download_count_label = ctk.CTkLabel(
            controls_frame,
            text="Téléchargements détectés: 0",
            font=ctk.CTkFont(size=10)
        )
        self.download_count_label.pack(pady=5)

    def _create_organize_content(self):
        """Crée le contenu de l'onglet Organisation"""
        # Titre de la section
        section_title = ctk.CTkLabel(
            self.organize_frame,
            text="Organisation Musicale",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.pack(pady=(20, 15))

        # Sélection de dossier
        folder_frame = ctk.CTkFrame(self.organize_frame)
        folder_frame.pack(fill="x", padx=20, pady=10)

        folder_label = ctk.CTkLabel(
            folder_frame,
            text="[FOLDER] Dossier à organiser:",
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
            command=self._browse_folder,
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            width=100
        )
        folder_btn.pack(side="left")

        # Boutons d'action
        actions_frame = ctk.CTkFrame(self.organize_frame)
        actions_frame.pack(fill="x", padx=20, pady=20)

        self.scan_btn = ctk.CTkButton(
            actions_frame,
            text="[SCAN] Scanner",
            command=self._scan_folder,
            fg_color="#FF9800",
            hover_color="#F57C00",
            width=150
        )
        self.scan_btn.pack(side="left", padx=5)

        self.organize_btn = ctk.CTkButton(
            actions_frame,
            text="[LOGS] Organiser",
            command=self._organize_folder,
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
            text="[STATS] Statistiques:",
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

    def _create_tab_content(self):
        """Crée le contenu des onglets"""
        # Frame pour le contenu des téléchargements
        self.download_frame = ctk.CTkFrame(self.content_frame)
        self._create_download_content()

        # Frame pour le contenu de l'organisation
        self.organize_frame = ctk.CTkFrame(self.content_frame)
        self._create_organize_content()

    def _create_download_content(self):
        """Crée le contenu de l'onglet Téléchargements"""
        # Titre de la section
        section_title = ctk.CTkLabel(
            self.download_frame,
            text="Gestionnaire de telechargement",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.pack(pady=(20, 15))

        # Contrôles du monitoring
        controls_frame = ctk.CTkFrame(self.download_frame)
        controls_frame.pack(fill="x", padx=20, pady=10)

        # Status
        self.download_status = ctk.CTkLabel(
            controls_frame,
            text="Monitoring: Arrêté",
            font=ctk.CTkFont(size=12)
        )
        self.download_status.pack(pady=8)

        # Boutons
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(pady=12)

        self.start_btn = ctk.CTkButton(
            buttons_frame,
            text="[PLAY] Démarrer",
            command=self._start_monitoring,
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=120
        )
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ctk.CTkButton(
            buttons_frame,
            text="[PAUSE] Arrêter",
            command=self._stop_monitoring,
            fg_color="#f44336",
            hover_color="#d32f2f",
            width=120
        )
        self.stop_btn.pack(side="left", padx=5)

        # Switch Auto-Save
        self.auto_save_var = tk.BooleanVar(value=True)
        self.auto_save_switch = ctk.CTkSwitch(
            controls_frame,
            text="Auto-Save",
            variable=self.auto_save_var,
            command=self._toggle_auto_save,
            font=ctk.CTkFont(size=11)
        )
        self.auto_save_switch.pack(pady=12)

        # Compteur de téléchargements
        self.download_count_label = ctk.CTkLabel(
            controls_frame,
            text="Téléchargements détectés: 0",
            font=ctk.CTkFont(size=10)
        )
        self.download_count_label.pack(pady=5)

    def show_tab(self, tab_name):
        """Affiche l'onglet spécifié avec gestion des couleurs"""
        # Masquer tous les frames
        self.download_frame.pack_forget()
        self.organize_frame.pack_forget()

        # Afficher l'onglet demandé
        if tab_name == "download":
            self.download_frame.pack(fill="both", expand=True)
            self.current_tab = "download"
            # Mettre à jour les couleurs : Téléchargements ACTIF, Organisation INACTIF
            self.parent.download_tab.configure(fg_color="#1f538d", text_color="white")
            self.parent.organize_tab.configure(fg_color="transparent", text_color="#666666")
        else:
            self.organize_frame.pack(fill="both", expand=True)
            self.current_tab = "organize"
            # Mettre à jour les couleurs : Téléchargements INACTIF, Organisation ACTIF
            self.parent.organize_tab.configure(fg_color="#1f538d", text_color="white")
            self.parent.download_tab.configure(fg_color="transparent", text_color="#666666")

    # Méthodes pour les téléchargements
    def _start_monitoring(self):
        """Démarre le monitoring avec les vraies fonctionnalités"""
        if hasattr(self.parent, 'chrome_monitor') and self.parent.chrome_monitor:
            # Vérifier d'abord l'état actuel du monitoring
            if self.parent.chrome_monitor._running:
                self.parent._log("[WARN] Monitoring déjà actif")
                # Mettre à jour l'interface pour refléter l'état actuel
                self.download_status.configure(text="Monitoring: Actif", text_color="#4CAF50")
                self.start_btn.configure(state="disabled")
                self.stop_btn.configure(state="normal")
                return

            if self.parent.chrome_monitor.start():
                self.download_status.configure(text="Monitoring: Actif", text_color="#4CAF50")
                self.start_btn.configure(state="disabled")
                self.stop_btn.configure(state="normal")
                self.parent._log("Monitoring démarré avec détection automatique")
            else:
                self.parent._log("[ERROR] Échec démarrage monitoring")
        else:
            # Mode simulation pour compatibilité
            self.download_status.configure(text="Monitoring: Actif (Simulation)", text_color="#4CAF50")
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.parent._log("Monitoring démarré (mode simulation)")

    def _stop_monitoring(self):
        """Arrête le monitoring avec les vraies fonctionnalités"""
        if hasattr(self.parent, 'chrome_monitor') and self.parent.chrome_monitor:
            if self.parent.chrome_monitor.stop():
                self.download_status.configure(text="Monitoring: Arrêté", text_color="#f44336")
                self.start_btn.configure(state="normal")
                self.stop_btn.configure(state="disabled")
                self.parent._log("Monitoring arrêté")
            else:
                self.parent._log("[ERROR] Échec arrêt monitoring")
        else:
            # Mode simulation pour compatibilité
            self.download_status.configure(text="Monitoring: Arrêté", text_color="#f44336")
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.parent._log("Monitoring arrêté (mode simulation)")

    def _toggle_auto_save(self):
        """Toggle l'auto-save"""
        status = "activé" if self.auto_save_var.get() else "désactivé"
        self.parent._log(f"Auto-Save {status}")

    def _test_download(self):
        """Test les fonctionnalités de téléchargement"""
        self.parent._log("🎯 Test du système de téléchargement...")

        try:
            from core.services.download_manager import SimpleAutoSaver
            saver = SimpleAutoSaver(log_callback=self.parent._log)
            result = saver.simple_save(auto_click_save=self.auto_save_var.get())

            if result:
                self.parent._log("✅ Test réussi ! Fenêtre activée et contenu collé")
            else:
                self.parent._log("⚠️ Test terminé avec des problèmes")

        except ImportError as e:
            self.parent._log(f"❌ Erreur d'import: {e}")
        except Exception as e:
            self.parent._log(f"❌ Erreur test: {e}")

    def _toggle_debug(self):
        """Toggle le mode debug du monitoring"""
        if hasattr(self.parent, 'chrome_monitor') and self.parent.chrome_monitor:
            debug_enabled = self.debug_var.get()
            # Note: La classe ChromeMonitor actuelle n'a pas de méthode set_debug_mode
            # Nous utiliserons simplement la variable pour le logging
            if debug_enabled:
                self.parent._log("🐛 Mode debug activé - fonctionnalité à implémenter")
            else:
                self.parent._log("🐛 Mode debug désactivé")

    # Méthodes pour l'organisation
    def _browse_folder(self):
        """Ouvre le dialogue de sélection de dossier"""
        from tkinter import filedialog

        folder = filedialog.askdirectory(
            title="Sélectionner le dossier de musique",
            initialdir=self.folder_entry.get() or os.path.expanduser("~/Music")
        )

        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
            self.parent._log(f"Dossier sélectionné: {folder}")

            # Créer l'organisateur de musique avec ce dossier
            try:
                from core.services.music_organizer import MusicOrganizer
                self.music_organizer = MusicOrganizer(folder, log_callback=self.parent._log)
                self.scan_btn.configure(state="normal")
                self.parent._log(f"Organisateur créé pour le dossier: {folder}")
            except ImportError as e:
                self.parent._log(f"[ERROR] Impossible de créer l'organisateur: {e}")
            except Exception as e:
                self.parent._log(f"[ERROR] Erreur création organisateur: {e}")
            self.parent._log("[WARN] Aucun dossier sélectionné")
            return

    def _scan_folder(self):
        """Scanne le dossier avec les vraies fonctionnalités"""
        if not self.music_organizer:
            self.parent._log("[WARN] Aucun organisateur créé - sélectionnez d'abord un dossier")
            return

        self.parent._log(f"Scan du dossier: {self.music_organizer.base_folder}")

        def scan_thread():
            try:
                # Utiliser le vrai scan du MusicOrganizer
                songs = self.music_organizer.scan()

                # Mettre à jour les statistiques
                stats = self.music_organizer.get_stats()
                self.total_label.configure(text=f"Total: {stats['total']} fichiers")
                self.valid_label.configure(text=f"Valides: {len(songs)} fichiers")
                self.ignored_label.configure(text=f"Ignorés: {stats['total'] - len(songs)} fichiers")

                # Activer le bouton organiser si des chansons valides trouvées
                if songs:
                    self.organize_btn.configure(state="normal")
                    self.parent._log(f"Scan terminé: {len(songs)} chansons valides trouvées")
                else:
                    self.organize_btn.configure(state="disabled")
                    self.parent._log("Scan terminé: aucune chanson valide trouvée")

            except Exception as e:
                self.parent._log(f"[ERROR] Erreur lors du scan: {e}")
                import traceback
                traceback.print_exc()

        Thread(target=scan_thread, daemon=True).start()

    def _organize_folder(self):
        """Organise le dossier avec les vraies fonctionnalités"""
        if not self.music_organizer or not self.music_organizer.songs_found:
            self.parent._log("[WARN] Aucun organisateur ou chansons trouvées - scannez d'abord")
            return

        self.parent._log(f"Organisation du dossier: {self.music_organizer.base_folder}")

        # Confirmation avec les vraies statistiques
        stats = self.music_organizer.get_stats()
        response = tk.messagebox.askyesno(
            "Confirmation d'organisation",
            f"Voulez-vous organiser {stats['total']} chanson(s) trouvée(s)?\n\n"
            f"Artistes: {stats['artists']}\n"
            f"Albums: {stats['albums']}\n\n"
            "Les fichiers seront déplacés dans:\n"
            f"{self.music_organizer.base_folder}/Artiste/Album/"
        )

        if not response:
            return

        def organize_thread():
            try:
                # Utiliser la vraie organisation du MusicOrganizer
                success, errors = self.music_organizer.organize()

                # Mettre à jour les statistiques après organisation
                self.total_label.configure(text=f"Total organisé: {success} fichiers")
                self.valid_label.configure(text=f"Succès: {success}")
                self.ignored_label.configure(text=f"Erreurs: {errors}")

                # Désactiver le bouton organiser après organisation
                self.organize_btn.configure(state="disabled")

                self.parent._log(f"Organisation terminée: {success} succès, {errors} erreurs")

            except Exception as e:
                self.parent._log(f"[ERROR] Erreur lors de l'organisation: {e}")
                import traceback
                traceback.print_exc()

        Thread(target=organize_thread, daemon=True).start()

class SongsurfApp:
    def __init__(self):
        """Initialise l'application avec navigation par onglets"""
        try:
            # Configuration de base
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")

            # Créer la fenêtre principale
            self.root = ctk.CTk()
            self.root.title("Songsurf - Music Organizer")
            self.root.geometry("1200x800")
            self.root.minsize(800, 600)

            # État de l'application
            self.services_available = False
            self.chrome_monitor = None
            self.download_count = 0

            # Créer l'interface avec navigation EN HAUT
            self._create_ui()

            # Initialiser les services
            self._initialize_services()

            print("[OK] Application démarrée avec succès")

        except Exception as e:
            print(f"[ERROR] Erreur initialisation: {e}")
            import traceback
            traceback.print_exc()
            raise

    def _create_ui(self):
        """Crée l'interface utilisateur avec navigation CLASSIQUE EN HAUT"""
        # Navigation TOUT EN HAUT (comme un navigateur)
        self._create_navigation()

        # Frame principale (en dessous de la navigation)
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame de contenu pour les onglets (tout l'espace disponible)
        self.content_frame = ctk.CTkFrame(main_frame)
        self.content_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Créer le gestionnaire de navigation
        self.navigation = NavigationManager(self.content_frame, self)

        # Section Donation et Status tout en bas
        self._create_bottom_section()

        # Logs tout en bas
        self._create_logs_section()

        # Initialiser l'état de l'interface après création
        self._update_ui_state()

    def _create_bottom_section(self):
        """Crée la section donation et status en bas"""
        bottom_frame = ctk.CTkFrame(self.root)
        bottom_frame.pack(fill="x", side="bottom", pady=(0, 10))

        # Titre avec donation
        title_label = ctk.CTkLabel(
            bottom_frame,
            text="[DONATION] dev by Rev0li",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 5))

        # Status bar
        self.status_label = ctk.CTkLabel(
            bottom_frame,
            text="Status: Services actifs",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(0, 10))

    def _update_ui_state(self):
        """Met à jour l'état de l'interface selon l'état des services"""
        try:
            # Vérifier l'état du monitoring Chrome
            if hasattr(self, 'chrome_monitor') and self.chrome_monitor:
                if self.chrome_monitor._running:
                    # Monitoring actif - mettre à jour l'onglet Téléchargements
                    if hasattr(self, 'navigation') and self.navigation:
                        self.navigation.download_status.configure(text="Monitoring: Actif", text_color="#4CAF50")
                        self.navigation.start_btn.configure(state="disabled")
                        self.navigation.stop_btn.configure(state="normal")
                        self._log("Interface mise à jour: Monitoring actif détecté")
                else:
                    # Monitoring arrêté - mettre à jour l'onglet Téléchargements
                    if hasattr(self, 'navigation') and self.navigation:
                        self.navigation.download_status.configure(text="Monitoring: Arrêté", text_color="#f44336")
                        self.navigation.start_btn.configure(state="normal")
                        self.navigation.stop_btn.configure(state="disabled")
                        self._log("Interface mise à jour: Monitoring arrêté détecté")
        except Exception as e:
            self._log(f"[ERROR] Erreur mise à jour état interface: {e}")

    def _create_navigation(self):
        """Crée la navigation CLASSIQUE tout en haut"""
        # Frame pour la navigation (tout en haut comme une barre de navigateur)
        nav_frame = ctk.CTkFrame(self.root, height=60)
        nav_frame.pack(fill="x", padx=0, pady=0)
        nav_frame.pack_propagate(False)  # Empêcher le redimensionnement automatique

        # Frame interne pour centrer le contenu
        nav_content = ctk.CTkFrame(nav_frame)
        nav_content.pack(expand=True)

        # Onglets centrés dans la barre de navigation
        tabs_frame = ctk.CTkFrame(nav_content)
        tabs_frame.pack(expand=True)

        # Onglet Téléchargements (gauche)
        self.download_tab = ctk.CTkButton(
            tabs_frame,
            text="[DOWNLOAD]",
            command=lambda: self.navigation.show_tab("download"),
            font=ctk.CTkFont(size=14, weight="bold"),
            width=220,
            height=45,
            corner_radius=8,
            fg_color="#1f538d",
            hover_color="#2c6aa0"
        )
        self.download_tab.pack(side="left", padx=(20, 10), pady=8)

        # Onglet Organisation (droite)
        self.organize_tab = ctk.CTkButton(
            tabs_frame,
            text="[ORGANIZE]",
            command=lambda: self.navigation.show_tab("organize"),
            font=ctk.CTkFont(size=14, weight="bold"),
            width=220,
            height=45,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#555555",
            text_color="#666666"
        )
        self.organize_tab.pack(side="left", padx=10, pady=8)

    def _create_logs_section(self):
        """Crée la section des logs"""
        logs_frame = ctk.CTkFrame(self.root)
        logs_frame.pack(fill="x", side="bottom", pady=(0, 10))

        logs_label = ctk.CTkLabel(
            logs_frame,
            text="[LOGS] Logs de l'Application",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        logs_label.pack(anchor="w", padx=10, pady=(5, 0))

        # Zone de texte pour les logs
        self.logs_text = ctk.CTkTextbox(
            logs_frame,
            height=200,
            font=ctk.CTkFont(family="Consolas", size=9),
            fg_color="#1e1e1e",
            text_color="#00ff00"
        )
        self.logs_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Bouton effacer
        clear_btn = ctk.CTkButton(
            logs_frame,
            text="[CLEAR] Effacer",
            command=self._clear_logs,
            fg_color="#f44336",
            hover_color="#d32f2f",
            width=100
        )
        clear_btn.pack(anchor="e", padx=10, pady=(0, 10))

    def _initialize_services(self):
        """Initialise les services avec fallback"""
        try:
            # Tentative d'import et initialisation
            from core.services.chrome_monitor import ChromeMonitor

            # Configuration des paramètres
            ws_port = 8765

            # Créer le service Chrome
            self.chrome_monitor = ChromeMonitor(port=ws_port, log_callback=self._log)
            self.chrome_monitor.register_callback('on_detection', self._on_chrome_detection)

            # Démarrer le service
            if self.chrome_monitor.start():
                self.services_available = True
                self._log("Services Chrome initialisés avec succès")
                self._log(f"Port WebSocket: {ws_port}")
            else:
                self._log("[WARN] Échec démarrage services Chrome")

        except ImportError as e:
            self._log(f"[ERROR] Import échoué: {e}")
        except Exception as e:
            self._log(f"[ERROR] Erreur services: {e}")

    def _on_chrome_detection(self, data):
        """Callback pour les détections Chrome"""
        self.download_count += 1
        self._log(f"Téléchargement détecté: {data.get('title', 'Titre inconnu')}")

        # Mettre à jour le compteur si la navigation existe
        if hasattr(self, 'navigation'):
            self.navigation.download_count_label.configure(
                text=f"Téléchargements détectés: {self.download_count}"
            )

    def _log(self, message):
        """Ajoute un message aux logs"""
        try:
            self.logs_text.insert("end", f"{message}\n")
            self.logs_text.see("end")

            # Limiter le nombre de lignes
            lines = self.logs_text.get("1.0", "end").split('\n')
            if len(lines) > 1000:
                self.logs_text.delete("1.0", f"{len(lines)-800}.0")
        except:
            # Si logs non disponibles, utiliser print
            print(message)

    def _clear_logs(self):
        """Efface les logs"""
        try:
            self.logs_text.delete("1.0", "end")
        except:
            pass

    def run(self):
        """Lance l'application"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"[ERROR] Erreur exécution: {e}")
            raise

def main():
    """Point d'entrée principal"""
    print("[LAUNCH] Démarrage de Songsurf avec navigation...")
    print("=" * 50)

    try:
        app = SongsurfApp()
        app.run()
    except KeyboardInterrupt:
        print("\n[OK] Application arrêtée proprement")
    except Exception as e:
        print(f"\n[ERROR] Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
