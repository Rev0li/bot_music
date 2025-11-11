# 🎵 SongSurf

Téléchargez facilement vos musiques depuis YouTube Music avec une extension Chrome et un serveur Python.

## 🚀 Installation Rapide

### 🐳 Méthode 1 : Docker (Recommandé)

**Aucune installation manuelle, tout est inclus !**

```bash
./docker-start.sh
```

C'est tout ! Le serveur démarre sur **http://localhost:8080**

Pour arrêter :
```bash
./docker-stop.sh
```

---

### 🐍 Méthode 2 : Installation Python Classique

#### 1. Installer le serveur Python

```bash
cd python-server
./install.sh
```

Le script installe **automatiquement** :
- ✅ Python 3 et environnement virtuel
- ✅ FFmpeg (détection OS + choix d'installation)
  - Avec sudo (système) - Recommandé
  - Sans sudo (local) - Pour école/entreprise
- ✅ Toutes les dépendances Python

#### 2. Démarrer le serveur

```bash
./start.sh
```

Le serveur démarre sur **http://localhost:8080**

---

## 📱 Installation Extension Chrome

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

### 🐳 Avec Docker

```bash
# Démarrer
./docker-start.sh

# Arrêter
./docker-stop.sh

# Voir les logs
docker compose logs -f

# Redémarrer
docker compose restart

# Statut
docker compose ps
```

### 🐍 Sans Docker

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

### Avec Docker (Recommandé)
- **Docker** et **Docker Compose**
- **Chrome/Edge** (pour l'extension)

### Sans Docker
- **Python 3.8+**
- **FFmpeg** (installé automatiquement)
- **Chrome/Edge** (pour l'extension)

### 🏫 Sans Droits Administrateur (École/Entreprise)

Le script `install.sh` propose automatiquement une **installation locale** de FFmpeg si vous n'avez pas les droits sudo. Choisissez simplement l'option 2 lors de l'installation !

## 🐳 Pourquoi Docker ?

- ✅ **Aucune installation manuelle** - Python, FFmpeg, tout est inclus
- ✅ **Pas de pollution** - Rien n'est installé sur votre PC
- ✅ **Portable** - Fonctionne sur Linux, Mac, Windows
- ✅ **Isolation** - Pas de conflit avec vos autres projets
- ✅ **Mise à jour facile** - Un simple `docker compose pull`

## 📝 Notes

- Les musiques sont sauvegardées dans `music/Artiste/Album/`
- Le serveur doit tourner pour que l'extension fonctionne
- Le widget est déplaçable (drag & drop)
- La progression s'affiche en temps réel
- Avec Docker, vos musiques restent sur votre PC (volume monté)

## 🚀 Développé avec

- **Backend** : Python, Flask, yt-dlp, Mutagen
- **Frontend** : JavaScript, HTML, CSS
- **Extension** : Chrome Extension API

---

**Prêt à télécharger de la musique ! 🎵**
