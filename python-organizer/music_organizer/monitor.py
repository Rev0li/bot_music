"""
monitor.py - Surveillance des téléchargements

Ce module surveille les fenêtres "Enregistrer sous" pour détecter
les nouveaux téléchargements et afficher des notifications.
"""

import subprocess
import time
import threading
from typing import Callable, Optional, Set

try:
    from .auto_saver import AutoSaver
    AUTO_SAVE_AVAILABLE = True
except ImportError:
    AUTO_SAVE_AVAILABLE = False

try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


class DownloadMonitor:
    """
    Surveille les fenêtres "Enregistrer sous" et notifie l'utilisateur.
    """
    
    def __init__(self, notification_callback: Optional[Callable] = None, log_callback: Optional[Callable] = None, auto_paste: bool = True, auto_save: bool = False):
        """
        Initialise le moniteur de téléchargements.
        
        Args:
            notification_callback (Callable, optional): Fonction appelée lors d'une détection
            log_callback (Callable, optional): Fonction pour logger les messages
            auto_paste (bool): Coller automatiquement le nom de fichier
            auto_save (bool): Cliquer automatiquement sur Save
        """
        self.notification_callback = notification_callback
        self.log_callback = log_callback or print
        self.is_monitoring = False
        self.monitor_thread = None
        self.detected_windows: Set[str] = set()
        self.auto_paste = auto_paste
        self.auto_save = auto_save
        self.debug_mode = False
        
        # AutoSaver pour l'automatisation
        if AUTO_SAVE_AVAILABLE:
            self.auto_saver = AutoSaver(log_callback=self.log)
        else:
            self.auto_saver = None
        
        # Mots-clés pour détecter les fenêtres de sauvegarde
        self.keywords = [
            "wants to save",  # Chrome download dialog
            "Enregistrer sous",
            "Save As",
            "Enregistrer",
            "Save",
            "Télécharger",
            "Download"
        ]
    
    def log(self, message: str):
        """
        Log un message via le callback.
        
        Args:
            message (str): Message à logger
        """
        if self.log_callback:
            self.log_callback(message)
    
    def start(self):
        """
        Démarre la surveillance des fenêtres.
        
        Examples:
            >>> monitor = DownloadMonitor()
            >>> monitor.start()
            >>> # La surveillance est maintenant active
        """
        if self.is_monitoring:
            self.log("⚠️ Le moniteur est déjà actif")
            return
        
        self.is_monitoring = True
        self.log("🚀 Scanner de téléchargement activé")
        
        # Indiquer la méthode de détection utilisée
        if WIN32_AVAILABLE:
            self.log("✅ Utilisation de win32gui (détection optimale)")
        else:
            self.log("⚠️ win32gui non disponible, utilisation de PowerShell")
            self.log("💡 Pour une meilleure détection: pip install pywin32")
        
        self.log("🔍 Surveillance des fenêtres 'Enregistrer sous' en cours...")
        
        # Lancer le thread de surveillance
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop(self):
        """
        Arrête la surveillance des fenêtres.
        
        Examples:
            >>> monitor = DownloadMonitor()
            >>> monitor.start()
            >>> monitor.stop()
            >>> # La surveillance est maintenant arrêtée
        """
        if not self.is_monitoring:
            self.log("⚠️ Le moniteur n'est pas actif")
            return
        
        self.is_monitoring = False
        self.log("🛑 Scanner de téléchargement arrêté")
    
    def _monitor_loop(self):
        """
        Boucle principale de surveillance (exécutée dans un thread).
        """
        while self.is_monitoring:
            try:
                self._check_windows()
                time.sleep(1)  # Vérifier toutes les 1 seconde
            except Exception as e:
                self.log(f"⚠️ Erreur monitoring: {str(e)}")
                time.sleep(2)
    
    def _check_windows(self):
        """
        Vérifie les fenêtres actives et détecte les fenêtres de sauvegarde.
        Utilise win32gui si disponible, sinon PowerShell.
        """
        if WIN32_AVAILABLE:
            self._check_windows_win32()
        else:
            self._check_windows_powershell()
    
    def _check_windows_win32(self):
        """
        Détecte les fenêtres avec win32gui (méthode la plus fiable).
        """
        try:
            windows_found = []
            
            def enum_callback(hwnd, results):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if title:
                        results.append(title)
            
            win32gui.EnumWindows(enum_callback, windows_found)
            
            # Mode debug: afficher toutes les fenêtres
            if self.debug_mode:
                self.log(f"🐛 Fenêtres détectées (win32): {len(windows_found)}")
            
            for title in windows_found:
                if self.debug_mode:
                    self.log(f"🐛 Fenêtre: {title}")
                
                self._check_window_title(title)
            
            # Nettoyer les anciennes détections
            if len(self.detected_windows) > 10:
                self.detected_windows.clear()
                
        except Exception as e:
            if self.debug_mode:
                self.log(f"⚠️ Erreur win32: {str(e)}")
    
    def _check_windows_powershell(self):
        """
        Détecte les fenêtres avec PowerShell (fallback).
        """
        try:
            # Utiliser PowerShell pour obtenir les fenêtres avec titre
            ps_command = 'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object MainWindowTitle | ConvertTo-Json'
            
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=2
            )
            
            # Analyser la sortie JSON
            import json
            try:
                windows = json.loads(result.stdout)
                if not isinstance(windows, list):
                    windows = [windows]
                
                # Mode debug: afficher toutes les fenêtres
                if self.debug_mode and windows:
                    self.log(f"🐛 Fenêtres détectées (PowerShell): {len(windows)}")
                
                for window in windows:
                    if window and 'MainWindowTitle' in window:
                        title = window['MainWindowTitle']
                        
                        # Mode debug: afficher chaque titre
                        if self.debug_mode:
                            self.log(f"🐛 Fenêtre: {title}")
                        
                        self._check_window_title(title)
                        
            except json.JSONDecodeError:
                # Fallback: analyser ligne par ligne
                for line in result.stdout.split('\n'):
                    if line.strip():
                        if self.debug_mode:
                            self.log(f"🐛 Ligne: {line.strip()}")
                        self._check_window_title(line.strip())
            
            # Nettoyer les anciennes détections
            if len(self.detected_windows) > 10:
                self.detected_windows.clear()
                
        except Exception as e:
            if self.debug_mode:
                self.log(f"⚠️ Erreur PowerShell: {str(e)}")
    
    def _check_window_title(self, title: str):
        """
        Vérifie si un titre de fenêtre correspond aux mots-clés.
        
        Args:
            title (str): Titre de la fenêtre
        """
        for keyword in self.keywords:
            if keyword.lower() in title.lower():
                if self._is_valid_window(title):
                    self.detected_windows.add(title)
                    self._on_window_detected(title)
                    break
    
    def set_debug_mode(self, debug: bool):
        """
        Active/Désactive le mode debug qui affiche toutes les fenêtres.
        
        Args:
            debug (bool): True pour activer le debug
        """
        self.debug_mode = debug
        if debug:
            self.log("🐛 Mode debug activé - toutes les fenêtres seront affichées")
    
    def _is_valid_window(self, window_title: str) -> bool:
        """
        Vérifie si un titre de fenêtre est valide pour notification.
        
        Args:
            window_title (str): Titre de la fenêtre
            
        Returns:
            bool: True si valide, False sinon
        """
        # Ignorer les fenêtres déjà détectées
        if window_title in self.detected_windows:
            return False
        
        # Ignorer les fenêtres trop courtes
        if not window_title or len(window_title) <= 5:
            return False
        
        # Ignorer certaines fenêtres spécifiques qui ne sont pas des "Save As"
        ignore_keywords = [
            "Recent download history",  # Historique Chrome
            "Downloads",  # Fenêtre de téléchargements
            "History",  # Historique
        ]
        
        for ignore in ignore_keywords:
            if ignore.lower() in window_title.lower():
                if self.debug_mode:
                    self.log(f"⏭️ Fenêtre ignorée: {window_title}")
                return False
        
        return True
    
    def _on_window_detected(self, window_title: str):
        """
        Appelé quand une fenêtre "Enregistrer sous" est détectée.
        
        Args:
            window_title (str): Titre de la fenêtre détectée
        """
        self.log(f"🔔 Fenêtre détectée: {window_title}")
        
        # Automatiser le collage et la sauvegarde si activé
        if self.auto_saver and self.auto_paste:
            self.log(f"⏳ Attente de 2 secondes pour que la fenêtre soit prête...")
            time.sleep(2)  # Attendre que la fenêtre soit prête (augmenté à 2s)
            
            self.log(f"🤖 Démarrage de l'automatisation...")
            self.log(f"   - auto_paste: {self.auto_paste}")
            self.log(f"   - auto_save: {self.auto_save}")
            self.log(f"   - auto_saver disponible: {self.auto_saver is not None}")
            
            try:
                result = self.auto_saver.auto_save(
                    verify_path=True,
                    auto_click_save=self.auto_save
                )
                if result:
                    self.log("✅ Automatisation terminée avec succès")
                else:
                    self.log("⚠️ Automatisation terminée avec avertissements")
            except Exception as e:
                self.log(f"❌ Erreur lors de l'automatisation: {str(e)}")
        else:
            if not self.auto_saver:
                self.log("⚠️ AutoSaver non disponible (pyautogui/pyperclip manquants)")
            if not self.auto_paste:
                self.log("⚠️ Auto-paste désactivé")
        
        # Appeler le callback de notification si défini
        if self.notification_callback:
            self.notification_callback(window_title)
    
    def is_active(self) -> bool:
        """
        Vérifie si le moniteur est actif.
        
        Returns:
            bool: True si actif, False sinon
        """
        return self.is_monitoring
    
    def get_detected_count(self) -> int:
        """
        Retourne le nombre de fenêtres détectées.
        
        Returns:
            int: Nombre de détections
        """
        return len(self.detected_windows)
    
    def clear_history(self):
        """
        Efface l'historique des fenêtres détectées.
        """
        self.detected_windows.clear()
        self.log("🗑️ Historique des détections effacé")
