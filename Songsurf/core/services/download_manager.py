"""
download_manager.py - Module de gestion des téléchargements pour Songsurf

Fonctionnalités intégrées depuis python-organizer:
- Surveillance des fenêtres "Enregistrer sous"
- Activation automatique des navigateurs
- Collage automatique du nom de fichier
- Clic automatique sur le bouton Save
- Notifications en temps réel
"""

import time
import subprocess
import threading
from typing import Callable, Optional, Dict

# Essayer d'importer les dépendances optionnelles
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

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    # Configuration pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False


class AutoSaver:
    """Automatisation avancée de la fenêtre "Enregistrer sous"."""

    def __init__(self, log_callback: Optional[Callable] = None, target_path: Optional[str] = None):
        self.log_callback = log_callback or print
        self.target_path = target_path or r"C:\\Users\\Molim\\Music\\itunes"
        self.available = WIN32_AVAILABLE and PYAUTOGUI_AVAILABLE

        if PYAUTOGUI_AVAILABLE:
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.5

    def log(self, message: str):
        if self.log_callback:
            self.log_callback(message)

    def _enum_save_windows(self) -> list:
        windows: list = []

        if not WIN32_AVAILABLE:
            return windows

        try:
            def find_window_callback(hwnd, results):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if title and ("wants to save" in title.lower() or
                                  "save as" in title.lower() or
                                  "enregistrer" in title.lower() or
                                  "save" in title.lower()):
                        results.append((hwnd, title))

            win32gui.EnumWindows(find_window_callback, windows)
        except Exception as exc:
            self.log(f"⚠️ Erreur énumération fenêtres Save As: {exc}")

        return windows

    def activate_save_window(self) -> bool:
        if not WIN32_AVAILABLE:
            self.log("⚠️ win32gui non disponible, impossible d'activer la fenêtre")
            return False

        try:
            self.log("🎯 Recherche de la fenêtre 'Save As'...")
            windows = self._enum_save_windows()

            if not windows:
                self.log("⚠️ Fenêtre 'Save As' non trouvée")
                return False

            hwnd, title = windows[0]
            self.log(f"✅ Fenêtre trouvée: {title}")

            try:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(0.2)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.5)

                current_hwnd = win32gui.GetForegroundWindow()
                if current_hwnd == hwnd:
                    self.log("✅ Fenêtre activée avec succès!")
                    return True

                current_title = win32gui.GetWindowText(current_hwnd)
                self.log(f"⚠️ Fenêtre toujours pas active. Fenêtre actuelle: {current_title}")
                return False
            except Exception as exc:
                self.log(f"⚠️ Erreur lors de l'activation: {exc}")
                return False

        except Exception as exc:
            self.log(f"⚠️ Erreur lors de la recherche de fenêtre: {exc}")
            return False

    def auto_save(self, verify_path: bool = True, auto_click_save: bool = False) -> bool:
        if not self.available:
            self.log("⚠️ AutoSaver indisponible (pyautogui/win32 manquants)")
            return False

        try:
            self.log("🤖 Automatisation de la sauvegarde...")
            self.log(f"   - verify_path: {verify_path}")
            self.log(f"   - auto_click_save: {auto_click_save}")

            activated = self.activate_save_window()
            if not activated:
                self.log("⚠️ Impossible d'activer la fenêtre automatiquement")
                self.log("💡 Assurez-vous que la fenêtre 'Save As' est au premier plan")

            self.log("⏳ Attente de 1 seconde pour stabiliser...")
            time.sleep(1.0)

            self.log("📋 Collage du nom de fichier (Ctrl+V)...")
            pyautogui.hotkey('ctrl', 'v')
            self.log("   ✅ Ctrl+V envoyé")
            time.sleep(0.8)

            if verify_path:
                path_ok = self.verify_save_path()
                if not path_ok:
                    self.log("⚠️ Le chemin ne contient pas 'Music\\itunes'")
                    return False
            else:
                self.log("⏭️ Vérification du chemin ignorée")

            if auto_click_save:
                self.log("💾 Clic sur le bouton Save...")
                success = self.click_save_button()
                if success:
                    self.log("✅ Fichier sauvegardé automatiquement!")
                    return True
                self.log("⚠️ Bouton Save non trouvé, cliquez manuellement")
                return False

            self.log("✅ Nom de fichier collé! Cliquez sur Save manuellement")
            return True

        except Exception as exc:
            self.log(f"❌ Erreur lors de l'automatisation: {exc}")
            return False

    def verify_save_path(self) -> bool:
        if not PYAUTOGUI_AVAILABLE or not PYPERCLIP_AVAILABLE:
            self.log("⚠️ Vérification du chemin indisponible (pyautogui/pyperclip)")
            return True

        try:
            self.log("🔍 Début de la vérification du chemin...")
            pyautogui.hotkey('alt', 'd')
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.3)

            current_path = pyperclip.paste()
            self.log(f"📂 Chemin actuel: {current_path}")

            has_music = "music" in current_path.lower()
            has_itunes = "itunes" in current_path.lower()

            if has_music and has_itunes:
                self.log("✅ Chemin correct: Music\\itunes")
                pyautogui.press('escape')
                time.sleep(0.2)
                return True

            self.log("⚠️ Chemin incorrect: ajustez manuellement")
            pyautogui.press('escape')
            time.sleep(0.2)
            return False

        except Exception as exc:
            self.log(f"⚠️ Impossible de vérifier le chemin: {exc}")
            return True

    def click_save_button(self) -> bool:
        if not PYAUTOGUI_AVAILABLE:
            return False

        try:
            self.log("⌨️ Tentative avec Alt+S...")
            pyautogui.hotkey('alt', 's')
            time.sleep(0.3)
            return True
        except Exception as exc:
            self.log(f"⚠️ Erreur lors du clic sur Save: {exc}")
            return False


