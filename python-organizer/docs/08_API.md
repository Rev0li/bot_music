# 📖 API Reference

## 🎯 Vue d'Ensemble

Documentation complète de l'API du package `music_organizer`.

---

## 📦 Package: music_organizer

### Exports

```python
from music_organizer import MetadataParser
from music_organizer import MusicOrganizer
from music_organizer import DownloadMonitor
from music_organizer import AutoSaver  # Si pyautogui disponible
```

---

## 🔍 MetadataParser

### Description

Parse les noms de fichiers pour extraire les métadonnées.

### Import

```python
from music_organizer import MetadataParser
```

### Constructeur

```python
parser = MetadataParser()
```

**Paramètres:** Aucun

---

### Méthode: `parse(filename)`

Extrait les métadonnées d'un nom de fichier.

**Signature:**
```python
def parse(self, filename: str) -> tuple[str, str, str, str]
```

**Paramètres:**
- `filename` (str): Nom du fichier à parser

**Retour:**
- `tuple`: (artist, album, title, year)
  - `artist` (str): Nom de l'artiste
  - `album` (str): Nom de l'album (ou "Unknown Album")
  - `title` (str): Titre de la chanson
  - `year` (str): Année (ou "Unknown")

**Retourne `(None, None, None, None)` si:**
- `art=` manquant
- `N=` manquant

**Exemples:**

```python
parser = MetadataParser()

# Format complet
result = parser.parse("art=Drake alb=Views N=OneDance Y=2016.mp3")
# ("Drake", "Views", "OneDance", "2016")

# Format minimal
result = parser.parse("art=Drake N=OneDance.mp3")
# ("Drake", "Unknown Album", "OneDance", "Unknown")

# Format invalide
result = parser.parse("Drake - OneDance.mp3")
# (None, None, None, None)
```

---

## 📂 MusicOrganizer

### Description

Organise les fichiers MP3 en structure Artiste/Album/Titre.

### Import

```python
from music_organizer import MusicOrganizer
```

### Constructeur

```python
organizer = MusicOrganizer(source_folder, log_callback=None)
```

**Paramètres:**
- `source_folder` (str): Chemin du dossier source
- `log_callback` (Callable, optional): Fonction pour logger les messages

---

### Méthode: `scan()`

Scanne le dossier pour trouver les fichiers MP3.

**Signature:**
```python
def scan(self) -> list[dict]
```

**Retour:**
- `list[dict]`: Liste des chansons trouvées
  - Chaque dict contient: `path`, `filename`, `artist`, `album`, `title`, `year`

**Exemple:**

```python
organizer = MusicOrganizer("C:\\Music\\Downloads")
songs = organizer.scan()

for song in songs:
    print(f"{song['artist']} - {song['title']}")
```

---

### Méthode: `organize()`

Organise les fichiers scannés.

**Signature:**
```python
def organize(self) -> dict
```

**Retour:**
- `dict`: Résultats de l'organisation
  - `success` (int): Nombre de fichiers organisés avec succès
  - `errors` (int): Nombre d'erreurs

**Exemple:**

```python
organizer = MusicOrganizer("C:\\Music\\Downloads")
organizer.scan()
results = organizer.organize()

print(f"Succès: {results['success']}")
print(f"Erreurs: {results['errors']}")
```

---

### Méthode: `get_stats()`

Retourne les statistiques des chansons scannées.

**Signature:**
```python
def get_stats(self) -> dict
```

**Retour:**
- `dict`: Statistiques
  - `total` (int): Nombre total de chansons
  - `artists` (int): Nombre d'artistes uniques
  - `albums` (int): Nombre d'albums uniques

**Exemple:**

```python
organizer = MusicOrganizer("C:\\Music\\Downloads")
organizer.scan()
stats = organizer.get_stats()

print(f"Total: {stats['total']} chansons")
print(f"Artistes: {stats['artists']}")
print(f"Albums: {stats['albums']}")
```

---

## 👁️ DownloadMonitor

### Description

Surveille les fenêtres "Enregistrer sous" et automatise le téléchargement.

### Import

```python
from music_organizer import DownloadMonitor
```

### Constructeur

```python
monitor = DownloadMonitor(
    notification_callback=None,
    log_callback=None,
    auto_paste=True,
    auto_save=False
)
```

**Paramètres:**
- `notification_callback` (Callable, optional): Fonction appelée lors d'une détection
- `log_callback` (Callable, optional): Fonction pour logger les messages
- `auto_paste` (bool): Coller automatiquement le nom de fichier (défaut: True)
- `auto_save` (bool): Cliquer automatiquement sur Save (défaut: False)

---

### Méthode: `start()`

Démarre la surveillance des fenêtres.

**Signature:**
```python
def start(self) -> None
```

**Exemple:**

```python
def on_detected(window_title):
    print(f"Fenêtre détectée: {window_title}")

monitor = DownloadMonitor(notification_callback=on_detected)
monitor.start()
```

---

### Méthode: `stop()`

Arrête la surveillance.

**Signature:**
```python
def stop(self) -> None
```

**Exemple:**

```python
monitor.stop()
```

---

### Méthode: `is_active()`

Vérifie si le moniteur est actif.

**Signature:**
```python
def is_active(self) -> bool
```

**Retour:**
- `bool`: True si actif, False sinon

**Exemple:**

```python
if monitor.is_active():
    print("Moniteur actif")
```

---

### Méthode: `set_debug_mode(debug)`

Active/désactive le mode debug.

**Signature:**
```python
def set_debug_mode(self, debug: bool) -> None
```

