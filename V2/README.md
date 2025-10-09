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
4. Sélectionner le dossier V2/chrome-extension/
```

### 2. Serveur Python

```bash
cd V2/python-server
pip install -r requirements.txt
python app.py
```

## 📁 Structure

```
V2/
├── chrome-extension/      # Extension Chrome uniquement
│   ├── manifest.json      # Configuration
│   ├── background.js      # Service Worker
│   ├── content.js         # Interface utilisateur
│   ├── popup.html/js      # Popup
│   └── icons/             # Icônes
│
├── python-server/         # Serveur Python uniquement
│   ├── app.py             # Serveur Flask
│   ├── save_as_handler.py # Automatisation Save As
│   └── requirements.txt   # Dépendances
│
├── queue/                 # Dossier temporaire (métadonnées)
└── a_trier/               # Dossier de destination (MP3)
```

## 🎮 Utilisation

1. Lancer `python python-server/app.py`
2. Aller sur YouTube Music
3. Cliquer sur "🎯 GrabSong"
4. Éditer les métadonnées
5. Cliquer "💾 Sauvegarder et Continuer"
6. Le fichier MP3 se télécharge et se sauvegarde automatiquement dans `a_trier/`
7. L'extension se réinitialise automatiquement après succès

## 📖 Documentation

Voir les fichiers MD dans chaque dossier pour plus de détails.

## 🎯 Version

**v1.1 - Automatisation Complète** - 2025-10-09
