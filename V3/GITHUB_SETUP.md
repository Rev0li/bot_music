# 🚀 Configuration GitHub

Guide pour pousser GrabSong V3 sur GitHub.

## 📋 Pré-requis

- Compte GitHub
- Git installé
- Projet nettoyé (voir [CLEANUP.md](../CLEANUP.md))

## 🎯 Étapes

### 1. Créer un Dépôt GitHub

1. Aller sur https://github.com/new
2. Nom du dépôt: `grabsong-v3`
3. Description: `🎵 YouTube Music downloader with automatic organization`
4. Public ou Private (votre choix)
5. **NE PAS** initialiser avec README, .gitignore ou LICENSE (on les a déjà)
6. Cliquer "Create repository"

### 2. Initialiser Git Localement

```bash
cd V3

# Initialiser le dépôt
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "feat: initial commit - GrabSong V3"
```

### 3. Lier au Dépôt GitHub

```bash
# Remplacer YOUR_USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/YOUR_USERNAME/grabsong-v3.git

# Vérifier
git remote -v
```

### 4. Pousser le Code

```bash
# Pousser vers GitHub
git push -u origin main

# Si erreur "main" n'existe pas, essayer:
git branch -M main
git push -u origin main
```

## ✅ Vérifications Avant Push

### Fichiers à Vérifier

- [ ] `.gitignore` est correct (pas de `temp/`, `music/`, `venv/`)
- [ ] `README.md` est à jour
- [ ] `LICENSE` existe
- [ ] Pas de secrets/tokens dans le code
- [ ] Documentation complète

### Commandes de Vérification

```bash
# Voir les fichiers qui seront commités
git status

# Voir les fichiers ignorés
git status --ignored

# Vérifier qu'aucun fichier sensible n'est tracké
git ls-files | grep -E "(venv|temp|music|\.env|\.log)"
# (devrait être vide)
```

## 📝 Structure du Dépôt

```
grabsong-v3/
├── .github/
│   └── workflows/
│       └── docker-build.yml
├── chrome-extension/
├── python-server/
├── .gitignore
├── .gitattributes
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── install.sh
├── start.sh
├── LICENSE
├── README.md
├── INSTALL.md
├── QUICKSTART.md
├── DOCKER.md
├── MIGRATION_V2_V3.md
├── CONTRIBUTING.md
└── GITHUB_SETUP.md
```

## 🏷️ Tags et Releases

### Créer un Tag

```bash
# Tag de version
git tag -a v3.0.0 -m "Release v3.0.0 - Initial stable release"

# Pousser le tag
git push origin v3.0.0
```

### Créer une Release sur GitHub

1. Aller sur https://github.com/YOUR_USERNAME/grabsong-v3/releases
2. Cliquer "Create a new release"
3. Choisir le tag `v3.0.0`
4. Titre: `v3.0.0 - Initial Release`
5. Description:
   ```markdown
   ## 🎉 GrabSong V3 - Initial Release
   
   ### ✨ Features
   - Direct download via yt-dlp
   - Automatic organization (Artist/Album/Title.mp3)
   - Embedded album art
   - Real-time progress tracking
   - Docker support
   
   ### 📦 Installation
   See [INSTALL.md](INSTALL.md)
   
   ### 🐳 Docker
   ```bash
   docker-compose up -d
   ```
   ```
6. Cliquer "Publish release"

## 🔒 Sécurité

### Fichiers à NE JAMAIS Commiter

- ❌ `venv/` - Environnement virtuel
- ❌ `temp/` - Téléchargements temporaires
- ❌ `music/` - Bibliothèque musicale
- ❌ `.env` - Variables d'environnement
- ❌ `*.log` - Fichiers de log
- ❌ `*.db` - Bases de données

### Si Vous Avez Commité par Erreur

```bash
# Supprimer un fichier du dernier commit
git rm --cached fichier_sensible
git commit --amend -m "fix: remove sensitive file"
git push --force

# Supprimer de l'historique complet (DANGER)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch fichier_sensible" \
  --prune-empty --tag-name-filter cat -- --all
```

## 📊 Badges pour README

Ajouter ces badges dans votre README.md :

```markdown
![GitHub release](https://img.shields.io/github/v/release/YOUR_USERNAME/grabsong-v3)
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/grabsong-v3)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/grabsong-v3)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
```

## 🌟 Après le Push

### Activer GitHub Actions

Les workflows dans `.github/workflows/` se lanceront automatiquement.

### Configurer GitHub Pages (Optionnel)

Pour héberger la documentation :
1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main`, folder: `/docs`

### Ajouter des Topics

Sur la page du dépôt :
- Cliquer sur ⚙️ à côté de "About"
- Ajouter des topics: `youtube`, `music`, `downloader`, `yt-dlp`, `chrome-extension`, `python`, `flask`, `docker`

## 🤝 Collaboration

### Inviter des Collaborateurs

Settings → Collaborators → Add people

### Protéger la Branche Main

Settings → Branches → Add rule
- Branch name pattern: `main`
- ✅ Require pull request reviews
- ✅ Require status checks to pass

## 📞 Support

Si vous rencontrez des problèmes :
- [GitHub Docs](https://docs.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**Votre projet est maintenant prêt pour GitHub ! 🎉**