class ProcessActivator:
    """
    Active les fenêtres par nom de processus de manière propre.
    Adapté depuis python-organizer.
    """

    def __init__(self, log_callback: Optional[Callable] = None):
        """Initialise l'activateur de processus."""
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

    def activate_browser_and_paste(self) -> bool:
        """
        Active la fenêtre "Save As" et colle le nom de fichier.

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

                # Activer cette fenêtre spécifiquement
                self.log("🎯 Activation de la fenêtre 'Save As'...")

                # Méthode 1: Restaurer la fenêtre
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(0.2)

                # Méthode 2: SetForegroundWindow
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

                # Méthode 4: Coller le contenu du clipboard
                if PYPERCLIP_AVAILABLE and PYAUTOGUI_AVAILABLE:
                    self.log("📋 Collage du nom de fichier...")
                    try:
                        # Petit délai pour s'assurer que la fenêtre est active
                        time.sleep(0.5)

                        # Coller avec Ctrl+V
                        pyautogui.hotkey('ctrl', 'v')
                        self.log("✅ Nom de fichier collé")
                        return True
                    except Exception as e:
                        self.log(f"⚠️ Échec du collage: {str(e)}")

                return True

            self.log("❌ Aucune fenêtre 'Save As' trouvée")
            return False

        except Exception as e:
            self.log(f"⚠️ Erreur activation navigateur: {str(e)}")
            return False

    def _find_save_as_window(self) -> Optional[tuple]:
        """Trouve la fenêtre Save As active."""
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
    Adapté depuis python-organizer.
    """

    def __init__(self, log_callback: Optional[Callable] = None):
        """Initialise l'auto-saver simple."""
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
        """Clique sur le bouton Save dans la fenêtre active."""
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


