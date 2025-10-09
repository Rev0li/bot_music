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
from pathlib import Path
from datetime import datetime

try:
    from pywinauto import Desktop, Application
    from pywinauto.findwindows import find_windows
    from pywinauto.keyboard import send_keys
    import win32gui
    import win32con
    PYWINAUTO_AVAILABLE = True
except ImportError:
    PYWINAUTO_AVAILABLE = False
    print("⚠️ pywinauto non installé. Installez avec: pip install pywinauto pywin32")

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
        print(f"⏳ En attente... (le script ne fera rien tant qu'une fenêtre n'apparaît pas)")
        
        start_time = time.time()
        last_print = 0
        
        while time.time() - start_time < timeout:
            # Afficher un point toutes les 5 secondes pour montrer que ça tourne
            elapsed = int(time.time() - start_time)
            if elapsed > last_print and elapsed % 5 == 0:
                print(f"   ... toujours en attente ({elapsed}s / {timeout}s)")
                last_print = elapsed
            try:
                # Chercher toutes les fenêtres avec les deux backends
                all_windows = []
                
                # Backend UIA (moderne)
                try:
                    all_windows.extend(Desktop(backend="uia").windows())
                except Exception:
                    pass
                
                # Backend Win32 (classique - souvent meilleur pour les dialogues)
                try:
                    all_windows.extend(Desktop(backend="win32").windows())
                except Exception:
                    pass
                
                # Méthode alternative: Énumérer toutes les fenêtres avec win32gui
                def enum_windows_callback(hwnd, results):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if title:
                            results.append((hwnd, title))
                
                win32_windows = []
                try:
                    win32gui.EnumWindows(enum_windows_callback, win32_windows)
                except Exception:
                    pass
                
                # Debug: Afficher le nombre de fenêtres toutes les 20 secondes
                if elapsed % 20 == 0 and elapsed > 0:
                    print(f"   📊 Fenêtres scannées: {len(all_windows)} (pywinauto) + {len(win32_windows)} (win32gui)")
                
                new_windows_found = []
                
                for window in all_windows:
                    try:
                        window_title = window.window_text()
                        window_handle = window.handle
                        
                        # Ignorer les fenêtres existantes
                        if window_handle in self.existing_windows:
                            continue
                        
                        # C'est une nouvelle fenêtre
                        if window_title and len(window_title) > 0:
                            new_windows_found.append(window_title)
                        
                        # Vérifier si le titre correspond
                        for keyword in self.window_keywords:
                            if keyword.lower() in window_title.lower():
                                print(f"✅ Nouvelle fenêtre trouvée: '{window_title}'")
                                self.window = window
                                return window
                                
                    except Exception:
                        continue
                
                # Vérifier aussi les fenêtres win32gui
                for hwnd, title in win32_windows:
                    if hwnd not in self.existing_windows:
                        if title:
                            new_windows_found.append(title)
                        
                        # Vérifier si le titre correspond
                        for keyword in self.window_keywords:
                            if keyword.lower() in title.lower():
                                print(f"✅ Nouvelle fenêtre trouvée (win32gui): '{title}'")
                                # Créer un wrapper pywinauto pour cette fenêtre
                                try:
                                    from pywinauto.application import Application
                                    app = Application(backend="win32").connect(handle=hwnd)
                                    self.window = app.window(handle=hwnd)
                                    return self.window
                                except:
                                    print(f"⚠️ Impossible de créer un wrapper pour cette fenêtre")
                
                # Debug: Afficher les nouvelles fenêtres toutes les 20 secondes (si beaucoup)
                if elapsed % 20 == 0 and elapsed > 0 and len(new_windows_found) > 5:
                    print(f"   🆕 {len(new_windows_found)} nouvelles fenêtres détectées")
                
                # Attendre un peu avant de réessayer
                time.sleep(0.5)
                
            except Exception as e:
                print(f"⚠️ Erreur lors de la recherche: {e}")
                time.sleep(1)
        
        print(f"❌ Fenêtre 'Save As' non trouvée après {timeout}s")
        return None
    
    def fill_filename(self, filename):
        """
        Remplit le champ "Nom du fichier" - Méthode directe
        
        Args:
            filename (str): Nom du fichier à sauvegarder
            
        Returns:
            bool: True si succès
        """
        try:
            print(f"📝 Remplissage du nom de fichier: {filename}")
            
            # Méthode directe: On est déjà sur le champ filename par défaut
            self.window.set_focus()
            time.sleep(0.3)
            
            # Sélectionner tout
            send_keys("^a")
            time.sleep(0.2)
            
            # Taper le nouveau nom
            send_keys(filename, with_spaces=True)
            time.sleep(0.3)
            
            print("✅ Nom de fichier rempli")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du remplissage: {e}")
            return False
    
    def change_folder(self, target_folder):
        """
        Change le dossier de destination - Méthode directe
        
        Args:
            target_folder (str): Chemin du dossier cible
            
        Returns:
            bool: True si succès
        """
        try:
            print(f"📁 Changement de dossier vers: {target_folder}")
            
            # Méthode directe: Ctrl+L pour la barre d'adresse
            self.window.set_focus()
            time.sleep(0.3)
            
            # Aller à la barre d'adresse
            send_keys("^l")
            time.sleep(0.3)
            
            # Sélectionner tout et taper le chemin
            # send_keys("^a")
            # time.sleep(0.2)
            send_keys(target_folder, with_spaces=True)
            time.sleep(0.3)
            
            # Première Entrée pour valider le changement de dossier
            send_keys("{ENTER}")
            time.sleep(0.8)  # Attendre que le dossier change
            
            print("✅ Dossier changé")
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
    
    def wait_and_fill(self, filename, target_folder, timeout=60):
        """
        Attend la fenêtre "Save As" et remplit automatiquement
        
        WORKFLOW:
        1. Détecter la fenêtre
        2. Remplir le filename (Ctrl+A → Taper)
        3. Changer le PATH (Ctrl+L → Taper → Entrée)
        4. Valider (Entrée)
        
        Args:
            filename (str): Nom du fichier
            target_folder (str): Dossier de destination
            timeout (int): Temps d'attente maximum
            
        Returns:
            bool: True si succès complet
        """
        print("\n" + "="*50)
        print("🚀 Démarrage de l'automatisation 'Save As'")
        print("="*50)
        
        # 1. Attendre la fenêtre
        window = self.find_save_as_window(timeout)
        if not window:
            return False
        
        time.sleep(0.5)
        
        # 2. Remplir le nom de fichier EN PREMIER
        if not self.fill_filename(filename):
            print("❌ Échec du remplissage du nom de fichier")
            return False
        
        time.sleep(0.5)
        
        # 3. Changer le dossier
        if not self.change_folder(target_folder):
            print("⚠️ Échec du changement de dossier (continuera dans Downloads)")
        
        time.sleep(0.5)
        
        # 4. Valider avec Entrée (après le changement de PATH)
        if not self.click_save():
            print("❌ Échec de la validation")
            return False
        
        print("\n" + "="*50)
        print("🎉 Automatisation terminée avec succès!")
        print("="*50 + "\n")
        
        return True

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
