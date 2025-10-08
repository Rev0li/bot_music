# 📦 Installation Complète

## 🎯 Prérequis

### Système d'exploitation
- ✅ Windows 10/11 (recommandé)
- ⚠️ Linux/Mac (fonctionnel mais scanner limité)

### Python
- **Version minimale:** Python 3.8
- **Version recommandée:** Python 3.11+
- **Téléchargement:** [python.org/downloads](https://www.python.org/downloads/)

---

## 🚀 Installation Étape par Étape

### Étape 1: Installer Python

1. Télécharger l'installateur depuis [python.org](https://www.python.org/downloads/)
2. Lancer l'installateur
3. **IMPORTANT:** ✅ Cocher "Add Python to PATH"
4. Cliquer sur "Install Now"
5. Attendre la fin de l'installation

**Vérification:**
```powershell
python --version
```
**Résultat attendu:** `Python 3.11.x` (ou supérieur)

---

### Étape 2: Naviguer vers le Dossier

```powershell
# Ouvrir PowerShell (Windows + X → PowerShell)
cd C:\Users\Molim\Music\bot\bot

# Vérifier que vous êtes au bon endroit
dir
# Vous devez voir: app.py, requirements.txt, music_organizer/
```

---

### Étape 3: Installer les Dépendances

#### **Option A: Script Automatique (Recommandé)**

Double-cliquez sur :
```
install_deps.bat
```

Ou dans PowerShell :
```powershell
.\install_deps.ps1
```

#### **Option B: Commande Manuelle**

```powershell
pip install -r requirements.txt
```

#### **Option C: Installation Individuelle**

```powershell
pip install mutagen>=1.45.1
pip install pyautogui>=0.9.53
pip install pyperclip>=1.8.2
pip install pywin32>=305
```

---

### Étape 4: Vérification

```powershell
# Test 1: Vérifier Python
python --version

# Test 2: Vérifier mutagen
python -c "import mutagen; print('✅ mutagen OK')"

# Test 3: Vérifier pyautogui
python -c "import pyautogui; print('✅ pyautogui OK')"

# Test 4: Vérifier pyperclip
python -c "import pyperclip; print('✅ pyperclip OK')"

# Test 5: Vérifier pywin32
python -c "import win32gui; print('✅ pywin32 OK')"

# Test 6: Vérifier les modules du projet
python -c "from music_organizer import MetadataParser; print('✅ Modules OK')"
```

**Si tous les tests passent:** ✅ Installation réussie !

---

### Étape 5: Premier Lancement

```powershell
python app.py
```

**Résultat attendu:** Une fenêtre graphique s'ouvre ! 🎉

---

## 📊 Dépendances Détaillées

| Package | Version | Usage | Obligatoire |
|---------|---------|-------|-------------|
| `mutagen` | ≥1.45.1 | Lecture/écriture tags ID3 | ✅ Oui |
| `pyautogui` | ≥0.9.53 | Automatisation (Ctrl+V) | ✅ Oui |
| `pyperclip` | ≥1.8.2 | Lecture clipboard | ✅ Oui |
| `pywin32` | ≥305 | Détection fenêtres | ✅ Oui |
| `tkinter` | (inclus) | Interface graphique | ✅ Oui |

---

## 🐛 Résolution de Problèmes

### Problème 1: "python n'est pas reconnu"

**Cause:** Python n'est pas dans le PATH

**Solution:**
1. Réinstaller Python
2. ✅ Cocher "Add Python to PATH"
3. Redémarrer PowerShell

**Alternative:**
```powershell
# Utiliser le chemin complet
C:\Users\Molim\AppData\Local\Programs\Python\Python311\python.exe --version
```

---

### Problème 2: "pip n'est pas reconnu"

**Cause:** pip n'est pas installé ou pas dans le PATH

**Solution:**
```powershell
# Utiliser python -m pip
python -m pip --version

# Réinstaller pip
python -m ensurepip --upgrade
```

---

### Problème 3: "ModuleNotFoundError: No module named 'mutagen'"

**Cause:** Package non installé

**Solution:**
```powershell
pip install mutagen
```

---

### Problème 4: "Permission denied"

**Cause:** Droits administrateur requis

**Solution:**
```powershell
# Option 1: Installer pour l'utilisateur actuel
pip install --user mutagen

# Option 2: Lancer PowerShell en administrateur
# Clic droit sur PowerShell → "Exécuter en tant qu'administrateur"
pip install mutagen
```

---

### Problème 5: Politique d'exécution PowerShell

**Erreur:**
```
.\install_deps.ps1 cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
# Autoriser l'exécution de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Vérifier la politique
Get-ExecutionPolicy
```

---

## 🌐 Environnement Virtuel (Optionnel)

### Pourquoi ?
- ✅ Isole les dépendances du projet
- ✅ Évite les conflits entre projets
- ✅ Facilite le déploiement

### Création

```powershell
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement (PowerShell)
.\venv\Scripts\Activate.ps1

# Si erreur de politique:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python app.py

# 5. Désactiver l'environnement (quand terminé)
deactivate
```

---

## 📋 Checklist d'Installation

Cochez chaque étape :

- [ ] Python 3.8+ installé
- [ ] Python dans le PATH
- [ ] pip fonctionne
- [ ] Navigué vers le dossier du projet
- [ ] `requirements.txt` présent
- [ ] mutagen installé
- [ ] pyautogui installé
- [ ] pyperclip installé
- [ ] pywin32 installé
- [ ] Test d'import réussi
- [ ] `app.py` lance l'interface graphique

**Si toutes les cases sont cochées:** Installation réussie ! ✅

---

## 🚀 Installation Rapide (Copier-Coller)

```powershell
# Installation complète en une commande
cd C:\Users\Molim\Music\bot\bot && pip install -r requirements.txt && python -c "import mutagen, pyautogui, pyperclip, win32gui; print('✅ Tout est installé!')" && python app.py
```

---

## 📊 Versions Testées

| Composant | Version Testée | Statut |
|-----------|----------------|--------|
| Python | 3.11.5 | ✅ OK |
| Python | 3.10.x | ✅ OK |
| Python | 3.9.x | ✅ OK |
| Python | 3.8.x | ✅ OK |
| mutagen | 1.47.0 | ✅ OK |
| pyautogui | 0.9.54 | ✅ OK |
| pyperclip | 1.8.2 | ✅ OK |
| pywin32 | 306 | ✅ OK |
| Windows | 11 | ✅ OK |
| Windows | 10 | ✅ OK |

---

## ✅ Installation Terminée !

Si vous avez suivi toutes les étapes, vous devriez pouvoir :

1. ✅ Lancer `python app.py`
2. ✅ Voir l'interface graphique
3. ✅ Activer le scanner
4. ✅ Sélectionner un dossier
5. ✅ Scanner des chansons
6. ✅ Organiser vos MP3

**Passez au [Guide Utilisateur](03_USER_GUIDE.md) ! 🎉**
