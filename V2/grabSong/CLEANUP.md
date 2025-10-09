# 🧹 Nettoyage - Fichiers à Supprimer/Garder

## ✅ Fichiers à GARDER (Essentiels)

### Extension Chrome
```
✅ manifest.json
✅ background.js
✅ content.js
✅ popup.html
✅ popup.js
✅ icons/ (dossier complet)
```

### Serveur Python
```
✅ app.py
✅ requirements.txt
```

### Documentation
```
✅ VERSION_1.0_STABLE.md
✅ START_HERE.md
✅ CLEANUP.md (ce fichier)
```

---

## ❌ Fichiers à SUPPRIMER (Obsolètes)

### Native Messaging (Obsolète - remplacé par Flask)
```
❌ native_host.py
❌ com.musicorganizer.grabsong.json
❌ install_native_host.bat
```

### Anciens Modules (Non utilisés)
```
❌ autoclicker.js
❌ modules/ (dossier complet si existe)
❌ _archive/ (dossier complet si existe)
```

### Documentation Obsolète
```
❌ DEBUG_NO_DETECTION.md
❌ FIX_PERMISSIONS.md
❌ NEXT_STEPS.md
❌ PROGRESS.md
❌ README.md (ancien)
❌ READY_TO_TEST.md
❌ SIMPLIFICATION.md
❌ STEP2_CLIPBOARD_MONITOR.md
❌ STEP_BY_STEP_SUMMARY.md
❌ TESTING_GUIDE.md
❌ FIX_UNDERSCORE.md
❌ FIX_OPENTAB.md
❌ FIX_DRAG_CLICK.md
❌ NEW_FEATURES.md
❌ EXPANDABLE_CHAT.md
❌ FINAL_VERSION.md
❌ EDIT_FORM.md
❌ SMOOTH_DRAG.md
❌ PYTHON_INTEGRATION.md
❌ PYTHON_SETUP.md
```

### Tests (Obsolètes)
```
❌ test-*.html (tous les fichiers de test)
```

---

## 📁 Structure Finale Propre

```
grabSong/
├── manifest.json          ✅ Extension
├── background.js          ✅ Extension
├── content.js             ✅ Extension
├── popup.html             ✅ Extension
├── popup.js               ✅ Extension
├── icons/                 ✅ Extension
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
├── app.py                 ✅ Serveur Python
├── requirements.txt       ✅ Dépendances
├── VERSION_1.0_STABLE.md  ✅ Documentation
├── START_HERE.md          ✅ Guide rapide
└── CLEANUP.md             ✅ Ce fichier
```

---

## 🗑️ Commandes de Nettoyage

### Windows PowerShell

```powershell
cd C:\Users\Molim\Music\bot\python-organizer-v2\grabSong

# Supprimer les fichiers obsolètes
Remove-Item native_host.py
Remove-Item com.musicorganizer.grabsong.json
Remove-Item install_native_host.bat
Remove-Item autoclicker.js -ErrorAction SilentlyContinue

# Supprimer les dossiers obsolètes
Remove-Item -Recurse -Force modules -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force _archive -ErrorAction SilentlyContinue

# Supprimer la documentation obsolète
Remove-Item DEBUG_NO_DETECTION.md -ErrorAction SilentlyContinue
Remove-Item FIX_PERMISSIONS.md -ErrorAction SilentlyContinue
Remove-Item NEXT_STEPS.md -ErrorAction SilentlyContinue
Remove-Item PROGRESS.md -ErrorAction SilentlyContinue
Remove-Item README.md -ErrorAction SilentlyContinue
Remove-Item READY_TO_TEST.md -ErrorAction SilentlyContinue
Remove-Item SIMPLIFICATION.md -ErrorAction SilentlyContinue
Remove-Item STEP2_CLIPBOARD_MONITOR.md -ErrorAction SilentlyContinue
Remove-Item STEP_BY_STEP_SUMMARY.md -ErrorAction SilentlyContinue
Remove-Item TESTING_GUIDE.md -ErrorAction SilentlyContinue
Remove-Item FIX_UNDERSCORE.md -ErrorAction SilentlyContinue
Remove-Item FIX_OPENTAB.md -ErrorAction SilentlyContinue
Remove-Item FIX_DRAG_CLICK.md -ErrorAction SilentlyContinue
Remove-Item NEW_FEATURES.md -ErrorAction SilentlyContinue
Remove-Item EXPANDABLE_CHAT.md -ErrorAction SilentlyContinue
Remove-Item FINAL_VERSION.md -ErrorAction SilentlyContinue
Remove-Item EDIT_FORM.md -ErrorAction SilentlyContinue
Remove-Item SMOOTH_DRAG.md -ErrorAction SilentlyContinue
Remove-Item PYTHON_INTEGRATION.md -ErrorAction SilentlyContinue
Remove-Item PYTHON_SETUP.md -ErrorAction SilentlyContinue

# Supprimer les fichiers de test
Remove-Item test-*.html -ErrorAction SilentlyContinue

echo "✅ Nettoyage terminé!"
```

---

## 💾 Sauvegarde Avant Nettoyage

**Créer une sauvegarde complète:**

```powershell
# Créer un dossier de sauvegarde
cd C:\Users\Molim\Music\bot\python-organizer-v2
mkdir grabSong_backup_20251009

# Copier tout
Copy-Item -Recurse grabSong\* grabSong_backup_20251009\

echo "✅ Sauvegarde créée: grabSong_backup_20251009"
```

---

## 📊 Avant/Après

### Avant Nettoyage
- **Fichiers:** ~40
- **Documentation:** ~20 fichiers MD
- **Code obsolète:** Native Messaging, modules inutilisés

### Après Nettoyage
- **Fichiers:** ~12
- **Documentation:** 3 fichiers essentiels
- **Code:** Uniquement ce qui est utilisé

---

**Fais une sauvegarde puis lance les commandes de nettoyage ! 🧹**
