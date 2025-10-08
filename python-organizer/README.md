# 🎵 Music Organizer Pro

Application professionnelle pour organiser automatiquement vos fichiers MP3.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Fonctionnalités

- ✅ **Détection automatique** des téléchargements
- ✅ **Collage automatique** du nom de fichier (Ctrl+V)
- ✅ **Organisation automatique** en Artiste/Album/Titre
- ✅ **Mise à jour des tags ID3**
- ✅ **Interface graphique** intuitive
- ✅ **Mode debug** pour dépannage

---

## 📚 Documentation Complète

**Toute la documentation est dans le dossier [`docs/`](docs/00_INDEX.md)**

### 🚀 Démarrage
- **[Quick Start](docs/01_QUICK_START.md)** - Démarrer en 5 minutes
- **[Installation](docs/02_INSTALLATION.md)** - Installation complète
- **[Guide Utilisateur](docs/03_USER_GUIDE.md)** - Comment utiliser

### 📖 Référence
- **[Formats de Fichiers](docs/04_FILENAME_FORMATS.md)** - Formats acceptés
- **[Auto-Save Feature](docs/05_AUTO_SAVE.md)** - Automatisation
- **[Troubleshooting](docs/09_TROUBLESHOOTING.md)** - Dépannage
- **[FAQ](docs/10_FAQ.md)** - Questions fréquentes

---

## ⚡ Installation Rapide

```powershell
# 1. Cloner ou télécharger le projet
cd C:\Users\Molim\Music\bot\bot

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python app.py
```

**C'est tout ! 🎉**

---

## 📁 Structure du Projet

```
bot/
├── app.py                          # 🚀 Application principale
├── requirements.txt                # Dépendances
├── README.md                       # Ce fichier
│
├── music_organizer/                # Package modulaire
│   ├── parser.py                   # Extraction métadonnées
│   ├── organizer.py                # Organisation fichiers
│   ├── monitor.py                  # Surveillance téléchargements
│   └── auto_saver.py               # Automatisation "Save As"
│
└── docs/                           # 📚 Documentation complète
    ├── 00_INDEX.md                 # Table des matières
    ├── 01_QUICK_START.md           # Démarrage rapide
    ├── 02_INSTALLATION.md          # Installation
    ├── 03_USER_GUIDE.md            # Guide utilisateur
    ├── 04_FILENAME_FORMATS.md      # Formats
    ├── 05_AUTO_SAVE.md             # Auto-Save
    ├── 09_TROUBLESHOOTING.md       # Dépannage
    └── 10_FAQ.md                   # FAQ
│
└── music_organizer/                # Package principal
    ├── __init__.py                 # Initialisation du package
    ├── parser.py                   # Extraction des métadonnées
    ├── organizer.py                # Organisation des fichiers
    └── monitor.py                  # Surveillance des téléchargements
```

## 🚀 Installation

