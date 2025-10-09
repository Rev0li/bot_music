#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
save_as_handler.py - Détection et automatisation de la fenêtre "Save As"

FONCTIONNALITÉ:
  - Détecte la fenêtre "Enregistrer sous" / "Save As"
  - Remplit automatiquement le nom de fichier
  - Change le dossier de destination
  - Clique sur "Enregistrer"
  
UTILISATION:
  from save_as_handler import SaveAsHandler
  
  handler = SaveAsHandler()
  success = handler.wait_and_fill(
      filename="art=Ren N=Hi Ren.mp3",
      target_folder="C:\\Users\\...\\a_trier"
  )
"""

import time
import os
import ctypes
import threading
from pathlib import Path
from datetime import datetime

try:
    from pywinauto import Desktop, Application
    from pywinauto.findwindows import find_windows
    from pywinauto.keyboard import send_keys
    import win32gui
    import win32con
    import win32process
    import psutil
    PYWINAUTO_AVAILABLE = True
except ImportError:
    PYWINAUTO_AVAILABLE = False
    print("⚠️ pywinauto non installé. Installez avec: pip install pywinauto pywin32 psutil")

class InputBlocker:
    """Gère le blocage temporaire du clavier/souris"""
    
    def __init__(self, timeout=3):
        self.timeout = timeout
        self.blocked = False
        self._timer = None
    
    def block(self):
        """Bloque les inputs avec timeout de sécurité"""
        try:
            ctypes.windll.user32.BlockInput(True)
            self.blocked = True
            print(f"🔒 Clavier/souris bloqués ({self.timeout}s)")
            
            # Timer de sécurité pour débloquer automatiquement
            self._timer = threading.Timer(self.timeout, self._auto_unblock)
            self._timer.start()
        except Exception as e:
            print(f"⚠️ Impossible de bloquer les inputs: {e}")
    
    def unblock(self):
        """Débloque les inputs"""
        if self._timer:
            self._timer.cancel()
        
        if self.blocked:
            try:
                ctypes.windll.user32.BlockInput(False)
                self.blocked = False
                print("🔓 Clavier/souris débloqués")
            except Exception as e:
                print(f"⚠️ Erreur déblocage: {e}")
    
    def _auto_unblock(self):
        """Déblocage automatique de sécurité"""
        print("⏰ Déblocage automatique (timeout)")
        self.unblock()
    
    def __enter__(self):
        self.block()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unblock()


class SaveAsHandler:
    """
    Gestionnaire de la fenêtre "Save As" / "Enregistrer sous"
    """
    
    def __init__(self):
        """Initialise le handler"""
        if not PYWINAUTO_AVAILABLE:
            raise ImportError("pywinauto n'est pas installé")
        
        self.window = None
        self.app = None
        self._saved_clipboard = None
        
        # Mots-clés à chercher dans le titre (n'importe où)
        self.window_keywords = [
            "wants to save",      # Fenêtre de téléchargement navigateur (ex: "* wants to save")
            "save as",            # Fenêtre Save As standard
            "enregistrer sous",   # Version française
            "enregistrer",        # Version courte
        ]
        
        # Mémoriser les fenêtres existantes pour les ignorer
        self.existing_windows = set()
        self._scan_existing_windows()
        
        print("✅ SaveAsHandler initialisé")
    
    def _get_browser_pids(self):
        """
        Récupère les PIDs des processus navigateurs (Chrome, Edge, Firefox)
        
        Returns:
            list: Liste des PIDs des navigateurs
        """
        browser_names = ['chrome.exe', 'msedge.exe', 'firefox.exe', 'brave.exe', 'opera.exe']
        pids = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() in browser_names:
                    pids.append(proc.info['pid'])
        except Exception as e:
            print(f"⚠️ Erreur lors de la recherche des navigateurs: {e}")
        
        return pids
    
    def _save_clipboard(self):
        """Sauvegarde le contenu actuel du clipboard"""
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            try:
                self._saved_clipboard = win32clipboard.GetClipboardData()
            except:
                self._saved_clipboard = None
            win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"⚠️ Impossible de sauvegarder le clipboard: {e}")
            self._saved_clipboard = None
    
    def _restore_clipboard(self):
        """Restaure le contenu du clipboard"""
        if self._saved_clipboard is not None:
            try:
                import win32clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(self._saved_clipboard)
                win32clipboard.CloseClipboard()
            except Exception as e:
                print(f"⚠️ Impossible de restaurer le clipboard: {e}")
    
    def _set_clipboard(self, text):
        """Met un texte dans le clipboard"""
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text)
            win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"❌ Erreur clipboard: {e}")
            raise
    
    def _scan_existing_windows(self):
        """Scanne et mémorise les fenêtres existantes pour les ignorer"""
        try:
            all_windows = Desktop(backend="uia").windows()
            for window in all_windows:
                try:
                    window_title = window.window_text()
                    # Mémoriser les fenêtres "Save As" déjà ouvertes
                    for keyword in self.window_keywords:
                        if keyword.lower() in window_title.lower():
                            window_handle = window.handle
                            self.existing_windows.add(window_handle)
                            print(f"⚠️ Fenêtre existante ignorée: '{window_title}'")
                except Exception:
                    continue
        except Exception:
            pass
    
    def find_save_as_window(self, timeout=60):
        """
        Cherche la fenêtre "Save As" / "Enregistrer sous"
        
        Args:
            timeout (int): Temps d'attente maximum en secondes
            
        Returns:
            window: Fenêtre trouvée ou None
        """
        print(f"🔍 Recherche de la fenêtre 'Save As' (timeout: {timeout}s)...")
        
        start_time = time.time()
        last_print = 0
        
        while time.time() - start_time < timeout:
            elapsed = int(time.time() - start_time)
            
            # Afficher un point toutes les 10 secondes
            if elapsed > last_print and elapsed % 10 == 0:
                print(f"   ⏳ Toujours en attente... ({elapsed}s / {timeout}s)")
                last_print = elapsed
            
            try:
                # Méthode win32gui: Énumérer toutes les fenêtres
                def enum_windows_callback(hwnd, results):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if title:
                            results.append((hwnd, title))
                
                win32_windows = []
                win32gui.EnumWindows(enum_windows_callback, win32_windows)
                
                # Vérifier les fenêtres
                for hwnd, title in win32_windows:
                    # Ignorer les fenêtres existantes
                    if hwnd in self.existing_windows:
                        continue
                    
                    # Vérifier si le titre correspond
                    for keyword in self.window_keywords:
                        if keyword.lower() in title.lower():
                            print(f"✅ Nouvelle fenêtre trouvée: '{title}'")
                            
                            # Créer un wrapper pywinauto pour cette fenêtre
                            try:
                                from pywinauto.application import Application
                                app = Application(backend="win32").connect(handle=hwnd)
                                self.window = app.window(handle=hwnd)
                                return self.window
                            except Exception as e:
                                print(f"⚠️ Impossible de créer un wrapper: {e}")
                
                # Attendre un peu avant de réessayer
                time.sleep(0.5)
                
            except Exception as e:
                print(f"⚠️ Erreur lors de la recherche: {e}")
                time.sleep(1)
        
        print(f"❌ Fenêtre 'Save As' non trouvée après {timeout}s")
        return None
    
    def fill_filename(self, filename):
        """
        Remplit le champ "Nom du fichier" via clipboard (rapide)
        
        Args:
            filename (str): Nom du fichier à sauvegarder
            
        Returns:
            bool: True si succès
        """
        try:
            print(f"📝 Remplissage du nom de fichier: {filename}")
            
            # Mettre le filename dans le clipboard
            self._set_clipboard(filename)
            
            # Focus et coller
            self.window.set_focus()
            time.sleep(0.1)
            
            # Sélectionner tout et coller
            send_keys("^a")
            time.sleep(0.05)
            send_keys("^v")
            time.sleep(0.1)
            
            print("✅ Nom de fichier rempli (collé)")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du remplissage: {e}")
            return False
    
    def change_folder(self, target_folder):
        """
        Change le dossier de destination via clipboard (rapide)
        
        Args:
            target_folder (str): Chemin du dossier cible
            
        Returns:
            bool: True si succès
        """
        try:
            print(f"📁 Changement de dossier vers: {target_folder}")
            
            # Mettre le path dans le clipboard
            self._set_clipboard(target_folder)
            
            # Focus
            self.window.set_focus()
            time.sleep(0.1)
            
            # Aller à la barre d'adresse et coller
            send_keys("^l")
            time.sleep(0.1)
            send_keys("^v")
            time.sleep(0.1)
            
            # Entrée pour valider le changement de dossier
            send_keys("{ENTER}")
            time.sleep(0.3)
            
            print("✅ Dossier changé (collé)")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du changement de dossier: {e}")
            return False
    
    def click_save(self):
        """
        Valide la sauvegarde - Deuxième Entrée
        
        Returns:
            bool: True si succès
        """
        try:
            print("💾 Validation finale (Entrée)...")
            
            # Deuxième Entrée pour valider le Save
            # self.window.set_focus()
            # time.sleep(0.3)
            send_keys("{ENTER}")
            time.sleep(0.5)
            
            print("✅ Sauvegarde validée")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la validation: {e}")
            return False
    
    def wait_for_file_download(self, filename, target_folder, timeout=60):
        """
        Attend qu'un nouveau fichier MP3 apparaisse dans le dossier
        
        Args:
            filename (str): Nom du fichier attendu (depuis le JSON)
            target_folder (str): Dossier où le fichier doit apparaître
            timeout (int): Temps d'attente maximum
            
        Returns:
            dict: Informations sur le fichier trouvé ou None
        """
        print(f"\n⏳ Attente d'un nouveau fichier MP3...")
        print(f"📁 Dans: {target_folder}")
        print(f"🔍 Fichier attendu (JSON): {filename}")
        
        target_path = Path(target_folder)
        start_time = time.time()
        
        # Fonction pour nettoyer les noms de fichiers
        def clean_filename(name):
            """Nettoie le nom pour la comparaison"""
            name = name.replace('.mp3', '').lower()
            # Supprimer les caractères que le navigateur peut enlever
            for char in ['(', ')', '[', ']', '{', '}', ' ']:
                name = name.replace(char, '')
            return name
        
        expected_clean = clean_filename(filename)
        
        # Lister les fichiers MP3 existants au départ avec leur date de modification
        existing_files = {}
        if target_path.exists():
            for f in target_path.glob('*.mp3'):
                existing_files[f.name] = f.stat().st_mtime
            print(f"📊 Fichiers MP3 existants: {len(existing_files)}")
            
            # Vérifier si le fichier attendu existe déjà
            for fname in existing_files.keys():
                actual_clean = clean_filename(fname)
                if expected_clean == actual_clean:
                    print(f"✅ Le fichier existe déjà et correspond au JSON: {fname}")
                    file_path = target_path / fname
                    try:
                        file_size = file_path.stat().st_size
                        print(f"📊 Taille: {file_size / 1024 / 1024:.2f} MB")
                        return {
                            'success': True,
                            'filename': fname,
                            'path': str(target_path),
                            'size': file_size
                        }
                    except Exception as e:
                        print(f"⚠️ Erreur: {e}")
            
            if existing_files:
                print(f"   Fichiers ignorés (ne correspondent pas):")
                for fname in existing_files.keys():
                    print(f"   - {fname}")
        
        last_check = 0
        
        while time.time() - start_time < timeout:
            elapsed = int(time.time() - start_time)
            
            # Afficher un point toutes les 5 secondes
            if elapsed > last_check and elapsed % 5 == 0:
                print(f"   ... toujours en attente ({elapsed}s / {timeout}s)")
                last_check = elapsed
            
            # Vérifier les nouveaux fichiers MP3 ou fichiers modifiés récemment
            if target_path.exists():
                current_files = {}
                for f in target_path.glob('*.mp3'):
                    current_files[f.name] = f.stat().st_mtime
                
                # Debug: Afficher tous les fichiers trouvés toutes les 10 secondes
                if elapsed % 10 == 0 and elapsed > 0:
                    print(f"   📋 Fichiers actuels dans a_trier: {len(current_files)}")
                    for fname in current_files.keys():
                        print(f"      - {fname}")
                
                # Chercher les nouveaux fichiers ou fichiers modifiés après le début
                for file_name, mtime in current_files.items():
                    # Nouveau fichier OU fichier modifié après le début de la surveillance
                    is_new = file_name not in existing_files
                    is_modified = mtime > start_time
                    
                    if is_new or is_modified:
                        file_path = target_path / file_name
                        
                        print(f"🆕 Fichier détecté: {file_name}")
                        print(f"   Nouveau: {is_new}, Modifié récemment: {is_modified}")
                        print(f"   Date modification: {datetime.fromtimestamp(mtime).strftime('%H:%M:%S')}")
                        
                        # Vérifier que c'est bien le fichier attendu (nom similaire)
                        # Nettoyer les noms pour la comparaison (supprimer caractères spéciaux)
                        def clean_filename(name):
                            """Nettoie le nom pour la comparaison"""
                            name = name.replace('.mp3', '').lower()
                            # Supprimer les caractères que le navigateur peut enlever
                            for char in ['(', ')', '[', ']', '{', '}', ' ']:
                                name = name.replace(char, '')
                            return name
                        
                        expected_clean = clean_filename(filename)
                        actual_clean = clean_filename(file_name)
                        
                        print(f"   Comparaison:")
                        print(f"   - Attendu: {expected_clean}")
                        print(f"   - Trouvé:  {actual_clean}")
                        
                        # Vérifier si les noms correspondent (comparaison flexible)
                        if expected_clean == actual_clean or expected_clean in actual_clean or actual_clean in expected_clean:
                            print(f"✅ Le fichier correspond au JSON")
                            
                            # Attendre que la taille se stabilise (téléchargement terminé)
                            print(f"⏳ Vérification que le téléchargement est terminé...")
                            time.sleep(2)
                            
                            try:
                                initial_size = file_path.stat().st_size
                                time.sleep(2)
                                final_size = file_path.stat().st_size
                                
                                if final_size == initial_size and final_size > 0:
                                    print(f"✅ Fichier téléchargé: {file_name}")
                                    print(f"📊 Taille: {final_size / 1024 / 1024:.2f} MB")
                                    
                                    return {
                                        'success': True,
                                        'filename': file_name,
                                        'path': str(target_path),
                                        'size': final_size
                                    }
                                else:
                                    print(f"⏳ Téléchargement en cours... ({initial_size} → {final_size} bytes)")
                            except Exception as e:
                                print(f"⚠️ Erreur de vérification: {e}")
                        else:
                            print(f"⚠️ Le fichier ne correspond pas au JSON attendu")
                            print(f"   Attendu: {expected_base}")
                            print(f"   Trouvé: {actual_base}")
            
            time.sleep(1)
        
        print(f"❌ Timeout: Aucun nouveau fichier MP3 après {timeout}s")
        return None
    
    def wait_and_fill(self, filename, target_folder, timeout=60):
        """
        Attend la fenêtre "Save As" et remplit automatiquement
        
        WORKFLOW:
        1. Détecter la fenêtre
        2. Sauvegarder clipboard + Bloquer inputs (3s)
        3. Remplir filename via clipboard (Ctrl+A → Ctrl+V)
        4. Changer PATH via clipboard (Ctrl+L → Ctrl+V → Entrée)
        5. Valider (Entrée)
        6. Débloquer inputs + Restaurer clipboard
        7. Attendre la fin du téléchargement
        
        Args:
            filename (str): Nom du fichier
            target_folder (str): Dossier de destination
            timeout (int): Temps d'attente maximum
            
        Returns:
            dict: Informations sur le fichier téléchargé ou None
        """
        print("\n" + "="*50)
        print("🚀 Démarrage de l'automatisation 'Save As'")
        print("="*50)
        
        # 1. Attendre la fenêtre
        window = self.find_save_as_window(timeout)
        if not window:
            return None
        
        time.sleep(0.3)
        
        # 2. Sauvegarder le clipboard et bloquer les inputs
        self._save_clipboard()
        
        try:
            # Utiliser le context manager pour le blocage (3s max)
            with InputBlocker(timeout=3):
                # 3. Remplir le nom de fichier (via clipboard)
                if not self.fill_filename(filename):
                    print("❌ Échec du remplissage du nom de fichier")
                    return None
                
                time.sleep(0.1)
                
                # 4. Changer le dossier (via clipboard)
                if not self.change_folder(target_folder):
                    print("⚠️ Échec du changement de dossier (continuera dans Downloads)")
                
                time.sleep(0.1)
                
                # 5. Valider avec Entrée
                if not self.click_save():
                    print("❌ Échec de la validation")
                    return None
            
            # Les inputs sont automatiquement débloqués ici (sortie du context manager)
            
        finally:
            # 6. Restaurer le clipboard
            self._restore_clipboard()
        
        print("\n" + "="*50)
        print("✅ Formulaire validé - Téléchargement en cours...")
        print("="*50 + "\n")
        
        # 5. Attendre que le fichier soit téléchargé (comparer avec le filename du JSON)
        file_info = self.wait_for_file_download(filename, target_folder, timeout=120)
        
        if file_info and file_info['success']:
            print("\n" + "="*50)
            print("🎉 Téléchargement terminé avec succès!")
            print(f"📁 Fichier: {file_info['filename']}")
            print(f"📊 Taille: {file_info['size'] / 1024 / 1024:.2f} MB")
            print("="*50 + "\n")
            return file_info  # Retourner les infos du fichier
        else:
            print("\n" + "="*50)
            print("⚠️ Téléchargement non confirmé")
            print("="*50 + "\n")
            return None

# ============================================
# TEST
# ============================================

if __name__ == '__main__':
    print("🧪 Test du SaveAsHandler")
    print("="*50)
    print()
    print("Instructions:")
    print("1. Lancez ce script")
    print("2. Ouvrez une fenêtre 'Save As' manuellement")
    print("3. Le script va automatiquement la remplir")
    print()
    print("="*50)
    print()
    
    handler = SaveAsHandler()
    
    # Test avec des valeurs par défaut
    success = handler.wait_and_fill(
        filename="test_file.mp3",
        target_folder=str(Path.home() / "Downloads"),
        timeout=30
    )
    
    if success:
        print("✅ Test réussi!")
    else:
        print("❌ Test échoué")
