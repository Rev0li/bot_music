# 🚀 Installation Rapide - GrabSong V3

Guide d'installation en 5 minutes.

## ⚡ Installation Express

### Étape 1: Installer FFmpeg (requis)

**Windows (Chocolatey):**
```powershell
choco install ffmpeg
```

**Windows (Manuel):**
1. Télécharger depuis https://ffmpeg.org/download.html
2. Extraire dans `C:\ffmpeg`
3. Ajouter `C:\ffmpeg\bin` au PATH
![alt text](image.png)

**Linux:**
```bash
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### Étape 2: Installer les dépendances Python

```bash
cd V3/python-server
pip install -r requirements.txt
```

### Étape 3: Lancer le serveur

```bash
python app.py
```

Vous devriez voir:
```
====================================================================
🎵 GrabSong V3 - Serveur Python
====================================================================
📁 Dossier temporaire: C:\Users\...\bot\V3\temp
📁 Bibliothèque musicale: C:\Users\...\bot\V3\music
====================================================================
🚀 Serveur démarré sur http://localhost:5000
====================================================================
```

### Étape 4: Installer l'extension Chrome

1. Ouvrir `chrome://extensions/`
2. Activer **"Mode développeur"** (coin supérieur droit)
3. Cliquer **"Charger l'extension non empaquetée"**
4. Sélectionner le dossier `V3/chrome-extension/`
5. L'extension apparaît dans la barre d'outils

### Étape 5: Tester

1. Aller sur https://music.youtube.com
2. Lancer une musique
3. Le widget "🎵 GrabSong V3" apparaît en bas à droite
4. Cliquer sur "⬇️ Télécharger"
5. Vérifier les métadonnées
6. Cliquer sur "💾 Télécharger"
7. Attendre la fin du téléchargement
8. Vérifier dans le dossier `V3/music/`

## ✅ Vérification de l'Installation

### Test 1: FFmpeg
```bash
ffmpeg -version
```
Devrait afficher la version de FFmpeg.

### Test 2: Serveur Python
```bash
curl http://localhost:5000/ping
```
Devrait retourner:
```json
{
  "status": "ok",
  "message": "GrabSong V3 server is running",
  "timestamp": "..."
}
```

### Test 3: Extension Chrome
1. Ouvrir le popup de l'extension
2. Vérifier que "Serveur Python" est "En ligne" (point vert)

## 🐛 Problèmes Courants

### FFmpeg non trouvé
```
❌ ERROR: ffmpeg not found
```
**Solution:** Installer FFmpeg et l'ajouter au PATH

### Port 5000 déjà utilisé
```
❌ Address already in use
```
**Solution:** Modifier le port dans `app.py`:
```python
app.run(host='localhost', port=5001)  # Changer 5000 en 5001
```
Et dans `background.js`:
```javascript
const PYTHON_SERVER = 'http://localhost:5001';  // Changer 5000 en 5001
```

### Extension non visible sur YouTube Music
**Solution:** Rafraîchir la page YouTube Music (F5)

### Serveur Python "Hors ligne" dans le popup
**Solution:** 
1. Vérifier que le serveur est lancé (`python app.py`)
2. Vérifier qu'il tourne sur le port 5000
3. Vérifier les logs du serveur

## 📝 Checklist d'Installation

- [ ] FFmpeg installé et dans le PATH
- [ ] Dépendances Python installées (`pip install -r requirements.txt`)
- [ ] Serveur Python lancé (`python app.py`)
- [ ] Extension Chrome chargée
- [ ] Widget visible sur YouTube Music
- [ ] Test de téléchargement réussi

## 🎉 C'est Prêt !

Vous pouvez maintenant télécharger de la musique depuis YouTube Music en un clic !

**Prochaines étapes:**
- Lire le [README.md](README.md) pour plus de détails
- Consulter [ARCHITECTURE.md](ARCHITECTURE.md) pour comprendre le fonctionnement
- Voir [MIGRATION_V2_V3.md](MIGRATION_V2_V3.md) si vous venez de la V2
