# 🎵 Music Bot V3 - Architecture avec yt-dlp

## 🎯 Objectif

Simplifier drastiquement le workflow en utilisant **yt-dlp** pour télécharger directement depuis YouTube Music, éliminant le besoin de Y2Mate et de l'automatisation "Save As".

---

## 🔄 Workflow V2 vs V3

### V2 (Actuel - Complexe)
```
YouTube Music → Extension Chrome → Y2Mate (site externe)
    ↓
Fenêtre "Save As" → Détection pywinauto → Auto-paste → Sauvegarde
    ↓
Serveur Python → Organisation des fichiers
```

**Problèmes:**
- ❌ Dépendance à un site externe (Y2Mate)
- ❌ Détection de fenêtre fragile
- ❌ Automatisation complexe avec pywinauto
- ❌ Plusieurs points de défaillance

### V3 (Nouveau - Simple)
```
YouTube Music → Extension Chrome → Serveur Python
    ↓
yt-dlp télécharge directement → Organisation automatique
    ↓
Fichier MP3 organisé dans Music/Artist/Album/
```

**Avantages:**
- ✅ Pas de site externe
- ✅ Pas de détection de fenêtre
- ✅ Téléchargement direct et fiable
- ✅ Un seul point de contrôle (serveur Python)
- ✅ Plus rapide et plus robuste

---

## 📁 Structure du Projet V3

```
V3/
├── chrome-extension/           # Extension Chrome (simplifiée)
│   ├── manifest.json          # Configuration
│   ├── background.js          # Service Worker
│   ├── content.js             # UI sur YouTube Music
│   └── icons/                 # Icônes
│
├── python-server/             # Serveur Python avec yt-dlp
│   ├── app.py                 # Serveur Flask
│   ├── downloader.py          # Module yt-dlp
│   ├── organizer.py           # Organisation des fichiers
│   ├── parser.py              # Parsing des métadonnées
│   └── requirements.txt       # Dépendances (yt-dlp, flask, mutagen)
│
├── temp/                      # Téléchargements temporaires
├── music/                     # Bibliothèque musicale organisée
│   └── Artist/
│       └── Album/
│           └── Title.mp3
│
├── ARCHITECTURE.md            # Ce fichier
└── README.md                  # Documentation utilisateur
```

---

## 🔧 Composants Principaux

### 1. Extension Chrome (Simplifiée)

**Fichier: `chrome-extension/content.js`**

**Responsabilités:**
- Afficher le widget GrabSong sur YouTube Music
- Extraire les métadonnées (titre, artiste, album, année)
- Récupérer le lien YouTube
- Envoyer les données au serveur Python
- Afficher le statut du téléchargement

**Workflow:**
```javascript
1. Utilisateur clique sur "Télécharger"
2. Extension extrait les métadonnées
3. Extension récupère le lien YouTube (via Share)
4. Extension envoie POST /download au serveur Python
5. Extension poll GET /status pour suivre la progression
6. Extension affiche le succès/erreur
```

**Changements par rapport à V2:**
- ❌ Suppression de l'ouverture Y2Mate
- ❌ Suppression de l'autoclicker
- ✅ Communication directe avec le serveur Python
- ✅ Interface plus simple et réactive

---

### 2. Serveur Python avec yt-dlp

**Fichier: `python-server/app.py`**

**Responsabilités:**
- Recevoir les requêtes de l'extension
- Télécharger via yt-dlp
- Organiser les fichiers
- Retourner le statut

**Routes:**
```python
GET  /ping          → Test de connexion
POST /download      → Lancer un téléchargement
GET  /status        → Statut du téléchargement en cours
POST /cleanup       → Nettoyer les fichiers temporaires
```

**Workflow:**
```python
1. Recevoir POST /download avec:
   {
     "url": "https://music.youtube.com/watch?v=...",
     "artist": "Drake",
     "album": "Views",
     "title": "One Dance",
     "year": "2016"
   }

2. Télécharger avec yt-dlp:
   - Format: MP3 (audio uniquement)
   - Qualité: Meilleure disponible
   - Dossier: temp/

3. Organiser le fichier:
   - Parser les métadonnées
   - Créer la structure Artist/Album/
   - Déplacer le fichier
   - Mettre à jour les tags ID3

4. Retourner le statut:
   {
     "success": true,
     "file_path": "music/Drake/Views/One Dance.mp3"
   }
```

