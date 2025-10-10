# 🐍 Python Server - GrabSong V3

Serveur Flask pour télécharger et organiser la musique depuis YouTube Music.

## 📁 Structure

```
python-server/
├── app.py           # Serveur Flask principal
├── downloader.py    # Module yt-dlp (téléchargement)
├── organizer.py     # Module d'organisation
├── requirements.txt # Dépendances Python
├── install.sh       # 🆕 Script d'installation automatique
├── start.sh         # 🆕 Script de démarrage
└── venv/           # Environnement virtuel (ignoré par Git)
```

## 🚀 Installation

### Méthode 1 : Script automatique (recommandé)

```bash
# Rendre le script exécutable
chmod +x install.sh

# Lancer l'installation
./install.sh
```

Le script `install.sh` va automatiquement :
- ✅ Vérifier Python et FFmpeg
- ✅ Créer l'environnement virtuel
- ✅ Installer toutes les dépendances
- ✅ Créer les dossiers nécessaires
- ✅ Tester les modules

### Méthode 2 : Installation manuelle

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate  # Linux/macOS/WSL
# ou
venv\Scripts\activate     # Windows PowerShell

# Installer les dépendances
pip install -r requirements.txt
```

## ▶️ Lancement

### Méthode 1 : Script de démarrage (recommandé)

```bash
# Rendre le script exécutable
chmod +x start.sh

# Lancer le serveur
./start.sh
```

### Méthode 2 : Démarrage manuel

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le serveur
python app.py
```

Le serveur démarre sur `http://localhost:5000`

## 📡 API Endpoints

### `GET /ping`
Vérifier que le serveur est en ligne.

**Réponse:**
```json
{
  "status": "ok",
  "message": "GrabSong V3 Server"
}
```

### `POST /download`
Télécharger une chanson.

**Body:**
```json
{
  "url": "https://music.youtube.com/watch?v=...",
  "metadata": {
    "title": "Song Title",
    "artist": "Artist Name",
    "album": "Album Name",
    "year": "2024"
  }
}
```

**Réponse:**
```json
{
  "success": true,
  "message": "Téléchargement terminé",
  "final_path": "Artist/Album/Title.mp3"
}
```

### `GET /status`
Obtenir la progression du téléchargement en cours.

**Réponse:**
```json
{
  "status": "downloading",
  "percent": 45.5,
  "speed": "2.5 MiB/s",
  "eta": "00:05",
  "current_file": "Artist - Title"
}
```

### `POST /cleanup`
Nettoyer les fichiers temporaires.

**Réponse:**
```json
{
  "success": true,
  "message": "Nettoyage effectué"
}
```

### `GET /stats`
Obtenir les statistiques de la bibliothèque.

**Réponse:**
```json
{
  "artists": 42,
  "albums": 156,
  "songs": 1234
}
```

## 🔧 Configuration

### Variables d'Environnement

Créer un fichier `.env` (optionnel) :

```env
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
TEMP_DIR=../temp
MUSIC_DIR=../music
```

### FFmpeg

Le serveur détecte automatiquement FFmpeg. Si non trouvé, installez-le :

```bash
# Linux
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Voir INSTALL.md
```

## 📊 Logs

Les logs s'affichent dans le terminal :

```
🎵 Téléchargement: Song Title
   URL: https://music.youtube.com/watch?v=...
   🔧 FFmpeg trouvé: /usr/bin
   ⏳ Téléchargement en cours...
   [download] 100% of 3.5MiB
   ✅ Téléchargement terminé
   
📁 Organisation...
   📂 Création: Artist/Album/
   🖼️ Pochette trouvée: Artist - Title.jpg
   🏷️ Mise à jour des tags ID3...
      🖼️ Pochette intégrée au MP3
      ✅ Tags ID3 mis à jour
   ✅ Organisation terminée!
```

## 🐛 Dépannage

### Port 5000 déjà utilisé

```bash
# Changer le port dans app.py
app.run(host='0.0.0.0', port=5001)
```

### FFmpeg non trouvé

```bash
# Vérifier l'installation
which ffmpeg

# Ajouter au PATH si nécessaire
export PATH=$PATH:/chemin/vers/ffmpeg/bin
```

### Erreur de permissions

```bash
# Donner les permissions aux dossiers
chmod -R 755 ../temp ../music
```

## 📚 Modules

### `downloader.py`
- Télécharge les vidéos YouTube via yt-dlp
- Convertit en MP3 haute qualité
- Télécharge et intègre la pochette
- Suivi de progression en temps réel

### `organizer.py`
- Organise les fichiers en `Artist/Album/Title.mp3`
- Met à jour les tags ID3
- Intègre la pochette dans le MP3
- Gère les doublons

### `app.py`
- Serveur Flask
- API REST
- Gestion des requêtes
- Coordination des modules

## 🧪 Tests

```bash
# Test manuel
curl http://localhost:5000/ping

# Test de téléchargement
curl -X POST http://localhost:5000/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://music.youtube.com/watch?v=...",
    "metadata": {
      "title": "Test",
      "artist": "Artist",
      "album": "Album",
      "year": "2024"
    }
  }'
```

## 📝 Notes

- Les téléchargements sont stockés temporairement dans `../temp/`
- La bibliothèque finale est dans `../music/`
- Les fichiers temporaires sont nettoyés automatiquement
- La pochette est intégrée dans le MP3 (tag APIC)

---

**Pour plus d'informations, voir [README.md](../README.md)**
