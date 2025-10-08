#!/usr/bin/env python3
"""
Script de test pour l'activation par processus.
"""

import time
from music_organizer.process_activator import ProcessActivator, SimpleAutoSaver

def test_process_detection():
    """Test la détection des processus de navigateur."""
    print("🧪 Test Détection des Processus")
    print("=" * 50)
    
    activator = ProcessActivator()
    
    print("🔍 Recherche des navigateurs en cours...")
    
    # Tester chaque navigateur
    browsers = ["brave.exe", "chrome.exe", "msedge.exe", "firefox.exe"]
    
    for browser in browsers:
        found = activator._activate_process_by_name(browser)
        status = "✅ TROUVÉ" if found else "❌ Non trouvé"
        print(f"   {browser}: {status}")
    
    print("\n🔍 Recherche par fenêtre...")
    browser_window = activator._find_browser_window()
    if browser_window:
        hwnd, title = browser_window
        print(f"✅ Fenêtre navigateur trouvée: {title}")
    else:
        print("❌ Aucune fenêtre navigateur trouvée")

def test_simple_activation():
    """Test l'activation simple."""
    print("\n🧪 Test Activation Simple")
    print("=" * 40)
    
    print("📋 Instructions:")
    print("1. Ouvrez Brave/Chrome")
    print("2. Allez sur n'importe quelle page")
    print("3. Cliquez sur cette fenêtre (pour la désactiver)")
    print("4. Appuyez sur Entrée pour tester l'activation")
    
    input("\nAppuyez sur Entrée pour tester...")
    
    activator = ProcessActivator()
    result = activator._activate_browser_process()
    
    if result:
        print("✅ SUCCESS: Navigateur activé!")
        print("💡 Le navigateur devrait maintenant être au premier plan")
    else:
        print("❌ FAILED: Impossible d'activer le navigateur")

def test_full_workflow():
    """Test le workflow complet."""
    print("\n🧪 Test Workflow Complet")
    print("=" * 40)
    
    print("📋 Instructions:")
    print("1. Copiez du texte dans le clipboard (Ctrl+C)")
    print("2. Ouvrez Brave/Chrome et téléchargez un fichier")
    print("3. Quand 'Save As' s'ouvre, revenez ici")
    print("4. Le bot va activer Brave et coller le texte")
    
    input("\nAppuyez sur Entrée pour tester...")
    
    saver = SimpleAutoSaver()
    result = saver.simple_save()
    
    if result:
        print("✅ SUCCESS: Workflow complet réussi!")
    else:
        print("❌ FAILED: Problème dans le workflow")

def main():
    """Menu principal."""
    print("🎯 Test Activation par Processus")
    print("=" * 50)
    print("1. Test détection des processus")
    print("2. Test activation simple")
    print("3. Test workflow complet")
    print("4. Tout tester")
    print("5. Quitter")
    
    choice = input("\nChoisissez une option (1-5): ").strip()
    
    if choice == "1":
        test_process_detection()
    elif choice == "2":
        test_simple_activation()
    elif choice == "3":
        test_full_workflow()
    elif choice == "4":
        test_process_detection()
        test_simple_activation()
        test_full_workflow()
    elif choice == "5":
        print("👋 Au revoir!")
    else:
        print("❌ Option invalide")

if __name__ == "__main__":
    main()
