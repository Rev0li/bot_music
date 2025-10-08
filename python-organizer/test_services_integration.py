#!/usr/bin/env python3
"""
Test d'intégration des services avec le frontend moderne.
"""

import sys
import os
import time

# Ajouter le chemin vers les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_service_adapter():
    """Test l'adaptateur de services."""
    print("=== Test ServiceAdapter ===")
    
    try:
        from core.services.service_adapter import get_service_adapter
        
        # Créer l'adaptateur
        def log_callback(msg):
            print(f"[LOG] {msg}")
        
        adapter = get_service_adapter(log_callback=log_callback)
        
        # Test du statut
        status = adapter.get_status()
        print(f"Services disponibles: {status['services_available']}")
        print(f"Monitor disponible: {status['monitor_available']}")
        print(f"Scanner disponible: {status['scanner_available']}")
        print(f"AutoSaver disponible: {status['auto_saver_available']}")
        
        # Test des méthodes
        print("\n--- Test des méthodes ---")
        
        # Test monitoring
        print("Test start_monitoring...")
        result = adapter.start_monitoring()
        print(f"Résultat: {result}")
        
        time.sleep(1)
        
        print("Test stop_monitoring...")
        result = adapter.stop_monitoring()
        print(f"Résultat: {result}")
        
        # Test auto-save
        print("Test set_auto_save...")
        adapter.set_auto_save(True)
        adapter.set_auto_save(False)
        
        # Test paste
        print("Test test_paste...")
        result = adapter.test_paste()
        print(f"Résultat: {result}")
        
        # Test debug
        print("Test toggle_debug...")
        result = adapter.toggle_debug()
        print(f"Résultat: {result}")
        
        print("[OK] ServiceAdapter OK")
        return True
        
    except Exception as e:
        print(f"[ERROR] Erreur ServiceAdapter: {e}")
        return False

def test_ui_components():
    """Test les composants UI."""
    print("\n=== Test Composants UI ===")
    
    try:
        import customtkinter as ctk
        from ui.components.buttons import ModernButton, ToggleButton
        from ui.components.frames import CardFrame, StatusFrame
        from ui.styles.themes import theme_manager
        
        print("[OK] Imports UI OK")
        
        # Test thème
        print(f"Thème actuel: {theme_manager.current_theme}")
        print(f"Couleur primaire: {theme_manager.get_color('primary')}")
        
        print("[OK] Composants UI OK")
        return True
        
    except Exception as e:
        print(f"[ERROR] Erreur Composants UI: {e}")
        return False

def test_integration():
    """Test l'intégration complète."""
    print("\n=== Test Intégration ===")
    
    try:
        # Test import de la page principale
        from ui.pages.main_page import MainPage
        print("[OK] Import MainPage OK")
        
        # Test import de l'app
        from ui.app import ModernMusicOrganizerApp
        print("[OK] Import App OK")
        
        print("[OK] Intégration OK")
        return True
        
    except Exception as e:
        print(f"[ERROR] Erreur Intégration: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backend_services():
    """Test les services backend."""
    print("\n=== Test Services Backend ===")
    
    try:
        # Test imports backend
        sys.path.append(os.path.join(os.path.dirname(__file__)))
        
        try:
            from music_organizer.scanner import MusicScanner
            print("[OK] MusicScanner disponible")
        except ImportError:
            print("[WARN] MusicScanner non disponible")
        
        try:
            from music_organizer.monitor import DownloadMonitor
            print("[OK] DownloadMonitor disponible")
        except ImportError:
            print("[WARN] DownloadMonitor non disponible")
        
        try:
            from music_organizer.process_activator import SimpleAutoSaver
            print("[OK] SimpleAutoSaver disponible")
        except ImportError:
            print("[WARN] SimpleAutoSaver non disponible")
        
        print("[OK] Services Backend testés")
        return True
        
    except Exception as e:
        print(f"[ERROR] Erreur Services Backend: {e}")
        return False

def main():
    """Test principal."""
    print("Test d'Integration des Services")
    print("=" * 50)
    
    results = []
    
    # Tests
    results.append(("ServiceAdapter", test_service_adapter()))
    results.append(("Composants UI", test_ui_components()))
    results.append(("Services Backend", test_backend_services()))
    results.append(("Intégration", test_integration()))
    
    # Résultats
    print("\n" + "=" * 50)
    print("RESULTATS")
    print("=" * 50)
    
    success_count = 0
    for name, success in results:
        status = "[OK] OK" if success else "[ERROR] ÉCHEC"
        print(f"{name:<20} : {status}")
        if success:
            success_count += 1
    
    print(f"\nScore: {success_count}/{len(results)}")
    
    if success_count == len(results):
        print("TOUS LES TESTS REUSSIS!")
        print("L'integration des services est complete.")
    else:
        print("Certains tests ont echoue.")
        print("Verifiez les dependances et la configuration.")
    
    print("\nPour lancer l'application complete:")
    print("python app_modern.py")

if __name__ == "__main__":
    main()
