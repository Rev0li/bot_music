#!/usr/bin/env python3
"""
app_modern.py - Lanceur pour la version moderne de Music Organizer
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from ui.app import main
    
    if __name__ == "__main__":
        print("Lancement de Music Organizer Pro - Modern Edition")
        print("Interface moderne avec CustomTkinter")
        print("=" * 60)
        main()
        
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assurez-vous que CustomTkinter est installé: pip install customtkinter")
    sys.exit(1)
except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
