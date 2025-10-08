# ⚡ Quick Start - Démarrage Rapide

## 🎯 Objectif

Installer et utiliser Music Organizer Pro en **5 minutes**.

---

## 📦 Installation en 3 Commandes

```powershell
# 1. Naviguer vers le dossier
cd C:\Users\Molim\Music\bot\bot

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python app.py
```

**C'est tout ! 🎉**

---

## 🚀 Première Utilisation

### Étape 1: Interface Principale

L'application s'ouvre avec 3 sections :
- **📁 Dossier source** - Où sont vos MP3
- **🔍 Scanner de téléchargement** - Détecte les nouveaux téléchargements
- **🎵 Organisation** - Scanner et organiser les fichiers

### Étape 2: Activer le Scanner (Optionnel)

Pour automatiser les téléchargements :
1. Cliquez sur **"▶️ Activer"** (Scanner de téléchargement)
2. Status devient **"✅ ON"**

**Maintenant, quand vous téléchargez une chanson :**
- La fenêtre "Save As" est détectée automatiquement
- Le nom de fichier est collé automatiquement (Ctrl+V)
- Le chemin est vérifié
- Vous cliquez sur "Save"

### Étape 3: Organiser vos MP3

1. Cliquez sur **"📂 Parcourir"**
2. Sélectionnez le dossier contenant vos MP3 (ex: `C:\Users\Molim\Music\itunes`)
3. Cliquez sur **"🔍 Scanner les chansons"**
4. Vérifiez les résultats dans les logs
5. Cliquez sur **"✨ Organiser les chansons"**

**Résultat :**
```
Avant:
Downloads/art=Drake alb=Views N=OneDance Y=2016.mp3

Après:
Music/Drake/Views/OneDance.mp3
```

---

## 📝 Format des Noms de Fichiers

### **Obligatoire:**
- `art=` - Artiste
- `N=` - Titre

### **Optionnel:**
- `alb=` - Album
- `Y=` - Année

### **Exemples:**
```
✅ art=Drake N=OneDance.mp3
✅ art=Drake alb=Views N=OneDance.mp3
✅ art=Drake alb=Views N=OneDance Y=2016.mp3
```

---

## 🎯 Workflow Complet

```
1. Télécharger une chanson (Chrome Extension V2)
   ↓
2. Fenêtre "Save As" s'ouvre
   ↓
3. Scanner détecte la fenêtre (si activé)
   ↓
4. Nom de fichier collé automatiquement
   ↓
5. Cliquer sur "Save"
   ↓
6. Dans Music Organizer: Scanner le dossier
   ↓
7. Organiser les chansons
   ↓
8. Fichiers organisés en Artiste/Album/Titre.mp3
```

---

## 🐛 Problème ?

### Scanner ne détecte pas
```powershell
pip install pywin32
```

### Nom de fichier non collé
```powershell
pip install pyautogui pyperclip
```

### Aucune chanson trouvée
Vérifiez le format des noms : `art=Artiste N=Titre.mp3`

---

## 📚 Aller Plus Loin

- **Installation détaillée:** [02_INSTALLATION.md](02_INSTALLATION.md)
- **Guide complet:** [03_USER_GUIDE.md](03_USER_GUIDE.md)
- **Formats de fichiers:** [04_FILENAME_FORMATS.md](04_FILENAME_FORMATS.md)
- **Dépannage:** [09_TROUBLESHOOTING.md](09_TROUBLESHOOTING.md)

---

## ✅ Checklist

- [ ] Python installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Application lancée (`python app.py`)
- [ ] Scanner activé (optionnel)
- [ ] Dossier sélectionné
- [ ] Chansons scannées
- [ ] Chansons organisées

**Tout coché ? Vous êtes opérationnel ! 🎉**

---

**Temps total: 5 minutes ⏱️**
