#!/usr/bin/env python3
"""
Script de test pour les notifications intelligentes.
"""

import time
from music_organizer.notification_helper import SmartNotifier, test_notification
from music_organizer.auto_saver import AutoSaver

def test_smart_auto_save():
    """Test l'auto-save intelligent avec notifications."""
    print("🧪 Test Smart Auto-Save avec Notifications")
    print("=" * 60)
    
    # Créer l'auto-saver
    saver = AutoSaver()
    
    print("📋 Instructions:")
    print("1. Ouvrez Chrome et téléchargez un fichier")
    print("2. Quand la fenêtre 'Save As' s'ouvre, revenez ici")
    print("3. Appuyez sur Entrée pour tester l'automatisation intelligente")
    print("4. Suivez les notifications qui apparaîtront")
    
    input("\nAppuyez sur Entrée quand la fenêtre 'Save As' est ouverte...")
    
    print("\n🧠 Démarrage de l'automatisation intelligente...")
    
    # Tester la méthode intelligente
    result = saver.smart_auto_save(verify_path=True, auto_click_save=False)
    
    if result:
        print("✅ SUCCESS: Automatisation intelligente réussie!")
        print("💡 Les notifications ont guidé l'utilisateur")
    else:
        print("❌ FAILED: Problème avec l'automatisation")
    
    return result

def test_notifications_only():
    """Test seulement les notifications."""
    print("🧪 Test des Notifications Seules")
    print("=" * 40)
    
    print("Ceci va tester les différents types de notifications...")
    input("Appuyez sur Entrée pour commencer...")
    
    test_notification()

def main():
    """Menu principal."""
    print("🎯 Test des Fonctionnalités Intelligentes")
    print("=" * 50)
    print("1. Test complet (Smart Auto-Save)")
    print("2. Test notifications seulement")
    print("3. Quitter")
    
    choice = input("\nChoisissez une option (1-3): ").strip()
    
    if choice == "1":
        test_smart_auto_save()
    elif choice == "2":
        test_notifications_only()
    elif choice == "3":
        print("👋 Au revoir!")
    else:
        print("❌ Option invalide")

if __name__ == "__main__":
    main()
