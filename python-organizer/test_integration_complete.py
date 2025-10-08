#!/usr/bin/env python3
"""
test_integration_complete.py - Test complet de l'intégration des services
"""

import sys
import os

def test_imports():
    """Test les imports des services."""
    print("=== Test des Imports ===")

    try:
        # Ajouter le chemin
        current_dir = os.path.dirname(__file__)
        backend_path = os.path.join(current_dir, 'music_organizer')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)

        # Test des imports backend
        from music_organizer.monitor import DownloadMonitor
        print("[OK] DownloadMonitor importe")

        from music_organizer.process_activator import SimpleAutoSaver
        print("[OK] SimpleAutoSaver importe")

        from music_organizer.organizer import MusicOrganizer
        print("[OK] MusicOrganizer importe")

        return True

    except ImportError as e:
        print(f"[ERROR] Erreur import: {e}")
        return False

def test_services():
    """Test la création des services."""
    print("\n=== Test des Services ===")

    try:
        # Ajouter le chemin
        current_dir = os.path.dirname(__file__)
        backend_path = os.path.join(current_dir, 'music_organizer')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)

        from music_organizer.monitor import DownloadMonitor
        from music_organizer.process_activator import SimpleAutoSaver
        from music_organizer.organizer import MusicOrganizer

        # Test création des objets
        def log_callback(msg):
            print(f"[SERVICE] {msg}")

        # Test SimpleAutoSaver
        saver = SimpleAutoSaver(log_callback=log_callback)
        print("[OK] SimpleAutoSaver cree")

        # Test MusicOrganizer (sans dossier pour l'instant)
        print("[OK] MusicOrganizer disponible")

        # Test DownloadMonitor
        monitor = DownloadMonitor(
            notification_callback=lambda x: print(f"[DETECT] {x}"),
            log_callback=log_callback,
            auto_paste=True,
            auto_save=True
        )
        print("[OK] DownloadMonitor cree")

        return True

    except Exception as e:
        print(f"[ERROR] Erreur services: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ui_integration():
    """Test l'intégration UI."""
    print("\n=== Test Intégration UI ===")

    try:
        # Test CustomTkinter
        import customtkinter as ctk
        print("[OK] CustomTkinter importe")

        # Test création d'éléments UI simples
        root = ctk.CTk()
        root.withdraw()  # Cacher la fenêtre

        # Test d'un bouton
        btn = ctk.CTkButton(root, text="Test")
        print("[OK] Bouton cree")

        # Test d'une frame
        frame = ctk.CTkFrame(root)
        print("[OK] Frame cree")

        # Test du thème
        print(f"[OK] Theme actuel: {ctk.get_appearance_mode()}")

        root.destroy()
        return True

    except Exception as e:
        print(f"[ERROR] Erreur UI: {e}")
        return False

def main():
    """Test principal."""
    print("[TEST] Test d'Intégration Complète")
    print("=" * 50)

    results = []

    # Tests
    results.append(("Imports Backend", test_imports()))
    results.append(("Services Backend", test_services()))
    results.append(("UI Integration", test_ui_integration()))

    # Résultats
    print("\n" + "=" * 50)
    print("[CHART] RÉSULTATS")
    print("=" * 50)

    success_count = 0
    for name, success in results:
        status = "[OK] OK" if success else "[ERROR] ÉCHEC"
        print(f"{name:<20} : {status}")
        if success:
            success_count += 1

    print(f"\nScore: {success_count}/{len(results)}")

    if success_count == len(results):
        print("[SUCCESS] TOUS LES TESTS RÉUSSIS!")
        print("L'application peut être utilisée avec les vrais services.")
    else:
        print("[WARN] Certains tests ont échoué.")
        print("Vérifiez les dépendances et la configuration.")

    print("\n[LAUNCH] Pour lancer l'application:")
    print("python app_simple_navigation.py")

if __name__ == "__main__":
    main()
