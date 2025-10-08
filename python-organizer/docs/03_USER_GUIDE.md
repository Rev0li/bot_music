# 📘 Guide Utilisateur Complet

## 🎯 Vue d'Ensemble

Music Organizer Pro vous permet de :
- ✅ Détecter automatiquement les téléchargements
- ✅ Coller le nom de fichier automatiquement
- ✅ Organiser vos MP3 par Artiste/Album
- ✅ Mettre à jour les tags ID3

---

## 🖥️ Interface Principale

### Section 1: Dossier Source
```
📁 Dossier source: [Aucun dossier sélectionné] [📂 Parcourir]
```
- Sélectionnez le dossier contenant vos MP3 téléchargés

### Section 2: Scanner de Téléchargement
```
🔍 Scanner de téléchargement: [⭕ OFF] [▶️ Activer] [🐛 Debug]
```
- **Activer:** Démarre la surveillance des téléchargements
- **Debug:** Affiche toutes les fenêtres détectées (pour dépannage)

### Section 3: Actions
```
[🔍 Scanner les chansons] [✨ Organiser les chansons]
```
- **Scanner:** Trouve les MP3 dans le dossier
- **Organiser:** Déplace et organise les fichiers

### Section 4: Logs
```
📋 Logs:
[Zone de texte avec les messages]
```
- Affiche toutes les actions en temps réel

---

## 🔄 Workflow Complet

### Étape 1: Activer le Scanner (Optionnel)

1. Cliquez sur **"▶️ Activer"**
2. Vérifiez le message: `✅ Utilisation de win32gui (détection optimale)`
3. Le scanner surveille maintenant les téléchargements

**Logs attendus:**
```
🚀 Scanner de téléchargement activé
✅ Utilisation de win32gui (détection optimale)
🔍 Surveillance des fenêtres 'Enregistrer sous' en cours...
```

---

### Étape 2: Télécharger une Chanson

**Avec Chrome Extension V2:**
1. Allez sur YouTube Music
2. Cliquez sur "🎯 Auto Share V2"
3. Y2Mate s'ouvre en arrière-plan
4. La conversion démarre
5. Le téléchargement commence

**Fenêtre "Save As" s'ouvre:**
- Le scanner la détecte automatiquement
- Le nom de fichier est collé (Ctrl+V)
- Le chemin est vérifié
- Vous cliquez sur "Save"

**Logs attendus:**
```
🔔 Fenêtre détectée: www8.mnuu.nu wants to save
⏳ Attente de 2 secondes...
🤖 Démarrage de l'automatisation...
🎯 Activation de la fenêtre 'Save As'...
✅ Fenêtre activée
📋 Collage du nom de fichier (Ctrl+V)...
✅ Ctrl+V envoyé
🔍 Vérification du chemin...
📂 Chemin actuel: C:\Users\Molim\Music\itunes
✅ Chemin correct: Music\itunes
✅ Nom de fichier collé! Cliquez sur Save manuellement
```

---

### Étape 3: Organiser les Fichiers

1. **Sélectionner le dossier:**
   - Cliquez sur "📂 Parcourir"
   - Naviguez vers `C:\Users\Molim\Music\itunes`
   - Cliquez "Sélectionner le dossier"

2. **Scanner les chansons:**
   - Cliquez sur "🔍 Scanner les chansons"
   - Attendez la fin du scan
   - Vérifiez le nombre de chansons trouvées

**Logs attendus:**
```
📁 Dossier sélectionné: C:\Users\Molim\Music\itunes
🔍 Scan en cours...
✅ Trouvé: art=Drake alb=Views N=OneDance Y=2016
✅ Trouvé: art=The Killers alb=Hot Fuss N=Mr. Brightside Y=2004
✅ Scan terminé: 2 chanson(s) trouvée(s)
📊 Statistiques:
   - Total: 2 chansons
   - Artistes: 2
   - Albums: 2
```

3. **Organiser:**
   - Cliquez sur "✨ Organiser les chansons"
   - Confirmez l'opération
   - Attendez la fin

**Logs attendus:**
```
✨ Organisation en cours...
🎵 [1/2] art=Drake alb=Views N=OneDance Y=2016.mp3
   → Artiste: Drake
   → Album: Views
   → Titre: OneDance
   → Année: 2016
   ✅ Déplacé vers: C:\Users\Molim\Music\itunes\Drake\Views\OneDance.mp3

🎵 [2/2] art=The Killers alb=Hot Fuss N=Mr. Brightside Y=2004.mp3
   → Artiste: The Killers
   → Album: Hot Fuss
   → Titre: Mr. Brightside
   → Année: 2004
   ✅ Déplacé vers: C:\Users\Molim\Music\itunes\The Killers\Hot Fuss\Mr. Brightside.mp3

🎉 Organisation terminée!
✅ Succès: 2
```

