# 📁 Structure du Projet GrabSong V3

## 🌳 Arborescence Complète

```
V3/
│
├── 📂 .github/                      # GitHub Configuration
│   └── workflows/
│       └── docker-build.yml         # CI/CD Docker
│
├── 📂 chrome-extension/             # Extension Chrome
│   ├── manifest.json                # Configuration extension
│   ├── background.js                # Service Worker
│   ├── content.js                   # Script d'injection (YouTube Music)
│   ├── popup.html                   # Interface popup
│   ├── popup.js                     # Logique popup
│   └── icons/                       # Icônes extension
│       └── README.md                # Guide création icônes
│
├── 📂 python-server/                # Serveur Python
│   ├── app.py                       # Serveur Flask (API REST)
│   ├── downloader.py                # Module yt-dlp
│   ├── organizer.py                 # Module organisation
│   ├── requirements.txt             # Dépendances Python
│   ├── venv/                        # Environnement virtuel (ignoré)
│   └── README.md                    # Documentation API
│
├── 📂 temp/                         # Téléchargements temporaires (ignoré)
├── 📂 music/                        # Bibliothèque musicale (ignoré)
│
├── 📄 .gitignore                    # Fichiers ignorés par Git
├── 📄 .gitattributes                # Configuration fins de ligne
├── 📄 .editorconfig                 # Configuration éditeur
├── 📄 .dockerignore                 # Fichiers exclus de Docker
│
├── 🐳 Dockerfile                    # Image Docker
├── 🐳 docker-compose.yml            # Orchestration Docker
│
├── 🔧 install.sh                    # Script installation (Linux/macOS)
├── 🔧 start.sh                      # Script lancement rapide
│
├── 📖 LICENSE                       # Licence MIT
├── 📖 README.md                     # Documentation principale
├── 📖 INSTALL.md                    # Guide installation détaillé
├── 📖 QUICKSTART.md                 # Démarrage rapide
├── 📖 DOCKER.md                     # Guide Docker
├── 📖 MIGRATION_V2_V3.md            # Migration V2 → V3
├── 📖 CONTRIBUTING.md               # Guide contribution
├── 📖 GITHUB_SETUP.md               # Configuration GitHub
├── 📖 PUSH_CHECKLIST.md             # Checklist avant push
└── 📖 PROJECT_STRUCTURE.md          # Ce fichier
```

## 📦 Modules Principaux

### 🌐 Extension Chrome

**Fichiers:**
- `manifest.json` - Configuration (permissions, scripts, icônes)
- `background.js` - Service Worker (communication serveur)
- `content.js` - Interface utilisateur + extraction métadonnées
- `popup.html/js` - Popup de statut serveur

**Fonctionnalités:**
- Widget flottant sur YouTube Music
- Extraction métadonnées (titre, artiste, album, année)
- Récupération URL via bouton "Partager"
- Communication avec serveur Python
- Affichage progression en temps réel

### 🐍 Serveur Python

**Fichiers:**
- `app.py` - Serveur Flask avec API REST
- `downloader.py` - Téléchargement via yt-dlp
- `organizer.py` - Organisation + tags ID3
- `requirements.txt` - Dépendances

**Fonctionnalités:**
- API REST (download, status, cleanup, stats)
- Téléchargement MP3 haute qualité
- Pochette intégrée automatiquement
- Organisation `Artist/Album/Title.mp3`
- Tags ID3 complets

## 🔄 Flux de Données

```
YouTube Music
    ↓
Extension Chrome
    ├─ Extrait métadonnées (DOM)
    ├─ Récupère URL (bouton Partager)
    └─ Envoie POST /download
         ↓
Serveur Python (Flask)
    ├─ Reçoit requête
    └─ Lance downloader.py
         ↓
yt-dlp
    ├─ Télécharge vidéo
    ├─ Convertit en MP3
    ├─ Télécharge pochette
    └─ Intègre pochette
         ↓
organizer.py
    ├─ Crée dossiers Artist/Album/
    ├─ Copie fichier
    ├─ Met à jour tags ID3
    └─ Intègre pochette (APIC)
         ↓
music/Artist/Album/Title.mp3
    ✅ Tags ID3 complets
    ✅ Pochette intégrée
```

## 📚 Documentation

### Pour Utilisateurs

| Fichier | Description |
|---------|-------------|
| `README.md` | Vue d'ensemble, installation rapide |
| `QUICKSTART.md` | Démarrage en 2 minutes |
| `INSTALL.md` | Installation détaillée (tous OS) |
| `DOCKER.md` | Utilisation avec Docker |
| `MIGRATION_V2_V3.md` | Migration depuis V2 |

### Pour Développeurs

| Fichier | Description |
|---------|-------------|
| `CONTRIBUTING.md` | Guide de contribution |
| `python-server/README.md` | Documentation API |
| `PROJECT_STRUCTURE.md` | Structure du projet |
| `GITHUB_SETUP.md` | Configuration GitHub |
| `PUSH_CHECKLIST.md` | Checklist avant push |

## 🐳 Docker

### Fichiers

- `Dockerfile` - Image Python 3.11 + FFmpeg
- `docker-compose.yml` - Configuration complète
- `.dockerignore` - Exclusions

### Volumes

```yaml
volumes:
  - ./temp:/app/temp      # Téléchargements temporaires
  - ./music:/app/music    # Bibliothèque musicale
```

### Ports

```yaml
ports:
  - "5000:5000"           # API REST
```

## 🔧 Configuration

### Variables d'Environnement

Créer `.env` (optionnel) :

```env
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
TEMP_DIR=temp
MUSIC_DIR=music
```

### Fichiers de Configuration

- `.gitignore` - Exclusions Git
- `.gitattributes` - Fins de ligne
- `.editorconfig` - Style de code
- `.dockerignore` - Exclusions Docker

## 📊 Tailles Approximatives

```
Extension Chrome:  ~50 KB
Serveur Python:    ~30 KB (code)
Documentation:     ~100 KB
Docker Image:      ~500 MB (avec FFmpeg)
```

## 🔒 Sécurité

### Fichiers Ignorés (.gitignore)

- `venv/` - Environnement virtuel
- `temp/` - Téléchargements temporaires
- `music/` - Bibliothèque musicale
- `*.log` - Logs
- `.env` - Variables d'environnement
- `*.db` - Bases de données

### Permissions Recommandées

```bash
chmod +x install.sh start.sh
chmod 755 python-server/
chmod 644 python-server/*.py
```

## 🎯 Points d'Entrée

### Utilisateur

1. **Extension Chrome** → Interface principale
2. **`install.sh`** → Installation automatique
3. **`start.sh`** → Lancement rapide
4. **Docker Compose** → Déploiement conteneurisé

### Développeur

1. **`python-server/app.py`** → Serveur Flask
2. **`chrome-extension/content.js`** → Interface utilisateur
3. **`CONTRIBUTING.md`** → Guide de contribution

## 📈 Évolution du Projet

### Version Actuelle (V3)

- ✅ Téléchargement direct (yt-dlp)
- ✅ Organisation automatique
- ✅ Pochette intégrée
- ✅ Support Docker
- ✅ Documentation complète

### Améliorations Futures

- [ ] Support playlists complètes
- [ ] Interface web de gestion
- [ ] API pour applications tierces
- [ ] Tests unitaires
- [ ] CI/CD complet

## 🤝 Contribution

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour :
- Signaler un bug
- Proposer une fonctionnalité
- Soumettre du code
- Conventions de commit

## 📞 Support

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Documentation:** Fichiers MD dans le projet

---

**Structure optimisée pour GitHub et collaboration ! 🚀**
