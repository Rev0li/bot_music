"""
auto_saver.py - Automatisation de la fenêtre "Enregistrer sous"

Ce module détecte la fenêtre "Save As" et automatise:
1. Détection de la fenêtre
2. Collage du nom de fichier (Ctrl+V)
3. Vérification du chemin (Music/itunes)
4. Clic sur le bouton Save
"""

import time
import pyautogui
from typing import Optional, Callable

try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

try:
    from .notification_helper import SmartNotifier
    NOTIFICATION_AVAILABLE = True
except ImportError:
    NOTIFICATION_AVAILABLE = False

class AutoSaver:
    """
    Automatise la sauvegarde dans la fenêtre "Enregistrer sous".
    """
    
    def __init__(self, log_callback: Optional[Callable] = None):
        """
        Initialise l'auto-saver.
        
        Args:
            log_callback (Callable, optional): Fonction pour logger les messages
        """
        self.log_callback = log_callback or print
        self.target_path = "C:\\Users\\Molim\\Music\\itunes"  # Chemin cible à vérifier
        
        # Notificateur intelligent
        if NOTIFICATION_AVAILABLE:
            self.notifier = SmartNotifier(log_callback=self.log)
        else:
            self.notifier = None
        
        # Configuration pyautogui
        pyautogui.FAILSAFE = True  # Déplacer la souris dans le coin arrête tout
        pyautogui.PAUSE = 0.5  # Pause entre les actions
    
    def log(self, message: str):
        """
        Log un message via le callback.
        
        Args:
            message (str): Message à logger
        """
        if self.log_callback:
            self.log_callback(message)
    
    def activate_save_window(self) -> bool:
        """
        Active la fenêtre "Save As" pour qu'elle reçoive les événements clavier.
        Utilise plusieurs méthodes pour forcer l'activation.
        
        Returns:
            bool: True si fenêtre trouvée et activée, False sinon
        """
        if not WIN32_AVAILABLE:
            self.log("⚠️ win32gui non disponible, impossible d'activer la fenêtre")
            return False
        
        try:
            self.log("🎯 Recherche de la fenêtre 'Save As'...")
            
            # Chercher la fenêtre avec "wants to save" dans le titre
            def find_window_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if "wants to save" in title.lower() or "save as" in title.lower() or "enregistrer" in title.lower():
                        windows.append(hwnd)
            
            windows = []
            win32gui.EnumWindows(find_window_callback, windows)
            
            if windows:
                hwnd = windows[0]  # Prendre la première fenêtre trouvée
                window_title = win32gui.GetWindowText(hwnd)
                self.log(f"✅ Fenêtre trouvée: {window_title}")
                
                # Méthode simple: Juste essayer SetForegroundWindow
                self.log("🎯 Activation de la fenêtre...")
                try:
                    # Restaurer si minimisée
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.2)
                    
                    # Activer au premier plan
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.5)
                    
                    # Vérifier si ça a marché
                    current_window = win32gui.GetForegroundWindow()
                    if current_window == hwnd:
                        self.log("✅ Fenêtre activée avec succès!")
                        return True
                    else:
                        current_title = win32gui.GetWindowText(current_window)
                        self.log(f"⚠️ Fenêtre toujours pas active. Fenêtre actuelle: {current_title}")
                        self.log("💡 Cliquez manuellement sur la fenêtre 'Save As' si nécessaire")
                        return False
                        
                except Exception as e:
                    self.log(f"⚠️ Erreur lors de l'activation: {str(e)}")
                    return False
                
            else:
                self.log("⚠️ Fenêtre 'Save As' non trouvée")
                return False
                
        except Exception as e:
            self.log(f"⚠️ Erreur lors de l'activation: {str(e)}")
            return False
    
    def smart_auto_save(self, verify_path: bool = True, auto_click_save: bool = False) -> bool:
        """
        Version intelligente avec notifications pour contourner les restrictions Windows.
        
        Args:
            verify_path (bool): Vérifier que le chemin contient "Music/itunes"
            auto_click_save (bool): Cliquer automatiquement sur Save
            
        Returns:
            bool: True si succès, False sinon
        """
        try:
            self.log("🧠 Automatisation intelligente avec notifications...")
            
            # Étape 1: Trouver la fenêtre Save As
            save_window_title = self._find_save_window_title()
            if not save_window_title:
                self.log("❌ Aucune fenêtre 'Save As' trouvée")
                return False
            
            # Étape 2: Notification à l'utilisateur
            if self.notifier:
                self.notifier.show_save_as_detected(save_window_title)
                self.log("📢 Notification affichée à l'utilisateur")
            
            # Étape 3: Notification avant collage
            if self.notifier:
                self.notifier.show_paste_ready()
            else:
                self.log("⏳ Attente de 3 secondes...")
                time.sleep(3)
            
            # Étape 4: Coller le nom (l'utilisateur a eu le temps d'activer la fenêtre)
            self.log("📋 Collage du nom de fichier...")
            pyautogui.hotkey('ctrl', 'v')
            self.log("✅ Ctrl+V envoyé")
            time.sleep(1)
            
            # Étape 5: Vérification du chemin si demandé
            if verify_path:
                self.log("🔍 Vérification du chemin...")
                path_ok = self.verify_save_path()
                if not path_ok:
                    self.log("⚠️ Chemin incorrect détecté")
                    if self.notifier:
                        self.notifier.show_manual_action_needed(
                            "Naviguez vers le dossier Music\\itunes avant de sauvegarder"
                        )
                    return False
            
            # Étape 6: Clic sur Save si demandé
            if auto_click_save:
                self.log("💾 Tentative de clic sur Save...")
                if self.notifier:
                    self.notifier.show_manual_action_needed(
                        "Cliquez sur le bouton 'Save' / 'Enregistrer' pour finaliser"
                    )
                else:
                    # Essayer quand même
                    success = self.click_save_button()
                    if not success:
                        self.log("⚠️ Impossible de cliquer sur Save automatiquement")
                        self.log("💡 Cliquez manuellement sur le bouton Save")
            
            self.log("✅ Automatisation intelligente terminée")
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur dans smart_auto_save: {str(e)}")
            return False
    
    def _find_save_window_title(self) -> Optional[str]:
        """
        Trouve le titre de la fenêtre Save As active.
        
        Returns:
            str: Titre de la fenêtre ou None si non trouvée
        """
        if not WIN32_AVAILABLE:
            return None
            
        try:
            def find_window_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if ("wants to save" in title.lower() or 
                        "save as" in title.lower() or 
                        "enregistrer" in title.lower()):
                        windows.append(title)
            
            windows = []
            win32gui.EnumWindows(find_window_callback, windows)
            
            return windows[0] if windows else None
            
        except Exception as e:
            self.log(f"⚠️ Erreur lors de la recherche de fenêtre: {str(e)}")
            return None
    
    def auto_save(self, verify_path: bool = True, auto_click_save: bool = False) -> bool:
        """
        Automatise la sauvegarde du fichier.
        
        Args:
            verify_path (bool): Vérifier que le chemin contient "Music/itunes"
            auto_click_save (bool): Cliquer automatiquement sur Save
            
        Returns:
            bool: True si succès, False sinon
            
        Examples:
            >>> saver = AutoSaver()
            >>> saver.auto_save(verify_path=True, auto_click_save=False)
            True
        """
        try:
            self.log("🤖 Automatisation de la sauvegarde...")
            self.log(f"   - verify_path: {verify_path}")
            self.log(f"   - auto_click_save: {auto_click_save}")
            
            # Étape 1: Activer la fenêtre "Save As" (CRITIQUE!)
            self.log("🎯 Activation de la fenêtre 'Save As'...")
            activated = self.activate_save_window()
            if not activated:
                self.log("⚠️ ATTENTION: Impossible d'activer la fenêtre automatiquement!")
                self.log("💡 Tentative de collage quand même (risque de coller ailleurs)")
                self.log("🔔 Assurez-vous que la fenêtre 'Save As' est active manuellement")
            
            # Attendre un peu après activation
            self.log("⏳ Attente de 1 seconde pour stabiliser...")
            time.sleep(1.0)
            
            # Étape 2: Coller le nom de fichier (Ctrl+V)
            self.log("📋 Collage du nom de fichier (Ctrl+V)...")
            self.log("   → Simulation de Ctrl+V...")
            pyautogui.hotkey('ctrl', 'v')
            self.log("   ✅ Ctrl+V envoyé")
            time.sleep(0.8)  # Augmenté pour laisser le temps au collage
            
            # Étape 3: Vérifier le chemin si demandé
            if verify_path:
                self.log("🔍 Vérification du chemin...")
                path_ok = self.verify_save_path()
                if not path_ok:
                    self.log("⚠️ Attention: Le chemin ne contient pas 'Music\\itunes'")
                    self.log("💡 Veuillez naviguer vers le bon dossier")
                    return False
            else:
                self.log("⏭️ Vérification du chemin ignorée")
            
            # Étape 4: Cliquer sur Save si demandé
            if auto_click_save:
                self.log("💾 Clic sur le bouton Save...")
                success = self.click_save_button()
                if success:
                    self.log("✅ Fichier sauvegardé automatiquement!")
                    return True
                else:
                    self.log("⚠️ Bouton Save non trouvé, cliquez manuellement")
                    return False
            else:
                self.log("✅ Nom de fichier collé! Cliquez sur Save manuellement")
                return True
                
        except Exception as e:
            self.log(f"❌ Erreur lors de l'automatisation: {str(e)}")
            import traceback
            self.log(f"📋 Traceback: {traceback.format_exc()}")
            return False
    
    def verify_save_path(self) -> bool:
        """
        Vérifie que le chemin de sauvegarde contient "Music\\itunes".
        
        Returns:
            bool: True si le chemin est correct, False sinon
        """
        try:
            self.log("🔍 Début de la vérification du chemin...")
            
            # Méthode: Utiliser Alt+D pour sélectionner la barre d'adresse
            self.log("   → Envoi de Alt+D pour sélectionner la barre d'adresse...")
            pyautogui.hotkey('alt', 'd')
            time.sleep(0.3)
            self.log("   ✅ Alt+D envoyé")
            
            # Copier le chemin (Ctrl+C)
            self.log("   → Envoi de Ctrl+C pour copier le chemin...")
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.3)
            self.log("   ✅ Ctrl+C envoyé")
            
            # Récupérer le chemin depuis le clipboard
            self.log("   → Lecture du clipboard...")
            import pyperclip
            current_path = pyperclip.paste()
            self.log(f"   ✅ Clipboard lu: {current_path}")
            
            self.log(f"📂 Chemin actuel: {current_path}")
            
            # Vérifier si le chemin contient "Music" et "itunes"
            has_music = "Music" in current_path or "music" in current_path
            has_itunes = "itunes" in current_path or "iTunes" in current_path
            
            self.log(f"   - Contient 'Music': {has_music}")
            self.log(f"   - Contient 'itunes': {has_itunes}")
            
            path_ok = has_music and has_itunes
            
            if path_ok:
                self.log("✅ Chemin correct: Music\\itunes")
            else:
                self.log(f"⚠️ Chemin incorrect: {current_path}")
                self.log(f"💡 Attendu: ...\\Music\\itunes")
            
            # Appuyer sur Escape pour désélectionner la barre d'adresse
            self.log("   → Envoi de Escape...")
            pyautogui.press('escape')
            time.sleep(0.2)
            self.log("   ✅ Escape envoyé")
            
            return path_ok
            
        except Exception as e:
            self.log(f"⚠️ Impossible de vérifier le chemin: {str(e)}")
            import traceback
            self.log(f"📋 Traceback: {traceback.format_exc()}")
            return True  # Continuer quand même
    
    def click_save_button(self) -> bool:
        """
        Clique sur le bouton "Save" / "Enregistrer".
        
        Returns:
            bool: True si le bouton a été trouvé et cliqué, False sinon
        """
        try:
            # Méthode 1: Utiliser Alt+S (raccourci clavier pour Save)
            self.log("⌨️ Tentative avec Alt+S...")
            pyautogui.hotkey('alt', 's')
            time.sleep(0.3)
            return True
            
        except Exception as e:
            self.log(f"⚠️ Erreur lors du clic sur Save: {str(e)}")
            return False
    
    def paste_filename_only(self) -> bool:
        """
        Colle uniquement le nom de fichier sans vérification ni clic.
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            self.log("📋 Collage du nom de fichier...")
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'v')
            self.log("✅ Nom de fichier collé!")
            return True
        except Exception as e:
            self.log(f"❌ Erreur: {str(e)}")
            return False
    
    def navigate_to_itunes(self) -> bool:
        """
        Tente de naviguer vers le dossier Music/itunes.
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            self.log("🧭 Navigation vers Music\\itunes...")
            
            # Cliquer dans la barre d'adresse
            pyautogui.hotkey('alt', 'd')
            time.sleep(0.2)
            
            # Taper le chemin
            import os
            music_path = os.path.join(os.path.expanduser("~"), "Music", "itunes")
            pyautogui.write(music_path, interval=0.05)
            time.sleep(0.2)
            
            # Appuyer sur Enter
            pyautogui.press('enter')
            time.sleep(0.5)
            
            self.log(f"✅ Navigation vers: {music_path}")
            return True
            
        except Exception as e:
            self.log(f"❌ Erreur de navigation: {str(e)}")
            return False
