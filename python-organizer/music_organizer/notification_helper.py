"""
notification_helper.py - Notifications visuelles pour guider l'utilisateur
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
from typing import Optional, Callable

class NotificationWindow:
    """
    Fenêtre de notification non-bloquante qui reste au premier plan.
    """
    
    def __init__(self, title: str, message: str, duration: int = 10):
        """
        Crée une fenêtre de notification.
        
        Args:
            title (str): Titre de la notification
            message (str): Message à afficher
            duration (int): Durée en secondes (0 = permanent)
        """
        self.root = None
        self.title = title
        self.message = message
        self.duration = duration
        self.closed = False
        
    def show(self):
        """Affiche la notification dans un thread séparé."""
        thread = threading.Thread(target=self._create_window, daemon=True)
        thread.start()
        
    def _create_window(self):
        """Crée la fenêtre de notification."""
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry("400x200")
        self.root.configure(bg='#2b2b2b')
        
        # Toujours au premier plan
        self.root.attributes('-topmost', True)
        
        # Centrer sur l'écran
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (200 // 2)
        self.root.geometry(f"400x200+{x}+{y}")
        
        # Titre
        title_label = tk.Label(
            self.root, 
            text=self.title,
            font=('Arial', 14, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        title_label.pack(pady=10)
        
        # Message
        message_label = tk.Label(
            self.root,
            text=self.message,
            font=('Arial', 10),
            fg='#ffffff',
            bg='#2b2b2b',
            wraplength=350,
            justify='center'
        )
        message_label.pack(pady=10, padx=20)
        
        # Boutons
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        ok_button = tk.Button(
            button_frame,
            text="✅ OK",
            command=self._close,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20
        )
        ok_button.pack(side=tk.LEFT, padx=10)
        
        ignore_button = tk.Button(
            button_frame,
            text="❌ Ignorer",
            command=self._close,
            bg='#f44336',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20
        )
        ignore_button.pack(side=tk.LEFT, padx=10)
        
        # Auto-fermeture si durée spécifiée
        if self.duration > 0:
            self.root.after(self.duration * 1000, self._close)
            
        # Gérer la fermeture
        self.root.protocol("WM_DELETE_WINDOW", self._close)
        
        # Démarrer la boucle
        self.root.mainloop()
        
    def _close(self):
        """Ferme la fenêtre."""
        if self.root and not self.closed:
            self.closed = True
            self.root.quit()
            self.root.destroy()

class SmartNotifier:
    """
    Gestionnaire de notifications intelligentes.
    """
    
    def __init__(self, log_callback: Optional[Callable] = None):
        """
        Initialise le notificateur.
        
        Args:
            log_callback (Callable, optional): Fonction pour logger
        """
        self.log_callback = log_callback or print
        self.active_notifications = []
        
    def log(self, message: str):
        """Log un message."""
        if self.log_callback:
            self.log_callback(message)
    
    def show_save_as_detected(self, window_title: str) -> bool:
        """
        Affiche une notification quand une fenêtre Save As est détectée.
        
        Args:
            window_title (str): Titre de la fenêtre détectée
            
        Returns:
            bool: True si l'utilisateur veut continuer
        """
        self.log(f"📢 Affichage notification pour: {window_title}")
        
        title = "🔔 Téléchargement Détecté"
        message = f"""Fenêtre de téléchargement détectée:
        
"{window_title}"

Le nom du fichier va être collé automatiquement.

💡 Cliquez sur la fenêtre de téléchargement 
   pour qu'elle soit active, puis cliquez OK."""
        
        # Créer et afficher la notification
        notification = NotificationWindow(title, message, duration=15)
        notification.show()
        
        return True
    
    def show_paste_ready(self) -> bool:
        """
        Affiche une notification avant de coller.
        
        Returns:
            bool: True si l'utilisateur est prêt
        """
        title = "📋 Prêt à Coller"
        message = """Le nom du fichier va être collé dans 3 secondes.

Assurez-vous que la fenêtre de téléchargement 
est active (cliquez dessus si nécessaire).

⏰ Collage automatique dans 3... 2... 1..."""
        
        notification = NotificationWindow(title, message, duration=3)
        notification.show()
        
        # Attendre 3 secondes
        time.sleep(3)
        return True
    
    def show_manual_action_needed(self, action: str) -> bool:
        """
        Affiche une notification pour une action manuelle.
        
        Args:
            action (str): Action à effectuer manuellement
            
        Returns:
            bool: True si l'utilisateur a compris
        """
        title = "👆 Action Manuelle Requise"
        message = f"""Action requise:

{action}

Le bot ne peut pas effectuer cette action automatiquement 
à cause des restrictions de sécurité Windows.

Cliquez OK quand c'est fait."""
        
        notification = NotificationWindow(title, message, duration=0)  # Permanent
        notification.show()
        
        return True

def test_notification():
    """Test les notifications."""
    print("🧪 Test des notifications...")
    
    notifier = SmartNotifier()
    
    # Test 1: Détection
    notifier.show_save_as_detected("www8.mnuu.nu wants to save")
    time.sleep(2)
    
    # Test 2: Prêt à coller
    notifier.show_paste_ready()
    
    # Test 3: Action manuelle
    notifier.show_manual_action_needed("Cliquez sur le bouton 'Save' dans la fenêtre de téléchargement")

if __name__ == "__main__":
    test_notification()
