# 🚀 Démarrage Rapide - SongSurf

## Prérequis

- Python 3.8+
- Google Chrome ou Brave
- Connexion Internet

## 📦 Installation

Voir [INSTALL.md](INSTALL.md) pour l'installation complète.

## ▶️ Démarrage

### 1. Démarrer le serveur

```bash
cd python-server
./start.sh
```

Le serveur démarre sur **http://localhost:8080**

### 2. Installer l'extension Chrome

1. Ouvrir Chrome/Brave
2. Aller dans `chrome://extensions/`
3. Activer le **Mode développeur**
4. Cliquer sur **Charger l'extension non empaquetée**
5. Sélectionner le dossier `chrome-extension/`

### 3. Utiliser SongSurf

1. Aller sur **YouTube Music** (https://music.youtube.com)
2. Cliquer sur l'icône **SongSurf** dans la barre d'outils
3. Remplir les métadonnées (Artiste, Album, Titre)
4. Cliquer sur **Download**

## 🎨 Dashboard

Ouvrir **http://localhost:8080** pour:

- Voir votre bibliothèque musicale
- Naviguer par artistes et albums
- Uploader des photos d'artistes
- Rechercher vos chansons

## 🛑 Arrêter le serveur

Appuyer sur `Ctrl+C` dans le terminal

## 🔧 Dépannage

### Le serveur ne démarre pas

```bash
cd python-server
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python app.py
```

### L'extension ne fonctionne pas

1. Vérifier que le serveur est démarré
2. Désactiver les bloqueurs de pub
3. Sur Brave: désactiver les Shields pour YouTube Music

### Erreur CORS

Le serveur est configuré pour accepter toutes les origines. Si problème:
- Redémarrer le serveur
- Vider le cache du navigateur

## 📚 Documentation

- [README.md](README.md) - Vue d'ensemble du projet
- [INSTALL.md](INSTALL.md) - Installation détaillée

## 🎯 Raccourcis

**Démarrer tout:**
```bash
cd python-server && ./start.sh
```

**Ouvrir le dashboard:**
```
http://localhost:8080
```

**Extension Chrome:**
```
chrome://extensions/
```

---

**Bon téléchargement! 🎵**
