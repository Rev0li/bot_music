"""
process_activator.py - Activation propre par processus

Approche simple et efficace : activer directement le processus du navigateur
au lieu de chercher des fenêtres spécifiques.
"""

import time
import pyautogui
from typing import Optional, Callable, List
import subprocess

try:
    import win32gui
    import win32con
    import win32process
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class ProcessActivator:
    """
    Active les fenêtres par nom de processus de manière propre.
    """
    
    def __init__(self, log_callback: Optional[Callable] = None):
        """
        Initialise l'activateur de processus.
        
        Args:
            log_callback (Callable, optional): Fonction pour logger
        """
        self.log_callback = log_callback or print
        
        # Processus de navigateurs à chercher (par ordre de priorité)
        self.browser_processes = [
            "brave.exe",
            "chrome.exe", 
            "msedge.exe",
            "firefox.exe",
            "opera.exe"
        ]
        
    def log(self, message: str):
        """Log un message."""
        if self.log_callback:
            self.log_callback(message)
    
    def activate_browser_and_paste(self, verify_path: bool = True) -> bool:
        """
        Active la fenêtre "Save As" et colle le nom de fichier.
        
        Args:
            verify_path (bool): Vérifier le chemin (ignoré pour l'instant)
            
        Returns:
            bool: True si succès
        """
        try:
            self.log("🎯 Recherche de la fenêtre 'Save As'...")
            
            # Étape 1: Chercher d'abord la fenêtre "Save As"
            save_window = self._find_save_as_window()
            if save_window:
                hwnd, title = save_window
                self.log(f"✅ Fenêtre 'Save As' trouvée: {title}")
                
                # Activer cette fenêtre spécifiquement avec méthodes multiples
                self.log("🎯 Activation de la fenêtre 'Save As'...")
                
                # Méthode 1: Restaurer la fenêtre
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(0.2)
                
                # Méthode 2: Essayer SetForegroundWindow
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    self.log("✅ SetForegroundWindow réussi")
                except Exception as e:
                    self.log(f"⚠️ SetForegroundWindow échoué: {str(e)}")
                    
                    # Méthode 3: Alt+Tab pour forcer l'activation
                    self.log("⌨️ Tentative Alt+Tab...")
                    try:
                        pyautogui.keyDown('alt')
                        time.sleep(0.1)
                        pyautogui.press('tab')
                        time.sleep(0.1)
                        pyautogui.keyUp('alt')
                        time.sleep(0.3)
                        self.log("✅ Alt+Tab effectué")
                    except Exception as e2:
                        self.log(f"⚠️ Alt+Tab échoué: {str(e2)}")
                    
                    # Méthode 4: Cliquer sur la fenêtre pour l'activer
                    self.log("🖱️ Tentative d'activation par clic...")
                    try:
                        rect = win32gui.GetWindowRect(hwnd)
                        x = rect[0] + (rect[2] - rect[0]) // 2
                        y = rect[1] + (rect[3] - rect[1]) // 2
                        
                        # Cliquer au centre de la fenêtre
                        pyautogui.click(x, y)
                        self.log("✅ Clic d'activation effectué")
                    except Exception as e3:
                        self.log(f"⚠️ Clic d'activation échoué: {str(e3)}")
                
                time.sleep(1.0)
                
                # Coller le nom de fichier
                self.log("📋 Collage du nom de fichier...")
                pyautogui.hotkey('ctrl', 'v')
                self.log("✅ Ctrl+V envoyé dans la fenêtre 'Save As'")
                
                return True
            
            # Étape 2: Si pas de fenêtre "Save As", essayer d'activer le navigateur
            self.log("⚠️ Pas de fenêtre 'Save As' trouvée, activation du navigateur...")
            browser_activated = self._activate_browser_process()
            if not browser_activated:
                self.log("❌ Aucun navigateur trouvé")
                return False
            
            # Attendre et coller
            self.log("⏳ Attente de stabilisation...")
            time.sleep(1.0)
            
            self.log("📋 Collage du nom de fichier...")
            pyautogui.hotkey('ctrl', 'v')
            self.log("✅ Ctrl+V envoyé")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur dans activate_browser_and_paste: {str(e)}")
            return False
    
    def _activate_browser_process(self) -> bool:
        """
        Trouve et active le processus du navigateur.
        
        Returns:
            bool: True si succès
        """
        if not WIN32_AVAILABLE:
            self.log("⚠️ win32gui non disponible")
            return False
        
        if not PSUTIL_AVAILABLE:
            self.log("⚠️ psutil non disponible, utilisation de la méthode alternative...")
            # Utiliser la méthode par fenêtre au lieu de processus
            return self._activate_browser_by_window()
        
        try:
            # Méthode 1: Chercher par processus en cours
            for process_name in self.browser_processes:
                if self._activate_process_by_name(process_name):
                    self.log(f"✅ Processus {process_name} activé")
                    return True
            
            # Méthode 2: Chercher les fenêtres avec des titres de navigateur
            browser_window = self._find_browser_window()
            if browser_window:
                hwnd, title = browser_window
                self.log(f"✅ Fenêtre navigateur trouvée: {title}")
                win32gui.SetForegroundWindow(hwnd)
                return True
            
            self.log("❌ Aucun navigateur trouvé")
            return False
            
        except Exception as e:
            self.log(f"⚠️ Erreur activation navigateur: {str(e)}")
            return False
    
    def _activate_process_by_name(self, process_name: str) -> bool:
        """
        Active un processus par son nom.
        
        Args:
            process_name (str): Nom du processus (ex: "brave.exe")
            
        Returns:
            bool: True si trouvé et activé
        """
        if not PSUTIL_AVAILABLE:
            return False
            
        try:
            # Utiliser psutil pour trouver le processus
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == process_name.lower():
                    pid = proc.info['pid']
                    self.log(f"🔍 Processus {process_name} trouvé (PID: {pid})")
                    
                    # Trouver la fenêtre principale de ce processus
                    windows = self._get_windows_by_pid(pid)
                    if windows:
                        # Activer la première fenêtre trouvée
                        hwnd = windows[0]
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        win32gui.SetForegroundWindow(hwnd)
                        return True
            
            return False
            
        except Exception as e:
            self.log(f"⚠️ Erreur recherche processus {process_name}: {str(e)}")
            return False
    
    def _get_windows_by_pid(self, pid: int) -> List[int]:
        """
        Récupère les fenêtres d'un processus donné.
        
        Args:
            pid (int): ID du processus
            
        Returns:
            List[int]: Liste des handles de fenêtres
        """
        def enum_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                if window_pid == pid:
                    windows.append(hwnd)
        
        windows = []
        win32gui.EnumWindows(enum_callback, windows)
        return windows
    
    def _find_browser_window(self) -> Optional[tuple]:
        """
        Trouve une fenêtre de navigateur par titre.
        
        Returns:
            tuple: (hwnd, title) ou None
        """
        browser_keywords = [
            "brave",
            "chrome", 
            "edge",
            "firefox",
            "opera"
        ]
        
        def enum_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd).lower()
                for keyword in browser_keywords:
                    if keyword in title:
                        windows.append((hwnd, title))
                        break
        
        windows = []
        win32gui.EnumWindows(enum_callback, windows)
        
        return windows[0] if windows else None
    
    def _activate_browser_by_window(self) -> bool:
        """
        Active le navigateur en cherchant directement les fenêtres (sans psutil).
        
        Returns:
            bool: True si succès
        """
        try:
            self.log("🔍 Recherche de fenêtres navigateur...")
            
            # Chercher les fenêtres avec des titres de navigateur
            browser_window = self._find_browser_window()
            if browser_window:
                hwnd, title = browser_window
                self.log(f"✅ Fenêtre navigateur trouvée: {title}")
                
                # Activer la fenêtre
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                return True
            
            # Si pas trouvé par titre, chercher les fenêtres "Save As" et activer leur processus parent
            self.log("🔍 Recherche via fenêtre Save As...")
            save_window = self._find_save_as_window()
            if save_window:
                hwnd, title = save_window
                self.log(f"✅ Fenêtre Save As trouvée: {title}")
                
                # Activer cette fenêtre (qui appartient au navigateur)
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                return True
            
            self.log("❌ Aucune fenêtre navigateur trouvée")
            return False
            
        except Exception as e:
            self.log(f"⚠️ Erreur activation par fenêtre: {str(e)}")
            return False
    
    def _find_save_as_window(self) -> Optional[tuple]:
        """
        Trouve la fenêtre Save As active.
        
        Returns:
            tuple: (hwnd, title) ou None
        """
        def enum_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if ("wants to save" in title.lower() or 
                    "save as" in title.lower() or 
                    "enregistrer" in title.lower()):
                    windows.append((hwnd, title))
        
        windows = []
        win32gui.EnumWindows(enum_callback, windows)
        
        return windows[0] if windows else None