---

### 3. Module yt-dlp

**Fichier: `python-server/downloader.py`**

**Classe: `YouTubeDownloader`**

```python
class YouTubeDownloader:
    def __init__(self, temp_dir, music_dir):
        self.temp_dir = temp_dir
        self.music_dir = music_dir
        
    def download(self, url, metadata):
        """
        Télécharge une vidéo YouTube en MP3
        
        Args:
            url: URL YouTube
            metadata: {artist, album, title, year}
            
        Returns:
            {success, file_path, error}
        """
        # Configuration yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{self.temp_dir}/%(title)s.%(ext)s',
            'quiet': False,
            'no_warnings': False,
        }
        
        # Télécharger
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        # Organiser
        organized_path = self.organize(filename, metadata)
        
        return {
            'success': True,
            'file_path': organized_path
        }
```

**Avantages de yt-dlp:**
- ✅ Téléchargement direct depuis YouTube
- ✅ Conversion MP3 automatique (via FFmpeg)
- ✅ Gestion des erreurs robuste
- ✅ Pas de dépendance à un site externe
- ✅ Très rapide et fiable

---

## 🎨 Interface Utilisateur (Extension)

### Widget GrabSong (Identique à V2)

```
┌─────────────────────────┐
│   🎵 GrabSong          │
├─────────────────────────┤
│  ⬇️ Télécharger         │
│  ⚙️ Paramètres          │
└─────────────────────────┘
```

### Vue Téléchargement (Simplifiée)

```
┌─────────────────────────────────────┐
│   🎵 GrabSong                       │
├─────────────────────────────────────┤
│ 🎵 Étape 1/3 : Extraction           │
│ Récupération des métadonnées...    │
│ ✅ Données extraites !              │
│                                     │
│ ✏️ Étape 2/3 : Vérification         │
│ 🎤 Artiste: Drake                   │
│ 💿 Album: Views                     │
│ 🎵 Titre: One Dance                 │
│ 📅 Année: 2016                      │
│ [💾 Sauvegarder et Continuer]      │
│                                     │
│ ⬇️ Étape 3/3 : Téléchargement       │
│ Téléchargement via yt-dlp...       │
│ ⏳ 45% - 2.3 MB / 5.1 MB           │
│                                     │
│ ✅ Téléchargement terminé !         │
│ 📁 music/Drake/Views/One Dance.mp3 │
│                                     │
│ [Fermer]                            │
└─────────────────────────────────────┘
```

**Changements par rapport à V2:**
- ❌ Suppression de l'étape "Ouverture Y2Mate"
- ❌ Suppression de l'étape "Détection Save As"
- ✅ Ajout de la progression du téléchargement
- ✅ Feedback en temps réel

---

## 🔄 Communication Extension ↔ Serveur

### 1. Lancer un Téléchargement

**Request:**
```javascript
POST http://localhost:5000/download
Content-Type: application/json

{
  "url": "https://music.youtube.com/watch?v=ABC123",
  "artist": "Drake",
  "album": "Views",
  "title": "One Dance",
  "year": "2016"
}
```

**Response:**
```json
{
  "success": true,
  "download_id": "abc123",
  "message": "Téléchargement démarré"
}
```

### 2. Suivre la Progression

**Request:**
```javascript
GET http://localhost:5000/status
```

**Response (En cours):**
```json
{
  "in_progress": true,
  "download_id": "abc123",
  "progress": {
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
    "file_path": "music/Drake/Views/One Dance.mp3",
    "timestamp": "2025-10-10T09:30:00"
  }
}
```

**Response (Erreur):**
```json
{
  "in_progress": false,
  "last_error": {
    "message": "Vidéo non disponible",
    "timestamp": "2025-10-10T09:30:00"
  }
}
```

---

## 📦 Dépendances

### Python (`requirements.txt`)
```txt
flask==3.0.0
flask-cors==4.0.0
yt-dlp==2024.10.7
mutagen==1.47.0
```

### Système
- **FFmpeg** (requis par yt-dlp pour conversion MP3)
  - Windows: `choco install ffmpeg` ou télécharger depuis ffmpeg.org
  - Linux: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`

---

## 🚀 Installation et Utilisation

### 1. Installation

```bash
# Cloner le projet
cd V3/python-server

# Installer les dépendances Python
pip install -r requirements.txt

