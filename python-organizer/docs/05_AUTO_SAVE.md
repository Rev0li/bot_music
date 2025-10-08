# 🤖 Auto-Save Feature

## 🎯 Fonctionnalités

Automatise le processus de sauvegarde :
1. ✅ Détecte la fenêtre "wants to save"
2. ✅ Active la fenêtre automatiquement
3. ✅ Colle le nom de fichier (Ctrl+V)
4. ✅ Vérifie le chemin (Music\itunes)

---

## 🔄 Workflow Complet

```
Chrome Extension V2
  ↓
Téléchargement MP3
  ↓
Fenêtre "wants to save" s'ouvre
  ↓
🤖 Scanner détecte la fenêtre
  ↓
🎯 Fenêtre activée automatiquement
  ↓
📋 Nom collé: "art=Drake alb=Views N=OneDance Y=2016.mp3"
  ↓
🔍 Chemin vérifié: "C:\Users\...\Music\itunes"
  ↓
✅ Chemin OK → Prêt à sauvegarder
  ↓
💾 Vous cliquez sur Save
  ↓
✅ Fichier sauvegardé!
```

---

## ⚙️ Configuration

### Par Défaut (Recommandé)

```python
auto_paste=True   # ✅ Coller automatiquement
auto_save=False   # ✅ Clic manuel sur Save (sécurité)
```

**Vous gardez le contrôle final !**

---

## 🎓 Comment ça Marche

### 1. Détection de la Fenêtre

Utilise `win32gui` pour détecter toutes les fenêtres :
```python
keywords = ["wants to save", "Save As", "Enregistrer sous"]
```

### 2. Activation de la Fenêtre

Force la fenêtre au premier plan :
```python
win32gui.SetForegroundWindow(hwnd)
```

### 3. Collage Automatique

Simule Ctrl+V :
```python
pyautogui.hotkey('ctrl', 'v')
```

### 4. Vérification du Chemin

Vérifie que le chemin contient "Music\itunes" :
```python
if "Music" in path and "itunes" in path:
    print("✅ Chemin correct")
```

---

## 📊 Exemple de Logs

```
🔔 Fenêtre détectée: www8.mnuu.nu wants to save
⏳ Attente de 2 secondes...
🤖 Démarrage de l'automatisation...
   - auto_paste: True
   - auto_save: False
   - auto_saver disponible: True
🎯 Activation de la fenêtre 'Save As'...
🎯 Recherche de la fenêtre 'Save As'...
✅ Fenêtre trouvée: www8.mnuu.nu wants to save
🎯 Activation de la fenêtre...
✅ Fenêtre activée
📋 Collage du nom de fichier (Ctrl+V)...
   → Simulation de Ctrl+V...
   ✅ Ctrl+V envoyé
🔍 Vérification du chemin...
📂 Chemin actuel: C:\Users\Molim\Music\itunes
   - Contient 'Music': True
   - Contient 'itunes': True
✅ Chemin correct: Music\itunes
✅ Nom de fichier collé! Cliquez sur Save manuellement
✅ Automatisation terminée avec succès
```

---

## 🎯 Avantages

### Avant (Manuel)
1. Fenêtre "Save As" s'ouvre
2. **Cliquer sur la fenêtre**
3. **Ctrl+V manuellement**
4. **Vérifier le chemin**
5. Cliquer sur Save

**Temps:** ~10 secondes

### Après (Automatique)
1. Fenêtre "Save As" s'ouvre
2. **Tout est fait automatiquement**
3. Cliquer sur Save

**Temps:** ~2 secondes

**Gain de temps: 80% ! 🚀**

---

## 🔧 Dépendances

| Package | Usage |
|---------|-------|
| `pywin32` | Détecter et activer les fenêtres |
| `pyautogui` | Simuler Ctrl+V |
| `pyperclip` | Lire le clipboard |

**Installation:**
```powershell
pip install pywin32 pyautogui pyperclip
```

---

## 💡 Conseils

### Conseil 1: Toujours Vérifier le Clipboard
Avant de télécharger, assurez-vous que le nom de fichier est dans le clipboard.

### Conseil 2: Créer le Dossier iTunes
```powershell
mkdir C:\Users\Molim\Music\itunes
```

### Conseil 3: Mode Debug
Activez le debug pour voir chaque étape en détail.

---

## ✅ Résumé

**Auto-Save automatise:**
1. ✅ Détection de la fenêtre
2. ✅ Activation de la fenêtre
3. ✅ Collage du nom (Ctrl+V)
4. ✅ Vérification du chemin

**Vous faites:**
- ✅ Clic sur Save (contrôle final)

**Résultat:** Workflow fluide et rapide ! 🎉