**Paramètres:**
- `debug` (bool): True pour activer, False pour désactiver

**Exemple:**

```python
monitor.set_debug_mode(True)  # Affiche toutes les fenêtres
```

---

## 🤖 AutoSaver

### Description

Automatise le processus de sauvegarde dans la fenêtre "Enregistrer sous".

### Import

```python
from music_organizer import AutoSaver
```

### Constructeur

```python
saver = AutoSaver(log_callback=None)
```

**Paramètres:**
- `log_callback` (Callable, optional): Fonction pour logger les messages

---

### Méthode: `activate_save_window()`

Active la fenêtre "Save As" (la met au premier plan).

**Signature:**
```python
def activate_save_window(self) -> bool
```

**Retour:**
- `bool`: True si fenêtre trouvée et activée, False sinon

**Exemple:**

```python
saver = AutoSaver()
if saver.activate_save_window():
    print("Fenêtre activée")
```

---

### Méthode: `auto_save(verify_path, auto_click_save)`

Automatise la sauvegarde du fichier.

**Signature:**
```python
def auto_save(self, verify_path: bool = True, auto_click_save: bool = False) -> bool
```

**Paramètres:**
- `verify_path` (bool): Vérifier que le chemin contient "Music/itunes"
- `auto_click_save` (bool): Cliquer automatiquement sur Save

**Retour:**
- `bool`: True si succès, False sinon

**Exemple:**

```python
saver = AutoSaver()

# Coller le nom et vérifier le chemin
saver.auto_save(verify_path=True, auto_click_save=False)

# Coller et cliquer automatiquement
saver.auto_save(verify_path=True, auto_click_save=True)
```

---

### Méthode: `verify_save_path()`

Vérifie que le chemin de sauvegarde contient "Music\\itunes".

**Signature:**
```python
def verify_save_path(self) -> bool
```

**Retour:**
- `bool`: True si le chemin est correct, False sinon

**Exemple:**

```python
saver = AutoSaver()
if saver.verify_save_path():
    print("Chemin correct")
```

---

### Méthode: `click_save_button()`

Clique sur le bouton "Save" / "Enregistrer".

**Signature:**
```python
def click_save_button(self) -> bool
```

**Retour:**
- `bool`: True si le bouton a été trouvé et cliqué, False sinon

**Exemple:**

```python
saver = AutoSaver()
saver.click_save_button()
```

---

## 🎓 Exemples Complets

### Exemple 1: Parser Simple

```python
from music_organizer import MetadataParser

parser = MetadataParser()
artist, album, title, year = parser.parse("art=Drake alb=Views N=OneDance Y=2016.mp3")

print(f"Artiste: {artist}")
print(f"Album: {album}")
print(f"Titre: {title}")
print(f"Année: {year}")
```

---

### Exemple 2: Organisation Complète

```python
from music_organizer import MusicOrganizer

def log_message(msg):
    print(msg)

# Créer l'organisateur
organizer = MusicOrganizer("C:\\Music\\Downloads", log_callback=log_message)

# Scanner les fichiers
songs = organizer.scan()
print(f"Trouvé: {len(songs)} chansons")

# Afficher les statistiques
stats = organizer.get_stats()
print(f"Artistes: {stats['artists']}")
print(f"Albums: {stats['albums']}")

# Organiser
results = organizer.organize()
print(f"Succès: {results['success']}")
print(f"Erreurs: {results['errors']}")
```

---

### Exemple 3: Moniteur avec Callbacks

```python
from music_organizer import DownloadMonitor

def on_window_detected(window_title):
    print(f"🔔 Fenêtre détectée: {window_title}")

def log_message(msg):
    print(msg)

# Créer le moniteur
monitor = DownloadMonitor(
    notification_callback=on_window_detected,
    log_callback=log_message,
    auto_paste=True,
    auto_save=False
)

# Démarrer la surveillance
monitor.start()

# Activer le mode debug
monitor.set_debug_mode(True)

# Vérifier le status
if monitor.is_active():
    print("Moniteur actif")

# Arrêter plus tard
# monitor.stop()
```

---

### Exemple 4: AutoSaver Manuel

```python
from music_organizer import AutoSaver

def log_message(msg):
    print(msg)

# Créer l'auto-saver
saver = AutoSaver(log_callback=log_message)

# Activer la fenêtre
if saver.activate_save_window():
    print("Fenêtre activée")
    
    # Coller le nom et vérifier
    if saver.auto_save(verify_path=True, auto_click_save=False):
        print("Nom collé, cliquez sur Save manuellement")
```

---

## 🔧 Types et Constantes

### Types de Retour

```python
# MetadataParser.parse()
tuple[str, str, str, str]  # (artist, album, title, year)

# MusicOrganizer.scan()
list[dict]  # [{"path": str, "filename": str, "artist": str, ...}]

# MusicOrganizer.organize()
dict  # {"success": int, "errors": int}

# MusicOrganizer.get_stats()
dict  # {"total": int, "artists": int, "albums": int}
```

### Mots-clés de Détection

```python
# DownloadMonitor keywords
["wants to save", "Save As", "Enregistrer sous", "Enregistrer", "Save"]
```

---

## ✅ Résumé

**API complète avec:**
- ✅ `MetadataParser` - Parsing des noms
- ✅ `MusicOrganizer` - Organisation des fichiers
- ✅ `DownloadMonitor` - Surveillance des fenêtres
- ✅ `AutoSaver` - Automatisation "Save As"

**Facile à utiliser et bien documenté ! 📚**