# Installer FFmpeg (si pas déjà installé)
# Windows: choco install ffmpeg
# Linux: sudo apt install ffmpeg
# macOS: brew install ffmpeg
```

### 2. Lancer le Serveur

```bash
python app.py
```

Le serveur démarre sur `http://localhost:5000`

### 3. Installer l'Extension Chrome

```
1. Ouvrir chrome://extensions/
2. Activer "Mode développeur"
3. Cliquer "Charger l'extension non empaquetée"
4. Sélectionner le dossier V3/chrome-extension/
```

### 4. Utiliser

```
1. Aller sur YouTube Music
2. Lancer une musique
3. Cliquer sur le widget "🎵 GrabSong"
4. Cliquer sur "⬇️ Télécharger"
5. Vérifier les métadonnées
6. Cliquer "💾 Sauvegarder et Continuer"
7. Le fichier se télécharge et s'organise automatiquement !
```

---

## 🎯 Avantages de la V3

### Simplicité
- ❌ **V2:** Extension → Y2Mate → Save As → Python
- ✅ **V3:** Extension → Python (yt-dlp) → Fichier organisé

### Fiabilité
- ❌ **V2:** Dépend de Y2Mate (peut changer)
- ✅ **V3:** yt-dlp (open-source, maintenu activement)

### Performance
- ❌ **V2:** ~30 secondes (ouverture Y2Mate + conversion + Save As)
- ✅ **V3:** ~10 secondes (téléchargement direct)

### Maintenance
- ❌ **V2:** Complexe (pywinauto, détection de fenêtre)
- ✅ **V3:** Simple (juste yt-dlp + Flask)

### Expérience Utilisateur
- ❌ **V2:** Fenêtres qui s'ouvrent, clics automatiques
- ✅ **V3:** Tout en arrière-plan, feedback clair

---

## 🔧 Configuration

### Fichier `config.json` (optionnel)

```json
{
  "server": {
    "host": "localhost",
    "port": 5000
  },
  "download": {
    "temp_dir": "temp",
    "music_dir": "music",
    "format": "mp3",
    "quality": "192"
  },
  "yt_dlp": {
    "quiet": false,
    "no_warnings": false,
    "extract_audio": true,
    "audio_format": "mp3",
    "audio_quality": "192"
  }
}
```

---

## 🐛 Gestion des Erreurs

### Erreurs Possibles

1. **Serveur Python non accessible**
   - Message: "⚠️ Serveur Python non accessible"
   - Solution: Lancer `python app.py`

2. **Vidéo non disponible**
   - Message: "❌ Cette vidéo n'est pas disponible"
   - Solution: Essayer une autre musique

3. **FFmpeg non installé**
   - Message: "❌ FFmpeg non trouvé"
   - Solution: Installer FFmpeg

4. **Erreur de téléchargement**
   - Message: "❌ Erreur lors du téléchargement"
   - Solution: Vérifier la connexion internet

### Gestion dans l'Extension

```javascript
try {
  const response = await fetch('http://localhost:5000/download', {
    method: 'POST',
    body: JSON.stringify(data)
  });
  
  if (!response.ok) {
    throw new Error('Serveur non accessible');
  }
  
  const result = await response.json();
  
  if (!result.success) {
    showError(result.error);
  }
} catch (error) {
  showError('⚠️ Serveur Python non accessible. Lancez: python app.py');
}
```

---

## 📊 Comparaison V2 vs V3

| Critère | V2 | V3 |
|---------|----|----|
| **Complexité** | Élevée | Faible |
| **Fiabilité** | Moyenne | Élevée |
| **Vitesse** | ~30s | ~10s |
| **Dépendances** | Y2Mate, pywinauto | yt-dlp, FFmpeg |
| **Points de défaillance** | 5+ | 2 |
| **Maintenance** | Difficile | Facile |
| **UX** | Fenêtres visibles | Tout en arrière-plan |

---

## 🎉 Conclusion

La V3 avec **yt-dlp** est une **amélioration majeure** par rapport à la V2 :

- ✅ **Plus simple** (moins de code)
- ✅ **Plus fiable** (pas de site externe)
- ✅ **Plus rapide** (téléchargement direct)
- ✅ **Plus maintenable** (moins de dépendances)
- ✅ **Meilleure UX** (tout en arrière-plan)

**Prêt à implémenter ! 🚀**
