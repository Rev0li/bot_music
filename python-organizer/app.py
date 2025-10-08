"""
app.py - Application principale avec interface graphique

Interface graphique pour organiser les fichiers MP3 avec:
- Sélection de dossier
- Scan des fichiers
- Organisation automatique
- Surveillance des téléchargements
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading

from music_organizer import MetadataParser, MusicOrganizer, DownloadMonitor


class MusicOrganizerApp:
    """
    Application principale avec interface graphique Tkinter.
    """
    
    def __init__(self, root):
        """
        Initialise l'application.
        
        Args:
            root: Fenêtre racine Tkinter
        """
        self.root = root
        self.root.title("🎵 Music Organizer Pro")
        self.root.geometry("700x650")
        self.root.configure(bg="#2b2b2b")
        
        # Variables
        self.source_folder = ""
        self.organizer = None
        self.monitor = None
        
        # Style
        self.colors = {
            'bg': "#2b2b2b",
            'fg': "#ffffff",
            'button': "#4CAF50",
            'button_hover': "#45a049",
            'error': "#f44336",
            'info': "#2196F3"
        }
        
        self.create_widgets()
        self.setup_monitor()
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface."""
        self._create_title()
        self._create_folder_selector()
        self._create_monitor_controls()
        self._create_action_buttons()
        self._create_status_labels()
        self._create_log_area()
        self._create_progress_label()
    
    def _create_title(self):
        """Crée le titre de l'application."""
        title = tk.Label(
            self.root,
            text="🎵 Music Organizer Pro",
            font=("Arial", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        title.pack(pady=20)
    
    def _create_folder_selector(self):
        """Crée la section de sélection de dossier."""
        folder_frame = tk.Frame(self.root, bg=self.colors['bg'])
        folder_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(
            folder_frame,
            text="📁 Dossier source:",
            font=("Arial", 12),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        ).pack(side="left", padx=5)
        
        self.folder_label = tk.Label(
            folder_frame,
            text="Aucun dossier sélectionné",
            font=("Arial", 10),
            bg=self.colors['bg'],
            fg="#888888",
            anchor="w"
        )
        self.folder_label.pack(side="left", fill="x", expand=True, padx=5)
        
        browse_btn = tk.Button(
            folder_frame,
            text="📂 Parcourir",
            command=self.browse_folder,
            font=("Arial", 10, "bold"),
            bg=self.colors['button'],
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=15,
            pady=5
        )
        browse_btn.pack(side="right", padx=5)
    
    def _create_monitor_controls(self):
        """Crée les contrôles du scanner de téléchargement."""
        monitor_frame = tk.Frame(self.root, bg=self.colors['bg'])
        monitor_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(
            monitor_frame,
            text="🔍 Scanner de téléchargement:",
            font=("Arial", 12),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        ).pack(side="left", padx=5)
        
        self.monitor_status = tk.Label(
            monitor_frame,
            text="⭕ OFF",
            font=("Arial", 11, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['error']
        )
        self.monitor_status.pack(side="left", padx=10)
        
        self.monitor_btn = tk.Button(
            monitor_frame,
            text="▶️ Activer",
            command=self.toggle_monitor,
            font=("Arial", 10, "bold"),
            bg=self.colors['button'],
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=15,
            pady=5
        )
        self.monitor_btn.pack(side="right", padx=5)
        
        # Bouton Debug
        debug_btn = tk.Button(
            monitor_frame,
            text="🐛 Debug",
            command=self.toggle_debug,
            font=("Arial", 9),
            bg="#FF9800",
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=10,
            pady=5
        )
        debug_btn.pack(side="right", padx=5)
    
    def _create_action_buttons(self):
        """Crée les boutons d'action principaux."""
        action_frame = tk.Frame(self.root, bg=self.colors['bg'])
        action_frame.pack(pady=20)
        
        self.scan_btn = tk.Button(
            action_frame,
            text="🔍 Scanner les chansons",
            command=self.scan_songs,
            font=("Arial", 12, "bold"),
            bg=self.colors['info'],
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=20,
            pady=10,
            state="disabled"
        )
        self.scan_btn.pack(side="left", padx=10)
        
        self.organize_btn = tk.Button(
            action_frame,
            text="✨ Organiser les chansons",
            command=self.organize_songs,
            font=("Arial", 12, "bold"),
            bg=self.colors['button'],
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=20,
            pady=10,
            state="disabled"
        )
        self.organize_btn.pack(side="left", padx=10)
    
    def _create_status_labels(self):
        """Crée les labels de statut."""
        self.count_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11),
            bg=self.colors['bg'],
            fg=self.colors['button']
        )
        self.count_label.pack(pady=5)
    
    def _create_log_area(self):
        """Crée la zone de logs."""
        log_label = tk.Label(
            self.root,
            text="📋 Logs:",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        log_label.pack(pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            self.root,
            height=15,
            width=80,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#00ff00",
            insertbackground="white",
            relief="flat"
        )
        self.log_text.pack(pady=10, padx=20, fill="both", expand=True)
    
    def _create_progress_label(self):
        """Crée le label de progression."""
        self.progress_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            bg=self.colors['bg'],
            fg="#888888"
        )
        self.progress_label.pack(pady=5)
    
    def setup_monitor(self):
        """Configure le moniteur de téléchargements."""
        self.monitor = DownloadMonitor(
            notification_callback=self.show_download_notification,
            log_callback=self.log,
            auto_paste=True,   # ✅ Coller automatiquement le nom
            auto_save=True     # ✅ Cliquer automatiquement sur Save
        )
    
    def log(self, message: str):
        """
        Ajoute un message dans les logs.
        
        Args:
            message (str): Message à logger
        """
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def browse_folder(self):
        """Ouvre le sélecteur de dossier."""
        folder = filedialog.askdirectory(
            title="Sélectionner le dossier contenant les musiques"
        )
        if folder:
            self.source_folder = folder
            self.folder_label.config(text=folder, fg=self.colors['fg'])
            self.scan_btn.config(state="normal")
            self.log(f"📁 Dossier sélectionné: {folder}")
            
            # Créer l'organisateur
            self.organizer = MusicOrganizer(folder, log_callback=self.log)
    
    def toggle_monitor(self):
        """Active/Désactive le scanner de téléchargement."""
        if self.monitor.is_active():
            self.monitor.stop()
            self.monitor_status.config(text="⭕ OFF", fg=self.colors['error'])
            self.monitor_btn.config(text="▶️ Activer", bg=self.colors['button'])
        else:
            self.monitor.start()
            self.monitor_status.config(text="✅ ON", fg=self.colors['button'])
            self.monitor_btn.config(text="⏸️ Désactiver", bg=self.colors['error'])
    
    def toggle_debug(self):
        """Active/Désactive le mode debug du scanner."""
        if self.monitor:
            current = getattr(self.monitor, 'debug_mode', False)
            self.monitor.set_debug_mode(not current)
            
            if not current:
                self.log("🐛 Mode debug activé - toutes les fenêtres seront affichées")
                messagebox.showinfo(
                    "Mode Debug",
                    "Mode debug activé!\n\n"
                    "Toutes les fenêtres détectées seront affichées dans les logs.\n"
                    "Ouvrez une fenêtre 'Save As' pour tester."
                )
            else:
                self.log("🐛 Mode debug désactivé")
    
    def scan_songs(self):
        """Scanne les chansons dans le dossier."""
        if not self.organizer:
            messagebox.showwarning("Attention", "Veuillez sélectionner un dossier d'abord!")
            return
        
        songs = self.organizer.scan()
        count = len(songs)
        
        self.count_label.config(text=f"🎵 {count} chanson(s) trouvée(s) et prête(s) à organiser")
        
        if count > 0:
            self.organize_btn.config(state="normal")
            
            # Afficher les statistiques
            stats = self.organizer.get_stats()
            self.log(f"📊 Statistiques:")
            self.log(f"   - Total: {stats['total']} chansons")
            self.log(f"   - Artistes: {stats['artists']}")
            self.log(f"   - Albums: {stats['albums']}")
        else:
            messagebox.showinfo("Information", "Aucune chanson avec le bon format trouvée!")
    
    def organize_songs(self):
        """Organise les chansons (dans un thread séparé)."""
        if not self.organizer or not self.organizer.songs_found:
            messagebox.showwarning("Attention", "Veuillez scanner les chansons d'abord!")
            return
        
        # Confirmation
        response = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous organiser {len(self.organizer.songs_found)} chanson(s)?\n\n"
            "Les fichiers seront déplacés dans:\n"
            f"{self.source_folder}/Artiste/Album/"
        )
        
        if not response:
            return
        
        # Désactiver les boutons pendant le traitement
        self.scan_btn.config(state="disabled")
        self.organize_btn.config(state="disabled")
        
        # Lancer dans un thread
        thread = threading.Thread(target=self.organize_thread)
        thread.start()
    
    def organize_thread(self):
        """Organise les chansons (thread)."""
        success, errors = self.organizer.organize()
        
        # Réactiver les boutons
        self.scan_btn.config(state="normal")
        self.organize_btn.config(state="disabled")
        self.count_label.config(text=f"✅ {success} chanson(s) organisée(s)")
        
        # Message de fin
        messagebox.showinfo(
            "Terminé",
            f"Organisation terminée!\n\n"
            f"✅ {success} chanson(s) organisée(s)\n"
            f"❌ {errors} erreur(s)"
        )
    
    def show_download_notification(self, window_title: str):
        """
        Affiche une notification pour un nouveau téléchargement.
        
        Args:
            window_title (str): Titre de la fenêtre détectée
        """
        # Créer une fenêtre de notification
        notification = tk.Toplevel(self.root)
        notification.title("🔔 Téléchargement détecté")
        notification.geometry("450x180")
        notification.configure(bg=self.colors['button'])
        notification.attributes('-topmost', True)
        
        tk.Label(
            notification,
            text="🔔 Nouveau téléchargement!",
            font=("Arial", 16, "bold"),
            bg=self.colors['button'],
            fg="white"
        ).pack(pady=15)
        
        tk.Label(
            notification,
            text=f"Fenêtre: {window_title[:40]}...",
            font=("Arial", 10),
            bg=self.colors['button'],
            fg="white"
        ).pack(pady=5)
        
        tk.Label(
            notification,
            text="💡 Le nom de fichier est dans votre clipboard!\nAppuyez sur Ctrl+V pour coller dans 'Enregistrer sous'",
            font=("Arial", 9),
            bg=self.colors['button'],
            fg="white",
            justify="center"
        ).pack(pady=10)
        
        tk.Button(
            notification,
            text="OK",
            command=notification.destroy,
            font=("Arial", 10, "bold"),
            bg="white",
            fg=self.colors['button'],
            cursor="hand2",
            relief="flat",
            padx=25,
            pady=8
        ).pack(pady=10)
        
        # Fermer automatiquement après 6 secondes
        notification.after(6000, notification.destroy)


def main():
    """Point d'entrée de l'application."""
    root = tk.Tk()
    app = MusicOrganizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
