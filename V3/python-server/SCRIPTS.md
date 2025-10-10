# 📜 Scripts d'Installation et de Démarrage

Ce dossier contient des scripts pour faciliter l'installation et le démarrage du serveur Python.

## 📋 Liste des scripts

### 1. `install.sh` - Installation automatique

**Description :** Configure automatiquement l'environnement de développement

**Fonctionnalités :**
- ✅ Vérifie Python 3.8+
- ✅ Vérifie FFmpeg
- ✅ Crée l'environnement virtuel (`venv/`)
- ✅ Met à jour pip
- ✅ Installe toutes les dépendances
- ✅ Crée les dossiers `temp/` et `music/`
- ✅ Teste l'importation des modules

**Usage :**
```bash
chmod +x install.sh
./install.sh
```

**Options interactives :**
- Recréer l'environnement virtuel si existant
- Continuer sans FFmpeg (non recommandé)

**Sortie :**
```
============================================
🎵 GrabSong V3 - Installation
============================================
▶ Vérification de Python...
✅ Python 3.12.0 détecté
▶ Vérification de FFmpeg...
✅ FFmpeg 6.1.1 détecté
▶ Création de l'environnement virtuel...
✅ Environnement virtuel créé
▶ Activation de l'environnement virtuel...
✅ Environnement virtuel activé
▶ Mise à jour de pip...
✅ pip 24.0
▶ Installation des dépendances...
✅ Dépendances installées
▶ Création des dossiers...
✅ Dossiers créés (temp/, music/)
▶ Test de l'importation des modules...
✅ Tous les modules fonctionnent

============================================
✅ Installation terminée avec succès !
============================================

ℹ️  Pour démarrer le serveur:
  source venv/bin/activate
  python app.py
```

---

### 2. `start.sh` - Démarrage rapide

**Description :** Démarre le serveur Python avec l'environnement virtuel

**Fonctionnalités :**
- ✅ Vérifie que `venv/` existe
- ✅ Active automatiquement l'environnement virtuel
- ✅ Lance le serveur Flask

**Usage :**
```bash
chmod +x start.sh
./start.sh
```

**Sortie :**
```
▶ Activation de l'environnement virtuel...
✅ Environnement virtuel activé

============================================
🎵 GrabSong V3 - Serveur Python
============================================

▶ Démarrage du serveur...

============================================================
🎵 GrabSong V3 - Serveur Python
============================================================
📁 Dossier temporaire: /mnt/c/Users/Molim/Music/bot/V3/temp
📁 Bibliothèque musicale: /mnt/c/Users/Molim/Music/bot/V3/music
============================================================
🚀 Serveur démarré sur http://localhost:5000
============================================================

💡 Endpoints disponibles:
   GET  /ping           → Test de connexion
   GET  /status         → Statut du téléchargement
   POST /download       → Lancer un téléchargement
   POST /cleanup        → Nettoyer le dossier temp/
   GET  /stats          → Statistiques de la bibliothèque
   POST /browse_folder  → Sélectionner un dossier
```

**Arrêt :**
```bash
Ctrl + C
```

---

## 🔄 Workflow recommandé

### Première installation
```bash
# 1. Rendre les scripts exécutables
chmod +x install.sh start.sh

# 2. Installer
./install.sh

# 3. Démarrer
./start.sh
```

### Utilisation quotidienne
```bash
# Démarrer le serveur
./start.sh

# Arrêter le serveur
Ctrl + C
```

### Mise à jour des dépendances
```bash
# Réinstaller
./install.sh

# Ou manuellement
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

---

## 🐛 Dépannage

### Erreur : "Permission denied"
```bash
chmod +x install.sh start.sh
```

### Erreur : "venv/ not found" lors du démarrage
```bash
# Lancer d'abord l'installation
./install.sh
```

### Erreur : "Python not found"
```bash
# Sur WSL/Ubuntu
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

### Erreur : "FFmpeg not found"
```bash
# Sur WSL/Ubuntu
sudo apt update
sudo apt install ffmpeg

# Vérifier
ffmpeg -version
```

### Le serveur ne démarre pas
```bash
# Vérifier que le port 5000 n'est pas utilisé
sudo lsof -i :5000

# Ou changer le port dans app.py
```

---

## 📝 Variables d'environnement

Les scripts utilisent les couleurs ANSI pour l'affichage :
- 🔴 Rouge : Erreurs
- 🟢 Vert : Succès
- 🟡 Jaune : Avertissements
- 🔵 Bleu : Informations
- 🟣 Violet : En-têtes
- 🔷 Cyan : Étapes

---

## 🔧 Personnalisation

### Modifier le port du serveur

Éditer `app.py` ligne 385 :
```python
app.run(
    host='localhost',
    port=5001,  # Changer ici
    debug=True,
    use_reloader=False
)
```

### Modifier les dossiers

Éditer `app.py` lignes 44-46 :
```python
BASE_DIR = Path(__file__).parent.parent
TEMP_DIR = BASE_DIR / "temp"
MUSIC_DIR = BASE_DIR / "music"
```

---

## 📚 Fichiers associés

- `requirements.txt` - Liste des dépendances Python
- `app.py` - Serveur Flask principal
- `downloader.py` - Module de téléchargement
- `organizer.py` - Module d'organisation
- `README.md` - Documentation complète

---

## 🎯 Commandes rapides

```bash
# Installation complète
./install.sh

# Démarrage
./start.sh

# Test de connexion
curl http://localhost:5000/ping

# Statistiques
curl http://localhost:5000/stats

# Nettoyage
curl -X POST http://localhost:5000/cleanup
```

---

**Pour plus d'informations, voir [README.md](README.md)**
