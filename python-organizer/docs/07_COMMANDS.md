# ⚡ Commandes PowerShell - Référence

## 🚀 Installation Rapide

```powershell
cd C:\Users\Molim\Music\bot\bot
pip install -r requirements.txt
python app.py
```

---

## 📦 Gestion de Python

### Vérifications
```powershell
# Vérifier la version de Python
python --version

# Vérifier où Python est installé
where python

# Vérifier pip
pip --version
```

### Exécution
```powershell
# Lancer l'application
python app.py

# Exécuter une commande Python
python -c "print('Hello')"

# Lancer Python en mode interactif
python
```

---

## 📥 Gestion de pip

### Installation
```powershell
# Installer un package
pip install mutagen

# Installer depuis requirements.txt
pip install -r requirements.txt

# Installer une version spécifique
pip install mutagen==1.47.0

# Installer avec mise à jour
pip install --upgrade mutagen

# Installer pour l'utilisateur actuel (sans admin)
pip install --user mutagen
```

### Informations
```powershell
# Lister tous les packages
pip list

# Chercher un package
pip list | findstr mutagen

# Voir les détails d'un package
pip show mutagen

# Voir les packages obsolètes
pip list --outdated
```

### Désinstallation
```powershell
# Désinstaller un package
pip uninstall mutagen

# Désinstaller sans confirmation
pip uninstall -y mutagen
```

### Mise à Jour
```powershell
# Mettre à jour pip
python -m pip install --upgrade pip

# Mettre à jour un package
pip install --upgrade mutagen
```

---

## 🌐 Environnement Virtuel

### Création
```powershell
# Créer un environnement virtuel
python -m venv venv

# Créer avec un nom personnalisé
python -m venv mon_env
```

### Activation
```powershell
# Activer (PowerShell)
.\venv\Scripts\Activate.ps1

# Activer (CMD)
.\venv\Scripts\activate.bat

# Si erreur de politique d'exécution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Utilisation
```powershell
# Après activation
pip install -r requirements.txt
python app.py

# Vérifier que vous êtes dans le venv
where python
# Doit afficher: ...\venv\Scripts\python.exe
```

### Désactivation
```powershell
# Désactiver l'environnement
deactivate
```

---

## 📂 Navigation

### Dossiers
```powershell
# Afficher le dossier actuel
pwd

# Lister les fichiers
dir
ls  # Alias

# Changer de dossier
cd C:\Users\Molim\Music\bot\bot

# Remonter d'un niveau
cd ..

# Créer un dossier
mkdir nouveau_dossier
New-Item -ItemType Directory -Path "nouveau_dossier"

# Supprimer un dossier vide
rmdir dossier

# Supprimer un dossier avec contenu
Remove-Item -Recurse -Force dossier
```

### Fichiers
```powershell
# Copier un fichier
Copy-Item source.txt destination.txt

# Déplacer un fichier
Move-Item source.txt destination.txt

# Renommer un fichier
Rename-Item ancien.txt nouveau.txt

# Supprimer un fichier
Remove-Item fichier.txt

# Créer un fichier vide
New-Item -ItemType File fichier.txt

# Afficher le contenu
Get-Content fichier.txt
cat fichier.txt  # Alias

# Éditer un fichier
notepad fichier.txt
```

---

## 🔍 Recherche

### Fichiers
```powershell
# Chercher un fichier
dir -Recurse -Filter "*.py"

# Chercher dans le contenu
Select-String -Path "*.py" -Pattern "import"

# Filtrer une liste
pip list | findstr mutagen
```

### Processus
```powershell
# Lister les processus Python
Get-Process python

# Tuer un processus
Stop-Process -Name python
```

---

## 🧪 Tests et Vérification

### Tests d'Import
```powershell
# Tester mutagen
python -c "import mutagen; print('✅ OK')"

# Tester pyautogui
python -c "import pyautogui; print('✅ OK')"

# Tester pyperclip
python -c "import pyperclip; print('✅ OK')"

# Tester pywin32
python -c "import win32gui; print('✅ OK')"

# Tester les modules du projet
python -c "from music_organizer import MetadataParser; print('✅ OK')"

# Tester tout en une commande
python -c "import mutagen, pyautogui, pyperclip, win32gui; from music_organizer import MetadataParser; print('✅ Tout OK')"
```

### Vérification Syntaxe
```powershell
# Vérifier la syntaxe d'un fichier
python -m py_compile app.py
```

---

## 📊 Informations Système

### Système
```powershell
# Version de Windows
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"

# Espace disque
Get-PSDrive C

# Mémoire disponible
Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory
```

### Python
```powershell
# Version de Python
python --version

