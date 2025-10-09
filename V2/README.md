# 🎵 Music Bot V2 - GrabSong

Extension Chrome + Serveur Python pour télécharger et organiser automatiquement de la musique depuis YouTube Music.

## ✨ Fonctionnalités

- 🎯 Bouton flottant déplaçable sur YouTube Music
- ✏️ Édition des métadonnées (artiste, album, titre, année)
- 📝 Aperçu du nom de fichier en temps réel
- 🐍 Sauvegarde automatique en JSON (Python)
- 🌐 Téléchargement automatique via Y2Mate
- 🪟 **Automatisation complète de la fenêtre "Save As"**
- 📁 Sauvegarde automatique dans le dossier `a_trier/`

## 🚀 Installation

### 1. Extension Chrome

```
1. Ouvrir chrome://extensions/
2. Activer "Mode développeur"
3. Cliquer "Charger l'extension non empaquetée"
4. Sélectionner le dossier V2/grabSong/
```

### 2. Serveur Python

```bash
cd V2/grabSong
pip install -r requirements.txt
python app.py
```

## 📁 Structure

```
V2/
├── grabSong/              # Extension Chrome + Serveur Python
│   ├── manifest.json      # Extension
│   ├── background.js      # Service Worker
│   ├── content.js         # Interface utilisateur
│   ├── popup.html/js      # Popup
│   ├── app.py             # Serveur Flask
│   ├── save_as_handler.py # Automatisation Save As
│   └── icons/             # Icônes
├── queue/                 # Dossier temporaire (métadonnées)
└── a_trier/               # Dossier de destination (MP3)
```

## 🎮 Utilisation

1. Lancer `python grabSong/app.py`
2. Aller sur YouTube Music
3. Cliquer sur "🎯 GrabSong"
4. Éditer les métadonnées
5. Cliquer "💾 Sauvegarder et Continuer"
6. Le fichier MP3 se télécharge et se sauvegarde automatiquement dans `a_trier/`

## 📖 Documentation

- `grabSong/README.md` - Documentation de l'extension
- `grabSong/VERSION.md` - Historique des versions
- `grabSong/SAVE_AS_SETUP.md` - Guide d'installation pywinauto

## 🎯 Version

**v1.1 - Automatisation Complète** - 2025-10-09
