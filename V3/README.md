# 🎵 GrabSong V3 - Téléchargement Direct avec yt-dlp

Extension Chrome + Serveur Python pour télécharger et organiser automatiquement de la musique depuis YouTube Music.

## ✨ Nouveautés V3

- ✅ **Téléchargement direct** via yt-dlp (plus besoin de Y2Mate)
- ✅ **Workflow simplifié** (Extension → Python → Fichier organisé)
- ✅ **Plus rapide** (~10s au lieu de ~30s)
- ✅ **Plus fiable** (pas de dépendance à un site externe)
- ✅ **Progression en temps réel** (pourcentage, vitesse, ETA)

## 🚀 Installation

### 1. Prérequis

**FFmpeg** (requis par yt-dlp pour la conversion MP3)

```bash
# Windows (avec Chocolatey)
choco install ffmpeg

# Ou télécharger depuis: https://ffmpeg.org/download.html
```

### 2. Serveur Python

```bash
cd V3/python-server

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python app.py
```

Le serveur démarre sur `http://localhost:5000`

### 3. Extension Chrome

```
1. Ouvrir chrome://extensions/
2. Activer "Mode développeur"
3. Cliquer "Charger l'extension non empaquetée"
4. Sélectionner le dossier V3/chrome-extension/
```

## 📁 Structure

```
V3/
├── chrome-extension/      # Extension Chrome
│   ├── manifest.json      # Configuration
│   ├── background.js      # Service Worker
│   ├── content.js         # Interface utilisateur
│   └── popup.html/js      # Popup
│
├── python-server/         # Serveur Python
│   ├── app.py             # Serveur Flask
│   ├── downloader.py      # Module yt-dlp
│   ├── organizer.py       # Organisation des fichiers
│   └── requirements.txt   # Dépendances
│
├── temp/                  # Téléchargements temporaires
└── music/                 # Bibliothèque musicale organisée
    └── Artist/
        └── Album/
            └── Title.mp3
```

## 🎮 Utilisation

1. **Lancer le serveur Python**
   ```bash
   python python-server/app.py
   ```

2. **Aller sur YouTube Music**
   - Ouvrir https://music.youtube.com
   - Lancer une musique

3. **Utiliser l'extension**
   - Cliquer sur le widget "🎵 GrabSong V3"
   - Cliquer sur "⬇️ Télécharger"
   - Vérifier les métadonnées
   - Cliquer sur "💾 Télécharger"

4. **Résultat**
   - Le fichier se télécharge automatiquement
   - Il est organisé dans `music/Artist/Album/Title.mp3`
   - Les tags ID3 sont mis à jour

## 🔄 Workflow

```
YouTube Music → Extension Chrome → Serveur Python
    ↓
yt-dlp télécharge en MP3 → Organisation automatique
    ↓
music/Artist/Album/Title.mp3 (avec tags ID3)
```

## 📊 Comparaison V2 vs V3

| Critère | V2 | V3 |
|---------|----|----|
| **Site externe** | Y2Mate | Aucun |
| **Détection fenêtre** | Oui (pywinauto) | Non |
| **Vitesse** | ~30s | ~10s |
| **Fiabilité** | Moyenne | Élevée |
| **Complexité** | Élevée | Faible |

## 🐛 Dépannage

### Serveur Python non accessible
```
❌ Erreur: Serveur Python non accessible

✅ Solution: Lancer python app.py
```

### FFmpeg non trouvé
```
❌ Erreur: FFmpeg non trouvé

✅ Solution: Installer FFmpeg
   Windows: choco install ffmpeg
   Linux: sudo apt install ffmpeg
   macOS: brew install ffmpeg
```

### Vidéo non disponible
```
❌ Erreur: Cette vidéo n'est pas disponible

✅ Solution: Essayer une autre musique
```

## 📖 API du Serveur Python

### GET /ping
Test de connexion

**Response:**
```json
{
  "status": "ok",
  "message": "GrabSong V3 server is running",
  "timestamp": "2025-10-10T09:30:00"
}
```

### POST /download
Lance un téléchargement

**Request:**
```json
{
  "url": "https://music.youtube.com/watch?v=...",
  "artist": "Artist Name",
  "album": "Album Name",
  "title": "Song Title",
  "year": "2024"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Téléchargement démarré",
  "timestamp": "2025-10-10T09:30:00"
}
```

### GET /status
Retourne le statut du téléchargement en cours

**Response (En cours):**
```json
{
  "in_progress": true,
  "progress": {
    "status": "downloading",
    "percent": 45,
    "downloaded": 2300000,
    "total": 5100000,
    "speed": "512 KB/s",
    "eta": "5s"
  }
}
```

**Response (Terminé):**
```json
{
  "in_progress": false,
  "last_completed": {
    "success": true,
    "file_path": "Drake/Views/One Dance.mp3",
    "timestamp": "2025-10-10T09:30:00"
  }
}
```

### POST /cleanup
Nettoie le dossier temporaire

**Response:**
```json
{
  "success": true,
  "deleted_files": ["file1.mp3", "file2.mp3"]
}
```

### GET /stats
Retourne les statistiques de la bibliothèque

**Response:**
```json
{
  "artists": 42,
  "albums": 156,
  "songs": 789
}
```

## 🎯 Exemple de Résultat

**Avant:**
```
Téléchargement d'une musique sur YouTube Music
```

**Après:**
```
music/
└── Drake/
    └── Views/
        └── One Dance.mp3
            (avec tags ID3: Artiste, Album, Titre, Année)
```

## 🎉 Avantages de la V3

1. **Simplicité** - Un seul workflow direct
2. **Fiabilité** - Pas de dépendance externe
3. **Rapidité** - 3x plus rapide que la V2
4. **Robustesse** - Moins de points de défaillance
5. **Progression** - Feedback en temps réel

## 📝 Notes

- **FFmpeg** est requis pour la conversion MP3
- Le serveur Python doit être lancé avant d'utiliser l'extension
- Les fichiers temporaires sont automatiquement supprimés après organisation
- Les doublons sont gérés automatiquement (ajout d'un suffixe)

## 🔧 Configuration

Le serveur Python peut être configuré en modifiant les constantes dans `app.py`:

```python
TEMP_DIR = BASE_DIR / "temp"      # Dossier temporaire
MUSIC_DIR = BASE_DIR / "music"    # Bibliothèque musicale
```

## ✅ Tests

Pour tester le serveur Python:

```bash
# Test de connexion
curl http://localhost:5000/ping

# Test de téléchargement
curl -X POST http://localhost:5000/download \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ","artist":"Rick Astley","album":"Whenever You Need Somebody","title":"Never Gonna Give You Up","year":"1987"}'

# Vérifier le statut
curl http://localhost:5000/status

# Statistiques
curl http://localhost:5000/stats
```

## 🎵 Happy Music Organizing!

**Version:** 3.0.0  
**Date:** 2025-10-10  
**Powered by:** yt-dlp, Flask, Chrome Extensions
