# ⚡ Quick Start - GrabSong V3

Démarrez en 2 minutes !

## 🎯 Prérequis

- Python 3.8+
- Google Chrome
- FFmpeg (voir installation ci-dessous)

## 🚀 Installation en 3 Commandes

### 1. Installer FFmpeg

**Windows:**
```powershell
choco install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 2. Installer et Lancer le Serveur

```bash
cd V3/python-server
pip install -r requirements.txt
python app.py
```

### 3. Charger l'Extension Chrome

```
chrome://extensions/ → Mode développeur → Charger V3/chrome-extension/
```

## ✅ Test Rapide

1. Aller sur https://music.youtube.com
2. Lancer une musique
3. Cliquer sur le widget "🎵 GrabSong V3" (bas à droite)
4. Cliquer "⬇️ Télécharger"
5. Vérifier les métadonnées
6. Cliquer "💾 Télécharger"
7. Attendre ~10 secondes
8. Vérifier dans `V3/music/Artist/Album/Title.mp3`

## 🎉 C'est Tout !

Vous pouvez maintenant télécharger de la musique en un clic !

## 📚 Documentation Complète

- [README.md](README.md) - Documentation complète
- [INSTALL.md](INSTALL.md) - Guide d'installation détaillé
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture technique
- [MIGRATION_V2_V3.md](MIGRATION_V2_V3.md) - Migration depuis V2

## 🐛 Problème ?

### Serveur Python non accessible
```bash
# Vérifier que le serveur est lancé
python app.py
```

### FFmpeg non trouvé
```bash
# Vérifier l'installation
ffmpeg -version
```

### Extension non visible
```
Rafraîchir YouTube Music (F5)
```

## 💡 Astuce

Lancez le serveur Python dans un terminal séparé pour voir les logs en temps réel:

```bash
cd V3/python-server
python app.py

# Vous verrez:
# 🎵 NOUVELLE REQUÊTE DE TÉLÉCHARGEMENT
# URL: https://music.youtube.com/watch?v=...
# Artiste: Drake
# Album: Views
# Titre: One Dance
# ⏳ Téléchargement en cours...
# ✅ Téléchargement terminé
# 📁 Organisation...
# ✅ Organisation terminée: Drake/Views/One Dance.mp3
```

## 🎵 Enjoy !
