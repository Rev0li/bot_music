# 🎵 GrabSong v1.0

Extension Chrome + Serveur Python pour télécharger et organiser automatiquement de la musique depuis YouTube Music.

## ✨ Fonctionnalités

- 🎯 Bouton flottant déplaçable sur YouTube Music
- ✏️ Édition des métadonnées (artiste, album, titre, année)
- 📝 Aperçu du nom de fichier en temps réel
- 🐍 Sauvegarde automatique en JSON (Python)
- 🌐 Téléchargement automatique via Y2Mate
- 💬 Interface chat avec étapes détaillées

## 🚀 Installation Rapide

### 1. Extension Chrome

```
1. Ouvrir chrome://extensions/
2. Activer "Mode développeur"
3. Cliquer "Charger l'extension non empaquetée"
4. Sélectionner le dossier grabSong/
```

### 2. Serveur Python

```bash
cd grabSong
pip install flask flask-cors
python app.py
```

## 🎮 Utilisation

1. Lancer `python app.py`
2. Aller sur YouTube Music
3. Cliquer sur "🎯 GrabSong"
4. Éditer les métadonnées
5. Cliquer "💾 Sauvegarder et Continuer"
6. Le fichier MP3 se télécharge automatiquement

## 📁 Structure

```
grabSong/
├── manifest.json          # Extension
├── background.js          # Service Worker
├── content.js             # Interface utilisateur
├── popup.html/js          # Popup
├── app.py                 # Serveur Python
└── icons/                 # Icônes
```

## 📖 Documentation

- `VERSION_1.0_STABLE.md` - Documentation complète
- `START_HERE.md` - Guide de démarrage
- `CLEANUP.md` - Nettoyage des fichiers

## 🎯 Version

**v1.1 - Automatisation Complète** - 2025-10-09

### ✨ Nouveau dans v1.1
- 🪟 Détection automatique de la fenêtre "Save As"
- 📝 Remplissage automatique du nom de fichier
- 📁 Changement automatique du dossier
- ✅ Validation automatique (double Entrée)

Voir [VERSION.md](VERSION.md) pour l'historique complet.
