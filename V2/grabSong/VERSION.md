# 🎵 GrabSong - Versions

## v1.1 - Automatisation Complète ✅
**Date:** 2025-10-09

### ✨ Nouvelles Fonctionnalités
- ✅ Détection automatique de la fenêtre "Save As"
- ✅ Remplissage automatique du nom de fichier
- ✅ Changement automatique du dossier vers `a_trier/`
- ✅ Validation automatique (double Entrée)
- ✅ Support multi-backend (UIA + Win32 + win32gui)
- ✅ Logs propres et détaillés

### 🔧 Technique
- **Module:** `save_as_handler.py`
- **Bibliothèques:** pywinauto, pywin32
- **Méthode:** Raccourcis clavier (Ctrl+A, Ctrl+L, Entrée)
- **Timeout:** 120 secondes

### 📊 Workflow
```
1. Détection fenêtre "* wants to save"
2. Ctrl+A → Taper filename
3. Ctrl+L → Taper path → Entrée
4. Entrée (Save)
```

---

## v1.0 - Version Stable
**Date:** 2025-10-09

### ✨ Fonctionnalités
- ✅ Extension Chrome avec bouton flottant
- ✅ Extraction automatique des métadonnées
- ✅ Formulaire d'édition
- ✅ Serveur Python Flask
- ✅ Sauvegarde JSON
- ✅ Workflow Y2Mate

### 🔧 Technique
- **Extension:** Manifest V3
- **Serveur:** Flask HTTP (localhost:5000)
- **Communication:** fetch() via background.js

---

## 🚀 Prochaines Versions

### v1.2 - Organisation Automatique
- [ ] Déplacer le MP3 vers `a_trier/`
- [ ] Copier `info.json` avec le MP3
- [ ] Nettoyer `queue/`
- [ ] Notification à l'extension

### v1.3 - Améliorations
- [ ] Gestion des erreurs avancée
- [ ] Retry automatique
- [ ] Support multi-navigateurs
- [ ] Interface de configuration
