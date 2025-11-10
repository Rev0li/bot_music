#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
organizer.py - Organisation des fichiers MP3

FONCTIONNALITÉ:
  - Organise les MP3 en structure Artist/Album/Title.mp3
  - Met à jour les tags ID3
  - Gère les doublons
"""

from pathlib import Path
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, APIC
import shutil
from datetime import datetime
import mimetypes
from PIL import Image
import io


class MusicOrganizer:
    """Organisateur de fichiers musicaux"""
    
    def __init__(self, music_dir):
        self.music_dir = Path(music_dir)
        self.music_dir.mkdir(exist_ok=True, parents=True)
    
    def detect_featuring(self, title, artist):
        """
        Detect featuring artists in title and return cleaned data
        
        Returns:
            dict: {
                'main_artist': str,
                'feat_artists': list,
                'clean_title': str,
                'has_feat': bool
            }
        """
        import re
        
        # Patterns to detect featuring
        feat_patterns = [
            r'\(feat\.?\s+([^)]+)\)',
            r'\(ft\.?\s+([^)]+)\)',
            r'\(featuring\s+([^)]+)\)',
            r'\[feat\.?\s+([^\]]+)\]',
            r'\[ft\.?\s+([^\]]+)\]',
            r'feat\.?\s+([^-\(\[]+)',
            r'ft\.?\s+([^-\(\[]+)',
        ]
        
        feat_artists = []
        clean_title = title
        
        # Check title for featuring
        for pattern in feat_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                feat_artist = match.group(1).strip()
                # Clean up multiple artists (separated by &, and, ,)
                feat_list = re.split(r'\s*(?:&|and|,)\s*', feat_artist)
                feat_artists.extend([a.strip() for a in feat_list if a.strip()])
                # Remove feat from title
                clean_title = re.sub(pattern, '', clean_title, flags=re.IGNORECASE).strip()
        
        # Check artist field for multiple artists
        if ' & ' in artist or ' and ' in artist or ', ' in artist or ' et ' in artist:
            # Split by common separators
            artist_list = re.split(r'\s*(?:&|and|et|,)\s*', artist, flags=re.IGNORECASE)
            main_artist = artist_list[0].strip()
            # Others are featuring
            feat_artists.extend([a.strip() for a in artist_list[1:] if a.strip()])
            
            print(f"   🔍 Multiple artists detected: {artist}")
            print(f"      → Main: {main_artist}")
            print(f"      → Feat: {', '.join(artist_list[1:])}")
        else:
            main_artist = artist
        
        return {
            'main_artist': main_artist,
            'feat_artists': list(set(feat_artists)),  # Remove duplicates
            'clean_title': clean_title,
            'has_feat': len(feat_artists) > 0
        }
    
    def organize(self, file_path, metadata):
        """
        Organise un fichier MP3 dans la structure Artist/Album/Title.mp3
        Auto-détecte les featuring et organise correctement
        
        Args:
            file_path (str): Chemin du fichier MP3 temporaire
            metadata (dict): {artist, album, title, year}
            
        Returns:
            dict: {success, final_path, error}
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"Fichier non trouvé: {file_path}")
            
            print(f"\n📁 Organisation du fichier: {file_path.name}")
            
            # Extraire les métadonnées
            raw_artist = metadata.get('artist', 'Unknown Artist')
            album = metadata.get('album', 'Unknown Album')
            raw_title = metadata.get('title', 'Unknown Title')
            year = metadata.get('year', '')
            
            # Détecter les featuring
            feat_info = self.detect_featuring(raw_title, raw_artist)
            
            # Utiliser l'artiste principal pour l'organisation
            artist = feat_info['main_artist']
            title = feat_info['clean_title']
            
            # Si featuring détecté, ajouter au titre
            if feat_info['has_feat']:
                feat_str = ', '.join(feat_info['feat_artists'])
                title = f"{title} (feat. {feat_str})"
                print(f"   🎭 Featuring détecté: {feat_str}")
                print(f"   ✅ Organisation sous: {artist}")
            
            # Nettoyer les noms (caractères interdits)
            artist = self._clean_filename(artist)
            album = self._clean_filename(album)
            title = self._clean_filename(title)
            
            print(f"   🎤 Artiste principal: {artist}")
            print(f"   💿 Album: {album}")
            print(f"   🎵 Titre: {title}")
            print(f"   📅 Année: {year}")
            
            # Créer la structure de dossiers
            artist_dir = self.music_dir / artist
            album_dir = artist_dir / album
            album_dir.mkdir(parents=True, exist_ok=True)
            
            # Chemin final
            final_path = album_dir / f"{title}.mp3"
            
            # Gérer les doublons
            if final_path.exists():
                print(f"   ⚠️ Fichier existant, ajout d'un suffixe...")
                counter = 1
                while final_path.exists():
                    final_path = album_dir / f"{title} ({counter}).mp3"
                    counter += 1
            
            # Copier le fichier
            print(f"   📋 Copie vers: {final_path}")
            shutil.copy2(file_path, final_path)
            
            # Chercher la pochette (image téléchargée par yt-dlp)
            thumbnail_path = self._find_thumbnail(file_path)
            
            # Mettre à jour les tags ID3 avec les métadonnées corrigées
            print(f"   🏷️ Mise à jour des tags ID3...")
            corrected_metadata = {
                'artist': artist,  # Artiste principal
                'album': album,
                'title': title,    # Titre avec feat si nécessaire
                'year': year
            }
            self._update_tags(final_path, corrected_metadata, thumbnail_path)
            
            # Supprimer le fichier temporaire
            file_path.unlink()
            print(f"   🗑️ Fichier temporaire supprimé")
            
            # Supprimer la pochette temporaire si elle existe
            if thumbnail_path and thumbnail_path.exists():
                thumbnail_path.unlink()
                print(f"   🗑️ Pochette temporaire supprimée")
            
            print(f"   ✅ Organisation terminée!")
            
            return {
                'success': True,
                'final_path': str(final_path.relative_to(self.music_dir)),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def move_and_rename_feat(self, song_path, target_artist, feat_artist):
        """
        Déplace un fichier MP3 vers le bon artiste et renomme avec le feat
        
        Args:
            song_path (str): Chemin relatif du fichier (depuis music/)
            target_artist (str): Artiste cible
            feat_artist (str): Artiste en featuring
            
        Returns:
            dict: {success, new_path, error}
        """
        try:
            # Convertir en chemin absolu
            source_file = self.music_dir / song_path
            
            if not source_file.exists():
                return {'success': False, 'error': f'Fichier introuvable: {source_file}'}
            
            # Lire les métadonnées actuelles
            audio = MP3(source_file, ID3=ID3)
            
            # Récupérer les infos
            title = audio.get('TIT2', ['Unknown'])[0] if 'TIT2' in audio else 'Unknown'
            album = audio.get('TALB', ['Unknown'])[0] if 'TALB' in audio else 'Unknown'
            
            # Nouveau titre avec feat
            new_title = f"{title} (feat. {feat_artist})"
            
            # Créer le nouveau chemin
            artist_dir = self.music_dir / target_artist
            album_dir = artist_dir / album
            album_dir.mkdir(parents=True, exist_ok=True)
            
            # Nouveau nom de fichier
            safe_title = self._clean_filename(new_title)
            new_filename = f"{safe_title}.mp3"
            new_path = album_dir / new_filename
            
            # Mettre à jour les métadonnées
            audio['TPE1'] = TPE1(encoding=3, text=target_artist)
            audio['TIT2'] = TIT2(encoding=3, text=new_title)
            audio.save()
            
            # Déplacer le fichier
            shutil.move(str(source_file), str(new_path))
            
            # Supprimer les dossiers vides
            self._cleanup_empty_dirs(source_file.parent)
            
            print(f"✅ Déplacé: {source_file.name} → {new_path}")
            
            return {
                'success': True,
                'new_path': str(new_path),
                'old_path': str(source_file)
            }
            
        except Exception as e:
            print(f"❌ Erreur lors du déplacement: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _cleanup_empty_dirs(self, directory):
        """Supprime les dossiers vides récursivement"""
        try:
            directory = Path(directory)
            
            # Ne pas supprimer le dossier music/ lui-même
            if directory == self.music_dir:
                return
            
            # Si le dossier est vide, le supprimer
            if directory.exists() and directory.is_dir():
                if not any(directory.iterdir()):
                    directory.rmdir()
                    print(f"🗑️  Dossier vide supprimé: {directory}")
                    
                    # Vérifier le parent
                    self._cleanup_empty_dirs(directory.parent)
        except Exception as e:
            print(f"⚠️  Erreur lors du nettoyage: {e}")
    
    def _clean_filename(self, name):
        """Nettoie un nom de fichier (supprime les caractères interdits)"""
        # Caractères interdits sur Windows
        forbidden = '<>:"/\\|?*'
        for char in forbidden:
            name = name.replace(char, '')
        return name.strip()
    
    def _find_thumbnail(self, mp3_path):
        """Cherche la pochette téléchargée par yt-dlp"""
        mp3_path = Path(mp3_path)
        base_name = mp3_path.stem
        
        print(f"   🔍 Recherche de pochette pour: {base_name}")
        
        # Extensions d'images possibles
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        
        # Lister tous les fichiers dans le dossier temp
        temp_files = list(mp3_path.parent.glob('*'))
        print(f"   📂 Fichiers dans temp/: {[f.name for f in temp_files]}")
        
        for ext in image_extensions:
            thumbnail = mp3_path.parent / f"{base_name}{ext}"
            if thumbnail.exists():
                print(f"   ✅ Pochette trouvée: {thumbnail.name}")
                return thumbnail
        
        print(f"   ⚠️ Aucune pochette trouvée")
        return None
    
    def _update_tags(self, file_path, metadata, thumbnail_path=None):
        """Met à jour les tags ID3 d'un fichier MP3 avec pochette"""
        try:
            # Charger le fichier MP3
            audio = MP3(file_path, ID3=ID3)
            
            # Ajouter les tags ID3 si ils n'existent pas
            try:
                audio.add_tags()
            except:
                pass
            
            # Vérifier si une pochette existe déjà (intégrée par yt-dlp)
            has_existing_cover = 'APIC:' in audio.tags or any(key.startswith('APIC') for key in audio.tags.keys())
            if has_existing_cover:
                print(f"      ℹ️ Pochette existante détectée (sera remplacée pour compatibilité)")
            
            # Mettre à jour les tags textuels
            audio.tags['TIT2'] = TIT2(encoding=3, text=metadata.get('title', ''))
            audio.tags['TPE1'] = TPE1(encoding=3, text=metadata.get('artist', ''))
            audio.tags['TALB'] = TALB(encoding=3, text=metadata.get('album', ''))
            
            if metadata.get('year'):
                audio.tags['TDRC'] = TDRC(encoding=3, text=metadata.get('year', ''))
            
            # Ajouter/Remplacer la pochette si disponible (pour compatibilité maximale)
            if thumbnail_path and thumbnail_path.exists():
                # Convertir en JPEG si nécessaire (pour compatibilité maximale)
                img_data, mime_type = self._convert_image_to_jpeg(thumbnail_path)
                
                if img_data:
                    # Supprimer les pochettes existantes pour éviter les doublons
                    audio.tags.delall('APIC')
                    
                    # Ajouter la pochette avec le bon format
                    audio.tags.add(
                        APIC(
                            encoding=3,          # UTF-8
                            mime=mime_type,      # Type MIME de l'image
                            type=3,              # Cover (front)
                            desc='Cover',        # Description
                            data=img_data        # Données de l'image
                        )
                    )
                    print(f"      🖼️ Pochette intégrée au MP3 ({len(img_data)} bytes, {mime_type})")
            
            # Sauvegarder
            audio.save()
            
            print(f"      ✅ Tags ID3 mis à jour")
            
        except Exception as e:
            print(f"      ⚠️ Erreur lors de la mise à jour des tags: {str(e)}")
    
    def _convert_image_to_jpeg(self, image_path):
        """
        Convertit une image en JPEG pour compatibilité maximale
        
        Args:
            image_path: Chemin vers l'image
            
        Returns:
            tuple: (image_data, mime_type) ou (None, None) si erreur
        """
        try:
            # Ouvrir l'image avec Pillow
            img = Image.open(image_path)
            
            # Convertir en RGB si nécessaire (pour JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Créer un fond blanc
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionner si trop grande (max 1000x1000)
            max_size = 1000
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                print(f"      📐 Image redimensionnée à {img.width}x{img.height}")
            
            # Sauvegarder en JPEG dans un buffer
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=90, optimize=True)
            img_data = buffer.getvalue()
            
            print(f"      🔄 Image convertie en JPEG ({len(img_data)} bytes)")
            return img_data, 'image/jpeg'
            
        except Exception as e:
            print(f"      ⚠️ Erreur conversion image: {str(e)}")
            # Fallback: utiliser l'image originale
            try:
                with open(image_path, 'rb') as f:
                    img_data = f.read()
                mime_type = mimetypes.guess_type(str(image_path))[0] or 'image/jpeg'
                return img_data, mime_type
            except:
                return None, None
    
    def get_stats(self):
        """Retourne les statistiques de la bibliothèque musicale"""
        try:
            artists = [d for d in self.music_dir.iterdir() if d.is_dir()]
            
            total_albums = 0
            total_songs = 0
            total_duration = 0  # en secondes
            
            for artist_dir in artists:
                albums = [d for d in artist_dir.iterdir() if d.is_dir()]
                total_albums += len(albums)
                
                for album_dir in albums:
                    songs = list(album_dir.glob('*.mp3'))
                    total_songs += len(songs)
                    
                    # Calculer la durée totale
                    for song in songs:
                        try:
                            audio = MP3(song)
                            total_duration += audio.info.length
                        except:
                            pass  # Ignorer les fichiers corrompus
            
            # Convertir en format lisible
            hours = int(total_duration // 3600)
            minutes = int((total_duration % 3600) // 60)
            
            return {
                'artists': len(artists),
                'albums': total_albums,
                'songs': total_songs,
                'total_duration_seconds': int(total_duration),
                'total_duration_formatted': f"{hours}h {minutes}min" if hours > 0 else f"{minutes}min"
            }
        except Exception as e:
            return {
                'artists': 0,
                'albums': 0,
                'songs': 0,
                'total_duration_seconds': 0,
                'total_duration_formatted': '0min',
                'error': str(e)
            }
    
    def get_library_structure(self):
        """Retourne la structure complète de la bibliothèque"""
        try:
            structure = {
                'artists': [],
                'albums': [],
                'songs': []
            }
            
            for artist_dir in self.music_dir.iterdir():
                if not artist_dir.is_dir():
                    continue
                
                artist_name = artist_dir.name
                artist_albums = []
                artist_songs_count = 0
                
                for album_dir in artist_dir.iterdir():
                    if not album_dir.is_dir():
                        continue
                    
                    album_name = album_dir.name
                    songs = list(album_dir.glob('*.mp3'))
                    artist_songs_count += len(songs)
                    
                    # Ajouter l'album
                    structure['albums'].append({
                        'name': album_name,
                        'artist': artist_name,
                        'songs_count': len(songs)
                    })
                    
                    artist_albums.append(album_name)
                    
                    # Extraire la pochette du premier MP3 de l'album
                    album_art_url = None
                    if songs:
                        try:
                            audio = MP3(songs[0], ID3=ID3)
                            if audio.tags:
                                for tag in audio.tags.values():
                                    if isinstance(tag, APIC):
                                        # Créer un chemin pour la pochette
                                        cover_filename = f"{artist_name}_{album_name}.jpg".replace('/', '_').replace('\\', '_')
                                        album_art_url = f"/api/cover/{cover_filename}"
                                        break
                        except:
                            pass
                    
                    # Ajouter les chansons
                    for song_path in songs:
                        structure['songs'].append({
                            'title': song_path.stem,
                            'artist': artist_name,
                            'album': album_name,
                            'path': str(song_path.relative_to(self.music_dir)),
                            'album_art': album_art_url
                        })
                
                # Ajouter l'artiste
                structure['artists'].append({
                    'name': artist_name,
                    'albums_count': len(artist_albums),
                    'songs_count': artist_songs_count
                })
            
            return structure
        except Exception as e:
            return {
                'artists': [],
                'albums': [],
                'songs': [],
                'error': str(e)
            }


# Test du module
if __name__ == '__main__':
    organizer = MusicOrganizer('music')
    
    # Simuler un fichier téléchargé
    # (créer un fichier de test)
    
    stats = organizer.get_stats()
    print(f"\n📊 Statistiques:")
    print(f"   Artistes: {stats['artists']}")
    print(f"   Albums: {stats['albums']}")
    print(f"   Chansons: {stats['songs']}")