# 🏗️ Architecture du Projet

## 🎯 Vue d'Ensemble

Music Organizer Pro est construit avec une **architecture modulaire** pour faciliter la maintenance et l'évolution.

---

## 📁 Structure des Fichiers

```
bot/
├── app.py                          # 🚀 Point d'entrée principal
├── requirements.txt                # 📦 Dépendances
├── install_deps.bat               # 🔧 Script d'installation
├── install_deps.ps1               # 🔧 Script PowerShell
│
├── music_organizer/                # 📚 Package principal
│   ├── __init__.py                 # Exports du package
│   ├── parser.py                   # 🔍 Parsing des métadonnées
│   ├── organizer.py                # 📂 Organisation des fichiers
│   ├── monitor.py                  # 👁️ Surveillance des fenêtres
│   └── auto_saver.py               # 🤖 Automatisation "Save As"
│
└── docs/                           # 📖 Documentation
    ├── 00_INDEX.md                 # Table des matières
    ├── 01_QUICK_START.md           # Démarrage rapide
    ├── 02_INSTALLATION.md          # Installation
    ├── 03_USER_GUIDE.md            # Guide utilisateur
    ├── 04_FILENAME_FORMATS.md      # Formats
    ├── 05_AUTO_SAVE.md             # Auto-Save
    ├── 06_ARCHITECTURE.md          # Architecture (ce fichier)
    ├── 07_COMMANDS.md              # Commandes
    ├── 08_API.md                   # API Reference
    ├── 09_TROUBLESHOOTING.md       # Dépannage
    └── 10_FAQ.md                   # FAQ
```

---

## 🧩 Modules

### **1. app.py** - Application Principale

**Responsabilité:** Interface graphique et coordination

**Classe principale:** `MusicOrganizerApp`

**Fonctionnalités:**
- Interface Tkinter
- Gestion des événements utilisateur
- Coordination entre les modules
- Affichage des logs

**Dépendances:**
- `tkinter` (GUI)
- `music_organizer.parser`
- `music_organizer.organizer`
- `music_organizer.monitor`

---

### **2. parser.py** - Extraction des Métadonnées

**Responsabilité:** Parser les noms de fichiers

**Classe principale:** `MetadataParser`

**Méthodes clés:**
```python
parse(filename: str) -> tuple
    # Extrait: (artist, album, title, year)
    # Exemple: "art=Drake N=Song.mp3" → ("Drake", "Unknown Album", "Song", "Unknown")
```

**Format supporté:**
- `art=` - Artiste (obligatoire)
- `N=` - Titre (obligatoire)
- `alb=` - Album (optionnel)
- `Y=` - Année (optionnel)

**Dépendances:**
- `re` (regex)

---

### **3. organizer.py** - Organisation des Fichiers

**Responsabilité:** Scanner et organiser les MP3

**Classe principale:** `MusicOrganizer`

**Méthodes clés:**
```python
scan() -> list
    # Scanne le dossier et retourne la liste des chansons

organize() -> dict
    # Organise les fichiers en Artiste/Album/Titre.mp3
    # Retourne: {"success": int, "errors": int}

get_stats() -> dict
    # Retourne les statistiques
    # {"total": int, "artists": int, "albums": int}
```

**Workflow:**
1. Scanner le dossier récursivement
2. Parser chaque nom de fichier
3. Créer la structure Artiste/Album/
4. Déplacer le fichier
5. Mettre à jour les tags ID3

**Dépendances:**
- `os` (système de fichiers)
- `shutil` (déplacement de fichiers)
- `mutagen` (tags ID3)
- `music_organizer.parser`

---

### **4. monitor.py** - Surveillance des Fenêtres

**Responsabilité:** Détecter les fenêtres "Save As"

**Classe principale:** `DownloadMonitor`

**Méthodes clés:**
```python
start()
    # Démarre la surveillance dans un thread

stop()
    # Arrête la surveillance

set_debug_mode(debug: bool)
    # Active/désactive le mode debug
```

**Workflow:**
1. Thread de surveillance en arrière-plan
2. Utilise `win32gui` pour lister les fenêtres
3. Filtre par mots-clés ("wants to save", "Save As")
4. Appelle `AutoSaver` quand détecté

**Dépendances:**
- `win32gui` (détection de fenêtres)
- `threading` (exécution parallèle)
- `music_organizer.auto_saver`

---

### **5. auto_saver.py** - Automatisation "Save As"

**Responsabilité:** Automatiser le processus de sauvegarde

**Classe principale:** `AutoSaver`

**Méthodes clés:**
```python
activate_save_window() -> bool
    # Active la fenêtre "Save As"

auto_save(verify_path: bool, auto_click_save: bool) -> bool
    # Automatise le collage et la sauvegarde

verify_save_path() -> bool
    # Vérifie que le chemin contient "Music\itunes"

click_save_button() -> bool
    # Clique sur le bouton Save (Alt+S)
```

**Workflow:**
1. Chercher la fenêtre "Save As"
2. Activer la fenêtre (premier plan)
3. Coller le nom (Ctrl+V)
4. Vérifier le chemin (Alt+D, Ctrl+C)
5. Cliquer sur Save (Alt+S)

**Dépendances:**
- `pyautogui` (simulation clavier)
- `pyperclip` (lecture clipboard)
- `win32gui` (activation de fenêtre)

---

## 🔄 Flux de Données

### **Workflow Complet**