class DownloadMonitor:
    """
    Surveille les fenêtres "Enregistrer sous" et notifie l'utilisateur.
    Adapté depuis python-organizer.
    """

    def __init__(self, notification_callback: Optional[Callable] = None,
                 log_callback: Optional[Callable] = None,
                 auto_paste: bool = True,
                 auto_save: bool = False):
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
        self.detected_windows: Dict[str, float] = {}
        self.detection_cooldown = 5.0
        self.total_detections = 0
        self.auto_saver = None
        self.simple_auto_saver = None
        self.debug_mode = False
        self.last_detection_time = 0
        self.auto_paste = auto_paste
        self.auto_save = auto_save

        # AutoSaver pour l'automatisation
        if WIN32_AVAILABLE and PYAUTOGUI_AVAILABLE:
            self.auto_saver = AutoSaver(log_callback=self.log)

        if PYAUTOGUI_AVAILABLE:
            self.simple_auto_saver = SimpleAutoSaver(log_callback=self.log)

        # Mots-clés pour détecter les fenêtres de sauvegarde
        self.keywords = [
            "wants to save",  # Chrome download dialog
            "Enregistrer sous",
            "Save As",
            "Enregistrer",
            "Save",
            "Télécharger",
            "Download",
            "Save file",  # Anglais générique
            "Enregistrer le fichier",  # Français générique
            "Choose where to save",  # Anglais
            "Choisir l'emplacement",  # Français
            "Save file as",  # Anglais
            "Enregistrer le fichier sous",  # Français
            # Extensions Chrome communes
            "extension",
            "chrome-extension",
            "manifest",
            # Autres patterns courants
            "Save Page As",
            "Enregistrer la page sous",
            "Export",
            "Exporter",
        ]

    def log(self, message: str):
        """Log un message via le callback."""
        if self.log_callback:
            self.log_callback(f"[DownloadMonitor] {message}")

    def start(self):
        """Démarre la surveillance des fenêtres."""
        if self.is_monitoring:
            self.log("⚠️ Le moniteur est déjà actif")
            return False

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
        return True

    def stop(self):
        """Arrête la surveillance des fenêtres."""
        if not self.is_monitoring:
            self.log("⚠️ Le moniteur n'est pas actif")
            return False

        self.is_monitoring = False
        self.log("🛑 Scanner de téléchargement arrêté")
        return True

    def _monitor_loop(self):
        """Boucle principale de surveillance."""
        while self.is_monitoring:
            try:
                self._check_windows()
                time.sleep(1)  # Vérifier toutes les 1 seconde
            except Exception as e:
                self.log(f"⚠️ Erreur monitoring: {str(e)}")
                time.sleep(2)

    def _check_windows(self):
        """Vérifie les fenêtres actives."""
        if WIN32_AVAILABLE:
            self._check_windows_win32()
        else:
            self._check_windows_powershell()

    def _check_windows_win32(self):
        """Détecte les fenêtres avec win32gui."""
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

            if len(self.detected_windows) > 20:
                self.detected_windows.clear()

        except Exception as e:
            if self.debug_mode:
                self.log(f"⚠️ Erreur win32: {str(e)}")

    def _check_windows_powershell(self):
        """Détecte les fenêtres avec PowerShell."""
        try:
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

                if self.debug_mode and windows:
                    self.log(f"🐛 Fenêtres détectées (PowerShell): {len(windows)}")

                for window in windows:
                    if window and 'MainWindowTitle' in window:
                        title = window['MainWindowTitle']

                        if self.debug_mode:
                            self.log(f"🐛 Fenêtre: {title}")

                        self._check_window_title(title)

                if len(self.detected_windows) > 20:
                    self.detected_windows.clear()

            except json.JSONDecodeError:
                for line in result.stdout.split('\n'):
                    if line.strip():
                        if self.debug_mode:
                            self.log(f"🐛 Ligne: {line.strip()}")
                        self._check_window_title(line.strip())

        except Exception as e:
            if self.debug_mode:
                self.log(f"⚠️ Erreur PowerShell: {str(e)}")

    def _check_window_title(self, title: str):
        """Vérifie si un titre de fenêtre correspond aux mots-clés."""
        normalized_title = title.strip()
        if not normalized_title:
            return

        lower_title = normalized_title.lower()

        for keyword in self.keywords:
            if keyword.lower() in lower_title:
                if self._is_valid_window(normalized_title):
                    self._on_window_detected(normalized_title)
                    break

    def _is_valid_window(self, window_title: str) -> bool:
        """Vérifie si un titre de fenêtre est valide pour notification."""
        # Nettoyer le titre
        if not window_title:
            return False

        window_title = window_title.strip()

        if len(window_title) <= 3:
            return False

        lower_title = window_title.lower()

        # Ignorer les fenêtres déjà détectées récemment
        now = time.time()
        last_seen = self.detected_windows.get(lower_title)
        if last_seen and (now - last_seen) < self.detection_cooldown:
            if self.debug_mode:
                self.log(f"⏳ Fenêtre ignorée (cooldown): {window_title}")
            return False

        # Chercher les fenêtres "Save As"
        save_keywords = ["wants to save", "save as", "enregistrer"]

        is_save_window = False
        for keyword in save_keywords:
            if keyword in lower_title:
                is_save_window = True
                break

        if not is_save_window:
            return False

        # Ignorer les fenêtres d'applications qui ne sont PAS des "Save As"
        ignore_keywords = [
            "bot - windsurf",         # Windsurf IDE
            "visual studio code",     # VS Code
            "notepad",               # Bloc-notes
            "chrome",                # Chrome (sauf "wants to save")
            "firefox",               # Firefox
            "explorer",              # Explorateur Windows
            "cmd",                   # Invite de commandes
            "powershell",            # PowerShell
            "python",                # Python
            "discord",               # Discord
            "spotify",               # Spotify
            "recent download history", # Historique Chrome
            "downloads",             # Fenêtre de téléchargements
            "history",               # Historique
            "settings",              # Paramètres
            "preferences",           # Préférences
            "options",               # Options
            "about:",                # Pages about:
            "chrome://",             # Pages internes Chrome
            "data:",                 # Data URLs
        ]

        for ignore in ignore_keywords:
            if ignore in lower_title:
                # Exception: Chrome avec "wants to save" est valide
                if "chrome" in ignore and "wants to save" in lower_title:
                    continue
                # Exception: Extensions Chrome avec mots-clés de sauvegarde
                if "extension" in lower_title and is_save_window:
                    continue
                if self.debug_mode:
                    self.log(f"⏭️ Fenêtre ignorée (blacklist): {window_title}")
                return False

        return True

    def _on_window_detected(self, window_title: str):
        """Appelé quand une fenêtre "Enregistrer sous" est détectée."""
        # Cooldown de 10 secondes pour éviter les détections multiples
        current_time = time.time()
        self.detected_windows[window_title.lower()] = current_time
        if hasattr(self, 'last_detection_time') and current_time - self.last_detection_time < 10:
            if self.debug_mode:
                self.log(f"⏳ Cooldown actif, ignoré: {window_title}")
            return

        self.last_detection_time = current_time
        self.total_detections += 1
        self.log(f"🔔 Fenêtre détectée: {window_title}")

        # Automatiser le collage et la sauvegarde si activé
        if self.auto_paste:
            self.log("⏳ Attente de 2 secondes pour que la fenêtre soit prête...")
            time.sleep(2)

            self.log("🤖 Démarrage de l'automatisation intelligente...")
            self.log(f"   - auto_paste: {self.auto_paste}")
            self.log(f"   - auto_save: {self.auto_save}")
            self.log(f"   - auto_saver avancé: {self.auto_saver is not None}")
            self.log(f"   - auto_saver simple: {self.simple_auto_saver is not None}")

            try:
                automation_done = False
                result = False

                if self.auto_saver and getattr(self.auto_saver, "available", True):
                    result = self.auto_saver.auto_save(verify_path=False, auto_click_save=self.auto_save)
                    automation_done = True
                elif self.simple_auto_saver:
                    result = self.simple_auto_saver.simple_save(auto_click_save=self.auto_save)
                    automation_done = True

                if automation_done:
                    if result:
                        self.log("✅ Automatisation terminée avec succès")
                    else:
                        self.log("⚠️ Automatisation terminée avec avertissements")
                else:
                    self.log("⚠️ Aucun automate disponible pour cette fenêtre")
            except Exception as e:
                self.log(f"❌ Erreur lors de l'automatisation: {str(e)}")
        else:
            if not self.auto_saver and not self.simple_auto_saver:
                self.log("⚠️ AutoSaver non disponible (pyautogui/pyperclip manquants)")
            if not self.auto_paste:
                self.log("⚠️ Auto-paste désactivé")

        # Appeler le callback de notification si défini
        if self.notification_callback:
            self.notification_callback(window_title)

    def is_active(self) -> bool:
        """Vérifie si le moniteur est actif."""
        return self.is_monitoring

    def set_debug_mode(self, debug: bool):
        """Active/Désactive le mode debug."""
        self.debug_mode = debug
        if debug:
            self.log("🐛 Mode debug activé - toutes les fenêtres seront affichées")

    def get_detected_count(self) -> int:
        """Retourne le nombre de fenêtres détectées."""
        return self.total_detections

    def clear_history(self):
        """Efface l'historique des fenêtres détectées."""
        self.detected_windows.clear()
        self.total_detections = 0
        self.log("🗑️ Historique des détections effacé")
