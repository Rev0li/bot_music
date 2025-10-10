# 🚀 GrabSong V3 - Démarrage Rapide

## 📦 Installation en 2 commandes

```bash
cd V3/python-server
./install.sh
```

Le script `install.sh` configure automatiquement :
- ✅ Environnement virtuel Python
- ✅ Installation des dépendances (Flask, yt-dlp, mutagen, Pillow)
- ✅ Vérification de FFmpeg
- ✅ Création des dossiers temp/ et music/
- ✅ Test des modules

## ▶️ Démarrage du serveur

```bash
cd V3/python-server
./start.sh
```

Le serveur démarre sur **http://localhost:5000**

## 🔧 Installation de FFmpeg (si nécessaire)

### Sur WSL/Ubuntu
```bash
sudo apt update
sudo apt install ffmpeg
```

### Sur Windows
```powershell
# Avec Winget (recommandé)
winget install ffmpeg

# Ou avec Chocolatey
choco install ffmpeg
```

## 🎵 Utilisation

### 1. Charger l'extension Chrome
1. Ouvrir `chrome://extensions/`
2. Activer **Mode développeur**
3. Cliquer **Charger l'extension non empaquetée**
4. Sélectionner le dossier `V3/chrome-extension/`

### 2. Télécharger de la musique
1. Aller sur https://music.youtube.com
2. Lancer une musique
3. Cliquer sur le widget **🎵 GrabSong**
4. Cliquer sur **⬇️ Télécharger**
5. Vérifier/modifier les métadonnées
6. Cliquer sur **💾 Télécharger**

### 3. Résultat
Les fichiers sont automatiquement organisés dans :
```
music/
└── Artist/
    └── Album/
        └── Title.mp3  (avec tags ID3 et pochette)
```

## 🛠️ Commandes utiles

```bash
# Démarrer le serveur
./start.sh

# Arrêter le serveur
Ctrl + C

# Réinstaller les dépendances
./install.sh

# Activer manuellement l'environnement virtuel
source venv/bin/activate

# Désactiver l'environnement virtuel
deactivate

# Tester la connexion au serveur
curl http://localhost:5000/ping

# Voir les statistiques de la bibliothèque
curl http://localhost:5000/stats
```

## 🐛 Dépannage

### Erreur : "externally-managed-environment"
✅ **Solution :** Utilisez `./install.sh` qui crée automatiquement un environnement virtuel

### Erreur : "FFmpeg not found"
✅ **Solution :** Installez FFmpeg (voir section ci-dessus)

### Erreur : "Permission denied: ./install.sh"
✅ **Solution :**
```bash
chmod +x install.sh start.sh
./install.sh
```

### Le serveur ne démarre pas
✅ **Solution :** Vérifiez que le port 5000 n'est pas utilisé
```bash
# Sur WSL/Linux
sudo lsof -i :5000

# Sur Windows PowerShell
netstat -ano | findstr :5000
```

### L'extension ne détecte pas le serveur
✅ **Solution :** Vérifiez que le serveur est bien lancé
```bash
curl http://localhost:5000/ping
```

## 📊 Structure du projet

```
V3/
├── chrome-extension/      # Extension Chrome
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   └── popup.html/js
│
├── python-server/         # Serveur Python
│   ├── app.py            # Serveur Flask
│   ├── downloader.py     # Module yt-dlp
│   ├── organizer.py      # Organisation des fichiers
│   ├── requirements.txt  # Dépendances
│   ├── install.sh        # 🆕 Installation automatique
│   └── start.sh          # 🆕 Démarrage rapide
│
├── temp/                 # Téléchargements temporaires
└── music/                # Bibliothèque musicale
```

## 🎯 Workflow complet

```
1. ./install.sh           → Installation
2. ./start.sh             → Démarrage du serveur
3. Charger l'extension    → chrome://extensions/
4. YouTube Music          → Télécharger de la musique
5. Ctrl+C                 → Arrêter le serveur
```

## 💡 Astuces

- **Démarrage rapide :** Créez un alias dans votre `.bashrc` ou `.zshrc`
  ```bash
  alias grabsong='cd /mnt/c/Users/Molim/Music/bot/V3/python-server && ./start.sh'
  ```

- **Lancement automatique :** Ajoutez `./start.sh` à votre script de démarrage

- **Logs :** Les logs s'affichent en temps réel dans le terminal

## 🎵 Prêt à télécharger de la musique !

Pour toute question, voir :
- [README.md](README.md) - Documentation complète
- [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) - Installation Windows détaillée
- [python-server/README.md](python-server/README.md) - Documentation du serveur
