# ❓ FAQ - Questions Fréquentes

## 🎯 Général

### Q: C'est quoi Music Organizer Pro ?
**R:** Une application Python qui organise automatiquement vos fichiers MP3 et automatise le téléchargement.

### Q: C'est gratuit ?
**R:** Oui, complètement gratuit et open source.

### Q: Ça fonctionne sur Mac/Linux ?
**R:** Oui, mais le scanner de téléchargements est optimisé pour Windows.

---

## 📦 Installation

### Q: Quelle version de Python ?
**R:** Python 3.8 minimum, 3.11+ recommandé.

### Q: Comment installer les dépendances ?
**R:** 
```powershell
pip install -r requirements.txt
```

### Q: J'ai une erreur "python not found" ?
**R:** Python n'est pas dans le PATH. Réinstallez Python en cochant "Add Python to PATH".

---

## 🔍 Scanner

### Q: Le scanner ne détecte pas la fenêtre ?
**R:** Installez `pywin32`:
```powershell
pip install pywin32
```

### Q: Comment activer le scanner ?
**R:** Cliquez sur "▶️ Activer" dans l'interface.

### Q: Le scanner détecte trop de fenêtres ?
**R:** Normal en mode debug. Les fenêtres indésirables sont filtrées automatiquement.

### Q: Puis-je utiliser sans le scanner ?
**R:** Oui ! Le scanner est optionnel. Vous pouvez juste organiser vos MP3.

---

## 🤖 Auto-Save

### Q: Le nom de fichier n'est pas collé ?
**R:** Vérifiez que `pyautogui` et `pyperclip` sont installés:
```powershell
pip install pyautogui pyperclip
```

### Q: La fenêtre n'est pas activée automatiquement ?
**R:** Installez `pywin32` pour l'activation automatique.

### Q: Puis-je désactiver l'auto-paste ?
**R:** Oui, mais ce n'est pas recommandé. C'est la fonctionnalité principale !

### Q: Le chemin est toujours incorrect ?
**R:** Naviguez vers `Music\itunes` avant de sauvegarder, ou désactivez la vérification.

---

## 📝 Formats

### Q: Quel format de nom de fichier ?
**R:** Minimum: `art=Artiste N=Titre.mp3`

### Q: L'ordre des balises est important ?
**R:** Non ! `art=Drake N=Song.mp3` = `N=Song art=Drake.mp3`

### Q: Que se passe-t-il si l'album manque ?
**R:** Le fichier va dans "Unknown Album".

### Q: Puis-je utiliser des caractères spéciaux ?
**R:** Évitez `< > : " / \ | ? *` car ils sont supprimés.

---

## 🎵 Organisation

### Q: Mes fichiers sont déplacés où ?
**R:** Dans `Artiste/Album/Titre.mp3` dans le dossier que vous avez sélectionné.

### Q: Les tags ID3 sont mis à jour ?
**R:** Oui, automatiquement !

### Q: Puis-je annuler l'organisation ?
**R:** Non, les fichiers sont déplacés définitivement. Faites une sauvegarde avant !

### Q: Ça fonctionne avec d'autres formats ?
**R:** Non, seulement MP3 pour le moment.

---

## 🐛 Problèmes

### Q: "AutoSaver non disponible" ?
**R:** 
```powershell
pip install pyautogui pyperclip
```

### Q: "Module not found" ?
**R:** 
```powershell
pip install -r requirements.txt
```

### Q: L'application ne se lance pas ?
**R:** Vérifiez que Python et toutes les dépendances sont installés.

### Q: Le scanner s'arrête tout seul ?
**R:** Vérifiez les logs pour voir l'erreur.

---

## ⚙️ Configuration

### Q: Puis-je changer le dossier cible ?
**R:** Oui, sélectionnez n'importe quel dossier avec "📂 Parcourir".

### Q: Puis-je changer le format de sortie ?
**R:** Non, le format est `Artiste/Album/Titre.mp3`.

### Q: Puis-je désactiver la vérification du chemin ?
**R:** Oui, modifiez `monitor.py` ligne 294: `verify_path=False`

---

## 🔧 Avancé

### Q: Comment augmenter les délais ?
**R:** Modifiez `monitor.py` ligne 285: `time.sleep(3)`

### Q: Puis-je cliquer automatiquement sur Save ?
**R:** Oui, mais non recommandé. Modifiez `app.py`: `auto_save=True`

### Q: Comment voir tous les logs ?
**R:** Activez le mode debug avec le bouton "🐛 Debug".

### Q: Puis-je modifier le code ?
**R:** Oui ! Le code est open source.

---

## 📚 Documentation

### Q: Où est la documentation complète ?
**R:** Dans le dossier `docs/`:
- [00_INDEX.md](00_INDEX.md) - Table des matières
- [01_QUICK_START.md](01_QUICK_START.md) - Démarrage rapide
- [02_INSTALLATION.md](02_INSTALLATION.md) - Installation
- [03_USER_GUIDE.md](03_USER_GUIDE.md) - Guide utilisateur
- [09_TROUBLESHOOTING.md](09_TROUBLESHOOTING.md) - Dépannage

### Q: Il y a des tutoriels vidéo ?
**R:** Non, mais la documentation est très détaillée.

---

## 🎯 Workflow

### Q: Quel est le workflow complet ?
**R:**
1. Activer le scanner
2. Télécharger une chanson
3. Le nom est collé automatiquement
4. Cliquer sur Save
5. Scanner le dossier
6. Organiser les fichiers

### Q: Puis-je organiser sans télécharger ?
**R:** Oui ! Sélectionnez un dossier existant et organisez.

### Q: Combien de temps ça prend ?
**R:** ~2 secondes par fichier.

---

## 💡 Conseils

### Q: Des conseils pour bien utiliser l'app ?
**R:**
1. Créez le dossier `Music\itunes` avant
2. Activez toujours le mode debug pour les tests
3. Vérifiez le format des noms de fichiers
4. Organisez régulièrement
5. Gardez une sauvegarde de vos fichiers

---

## 🆘 Support

### Q: J'ai un problème non listé ici ?
**R:** 
1. Consultez [09_TROUBLESHOOTING.md](09_TROUBLESHOOTING.md)
2. Activez le mode debug
3. Vérifiez les logs

---

**D'autres questions ? Consultez la documentation complète ! 📚**