class SimpleAutoSaver:
    """
    Version simplifiée et propre de l'auto-saver.
    """
    
    def __init__(self, log_callback: Optional[Callable] = None):
        """
        Initialise l'auto-saver simple.
        
        Args:
            log_callback (Callable, optional): Fonction pour logger
        """
        self.log_callback = log_callback or print
        self.activator = ProcessActivator(log_callback=self.log)
        
    def log(self, message: str):
        """Log un message."""
        if self.log_callback:
            self.log_callback(message)
    
    def simple_save(self, auto_click_save: bool = False) -> bool:
        """
        Méthode simple : Active la fenêtre "Save As" et colle.
        
        Args:
            auto_click_save (bool): Cliquer automatiquement sur Save
        
        Returns:
            bool: True si succès
        """
        self.log("🚀 Démarrage de la sauvegarde simple...")
        
        # Priorité à la fenêtre "Save As" !
        result = self.activator.activate_browser_and_paste()
        
        if result and auto_click_save:
            self.log("💾 Tentative de clic automatique sur 'Save'...")
            save_result = self._click_save_button()
            if save_result:
                self.log("✅ Bouton 'Save' cliqué automatiquement")
            else:
                self.log("⚠️ Impossible de cliquer sur 'Save' automatiquement")
        
        if result:
            self.log("✅ Sauvegarde simple terminée avec succès")
        else:
            self.log("❌ Échec de la sauvegarde simple")
        
        return result
    
    def _click_save_button(self) -> bool:
        """
        Clique sur le bouton Save dans la fenêtre active.
        
        Returns:
            bool: True si succès
        """
        try:
            self.log("🔍 Recherche du bouton 'Save'...")
            
            # Attendre un peu que la fenêtre soit stable
            time.sleep(0.5)
            
            # Méthode 1: Essayer Entrée (souvent le bouton par défaut)
            self.log("⌨️ Tentative avec Entrée...")
            pyautogui.press('enter')
            time.sleep(0.5)
            
            # Méthode 2: Essayer Alt+S (raccourci Save)
            self.log("⌨️ Tentative avec Alt+S...")
            pyautogui.hotkey('alt', 's')
            time.sleep(0.5)
            
            return True
            
        except Exception as e:
            self.log(f"⚠️ Erreur clic Save: {str(e)}")
            return False

def test_simple_save():
    """Test la sauvegarde simple."""
    print("🧪 Test Sauvegarde Simple")
    print("=" * 40)
    
    saver = SimpleAutoSaver()
    
    print("📋 Instructions:")
    print("1. Ouvrez Brave/Chrome et téléchargez un fichier")
    print("2. Quand la fenêtre 'Save As' s'ouvre, revenez ici")
    print("3. Le bot va activer Brave et coller automatiquement")
    
    input("\nAppuyez sur Entrée pour tester...")
    
    result = saver.simple_save()
    
    if result:
        print("✅ SUCCESS: Sauvegarde simple réussie!")
    else:
        print("❌ FAILED: Problème avec la sauvegarde")

if __name__ == "__main__":
    test_simple_save()
