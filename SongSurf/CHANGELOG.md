# 📝 Changelog - GrabSong V3

## [3.1.1] - 2025-10-10

### 🗑️ Suppression de fonctionnalités

#### Dossier personnalisé retiré
- ❌ **Suppression de la fonctionnalité de dossier personnalisé**
  - Simplification de l'interface utilisateur
  - La musique est maintenant toujours sauvegardée dans `V3/music/`
  - Suppression de l'endpoint `/browse_folder`
  - Suppression de l'UI de configuration du dossier
  - Code plus simple et plus maintenable

### 📝 Raison
- Simplification du projet pour se concentrer sur les fonctionnalités essentielles
- Réduction de la complexité du code
- Meilleure expérience utilisateur avec un workflow plus simple

---

## [3.1.0] - 2025-10-10

### 🆕 Nouveautés

#### Scripts d'installation et de démarrage
- ✅ **`install.sh`** - Script d'installation automatique
  - Vérifie Python 3.8+
  - Vérifie FFmpeg
  - Crée l'environnement virtuel
  - Installe toutes les dépendances
  - Crée les dossiers nécessaires
  - Teste l'importation des modules
  
- ✅ **`start.sh`** - Script de démarrage rapide
  - Active automatiquement l'environnement virtuel
  - Lance le serveur Flask
  - Affichage coloré et informatif

- ✅ **`setup_alias.sh`** - Configuration des alias shell
  - Ajoute des alias pratiques (grabsong-start, grabsong-install, etc.)
  - Compatible bash et zsh
  - Facilite l'utilisation quotidienne

#### Documentation
- ✅ **`QUICK_START.md`** - Guide de démarrage rapide
  - Installation en 2 commandes
  - Workflow complet
  - Dépannage
  
- ✅ **`SCRIPTS.md`** - Documentation des scripts
  - Description détaillée de chaque script
  - Options et paramètres
  - Exemples d'utilisation
  
- ✅ **`CHANGELOG.md`** - Historique des versions
  - Suivi des modifications
  - Nouvelles fonctionnalités
  - Corrections de bugs

#### Améliorations
- ✅ Support complet de **WSL (Windows Subsystem for Linux)**
- ✅ Gestion automatique de l'environnement virtuel Python
- ✅ Messages d'erreur plus clairs et informatifs
- ✅ Affichage coloré dans le terminal
- ✅ Vérifications automatiques des prérequis

### 📚 Documentation mise à jour
- README.md - Ajout de la méthode d'installation rapide
- python-server/README.md - Ajout des scripts
- INSTALL_WINDOWS.md - Mise à jour pour WSL

---

## [3.0.0] - 2025-10-09

### 🎉 Version initiale V3

#### Fonctionnalités principales
- ✅ Téléchargement direct via **yt-dlp** (plus de Y2Mate)
- ✅ Interface élégante style Apple
- ✅ Barre de progression animée
- ✅ Organisation automatique (Artist/Album/Title.mp3)
- ✅ Tags ID3 complets avec pochette d'album
- ✅ Explorateur de fichiers intégré (bouton 📂)
- ✅ Dossier personnalisé avec validation/verrouillage
- ✅ Bouton "Télécharger à nouveau"
- ✅ Bouton "Annuler" dans le formulaire

#### Architecture
- **Extension Chrome** (Manifest V3)
  - `background.js` - Service Worker
  - `content.js` - Interface utilisateur
  - `popup.html/js` - Popup de l'extension
  
- **Serveur Python Flask**
  - `app.py` - Serveur principal
  - `downloader.py` - Module yt-dlp
  - `organizer.py` - Organisation des fichiers
  
#### API Endpoints
- `GET /ping` - Test de connexion
- `POST /download` - Lancer un téléchargement
- `GET /status` - Statut du téléchargement
- `POST /cleanup` - Nettoyer le dossier temp/
- `GET /stats` - Statistiques de la bibliothèque
- `POST /browse_folder` - Sélectionner un dossier

#### Dépendances
- Flask 3.0.0
- flask-cors 4.0.0
- yt-dlp ≥2024.10.7
- mutagen 1.47.0
- Pillow ≥10.0.0

---

## Comparaison V2 vs V3

| Critère | V2 | V3 |
|---------|----|----|
| **Site externe** | Y2Mate | Aucun ✅ |
| **Détection fenêtre** | Oui (pywinauto) | Non ✅ |
| **Vitesse** | ~30s | ~10s ✅ |
| **Fiabilité** | Moyenne | Élevée ✅ |
| **Complexité** | Élevée | Faible ✅ |
| **Installation** | Manuelle | Scripts automatiques ✅ |
| **Maintenance** | Difficile | Facile ✅ |

---

## Roadmap

### Version 3.2.0 (À venir)
- [ ] Support des playlists YouTube Music
- [ ] Téléchargement en batch
- [ ] Interface de gestion de la bibliothèque
- [ ] Export de la bibliothèque (CSV, JSON)
- [ ] Recherche dans la bibliothèque
- [ ] Édition des tags ID3 depuis l'interface

### Version 3.3.0 (À venir)
- [ ] Support de Spotify (via API)
- [ ] Support de SoundCloud
- [ ] Conversion de formats (FLAC, AAC, etc.)
- [ ] Normalisation audio
- [ ] Détection automatique des doublons

### Version 4.0.0 (Future)
- [ ] Application desktop (Electron)
- [ ] Synchronisation cloud
- [ ] Mode hors ligne
- [ ] Lecteur audio intégré
- [ ] Recommandations musicales

---

## Contributions

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](../LICENSE) pour plus de détails.

---

## Auteur

**Rev0li** - [GitHub](https://github.com/Rev0li)

---

## Remerciements

- **yt-dlp** - Téléchargement de vidéos YouTube
- **Flask** - Framework web Python
- **mutagen** - Gestion des tags ID3
- **Pillow** - Traitement d'images
- **Chrome Extensions API** - Extension Chrome

---

**Version actuelle :** 3.1.0  
**Date :** 2025-10-10  
**Statut :** Stable ✅
