# 🪟 Installation et Test - Détection "Save As"

**Date:** 2025-10-09 13:53  
**Module:** save_as_handler.py

---

## 📦 Installation

### 1. Installer les Dépendances

```bash
cd C:\Users\Molim\Music\bot\python-organizer-v2\grabSong
pip install pywinauto pywin32
```

### 2. Vérifier l'Installation

```bash
python -c "import pywinauto; print('✅ pywinauto installé')"
```

---

## 🧪 Test du Module Seul

### Test Standalone

```bash
python save_as_handler.py
```

**Instructions:**
1. Le script démarre et attend
2. Ouvrez manuellement une fenêtre "Save As" (n'importe où)
3. Le script détecte automatiquement et remplit

**Résultat attendu:**
```
🔍 Recherche de la fenêtre 'Save As'...
✅ Fenêtre trouvée: 'Enregistrer sous'
📝 Remplissage du nom de fichier: test_file.mp3
✅ Nom de fichier rempli
📁 Changement de dossier vers: C:\Users\...\Downloads
✅ Dossier changé
💾 Clic sur 'Enregistrer'...
✅ Bouton 'Enregistrer' cliqué
🎉 Automatisation terminée avec succès!
```

---

## 🚀 Test avec le Workflow Complet

### 1. Lancer le Serveur (en Admin si possible)

```bash
# Clic droit sur PowerShell → "Exécuter en tant qu'administrateur"
cd C:\Users\Molim\Music\bot\python-organizer-v2\grabSong
python app.py
```

### 2. Utiliser l'Extension

1. Va sur YouTube Music
2. Clique "🎯 GrabSong"
3. Remplis le formulaire
4. Clique "Sauvegarder"
5. Y2Mate s'ouvre et télécharge
6. **La fenêtre "Save As" apparaît**
7. **Python remplit automatiquement** ✨

---

## 🔧 Configuration

### Timeout

Par défaut: **120 secondes** (2 minutes)

Pour changer, éditer `app.py`:

```python
success = handler.wait_and_fill(
    filename=metadata['filename'],
    target_folder=str(A_TRIER_DIR),
    timeout=180  # 3 minutes
)
```

### Dossier de Destination

Par défaut: `python-organizer-v2/a_trier/`

Pour changer, éditer `app.py`:

```python
A_TRIER_DIR = BASE_DIR / "mon_dossier"
```

---

## 🐛 Dépannage

### Problème 1: "pywinauto non installé"

**Solution:**
```bash
pip install pywinauto pywin32
```

### Problème 2: Fenêtre non détectée

**Causes possibles:**
- Titre de fenêtre différent
- Fenêtre pas en premier plan
- Timeout trop court

**Solution:**
1. Augmenter le timeout
2. Vérifier le titre exact de la fenêtre
3. S'assurer que la fenêtre est visible

### Problème 3: Nom de fichier pas rempli

**Causes possibles:**
- Structure de fenêtre différente
- Contrôles non accessibles

**Solution:**
- Le script essaie 3 méthodes différentes
- Si aucune ne fonctionne, remplir manuellement
- Logs détaillés pour débugger

### Problème 4: Dossier pas changé

**Note:** C'est normal si ça échoue
- Le fichier sera sauvegardé dans le dossier par défaut (Downloads)
- Vous pouvez le déplacer manuellement après

---

## 📊 Méthodes de Détection

### 3 Méthodes pour Remplir le Nom

1. **Par le label** - Cherche "nom du fichier" / "file name"
2. **Par l'automation ID** - Utilise l'ID 1001 (standard)
3. **Par raccourci** - Alt+N puis tape le nom

### 2 Méthodes pour Changer le Dossier

1. **Barre d'adresse** - Tape directement le chemin
2. **Raccourci Ctrl+L** - Va à la barre d'adresse

### 2 Méthodes pour Cliquer "Enregistrer"

1. **Bouton** - Cherche et clique sur le bouton
2. **Entrée** - Appuie sur Entrée

---

## 🎯 Avantages de pywinauto

- ✅ **Robuste** - Fonctionne avec toutes les fenêtres Windows
- ✅ **Flexible** - Plusieurs méthodes de fallback
- ✅ **Logs détaillés** - Facile à débugger
- ✅ **Pas de dépendance image** - Pas besoin de screenshots
- ✅ **Rapide** - Détection en temps réel

---

## 📝 Logs Détaillés

### Exemple de Logs Réussis

```
🔍 Surveillance de la fenêtre 'Save As' démarrée...
   Fichier attendu: art=Ren N=Hi Ren.mp3

🔍 Recherche de la fenêtre 'Save As' (timeout: 120s)...
✅ Fenêtre trouvée: 'Enregistrer sous'

📁 Changement de dossier vers: C:\Users\...\a_trier
✅ Dossier changé (méthode 1)

📝 Remplissage du nom de fichier: art=Ren N=Hi Ren.mp3
✅ Nom de fichier rempli (méthode 1)

💾 Clic sur 'Enregistrer'...
✅ Bouton 'Enregistrer' cliqué

🎉 Automatisation terminée avec succès!
📁 Fichier sauvegardé: C:\Users\...\a_trier\art=Ren N=Hi Ren.mp3
```

---

## 🚀 Prochaines Étapes

### v1.1 - Améliorations

1. **Notification à l'extension** - Envoyer "download_complete"
2. **Déplacement du JSON** - Copier info.json avec le MP3
3. **Nettoyage de queue/** - Supprimer les dossiers temporaires
4. **Gestion d'erreurs** - Retry automatique si échec

---

**Installe pywinauto et teste ! 🪟✨**
