# 🎵 SongSurf

Organise automatiquement ta musique avec une extension Chrome et un serveur Python.

---

## ✨ Fonctionnalités

- 📁 **Organisation automatique** par Artiste/Album
- 🎨 **Métadonnées ID3** complètes (titre, artiste, album, pochette)
- 📊 **Dashboard web** pour gérer ta bibliothèque
- 🔄 **Queue de téléchargement** pour les albums complets
- 🖼️ **Photos d'artistes** personnalisables
- 🐳 **Docker** pour installation simplifiée

---

## 🚀 Installation Rapide (Docker - Recommandé)

### Prérequis
- Docker installé ([Installation](https://docs.docker.com/get-docker/))

### Démarrage
```bash
./start-docker.sh
```

Le serveur sera accessible sur **http://localhost:8080**

📖 **Guide complet** : [DOCKER.md](DOCKER.md)


## 📱 Installation de l'Extension Chrome

1. Ouvre Chrome et va dans `chrome://extensions/`
2. Active le **Mode développeur** (en haut à droite)
3. Clique sur **Charger l'extension non empaquetée**
4. Sélectionne le dossier `chrome-extension/`
5. L'icône SongSurf apparaît dans ta barre d'outils

---

## 🎯 Utilisation

1. **Démarre le serveur** (Docker)
2. **Ouvre YT Music** dans Chrome
3. **Clique sur l'extension SongSurf**

---

## 📊 Dashboard Web

Le dashboard te permet de :
- 📁 Voir ta bibliothèque organisée
- 🎨 Ajouter des photos d'artistes
- 📊 Voir les statistiques

---

## 🐳 Docker vs Installation Manuelle

| Aspect | Docker | Manuel |
|--------|--------|--------|
| Installation | 1 commande | 5-10 minutes |
| Dépendances | Juste Docker | Python, venv, FFmpeg |
| Portabilité | ✅ Partout | ⚠️ Dépend du système |
| Mise à jour | `docker-compose build` | Réinstaller |
| Isolation | ✅ Conteneur isolé | ⚠️ Partage l'environnement |

---

## 📁 Structure du Projet

```
SongSurf/
├── chrome-extension/       # Extension Chrome
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
├── python-server/          # Serveur Flask
│   ├── app.py             # API principale
│   ├── downloader.py      # Téléchargement YT
│   ├── organizer.py       # Organisation des fichiers
│   ├── Dockerfile         # Image Docker
│   ├── requirements.txt   # Dépendances Python
│   ├── templates/         # Templates HTML
│   └── static/            # CSS/JS du dashboard
├── docker-compose.yml      # Orchestration Docker
├── start-docker.sh         # Démarrage Docker
├── temp/                   # Téléchargements temporaires
└── music/                  # Bibliothèque musicale
    └── artist_photos/      # Photos d'artistes
```

---

## 🔧 Configuration

### Changer le Port (Docker)

Édite `docker-compose.yml` :
```yaml
ports:
  - "9000:8080"  # Port 9000 au lieu de 8080
```

---

## 📋 Commandes Utiles

### Docker
```bash
./start-docker.sh           # Démarrer
docker-compose logs -f      # Voir les logs
docker-compose stop         # Arrêter
docker-compose restart      # Redémarrer
docker-compose down         # Arrêter et supprimer
```
---

## 🐛 Dépannage

### Le serveur ne démarre pas (Docker)
```bash
docker-compose logs songsurf-server
docker-compose build --no-cache
```

### L'extension ne se connecte pas
1. Vérifie que le serveur tourne : http://localhost:8080
2. Vérifie le port dans l'extension (popup.js)
3. Désactive les bloqueurs de pub sur YT Music

### Port déjà utilisé
```bash
# Trouver le processus
sudo lsof -i :8080

# Ou change le port (voir Configuration)
```

---

## 🔐 Sécurité

⚠️ **Important** :
- Le serveur est accessible uniquement en local (`localhost:8080`)
- N'expose pas le serveur sur Internet sans authentification
- Les téléchargements sont pour usage personnel uniquement

---

## 📝 Technologies

- **Backend** : Python 3.11, Flask, yt-dlp, mutagen
- **Frontend** : HTML5, CSS3, JavaScript (Vanilla)
- **Extension** : Chrome Extension API
- **Conversion** : FFmpeg
- **Conteneurisation** : Docker

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésite pas à :
- 🐛 Signaler des bugs
- 💡 Proposer des fonctionnalités
- 🔧 Soumettre des pull requests

---

## 📄 Licence

MIT License - Voir [LICENSE](LICENSE)

---

## 📚 Documentation

- **Guide Docker** : [DOCKER.md](DOCKER.md)
- **Migration Docker** : [MIGRATION-DOCKER.md](MIGRATION-DOCKER.md)

---

## ⚠️ Avertissement

Ce projet est destiné à un usage personnel uniquement. Respecte les droits d'auteur et les conditions d'utilisation.

---

## 🎉 Profite de ta musique !

Créé avec ❤️ pour les amateurs de musique

**Version** : 3.0 (Docker)  
**Dernière mise à jour** : Novembre 2025
