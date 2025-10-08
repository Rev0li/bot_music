# 🐛 Dépannage

## 🎯 Problèmes Courants

---

## ❌ Problème 1: Scanner Ne Détecte Pas

### Symptômes
```
🔔 Fenêtre détectée: (rien)
```

### Cause
`pywin32` non installé

### Solution
```powershell
pip install pywin32
```

### Vérification
```powershell
python -c "import win32gui; print('✅ OK')"
```

---

## ❌ Problème 2: AutoSaver Non Disponible

### Symptômes
```
⚠️ AutoSaver non disponible (pyautogui/pyperclip manquants)
```

### Cause
`pyautogui` ou `pyperclip` non installés

### Solution
```powershell
pip install pyautogui pyperclip
```

### Vérification
```powershell
python -c "import pyautogui, pyperclip; print('✅ OK')"
```

---

## ❌ Problème 3: Nom de Fichier Non Collé

### Symptômes
- Fenêtre détectée
- Logs montrent "✅ Ctrl+V envoyé"
- Mais rien n'apparaît dans le champ

### Causes Possibles

#### Cause 1: Clipboard Vide
**Solution:** Vérifiez que le nom est dans le clipboard
```powershell
# Testez Ctrl+V dans notepad
```

#### Cause 2: Fenêtre Pas Encore Prête
**Solution:** Augmentez le délai
```python
# Dans monitor.py ligne 285
time.sleep(3)  # Au lieu de 2
```

#### Cause 3: Focus Pas sur le Bon Champ
**Solution:** L'activation automatique devrait résoudre ça

---

## ❌ Problème 4: Fenêtre Non Activée

### Symptômes
```
⚠️ Impossible d'activer la fenêtre
```

### Cause
`win32gui` ne peut pas activer la fenêtre

### Solution
Cliquez manuellement sur la fenêtre avant que l'automatisation se déclenche

---

## ❌ Problème 5: Chemin Incorrect

### Symptômes
```
⚠️ Chemin incorrect: C:\Users\...\Downloads
💡 Attendu: ...\\Music\\itunes
```

### Solution 1: Naviguer Manuellement
Naviguez vers `Music\itunes` avant de sauvegarder

### Solution 2: Désactiver la Vérification
```python
# Dans monitor.py ligne 294
verify_path=False
```

---

## ❌ Problème 6: Doublons Détectés

### Symptômes
```
🔔 Fenêtre détectée: wants to save
🔔 Fenêtre détectée: Recent download history
```

### Cause
Le scanner détecte plusieurs fenêtres

### Solution
Déjà corrigé ! Les fenêtres indésirables sont filtrées :
- "Recent download history"
- "Downloads"
- "History"

---

## ❌ Problème 7: Python Non Reconnu

### Symptômes
```
'python' n'est pas reconnu...
```

### Cause
Python pas dans le PATH

### Solution
1. Réinstaller Python
2. ✅ Cocher "Add Python to PATH"
3. Redémarrer PowerShell

---

## ❌ Problème 8: Module Not Found

### Symptômes
```
ModuleNotFoundError: No module named 'mutagen'
```

### Cause
Package non installé

### Solution
```powershell
pip install mutagen
```

Ou installer tout :
```powershell
pip install -r requirements.txt
```

---

## ❌ Problème 9: Permission Denied

### Symptômes
```
PermissionError: [WinError 5] Access is denied
```

### Cause
Droits insuffisants

### Solution
```powershell
# Option 1: Installer pour l'utilisateur
pip install --user pyautogui

# Option 2: Lancer en administrateur
# Clic droit PowerShell → "Exécuter en tant qu'administrateur"
```

---

## ❌ Problème 10: Aucune Chanson Trouvée

### Symptômes
```
✅ Scan terminé: 0 chanson(s) trouvée(s)
```

### Cause
Format des noms incorrect

### Solution
Vérifiez que vos fichiers ont au minimum :
```
art=Artiste N=Titre.mp3
```

---

## 🔧 Commandes de Diagnostic

### Vérifier Python
```powershell
python --version
```

### Vérifier pip
```powershell
pip --version
```

### Vérifier Tous les Packages
```powershell
python -c "import mutagen, pyautogui, pyperclip, win32gui; print('✅ Tout OK')"
```

### Vérifier les Modules du Projet
```powershell
python -c "from music_organizer import MetadataParser; print('✅ OK')"
```

---

## 📋 Checklist de Dépannage

- [ ] Python installé et dans le PATH
- [ ] pip fonctionne
- [ ] mutagen installé
- [ ] pyautogui installé
- [ ] pyperclip installé
- [ ] pywin32 installé
- [ ] Modules du projet importables
- [ ] Application se lance
- [ ] Scanner s'active
- [ ] Mode debug activé pour voir les logs

---

## 💡 Conseils Généraux

### Conseil 1: Toujours Lire les Logs
Les logs vous disent exactement ce qui ne va pas.

### Conseil 2: Mode Debug
Activez le debug pour voir toutes les fenêtres détectées.

### Conseil 3: Réinstaller les Dépendances
```powershell
pip uninstall -y mutagen pyautogui pyperclip pywin32
pip install -r requirements.txt
```

### Conseil 4: Environnement Virtuel
Utilisez un environnement virtuel pour éviter les conflits.

---

## 🆘 Besoin d'Aide ?

1. **Activez le mode debug** (🐛)
2. **Reproduisez le problème**
3. **Copiez les logs complets**
4. **Consultez la FAQ** ([10_FAQ.md](10_FAQ.md))

---

**La plupart des problèmes sont résolus en installant les bonnes dépendances ! 🔧**
