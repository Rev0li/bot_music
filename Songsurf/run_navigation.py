#!/usr/bin/env python3
"""
Point d'entrée pour Songsurf avec navigation
"""
import sys
import os

# Ajouter le répertoire racine au path
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from app.main_navigation import main
    if __name__ == "__main__":
        exit_code = main()
        sys.exit(exit_code)
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assurez-vous que tous les fichiers sont présents dans le dossier Songsurf/")
    sys.exit(1)
