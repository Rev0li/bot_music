#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du dashboard - Vérifie que tous les fichiers sont en place
"""

import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from pathlib import Path

print("🔍 Vérification des fichiers du dashboard...\n")

# Fichiers à vérifier
files_to_check = [
    "templates/dashboard.html",
    "static/dashboard.css",
    "static/dashboard.js",
]

all_ok = True

for file_path in files_to_check:
    full_path = Path(__file__).parent / file_path
    if full_path.exists():
        size = full_path.stat().st_size
        print(f"✅ {file_path} ({size} bytes)")
    else:
        print(f"❌ {file_path} - MANQUANT")
        all_ok = False

print()

if all_ok:
    print("✅ Tous les fichiers sont présents!")
    print("\n📝 Pour lancer le dashboard:")
    print("   1. python app.py")
    print("   2. Ouvrir http://localhost:5000 dans votre navigateur")
else:
    print("❌ Certains fichiers sont manquants")

print()
