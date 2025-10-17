#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_library.py - Script pour corriger les fichiers mal organisés

UTILISATION:
    python fix_library.py
    
FONCTIONNALITÉ:
    - Scanne tous les fichiers MP3
    - Détecte les featuring mal organisés
    - Propose des corrections
    - Réorganise les fichiers
"""

from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import sys

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

from organizer import MusicOrganizer

def scan_library(music_dir):
    """Scanne la bibliothèque et trouve les problèmes"""
    music_dir = Path(music_dir)
    organizer = MusicOrganizer(music_dir)
    
    issues = []
    
    print("🔍 Scanning library for issues...")
    print("="*60)
    
    for mp3_file in music_dir.rglob('*.mp3'):
        try:
            # Lire les métadonnées
            audio = MP3(mp3_file, ID3=ID3)
            
            title = str(audio.get('TIT2', ['Unknown'])[0]) if 'TIT2' in audio else 'Unknown'
            artist = str(audio.get('TPE1', ['Unknown'])[0]) if 'TPE1' in audio else 'Unknown'
            album = str(audio.get('TALB', ['Unknown'])[0]) if 'TALB' in audio else 'Unknown'
            
            # Détecter les featuring
            feat_info = organizer.detect_featuring(title, artist)
            
            # Vérifier si le fichier est dans le bon dossier
            current_artist_folder = mp3_file.parent.parent.name
            expected_artist_folder = organizer._clean_filename(feat_info['main_artist'])
            
            if feat_info['has_feat'] and current_artist_folder != expected_artist_folder:
                issues.append({
                    'file': mp3_file,
                    'current_artist': current_artist_folder,
                    'expected_artist': expected_artist_folder,
                    'feat_artists': feat_info['feat_artists'],
                    'title': title,
                    'album': album
                })
                
        except Exception as e:
            print(f"⚠️ Error reading {mp3_file.name}: {e}")
    
    return issues


def fix_issues(issues, music_dir, dry_run=True):
    """Corrige les problèmes détectés"""
    music_dir = Path(music_dir)
    organizer = MusicOrganizer(music_dir)
    
    if not issues:
        print("\n✅ No issues found! Library is perfect.")
        return
    
    print(f"\n📋 Found {len(issues)} issue(s):")
    print("="*60)
    
    for i, issue in enumerate(issues, 1):
        print(f"\n{i}. {issue['file'].name}")
        print(f"   Current: {issue['current_artist']}/")
        print(f"   Should be: {issue['expected_artist']}/ (feat. {', '.join(issue['feat_artists'])})")
        print(f"   Album: {issue['album']}")
    
    if dry_run:
        print("\n" + "="*60)
        print("🔍 DRY RUN - No changes made")
        print("💡 Run with --fix to apply changes")
        return
    
    print("\n" + "="*60)
    confirm = input("Apply these fixes? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Cancelled")
        return
    
    print("\n🔧 Applying fixes...")
    
    for issue in issues:
        try:
            # Construire le nouveau chemin
            new_artist_dir = music_dir / issue['expected_artist']
            new_album_dir = new_artist_dir / issue['album']
            new_album_dir.mkdir(parents=True, exist_ok=True)
            
            new_path = new_album_dir / issue['file'].name
            
            # Déplacer le fichier
            issue['file'].rename(new_path)
            print(f"   ✅ Moved: {issue['file'].name}")
            
            # Nettoyer les dossiers vides
            organizer._cleanup_empty_dirs(issue['file'].parent)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ Done!")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix library organization issues')
    parser.add_argument('--music-dir', default='../music', help='Music directory path')
    parser.add_argument('--fix', action='store_true', help='Apply fixes (default: dry run)')
    
    args = parser.parse_args()
    
    music_dir = Path(__file__).parent.parent / 'music'
    
    if not music_dir.exists():
        print(f"❌ Music directory not found: {music_dir}")
        sys.exit(1)
    
    print("🎵 SongSurf Library Fixer")
    print("="*60)
    print(f"📁 Music directory: {music_dir}")
    print("="*60)
    
    # Scanner
    issues = scan_library(music_dir)
    
    # Corriger
    fix_issues(issues, music_dir, dry_run=not args.fix)
