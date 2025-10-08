#!/usr/bin/env python3
"""
Test rapide pour vérifier que l'activation fonctionne maintenant.
"""

def test_imports():
    """Test que tous les imports fonctionnent."""
    print("🧪 Test des Imports")
    print("=" * 30)
    
    try:
        import win32gui
        print("✅ win32gui: OK")
    except ImportError:
        print("❌ win32gui: MANQUANT")
        return False
    
    try:
        import psutil
        print("✅ psutil: OK")
    except ImportError:
        print("❌ psutil: MANQUANT")
        return False
    
    try:
        from music_organizer.process_activator import ProcessActivator, SimpleAutoSaver
        print("✅ process_activator: OK")
    except ImportError as e:
        print(f"❌ process_activator: ERREUR - {e}")
        return False
    
    return True

def test_browser_detection():
    """Test la détection de navigateur."""
    print("\n🧪 Test Détection Navigateur")
    print("=" * 40)
    
    from music_organizer.process_activator import ProcessActivator
    
    activator = ProcessActivator()
    
    # Test méthode par processus
    print("🔍 Test par processus...")
    found_by_process = False
    for browser in ["brave.exe", "chrome.exe", "msedge.exe"]:
        if activator._activate_process_by_name(browser):
            print(f"✅ {browser} trouvé et activé")
            found_by_process = True
            break
    
    if not found_by_process:
        print("⚠️ Aucun navigateur trouvé par processus")
    
    # Test méthode par fenêtre
    print("🔍 Test par fenêtre...")
    browser_window = activator._find_browser_window()
    if browser_window:
        hwnd, title = browser_window
        print(f"✅ Fenêtre navigateur trouvée: {title}")
    else:
        print("⚠️ Aucune fenêtre navigateur trouvée")
    
    return found_by_process or browser_window is not None

def test_simple_saver():
    """Test le SimpleAutoSaver."""
    print("\n🧪 Test SimpleAutoSaver")
    print("=" * 30)
    
    from music_organizer.process_activator import SimpleAutoSaver
    
    saver = SimpleAutoSaver()
    print("✅ SimpleAutoSaver créé")
    
    print("📋 Pour tester complètement:")
    print("1. Ouvrez Brave/Chrome")
    print("2. Téléchargez un fichier")
    print("3. Relancez l'app Python")
    
    return True

def main():
    """Test principal."""
    print("🎯 Test Rapide - Correction Process Activator")
    print("=" * 60)
    
    # Test 1: Imports
    if not test_imports():
        print("\n❌ ÉCHEC: Problème d'imports")
        return
    
    # Test 2: Détection navigateur
    browser_ok = test_browser_detection()
    
    # Test 3: SimpleAutoSaver
    saver_ok = test_simple_saver()
    
    print("\n" + "=" * 60)
    if browser_ok and saver_ok:
        print("✅ SUCCESS: Tout semble fonctionner!")
        print("💡 Vous pouvez maintenant tester avec un vrai téléchargement")
    else:
        print("⚠️ WARNING: Certains tests ont échoué")
        print("💡 Vérifiez qu'un navigateur est ouvert")

if __name__ == "__main__":
    main()
