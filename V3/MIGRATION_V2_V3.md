# 🔄 Migration V2 → V3

Guide de migration de GrabSong V2 vers V3.

## 📊 Principales Différences

### Architecture

**V2:**
```
Extension Chrome → Y2Mate → Fenêtre "Save As" → Serveur Python → Organisation
```

**V3:**
```
Extension Chrome → Serveur Python (yt-dlp) → Organisation
```

### Composants Supprimés

❌ **Y2Mate** - Plus besoin de site externe  
❌ **save_as_handler.py** - Plus de détection de fenêtre  
❌ **pywinauto** - Plus d'automatisation de fenêtre  
❌ **Autoclicker** - Plus de clics automatiques  

### Nouveaux Composants

✅ **downloader.py** - Module yt-dlp pour téléchargement direct  
✅ **Progression en temps réel** - Pourcentage, vitesse, ETA  
✅ **API REST complète** - Endpoints pour status, stats, cleanup  

## 🔧 Changements Techniques

### Serveur Python

**V2 (`app.py`):**
```python
# Dépendances
from save_as_handler import SaveAsHandler
from music_organizer import MusicOrganizer

# Workflow
1. Recevoir métadonnées
2. Sauvegarder en JSON
3. Détecter fenêtre "Save As"
4. Auto-paste et auto-save
5. Organiser le fichier
```

**V3 (`app.py`):**
```python
# Dépendances
from downloader import YouTubeDownloader
from organizer import MusicOrganizer

# Workflow
1. Recevoir URL + métadonnées
2. Télécharger via yt-dlp
3. Organiser le fichier
```

### Extension Chrome

**V2 (`content.js`):**
```javascript
// Workflow
1. Extraire métadonnées
2. Ouvrir Y2Mate en arrière-plan
3. Autoclicker (paste, convert, download)
4. Envoyer métadonnées au serveur Python
5. Attendre la détection "Save As"
```

**V3 (`content.js`):**
```javascript
// Workflow
1. Extraire métadonnées + URL
2. Envoyer au serveur Python
3. Polling du statut
4. Afficher la progression
```

## 📦 Dépendances

### V2
```txt
flask==3.0.0
flask-cors==4.0.0
mutagen==1.47.0
pywinauto==0.6.8  ← Supprimé
pyautogui==0.9.54  ← Supprimé
```

### V3
```txt
flask==3.0.0
flask-cors==4.0.0
mutagen==1.47.0
yt-dlp==2024.10.7  ← Nouveau
```

**Système:**
- FFmpeg (requis par yt-dlp)

## 🚀 Procédure de Migration

### Étape 1: Sauvegarder la V2

```bash
# Sauvegarder votre bibliothèque musicale
cp -r V2/music V2/music_backup

# Sauvegarder vos paramètres
# (Les paramètres de l'extension sont dans Chrome Storage)
```

### Étape 2: Installer FFmpeg

```bash
# Windows
choco install ffmpeg

# Linux
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### Étape 3: Installer la V3

```bash
cd V3/python-server
pip install -r requirements.txt
```

### Étape 4: Migrer la Bibliothèque (Optionnel)

Si vous voulez conserver votre bibliothèque V2:

```bash
# Copier la bibliothèque V2 vers V3
cp -r V2/music/* V3/music/
```

### Étape 5: Mettre à Jour l'Extension

1. Aller sur `chrome://extensions/`
2. Supprimer l'extension V2
3. Charger l'extension V3 (`V3/chrome-extension/`)

### Étape 6: Tester

```bash
# Lancer le serveur V3
cd V3/python-server
python app.py

# Tester sur YouTube Music
```

## 🎯 Avantages de la Migration

### Performance
- **V2:** ~30 secondes par chanson
- **V3:** ~10 secondes par chanson
- **Gain:** 3x plus rapide

### Fiabilité
- **V2:** Dépend de Y2Mate (peut changer)
- **V3:** yt-dlp (open-source, maintenu)
- **Gain:** Plus stable

### Simplicité
- **V2:** 5+ points de défaillance
- **V3:** 2 points de défaillance
- **Gain:** Moins de bugs

### Maintenance
- **V2:** Code complexe (pywinauto, détection)
- **V3:** Code simple (yt-dlp)
- **Gain:** Plus facile à maintenir

## 📋 Checklist de Migration

- [ ] Sauvegarder la bibliothèque V2
- [ ] Installer FFmpeg
- [ ] Installer les dépendances V3
- [ ] Tester le serveur V3
- [ ] Mettre à jour l'extension Chrome
- [ ] Tester un téléchargement
- [ ] Vérifier l'organisation des fichiers
- [ ] Migrer la bibliothèque (optionnel)

## 🔍 Comparaison des Fonctionnalités

| Fonctionnalité | V2 | V3 |
|----------------|----|----|
| Extraction métadonnées | ✅ | ✅ |
| Édition métadonnées | ✅ | ✅ |
| Téléchargement MP3 | ✅ (Y2Mate) | ✅ (yt-dlp) |
| Organisation fichiers | ✅ | ✅ |
| Tags ID3 | ✅ | ✅ |
| Widget déplaçable | ✅ | ✅ |
| Paramètres | ✅ | ✅ |
| Progression en temps réel | ❌ | ✅ |
| API REST | ❌ | ✅ |
| Statistiques | ❌ | ✅ |
| Cleanup automatique | ❌ | ✅ |

## 🐛 Problèmes Connus

### V2
- ❌ Y2Mate peut changer son interface
- ❌ Détection "Save As" fragile
- ❌ Automatisation pywinauto complexe
- ❌ Pas de feedback de progression

### V3
- ✅ Tous ces problèmes sont résolus !

## 💡 Conseils

1. **Gardez la V2** pendant quelques jours pour tester la V3
2. **Testez la V3** avec quelques chansons avant de migrer complètement
3. **Sauvegardez** votre bibliothèque avant de migrer
4. **Lisez** le [README.md](README.md) pour comprendre les nouveautés

## 🎉 Conclusion

La V3 est une **amélioration majeure** par rapport à la V2:
- Plus simple
- Plus rapide
- Plus fiable
- Plus maintenable

**Recommandation:** Migrer dès que possible !

## 📞 Support

Si vous rencontrez des problèmes lors de la migration:
1. Vérifier les logs du serveur Python
2. Vérifier la console Chrome (F12)
3. Consulter [INSTALL.md](INSTALL.md) pour les problèmes courants