# Chemin de Python
where python

# Informations détaillées
python -c "import sys; print(sys.version)"
```

---

## 🔧 Dépannage

### Permissions
```powershell
# Lancer PowerShell en administrateur
# Clic droit → "Exécuter en tant qu'administrateur"

# Changer la politique d'exécution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Voir la politique actuelle
Get-ExecutionPolicy

# Installer sans droits admin
pip install --user mutagen
```

### Nettoyage
```powershell
# Nettoyer le cache de pip
pip cache purge

# Supprimer les fichiers Python temporaires
Remove-Item -Recurse -Force __pycache__
Remove-Item -Recurse -Force *.pyc

# Réinstaller proprement
pip uninstall -y mutagen
pip install mutagen
```

### Réinitialisation
```powershell
# Supprimer l'environnement virtuel
Remove-Item -Recurse -Force venv

# Recréer
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🎯 Commandes Spécifiques au Projet

### Installation
```powershell
# Installation complète
cd C:\Users\Molim\Music\bot\bot
pip install -r requirements.txt

# Installation avec script
.\install_deps.bat
# ou
.\install_deps.ps1
```

### Lancement
```powershell
# Lancer l'application
python app.py
```

### Tests
```powershell
# Tester le parser
python -c "from music_organizer import MetadataParser; p = MetadataParser(); print(p.parse('art=Drake N=Test.mp3'))"

# Tester l'organisateur
python -c "from music_organizer import MusicOrganizer; print('✅ OK')"

# Tester le moniteur
python -c "from music_organizer import DownloadMonitor; print('✅ OK')"

# Tester l'auto-saver
python -c "from music_organizer import AutoSaver; print('✅ OK')"
```

### Documentation
```powershell
# Voir l'aide d'un module
python -c "from music_organizer import MetadataParser; help(MetadataParser)"

# Exporter les dépendances
pip freeze > requirements.txt

# Compter les lignes de code
(Get-Content music_organizer\*.py | Measure-Object -Line).Lines
```

---

## 🚀 Workflows Complets

### Premier Lancement
```powershell
# 1. Naviguer vers le projet
cd C:\Users\Molim\Music\bot\bot

# 2. Créer l'environnement virtuel (optionnel)
python -m venv venv

# 3. Activer l'environnement
.\venv\Scripts\Activate.ps1

# 4. Mettre à jour pip
python -m pip install --upgrade pip

# 5. Installer les dépendances
pip install -r requirements.txt

# 6. Vérifier l'installation
python -c "from music_organizer import MetadataParser; print('✅ OK')"

# 7. Lancer l'application
python app.py
```

### Lancements Suivants
```powershell
# 1. Naviguer vers le projet
cd C:\Users\Molim\Music\bot\bot

# 2. Activer l'environnement (si utilisé)
.\venv\Scripts\Activate.ps1

# 3. Lancer l'application
python app.py
```

### Mise à Jour
```powershell
# 1. Mettre à jour pip
python -m pip install --upgrade pip

# 2. Mettre à jour les dépendances
pip install --upgrade -r requirements.txt

# 3. Vérifier
python -c "import mutagen, pyautogui, pyperclip, win32gui; print('✅ OK')"
```

---

## 📚 Aide PowerShell

### Commandes d'Aide
```powershell
# Aide sur une commande
Get-Help Get-Command

# Liste des commandes disponibles
Get-Command

# Historique des commandes
Get-History
history  # Alias

# Effacer l'écran
Clear-Host
cls  # Alias
```

### Alias Utiles
```powershell
# Voir tous les alias
Get-Alias

# Créer un alias
Set-Alias ll Get-ChildItem

# Alias courants
ls    → Get-ChildItem
cd    → Set-Location
pwd   → Get-Location
cat   → Get-Content
```

---

## ✅ Checklist Rapide

```powershell
# Vérifier tout en une commande
python --version && pip --version && python -c "import mutagen, pyautogui, pyperclip, win32gui; from music_organizer import MetadataParser; print('✅ Tout est OK!')"
```

**Si cette commande fonctionne, votre installation est complète ! 🎉**

---

## 🎓 Commandes Avancées

### Gestion des Dépendances
```powershell
# Créer requirements.txt avec versions exactes
pip freeze > requirements.txt

# Installer exactement les mêmes versions
pip install -r requirements.txt

# Voir l'arbre des dépendances
pip show mutagen
```

### Performance
```powershell
# Mesurer le temps d'exécution
Measure-Command { python app.py }

# Profiler un script
python -m cProfile app.py
```

---

**Référence complète des commandes PowerShell ! 💻**