```
1. Utilisateur télécharge une chanson
   ↓
2. Chrome Extension V2 génère le nom
   "art=Drake alb=Views N=OneDance Y=2016.mp3"
   ↓
3. Nom copié dans le clipboard
   ↓
4. Fenêtre "Save As" s'ouvre
   ↓
5. monitor.py détecte la fenêtre (win32gui)
   ↓
6. auto_saver.py active la fenêtre
   ↓
7. auto_saver.py colle le nom (Ctrl+V)
   ↓
8. auto_saver.py vérifie le chemin
   ↓
9. auto_saver.py clique sur Save (Alt+S)
   ↓
10. Fichier sauvegardé dans Music\itunes
   ↓
11. Utilisateur lance app.py
   ↓
12. Sélectionne le dossier Music\itunes
   ↓
13. organizer.py scanne le dossier
   ↓
14. parser.py extrait les métadonnées
   ↓
15. organizer.py crée Artiste/Album/
   ↓
16. organizer.py déplace le fichier
   ↓
17. organizer.py met à jour les tags ID3
   ↓
18. Fichier organisé: Drake/Views/OneDance.mp3
```

---

## 🎨 Design Patterns

### **1. Séparation des Responsabilités**

Chaque module a une responsabilité unique :
- `parser.py` → Parsing
- `organizer.py` → Organisation
- `monitor.py` → Surveillance
- `auto_saver.py` → Automatisation
- `app.py` → Coordination

### **2. Callbacks**

Les modules communiquent via callbacks :
```python
monitor = DownloadMonitor(
    notification_callback=self.show_notification,
    log_callback=self.log
)
```

### **3. Threading**

Les tâches longues s'exécutent dans des threads :
```python
thread = threading.Thread(target=self._monitor_loop, daemon=True)
thread.start()
```

### **4. Gestion d'Erreurs**

Chaque module gère ses erreurs :
```python
try:
    # Opération
except Exception as e:
    self.log(f"❌ Erreur: {str(e)}")
    return False
```

---

## 🔧 Technologies

### **Langage**
- Python 3.8+

### **Interface Graphique**
- Tkinter (inclus dans Python)

### **Bibliothèques Externes**
- `mutagen` - Tags ID3
- `pyautogui` - Automatisation clavier
- `pyperclip` - Clipboard
- `pywin32` - API Windows

### **Modules Standard**
- `os` - Système de fichiers
- `shutil` - Opérations fichiers
- `re` - Expressions régulières
- `threading` - Parallélisme
- `subprocess` - Exécution de commandes

---

## 📊 Diagramme de Classes

```
┌─────────────────────────┐
│  MusicOrganizerApp      │
│  (app.py)               │
│                         │
│  - root: Tk             │
│  - monitor: Monitor     │
│  - organizer: Organizer │
│                         │
│  + create_widgets()     │
│  + setup_monitor()      │
│  + log()                │
└────────┬────────────────┘
         │
         │ utilise
         ├────────────────────────────────┐
         │                                │
         ▼                                ▼
┌─────────────────────┐      ┌─────────────────────┐
│  DownloadMonitor    │      │  MusicOrganizer     │
│  (monitor.py)       │      │  (organizer.py)     │
│                     │      │                     │
│  - auto_saver       │      │  - parser           │
│  - is_monitoring    │      │  - songs_found      │
│                     │      │                     │
│  + start()          │      │  + scan()           │
│  + stop()           │      │  + organize()       │
│  + set_debug_mode() │      │  + get_stats()      │
└──────┬──────────────┘      └──────┬──────────────┘
       │                            │
       │ utilise                    │ utilise
       ▼                            ▼
┌─────────────────────┐      ┌─────────────────────┐
│  AutoSaver          │      │  MetadataParser     │
│  (auto_saver.py)    │      │  (parser.py)        │
│                     │      │                     │
│  + activate_window()│      │  + parse()          │
│  + auto_save()      │      │                     │
│  + verify_path()    │      │                     │
│  + click_save()     │      │                     │
└─────────────────────┘      └─────────────────────┘
```

---

## 🚀 Points d'Extension

### **Ajouter un Nouveau Format**

Modifier `parser.py` :
```python
def parse(self, filename: str) -> tuple:
    # Ajouter votre logique ici
    genre_match = re.search(r"genre=([^=]+)", filename)
```

### **Ajouter une Nouvelle Action**

Créer un nouveau module dans `music_organizer/` :
```python
# music_organizer/new_feature.py
class NewFeature:
    def __init__(self):
        pass
    
    def do_something(self):
        pass
```

Exporter dans `__init__.py` :
```python
from .new_feature import NewFeature
__all__ = [..., 'NewFeature']
```

### **Modifier l'Interface**

Modifier `app.py` :
```python
def _create_new_section(self):
    # Ajouter votre section ici
    pass
```

---

## 📈 Performance

### **Optimisations**

1. **Threading** - Les tâches longues ne bloquent pas l'UI
2. **Lazy Loading** - Les modules sont chargés à la demande
3. **Caching** - Les fenêtres détectées sont mises en cache

### **Limitations**

- **Mono-thread UI** - Tkinter n'est pas thread-safe
- **Polling** - Le scanner vérifie toutes les 1 seconde
- **Regex** - Le parsing peut être lent sur de gros fichiers

---

## ✅ Résumé

**Architecture modulaire avec:**
- ✅ Séparation des responsabilités
- ✅ Communication par callbacks
- ✅ Threading pour les tâches longues
- ✅ Gestion d'erreurs robuste
- ✅ Code testable et maintenable

**Facile à étendre et à maintenir ! 🎉**
