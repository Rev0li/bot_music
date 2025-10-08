#!/usr/bin/env python3
"""
Debug du workflow complet pour identifier où ça bloque.
"""

import time
from music_organizer.monitor import DownloadMonitor

def debug_workflow():
    """Debug le workflow étape par étape."""
    print("🔍 Debug du Workflow Complet")
    print("=" * 50)
    
    print("📋 Checklist du Workflow:")
    print("1. ✅ Extension Chrome installée")
    print("2. ✅ Extension génère le nom de fichier") 
    print("3. ✅ Nom copié dans le clipboard")
    print("4. ❓ Y2Mate s'ouvre et convertit")
    print("5. ❓ Téléchargement démarre")
    print("6. ❓ Fenêtre 'Save As' s'ouvre")
    print("7. ❓ Bot détecte la fenêtre")
    print("8. ❓ Bot active Brave et colle")
    
    print("\n🧪 Test de Détection en Temps Réel")
    print("=" * 40)
    
    def log_callback(message):
        print(f"[{time.strftime('%H:%M:%S')}] {message}")
    
    def notification_callback(window_title):
        print(f"🔔 DÉTECTION: {window_title}")
    
    # Créer le monitor avec debug
    monitor = DownloadMonitor(
        notification_callback=notification_callback,
        log_callback=log_callback,
        auto_paste=False,  # Pas d'automatisation pour le debug
        auto_save=False
    )
    
    # Activer le mode debug
    monitor.set_debug_mode(True)
    
    print("📋 Instructions:")
    print("1. Le scanner va démarrer en mode debug")
    print("2. Allez sur YouTube Music")
    print("3. Cliquez sur 'Auto Share V2' sur une chanson")
    print("4. Observez les logs ici")
    print("5. Appuyez sur Ctrl+C pour arrêter")
    
    input("\nAppuyez sur Entrée pour démarrer le scanner...")
    
    try:
        monitor.start()
        print("🚀 Scanner démarré - Observez les fenêtres détectées...")
        
        # Attendre indéfiniment
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du scanner...")
        monitor.stop()
        print("✅ Scanner arrêté")

def test_clipboard():
    """Test le contenu du clipboard."""
    print("\n🧪 Test du Clipboard")
    print("=" * 30)
    
    try:
        import pyperclip
        content = pyperclip.paste()
        print(f"📋 Contenu actuel du clipboard:")
        print(f"   '{content}'")
        
        if "art=" in content and "N=" in content:
            print("✅ Format correct détecté!")
        else:
            print("⚠️ Format incorrect ou clipboard vide")
            print("💡 Testez l'extension Chrome d'abord")
            
    except ImportError:
        print("❌ pyperclip non disponible")

def main():
    """Menu principal."""
    print("🎯 Debug Workflow - Identifier le Problème")
    print("=" * 60)
    print("1. Test clipboard (vérifier l'extension)")
    print("2. Debug workflow complet")
    print("3. Les deux")
    print("4. Quitter")
    
    choice = input("\nChoisissez une option (1-4): ").strip()
    
    if choice == "1":
        test_clipboard()
    elif choice == "2":
        debug_workflow()
    elif choice == "3":
        test_clipboard()
        debug_workflow()
    elif choice == "4":
        print("👋 Au revoir!")
    else:
        print("❌ Option invalide")

if __name__ == "__main__":
    main()
