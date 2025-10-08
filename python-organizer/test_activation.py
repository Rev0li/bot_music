#!/usr/bin/env python3
"""
Script de test pour vérifier l'activation de fenêtre améliorée.
"""

import time
from music_organizer.auto_saver import AutoSaver

def test_window_activation():
    """Test l'activation de fenêtre."""
    print("🧪 Test d'activation de fenêtre")
    print("=" * 50)
    
    # Créer l'auto-saver
    saver = AutoSaver()
    
    print("📋 Instructions:")
    print("1. Ouvrez Chrome")
    print("2. Téléchargez un fichier pour ouvrir 'Save As'")
    print("3. Cliquez ailleurs (sur cette fenêtre par exemple)")
    print("4. Appuyez sur Entrée ici pour tester l'activation")
    
    input("Appuyez sur Entrée quand la fenêtre 'Save As' est ouverte...")
    
    print("\n🎯 Test de l'activation...")
    result = saver.activate_save_window()
    
    if result:
        print("✅ SUCCESS: Fenêtre activée!")
        print("💡 La fenêtre 'Save As' devrait maintenant être au premier plan")
    else:
        print("❌ FAILED: Impossible d'activer la fenêtre")
        print("💡 Vérifiez qu'une fenêtre 'Save As' est ouverte")
    
    return result

if __name__ == "__main__":
    test_window_activation()
