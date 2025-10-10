# 🎵 GrabSong - YouTube Music Downloader

**Version 3.0** - Téléchargement direct et organisation automatique de musique depuis YouTube Music.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-green.svg)](https://developer.chrome.com/docs/extensions/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-red.svg)](https://github.com/yt-dlp/yt-dlp)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## ✨ Nouveautés V3

- ✅ **Téléchargement direct** via yt-dlp (plus besoin de Y2Mate)
- ✅ **3x plus rapide** (~10s au lieu de ~30s)
- ✅ **Plus fiable** (pas de dépendance à un site externe)
- ✅ **Pochette intégrée** automatiquement dans le MP3
- ✅ **Support Docker** pour un déploiement facile
- ✅ **Progression en temps réel** (pourcentage, vitesse, ETA)

---

## 🎯 Fonctionnalités

**Workflow complet automatisé:**

1. **Extension Chrome** → Extrait les métadonnées depuis YouTube Music
2. **Serveur Python** → Télécharge via yt-dlp en MP3 haute qualité
3. **Organisation** → Classe automatiquement: `Artist/Album/Title.mp3`
4. **Tags ID3** → Artiste, Album, Titre, Année + Pochette intégrée

---

## ⚡ Installation Rapide

### Linux/macOS
```bash
cd V3
bash install.sh
bash start.sh
```


## 📁 Structure du Projet

```
bot/
└── V3/                          # Version stable actuelle
    ├── chrome-extension/        # Extension Chrome
    ├── python-server/           # Serveur Python (Flask + yt-dlp)
    ├── music/                   # Bibliothèque musicale organisée
    ├── install.sh               # Installation automatique
    ├── start.sh                 # Lancement rapide
    ├── Dockerfile               # Image Docker
    └── README.md                # Documentation complète
```

---

## 📖 Documentation

- **[QUICK_START.md](V3/QUICK_START.md)** - Démarrage en 2 minutes
- **[CHANGELOG.md](V3/CHANGELOG.md)** - Historique des changements

---

## 🎉 Résultat

**Avant:**
```
Téléchargements/
└── Måneskin - This Is The Life.mp3
```

**Après:**
```
music/
└── Måneskin/
    └── Rush!/
        └── This Is The Life.mp3
            ✅ Tags ID3 (Artiste, Album, Titre, Année)
            ✅ Pochette intégrée
```

---

## 🛠️ Technologies

- **Python 3.8+** - Serveur backend
- **Flask** - API REST
- **yt-dlp** - Téléchargement YouTube
- **Mutagen** - Tags ID3
- **Chrome Extension** - Interface utilisateur
- **Docker** - Conteneurisation

---

## 📝 Licence

MIT License - Voir [LICENSE](LICENSE)

---

## 🙏 Crédits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Téléchargement YouTube
- [FFmpeg](https://ffmpeg.org/) - Conversion audio
- [Mutagen](https://github.com/quodlibet/mutagen) - Tags ID3
