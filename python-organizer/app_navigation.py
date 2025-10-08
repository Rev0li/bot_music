#!/usr/bin/env python3
"""
app_navigation_launcher.py - Lanceur pour la version avec navigation par catégories
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from ui.app_navigation import main
    
    if __name__ == "__main__":
        print("Lancement de Music Organizer Pro - Navigation Edition")
        print("Interface avec navigation par categories (Download/Organize)")
        print("=" * 70)
        main()
        
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assurez-vous que CustomTkinter est installe: pip install customtkinter")
    sys.exit(1)
except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