### Prérequis
- **Python 3.8+** - [Télécharger ici](https://www.python.org/downloads/)
- **Windows 10/11** - Pour le scanner de téléchargements

### Installation Rapide

#### Option 1: Installation avec requirements.txt (Recommandé)
```powershell
# 1. Naviguer vers le dossier
cd C:\Users\Molim\Music\bot\bot

# 2. Installer toutes les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python app.py
```

#### Option 2: Installation manuelle
```powershell
# 1. Naviguer vers le dossier
cd C:\Users\Molim\Music\bot\bot

# 2. Installer mutagen (pour les tags ID3)
pip install mutagen

# 3. Lancer l'application
python app.py
```

### Vérification de l'Installation

```powershell
# Vérifier la version de Python
python --version
# Doit afficher: Python 3.8.x ou supérieur

# Vérifier que mutagen est installé
python -m pip list | findstr mutagen
# Doit afficher: mutagen x.x.x

# Tester l'import des modules
python -c "from music_organizer import MetadataParser; print('✅ OK')"
# Doit afficher: ✅ OK
```

### Dépendances Complètes

| Package | Version | Usage |
|---------|---------|-------|
| `mutagen` | ≥1.45.1 | Lecture/écriture des tags ID3 MP3 |
| `pyautogui` | ≥0.9.53 | Automatisation du collage (Ctrl+V) |
| `pyperclip` | ≥1.8.2 | Lecture du clipboard |
| `tkinter` | (inclus) | Interface graphique |
| `threading` | (inclus) | Traitement parallèle |
| `subprocess` | (inclus) | Scanner de fenêtres Windows |

### Commandes PowerShell Utiles

```powershell
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer une version spécifique de mutagen
pip install mutagen==1.47.0

# Désinstaller mutagen
pip uninstall mutagen

# Voir toutes les dépendances installées
pip list

# Créer un environnement virtuel (optionnel)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 📖 Utilisation

### Interface Graphique

1. **Sélectionner un dossier**
   - Cliquez sur "📂 Parcourir"
   - Sélectionnez le dossier contenant vos MP3

2. **Scanner les chansons**
   - Cliquez sur "🔍 Scanner les chansons"
   - Vérifiez les résultats dans les logs

3. **Organiser**
   - Cliquez sur "✨ Organiser les chansons"
   - Confirmez l'opération

4. **Scanner de téléchargement (optionnel)**
   - Cliquez sur "▶️ Activer"
   - Recevez des notifications lors des téléchargements

## 📝 Format des Fichiers

### Format Accepté
```
art=Artiste alb=Album N=Titre Y=Année.mp3
```

### Champs Obligatoires
- `art=` - Artiste
- `N=` - Titre

### Champs Optionnels
- `alb=` - Album (défaut: "Unknown Album")
- `Y=` - Année (défaut: "Unknown")

### Exemples
```
✅ art=Drake alb=Views N=OneDance Y=2016.mp3
✅ art=Drake N=OneDance.mp3
✅ N=OneDance art=Drake Y=2016.mp3
```

## 🏗️ Architecture

### Modules

#### `parser.py` - Extraction des métadonnées
```python
from music_organizer import MetadataParser

parser = MetadataParser()
artist, album, title, year = parser.parse("art=Drake N=OneDance.mp3")
```

#### `organizer.py` - Organisation des fichiers
```python
from music_organizer import MusicOrganizer

organizer = MusicOrganizer("/path/to/music")
songs = organizer.scan()
success, errors = organizer.organize()
```

#### `monitor.py` - Surveillance
```python
from music_organizer import DownloadMonitor

monitor = DownloadMonitor(notification_callback=my_callback)
monitor.start()
```

## 📊 Résultat

### Avant
```
Downloads/
├── art=Drake alb=Views N=OneDance Y=2016.mp3
├── art=The Killers alb=Hot Fuss N=Mr. Brightside Y=2004.mp3
└── art=Apashe N=Time Warp.mp3
```

### Après
```
Music/
├── Drake/
│   └── Views/
│       └── OneDance.mp3
├── The Killers/
│   └── Hot Fuss/
│       └── Mr. Brightside.mp3
└── Apashe/
    └── Unknown Album/
        └── Time Warp.mp3
```

Chaque fichier a ses **tags ID3 mis à jour** automatiquement !

## 🧪 Tests

### Test du Parser
```python
from music_organizer import MetadataParser

parser = MetadataParser()

# Test 1: Format complet
result = parser.parse("art=Drake alb=Views N=OneDance Y=2016.mp3")
assert result == ('Drake', 'Views', 'OneDance', '2016')

# Test 2: Format minimal
result = parser.parse("art=Drake N=OneDance.mp3")
assert result == ('Drake', 'Unknown Album', 'OneDance', 'Unknown')

# Test 3: Format invalide
result = parser.parse("Drake - OneDance.mp3")
assert result == (None, None, None, None)
```

## 📚 Documentation

- **README.md** - Ce fichier
- **FILENAME_FORMATS.md** - Formats de noms acceptés
- **PYTHON_ORGANIZER_GUIDE.md** - Guide d'apprentissage complet

### Docstrings

Tous les modules sont documentés avec des docstrings :

```python
from music_organizer import MetadataParser

help(MetadataParser)
help(MetadataParser.parse)
```

## 🐛 Dépannage

### Erreur: Module not found
```bash
pip install mutagen
```

### Erreur: Aucune chanson trouvée
Vérifiez le format des noms de fichiers :
- Doit contenir `art=` et `N=`
- Extension `.mp3`

### Erreur: Permission denied
- Fermez les lecteurs de musique
- Vérifiez que les fichiers ne sont pas ouverts

## 🔄 Migration

### Depuis l'ancienne version

**Ancien code (main_gui.py):**
```python
# Code monolithique dans un seul fichier
```

**Nouveau code (app.py + modules):**
```python
from music_organizer import MetadataParser, MusicOrganizer, DownloadMonitor

# Code modulaire et réutilisable
```

### Avantages
- ✅ Code organisé en modules
- ✅ Réutilisable
- ✅ Testable
- ✅ Documenté
- ✅ Maintenable

## 🎓 Apprentissage

### Pour les débutants
1. Lire `PYTHON_ORGANIZER_GUIDE.md`
2. Examiner `parser.py` (le plus simple)
3. Examiner `organizer.py`
4. Examiner `monitor.py`
5. Examiner `app.py` (interface)

### Concepts Python utilisés
- Classes et méthodes
- Type hints
- Docstrings
- Threading
- Regex
- Gestion de fichiers
- Tkinter (GUI)

## 🚀 Améliorations Futures

- [ ] Tests unitaires
- [ ] Interface web
- [ ] Support de formats audio supplémentaires
- [ ] Téléchargement de pochettes d'albums
- [ ] Génération de playlists
- [ ] Support multi-langues

## 📞 Support

Pour toute question, consultez :
- `FILENAME_FORMATS.md` - Formats de fichiers
- `PYTHON_ORGANIZER_GUIDE.md` - Guide complet
- Les docstrings dans le code

## ✅ Résumé

**Music Organizer Pro** est une application professionnelle pour organiser vos MP3 :
- 🎯 Simple à utiliser
- 🏗️ Architecture modulaire
- 📚 Bien documenté
- 🧪 Testable
- 🚀 Performant

**Profitez de votre musique bien organisée ! 🎉**
