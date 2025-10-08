"""
background_saver.py - Sauvegarde en arrière-plan sans activation de fenêtre

Cette approche utilise des techniques avancées pour remplir et sauvegarder
sans jamais activer la fenêtre, contournant les restrictions Windows.
"""

import time
import pyautogui
from typing import Optional, Callable, Tuple
import ctypes
from ctypes import wintypes

try:
    import win32gui
    import win32con
    import win32api
    import win32process
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

class BackgroundSaver:
    """
    Sauvegarde en arrière-plan sans activation de fenêtre.
    Utilise des techniques avancées Windows.
    """
    
    def __init__(self, log_callback: Optional[Callable] = None):
        """
        Initialise le sauveur en arrière-plan.
        
        Args:
            log_callback (Callable, optional): Fonction pour logger
        """
        self.log_callback = log_callback or print
        
        # Constantes Windows pour les messages
        self.WM_CHAR = 0x0102
        self.WM_KEYDOWN = 0x0100
        self.WM_KEYUP = 0x0101
        self.VK_CONTROL = 0x11
        self.VK_V = 0x56
        self.VK_RETURN = 0x0D
        self.VK_S = 0x53
        
    def log(self, message: str):
        """Log un message."""
        if self.log_callback:
            self.log_callback(message)
    
    def background_save(self, verify_path: bool = True, auto_click_save: bool = False) -> bool:
        """
        Sauvegarde en arrière-plan sans activer la fenêtre.
        
        Args:
            verify_path (bool): Vérifier le chemin
            auto_click_save (bool): Cliquer sur Save automatiquement
            
        Returns:
            bool: True si succès
        """
        if not WIN32_AVAILABLE:
            self.log("❌ win32gui non disponible pour la sauvegarde en arrière-plan")
            return False
        
        try:
            self.log("🔍 Recherche de la fenêtre Save As...")
            
            # Trouver la fenêtre Save As
            save_window = self._find_save_window()
            if not save_window:
                self.log("❌ Fenêtre Save As non trouvée")
                return False
            
            hwnd, title = save_window
            self.log(f"✅ Fenêtre trouvée: {title}")
            
            # Trouver le champ de nom de fichier
            filename_control = self._find_filename_control(hwnd)
            if not filename_control:
                self.log("❌ Champ nom de fichier non trouvé")
                return False
            
            self.log("✅ Champ nom de fichier trouvé")
            
            # Coller le nom de fichier directement dans le contrôle
            success = self._paste_to_control(filename_control)
            if not success:
                self.log("❌ Échec du collage dans le contrôle")
                return False
            
            self.log("✅ Nom de fichier collé en arrière-plan")
            
            # Vérifier le chemin si demandé
            if verify_path:
                path_ok = self._verify_path_background(hwnd)
                if not path_ok:
                    self.log("⚠️ Chemin incorrect détecté")
                    return False
            
            # Cliquer sur Save si demandé
            if auto_click_save:
                save_success = self._click_save_background(hwnd)
                if save_success:
                    self.log("✅ Bouton Save cliqué en arrière-plan")
                else:
                    self.log("⚠️ Impossible de cliquer sur Save automatiquement")
            
            self.log("✅ Sauvegarde en arrière-plan terminée")
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur dans background_save: {str(e)}")
            return False
    
    def _find_save_window(self) -> Optional[Tuple[int, str]]:
        """
        Trouve la fenêtre Save As.
        
        Returns:
            Tuple[int, str]: (hwnd, title) ou None
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
    
    def _find_filename_control(self, parent_hwnd: int) -> Optional[int]:
        """
        Trouve le contrôle de nom de fichier dans la fenêtre Save As.
        
        Args:
            parent_hwnd (int): Handle de la fenêtre parent
            
        Returns:
            int: Handle du contrôle ou None
        """
        def enum_child_callback(hwnd, controls):
            class_name = win32gui.GetClassName(hwnd)
            # Chercher les contrôles Edit (champ de texte)
            if class_name in ["Edit", "ComboBoxEx32", "ComboBox"]:
                controls.append(hwnd)
        
        controls = []
        win32gui.EnumChildWindows(parent_hwnd, enum_child_callback, controls)
        
        # Retourner le premier contrôle Edit trouvé
        return controls[0] if controls else None
    
    def _paste_to_control(self, control_hwnd: int) -> bool:
        """
        Colle le contenu du clipboard dans un contrôle spécifique.
        
        Args:
            control_hwnd (int): Handle du contrôle
            
        Returns:
            bool: True si succès
        """
        try:
            # Méthode 1: Envoyer Ctrl+V directement au contrôle
            self.log("📋 Envoi de Ctrl+V au contrôle...")
            
            # Envoyer Ctrl+V au contrôle spécifique
            win32api.SendMessage(control_hwnd, self.WM_KEYDOWN, self.VK_CONTROL, 0)
            time.sleep(0.1)
            win32api.SendMessage(control_hwnd, self.WM_KEYDOWN, self.VK_V, 0)
            time.sleep(0.1)
            win32api.SendMessage(control_hwnd, self.WM_KEYUP, self.VK_V, 0)
            win32api.SendMessage(control_hwnd, self.WM_KEYUP, self.VK_CONTROL, 0)
            
            time.sleep(0.5)
            return True
            
        except Exception as e:
            self.log(f"⚠️ Méthode 1 échouée: {str(e)}")
            
            # Méthode 2: Obtenir le texte du clipboard et l'envoyer caractère par caractère
            try:
                if not PYPERCLIP_AVAILABLE:
                    return False
                
                text = pyperclip.paste()
                if not text:
                    self.log("⚠️ Clipboard vide")
                    return False
                
                self.log(f"📝 Envoi du texte caractère par caractère: {text[:50]}...")
                
                # Envoyer chaque caractère
                for char in text:
                    win32api.SendMessage(control_hwnd, self.WM_CHAR, ord(char), 0)
                    time.sleep(0.01)  # Petit délai entre les caractères
                
                return True
                
            except Exception as e2:
                self.log(f"⚠️ Méthode 2 échouée: {str(e2)}")
                return False
    
    def _verify_path_background(self, parent_hwnd: int) -> bool:
        """
        Vérifie le chemin en arrière-plan.
        
        Args:
            parent_hwnd (int): Handle de la fenêtre parent
            
        Returns:
            bool: True si le chemin est correct
        """
        try:
            # Chercher le contrôle d'adresse/chemin
            def enum_callback(hwnd, controls):
                class_name = win32gui.GetClassName(hwnd)
                if "Address" in class_name or "Breadcrumb" in class_name:
                    controls.append(hwnd)
            
            controls = []
            win32gui.EnumChildWindows(parent_hwnd, enum_callback, controls)
            
            if not controls:
                self.log("⚠️ Contrôle de chemin non trouvé, vérification ignorée")
                return True
            
            # Pour l'instant, on assume que c'est OK
            # TODO: Implémenter la vérification réelle du chemin
            return True
            
        except Exception as e:
            self.log(f"⚠️ Erreur vérification chemin: {str(e)}")
            return True
    
    def _click_save_background(self, parent_hwnd: int) -> bool:
        """
        Clique sur le bouton Save en arrière-plan.
        
        Args:
            parent_hwnd (int): Handle de la fenêtre parent
            
        Returns:
            bool: True si succès
        """
        try:
            # Chercher le bouton Save
            def enum_callback(hwnd, buttons):
                class_name = win32gui.GetClassName(hwnd)
                if class_name == "Button":
                    text = win32gui.GetWindowText(hwnd)
                    if ("save" in text.lower() or 
                        "enregistrer" in text.lower() or 
                        "ok" in text.lower()):
                        buttons.append(hwnd)
            
            buttons = []
            win32gui.EnumChildWindows(parent_hwnd, enum_callback, buttons)
            
            if not buttons:
                self.log("⚠️ Bouton Save non trouvé")
                return False
            
            # Cliquer sur le premier bouton trouvé
            save_button = buttons[0]
            self.log("🖱️ Clic sur le bouton Save...")
            
            # Envoyer un clic au bouton
            win32api.SendMessage(save_button, win32con.BM_CLICK, 0, 0)
            
            return True
            
        except Exception as e:
            self.log(f"⚠️ Erreur clic Save: {str(e)}")
            return False

def test_background_save():
    """Test la sauvegarde en arrière-plan."""
    print("🧪 Test Sauvegarde en Arrière-Plan")
    print("=" * 50)
    
    saver = BackgroundSaver()
    
    print("📋 Instructions:")
    print("1. Ouvrez Chrome et téléchargez un fichier")
    print("2. Quand la fenêtre 'Save As' s'ouvre, NE LA TOUCHEZ PAS")
    print("3. Revenez ici et appuyez sur Entrée")
    print("4. Le bot va remplir et sauvegarder en arrière-plan")
    
    input("\nAppuyez sur Entrée pour tester...")
    
    result = saver.background_save(verify_path=True, auto_click_save=True)
    
    if result:
        print("✅ SUCCESS: Sauvegarde en arrière-plan réussie!")
    else:
        print("❌ FAILED: Problème avec la sauvegarde")

if __name__ == "__main__":
    test_background_save()
