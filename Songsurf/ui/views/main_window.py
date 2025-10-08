"""
Vue principale de l'application
"""
import customtkinter as ctk
from config import settings

class MainWindow:
    def __init__(self, root, services):
        self.root = root
        self.services = services
        
        # Configuration de base
        self.root.title("Songsurf")
        self.root.geometry("1200x800")
        ctk.set_appearance_mode(settings.THEME)
        ctk.set_default_color_theme(settings.COLOR_SCHEME)
        
        # Initialiser les composants
        self._setup_ui()
        self._connect_services()
    
    def _setup_ui(self):
        """Créer l'interface utilisateur"""
        # Navigation
        self.nav_frame = ctk.CTkFrame(self.root)
        self.nav_frame.pack(fill="x", padx=10, pady=10)
        
        # Zone de contenu
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(fill="both", expand=True)
        
        # Logs
        self._setup_logs()
    
    def _setup_logs(self):
        """Configurer le système de logs"""
        self.logs_frame = ctk.CTkFrame(self.root)
        self.logs_frame.pack(fill="x", side="bottom", pady=(0,10))
        
        self.log_text = ctk.CTkTextbox(self.logs_frame, height=150)
        self.log_text.pack(fill="both", padx=10, pady=(0,10))
    
    def _connect_services(self):
        """Connecter les callbacks des services"""
        self.services['chrome'].register_callback(
            'on_detection', 
            self._on_chrome_detection
        )
    
    def _on_chrome_detection(self, data):
        """Callback pour les détections Chrome"""
        self.log(f"Nouveau téléchargement détecté: {data['title']}")
    
    def log(self, message):
        """Ajouter un message aux logs"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