---

## 🎵 Résultat Final

### Avant:
```
Downloads/
├── art=Drake alb=Views N=OneDance Y=2016.mp3
└── art=The Killers alb=Hot Fuss N=Mr. Brightside Y=2004.mp3
```

### Après:
```
Music/itunes/
├── Drake/
│   └── Views/
│       └── OneDance.mp3
└── The Killers/
    └── Hot Fuss/
        └── Mr. Brightside.mp3
```

**Chaque fichier a ses tags ID3 mis à jour ! ✅**

---

## 🐛 Mode Debug

### Quand l'utiliser ?
- Le scanner ne détecte pas la fenêtre
- Le nom de fichier n'est pas collé
- Vous voulez voir ce qui se passe

### Comment l'activer ?
1. Cliquez sur "🐛 Debug"
2. Les logs affichent maintenant TOUTES les fenêtres détectées

**Logs en mode debug:**
```
🐛 Mode debug activé
🐛 Fenêtres détectées (win32): 15
🐛 Fenêtre: Music Organizer Pro
🐛 Fenêtre: Google Chrome
🐛 Fenêtre: Visual Studio Code
🐛 Fenêtre: www8.mnuu.nu wants to save  ← CELLE-CI!
🔔 Fenêtre détectée: www8.mnuu.nu wants to save
```

---

## ⚙️ Paramètres Avancés

### Désactiver la Vérification du Chemin

Si Alt+D ne fonctionne pas sur votre système, vous pouvez désactiver la vérification :

**Dans `music_organizer/monitor.py` ligne 294:**
```python
verify_path=False  # Au lieu de True
```

### Augmenter les Délais

Si l'automatisation est trop rapide :

**Dans `music_organizer/monitor.py` ligne 285:**
```python
time.sleep(3)  # Au lieu de 2
```

---

## 💡 Conseils d'Utilisation

### Conseil 1: Créer le Dossier iTunes
```powershell
mkdir C:\Users\Molim\Music\itunes
```

### Conseil 2: Toujours Vérifier les Logs
Les logs vous disent exactement ce qui se passe.

### Conseil 3: Utiliser le Mode Debug
En cas de problème, activez le debug pour voir toutes les fenêtres.

### Conseil 4: Format des Noms
Assurez-vous que vos fichiers ont au minimum `art=` et `N=`.

### Conseil 5: Scanner Régulièrement
Organisez vos fichiers régulièrement pour garder une bibliothèque propre.

---

## 🎯 Cas d'Usage

### Cas 1: Téléchargement Unique
1. Activer le scanner
2. Télécharger une chanson
3. Le nom est collé automatiquement
4. Cliquer sur Save
5. Organiser plus tard

### Cas 2: Téléchargement en Masse
1. Télécharger plusieurs chansons (sans scanner)
2. Tous les fichiers vont dans Downloads
3. Sélectionner le dossier Downloads
4. Scanner toutes les chansons
5. Organiser en une fois

### Cas 3: Organisation Existante
1. Vous avez déjà des MP3 avec le bon format
2. Sélectionner le dossier
3. Scanner
4. Organiser

---

## ✅ Checklist d'Utilisation

### Première Fois
- [ ] Application lancée
- [ ] Scanner activé
- [ ] Dossier iTunes créé
- [ ] Test avec une chanson
- [ ] Nom collé automatiquement
- [ ] Fichier sauvegardé
- [ ] Dossier sélectionné
- [ ] Chanson scannée
- [ ] Chanson organisée

### Utilisation Quotidienne
- [ ] Scanner activé
- [ ] Télécharger des chansons
- [ ] Noms collés automatiquement
- [ ] Fichiers sauvegardés
- [ ] Organiser régulièrement

---

## 📚 Prochaines Étapes

- **Formats de fichiers:** [04_FILENAME_FORMATS.md](04_FILENAME_FORMATS.md)
- **Auto-Save détaillé:** [05_AUTO_SAVE.md](05_AUTO_SAVE.md)
- **Dépannage:** [09_TROUBLESHOOTING.md](09_TROUBLESHOOTING.md)

---

**Profitez de votre musique bien organisée ! 🎵**
