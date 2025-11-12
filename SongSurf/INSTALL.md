# 📦 Guide d'Installation - SongSurf

## 🎯 Choisissez Votre Méthode

### 🐳 Option 1 : Docker (Le Plus Simple)

**Avantages :**
- ✅ Aucune installation manuelle
- ✅ Fonctionne partout (Linux, Mac, Windows)
- ✅ Pas de pollution du PC

**Prérequis :** Docker installé

```bash
./docker-start.sh
```

---

### 🐍 Option 2 : Installation Python

**Avantages :**
- ✅ Contrôle total
- ✅ Pas besoin de Docker
- ✅ Installation locale possible (sans sudo)

**Prérequis :** Python 3.8+

```bash
cd python-server
./install.sh
```

---

## 📋 Détails de l'Installation Python

### Étape 1 : Vérification de Python

Le script vérifie automatiquement si Python 3 est installé.

**Si Python manque :**
- **Linux** : Installation automatique via `apt`
- **macOS** : Installation via Homebrew
- **Windows** : Message d'erreur avec lien de téléchargement

### Étape 2 : Installation de FFmpeg

Le script détecte votre OS et propose **3 options** :

#### Option 1 : Installation Système (Recommandé)

**Avec droits sudo/admin**

- **Linux (Debian/Ubuntu)** : `sudo apt install ffmpeg`
- **Linux (RedHat/Fedora)** : `sudo dnf install ffmpeg`
- **Linux (Arch)** : `sudo pacman -S ffmpeg`
- **macOS** : `brew install ffmpeg`

#### Option 2 : Installation Locale (Sans Sudo)

**Pour école/entreprise sans droits admin**

- Télécharge FFmpeg statique depuis https://johnvansickle.com/ffmpeg/
- Installe dans `~/.local/ffmpeg`
- Détecté automatiquement par `start.sh`
- Supporte x86_64 et ARM64

#### Option 3 : Ignorer

**Si vous voulez installer FFmpeg manuellement plus tard**

⚠️ La conversion MP3 ne fonctionnera pas sans FFmpeg

### Étape 3 : Environnement Virtuel Python

Le script crée automatiquement un environnement virtuel Python isolé :

```bash
python3 -m venv venv
source venv/bin/activate
```

### Étape 4 : Installation des Dépendances

Installation automatique depuis `requirements.txt` :

- `flask` - Serveur web
- `yt-dlp` - Téléchargement YouTube
- `mutagen` - Métadonnées audio
- `Pillow` - Traitement d'images

### Étape 5 : Création des Dossiers

```bash
mkdir -p ../music ../temp
```

- `music/` - Bibliothèque musicale
- `temp/` - Fichiers temporaires

### Étape 6 : Vérification

Le script teste que tous les modules Python sont importables.

---

## 🚀 Démarrage

### Avec Docker

```bash
./docker-start.sh
```

Le serveur démarre sur **http://localhost:8080**

### Sans Docker

```bash
cd python-server
./start.sh
```

Le script :
1. Active l'environnement virtuel
2. Détecte FFmpeg (système ou local)
3. Vérifie les dépendances Python
4. Crée les dossiers nécessaires
5. Démarre le serveur Flask

---

## 🔍 Détection OS

Le script `install.sh` détecte automatiquement :

| Variable | Valeurs Possibles | OS |
|----------|-------------------|-----|
| `$OSTYPE` | `linux-gnu*` | Linux |
| `$OSTYPE` | `darwin*` | macOS |
| `$OSTYPE` | `msys`, `cygwin` | Windows (Git Bash) |

### Détection Distribution Linux

| Fichier | Distribution |
|---------|-------------|
| `/etc/debian_version` | Debian/Ubuntu |
| `/etc/redhat-release` | RedHat/Fedora/CentOS |
| `/etc/arch-release` | Arch Linux |

---

## 🏫 Cas d'Usage : École/Entreprise

**Problème :** Pas de droits sudo/admin

**Solution :** Installation locale de FFmpeg

### Étape par Étape

1. **Lancer l'installation**
   ```bash
   cd python-server
   ./install.sh
   ```

2. **Choisir l'option 2** quand FFmpeg est demandé
   ```
   Options d'installation FFmpeg:
     1. Installation système (avec sudo) - Recommandé
     2. Installation locale (sans sudo) - Pour école/entreprise  ← CHOISIR CELLE-CI
     3. Ignorer (installer manuellement plus tard)
   
   Choisissez une option (1/2/3): 2
   ```

3. **Attendre le téléchargement**
   - FFmpeg est téléchargé depuis johnvansickle.com
   - Extraction automatique dans `~/.local/ffmpeg`
   - Aucun privilège requis !

4. **Démarrer normalement**
   ```bash
   ./start.sh
   ```
   
   Le script détecte automatiquement FFmpeg local et l'ajoute au PATH.

---

## ❓ Dépannage

### Python non trouvé

**Linux :**
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

**macOS :**
```bash
brew install python3
```

### FFmpeg : Installation locale échoue

**Vérifier wget/curl :**
```bash
command -v wget || command -v curl
```

**Installer wget :**
```bash
# Linux
sudo apt install wget

# macOS
brew install wget
```

### Erreur de permission sur venv

```bash
rm -rf venv
python3 -m venv venv
```

### Port 8080 déjà utilisé

**Modifier le port dans `app.py` :**
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)  # Changez 8080 → 9090
```

---

## 📊 Résumé des Fichiers

| Fichier | Description |
|---------|-------------|
| `install.sh` | Installation complète (Python + FFmpeg + dépendances) |
| `start.sh` | Démarrage du serveur |
| `docker-start.sh` | Démarrage avec Docker |
| `docker-stop.sh` | Arrêt Docker |
| `requirements.txt` | Liste des dépendances Python |

---

## ✅ Checklist d'Installation

- [ ] Python 3.8+ installé
- [ ] FFmpeg installé (système ou local)
- [ ] Environnement virtuel créé
- [ ] Dépendances Python installées
- [ ] Dossiers `music/` et `temp/` créés
- [ ] Serveur démarre sans erreur
- [ ] Dashboard accessible sur http://localhost:8080
- [ ] Extension Chrome installée

---

**Besoin d'aide ?** Consultez le [README.md](README.md) ou [DOCKER.md](DOCKER.md)
