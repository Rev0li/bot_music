#!/usr/bin/env python3
"""
Test spécifique pour la détection de fenêtre "Save As".
"""

import time
from music_organizer.process_activator import ProcessActivator

def test_save_as_detection():
    """Test la détection de fenêtre Save As."""
    print("🧪 Test Détection Fenêtre 'Save As'")
    print("=" * 50)
    
    activator = ProcessActivator()
    
    print("📋 Instructions:")
    print("1. Ouvrez Brave/Chrome")
    print("2. Téléchargez un fichier pour ouvrir 'Save As'")
    print("3. NE FERMEZ PAS la fenêtre 'Save As'")
    print("4. Revenez ici et appuyez sur Entrée")
    
    input("\nAppuyez sur Entrée quand la fenêtre 'Save As' est ouverte...")
    
    # Test de détection
    print("\n🔍 Recherche de fenêtre 'Save As'...")
    save_window = activator._find_save_as_window()
    
    if save_window:
        hwnd, title = save_window
        print(f"✅ TROUVÉE: {title}")
        
        # Test d'activation
        print("🎯 Test d'activation...")
        try:
            import win32gui
            import win32con
            
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            print("✅ Fenêtre activée")
            
            # Test de collage
            print("📋 Test de collage dans 2 secondes...")
            time.sleep(2)
            
            import pyautogui
            pyautogui.hotkey('ctrl', 'v')
            print("✅ Ctrl+V envoyé")
            
        except Exception as e:
            print(f"❌ Erreur activation: {e}")
            
    else:
        print("❌ AUCUNE fenêtre 'Save As' trouvée")
        print("💡 Vérifiez qu'une fenêtre de téléchargement est ouverte")

def test_all_windows():
    """Affiche toutes les fenêtres pour debug."""
    print("\n🔍 Toutes les Fenêtres Visibles")
    print("=" * 40)
    
    try:
        import win32gui
        
        def enum_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:  # Ignorer les fenêtres sans titre
                    windows.append(title)
        
        windows = []
        win32gui.EnumWindows(enum_callback, windows)
        
        for i, title in enumerate(windows[:20], 1):  # Limiter à 20
            print(f"{i:2d}. {title}")
            
        print(f"\n📊 Total: {len(windows)} fenêtres")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Menu principal."""
    print("Test Detection 'Save As'")
    print("=" * 40)
    print("1. Test détection 'Save As'")
    print("2. Voir toutes les fenêtres")
    print("3. Les deux")
    print("4. Quitter")
    
    choice = input("\nChoisissez (1-4): ").strip()
    
    if choice == "1":
        test_save_as_detection()
    elif choice == "2":
        test_all_windows()
    elif choice == "3":
        test_all_windows()
        test_save_as_detection()
    elif choice == "4":
        print("👋 Au revoir!")
    else:
        print("❌ Option invalide")

if __name__ == "__main__":
    main()
