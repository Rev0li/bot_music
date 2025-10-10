# Version History

## v3.0.0 - Linux/WSL Edition (2025-10-10)

### ✨ Nouvelles Fonctionnalités
- Interface élégante style Apple avec transitions douces (3.6s)
- Barre de progression animée avec variations aléatoires (10s)
- Dossier personnalisé pour sauvegarder la musique (format WSL)
- Bouton "Télécharger à nouveau" après succès
- Bouton "Annuler" dans le formulaire de métadonnées
- Système de validation/modification du PATH avec verrouillage
- Tags ID3 complets avec pochette d'album intégrée (conversion JPEG automatique)

### 🎨 Interface
- Design Apple-like avec backdrop filter et ombres subtiles
- Transitions ultra-douces (fadeIn 3.6s, scaleIn 3.0s, buttons 2.4s)
- Barre de progression avec gradient bleu et variations naturelles
- Overflow hidden sur les cartes pour gérer les chemins longs
- Boutons avec effets hover et scale

### 🔧 Technique
- Téléchargement direct via yt-dlp (plus besoin de Y2Mate)
- Organisation automatique (Artiste/Album/Titre.mp3)
- Conversion automatique des pochettes en JPEG pour compatibilité maximale
- Redimensionnement des images trop grandes (max 1000x1000)
- Support des chemins WSL (/mnt/c/...)
- Gestion des doublons avec suffixes automatiques

### 📦 Dépendances
- Flask 3.0.0
- flask-cors 4.0.0
- yt-dlp ≥2024.10.7
- mutagen 1.47.0
- Pillow ≥10.0.0
- FFmpeg (système)

### 🐛 Corrections
- Suppression des pochettes existantes avant ajout (évite les doublons)
- Conversion WebP → JPEG pour compatibilité maximale
- Gestion correcte des chemins personnalisés
- Nettoyage des logs de debug

### 📝 Notes
- Version optimisée pour Linux/WSL
- Configuration manuelle du chemin de sauvegarde
- Pas de sélecteur de fichiers graphique (saisie manuelle)
- Pour une version Windows native, voir la branche `windows`

---

## Prochaines Versions

### v3.1.0 - Windows Edition (à venir)
- Serveur Python natif Windows
- Explorateur de fichiers intégré (PowerShell)
- Conversion automatique des chemins Windows
- Installation simplifiée sans WSL
