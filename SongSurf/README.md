# 🎵 SongSurf

Téléchargez facilement vos musiques depuis YouTube Music avec une extension Chrome et un serveur Python.

## ⚡ Installation Rapide

### 1. Installer le serveur Python

```bash
cd python-server
./install.sh
```

Le script installe automatiquement :
- ✅ Python 3 et environnement virtuel
- ✅ FFmpeg (conversion MP3)
- ✅ Toutes les dépendances

### 2. Démarrer le serveur

```bash
./start.sh
```

Le serveur démarre sur **http://localhost:8080**

### 3. Installer l'extension Chrome

1. Ouvrez Chrome et allez sur `chrome://extensions/`
2. Activez le **Mode développeur** (en haut à droite)
3. Cliquez sur **Charger l'extension non empaquetée**
4. Sélectionnez le dossier `chrome-extension/`

## 🎯 Utilisation

1. **Allez sur YouTube Music** (music.youtube.com)
2. **Cliquez sur le widget SongSurf** (en bas à droite)
3. **Téléchargez** :
   - 🎵 Une chanson
   - 💿 Un album complet
   - 📋 Une playlist

Les musiques sont automatiquement :
- ✅ Téléchargées en MP3
- ✅ Organisées par Artiste/Album
- ✅ Taguées avec métadonnées
- ✅ Avec pochette intégrée

## 📊 Dashboard

Accédez au dashboard sur **http://localhost:8080** pour :
- 📚 Voir votre bibliothèque musicale
- 📈 Statistiques en temps réel
- 🎵 Téléchargements récents

## 🛠️ Commandes Utiles

```bash
# Installer/Réinstaller
cd python-server
./install.sh

# Démarrer le serveur
./start.sh

# Arrêter le serveur
Ctrl+C
```

## 📁 Structure du Projet

```
SongSurf/
├── python-server/          # Serveur Flask
│   ├── install.sh         # Installation automatique
│   ├── start.sh           # Démarrage automatique
│   ├── app.py             # Serveur principal
│   ├── downloader.py      # Téléchargement yt-dlp
│   └── organizer.py       # Organisation des fichiers
│
├── chrome-extension/       # Extension Chrome
│   ├── manifest.json      # Configuration
│   ├── content.js         # Script principal
│   └── background.js      # Service worker
│
├── music/                  # Bibliothèque musicale
└── temp/                   # Fichiers temporaires
```

## 🔧 Prérequis

- **Python 3.8+**
- **FFmpeg** (installé automatiquement)
- **Chrome/Edge** (pour l'extension)

## 📝 Notes

- Les musiques sont sauvegardées dans `music/Artiste/Album/`
- Le serveur doit tourner pour que l'extension fonctionne
- Le widget est déplaçable (drag & drop)
- La progression s'affiche en temps réel

## 🚀 Développé avec

- **Backend** : Python, Flask, yt-dlp, Mutagen
- **Frontend** : JavaScript, HTML, CSS
- **Extension** : Chrome Extension API

---

**Prêt à télécharger de la musique ! 🎵**
