# 🚀 Démarrage Rapide - GrabSong

## 📦 Installation

```bash
cd C:\Users\Molim\Music\bot\python-organizer-v2\grabSong
pip install -r requirements.txt
```

## ▶️ Lancer le Serveur Python

```bash
python app.py
```

**Tu devrais voir:**
```
==================================================
🐍 Serveur Python GrabSong
==================================================
🌐 URL: http://localhost:5000
📁 Queue: C:\Users\Molim\Music\bot\python-organizer-v2\queue
📁 A trier: C:\Users\Molim\Music\bot\python-organizer-v2\a_trier
==================================================

✅ Serveur démarré - En attente de requêtes...
```

## 🧪 Tester

1. **Serveur Python lancé** ✅
2. **Extension rechargée** sur `chrome://extensions/`
3. **YouTube Music** ouvert
4. **Clic sur "🎯 GrabSong"**
5. **Remplis et clique "Sauvegarder"**

### Résultat Attendu

**Dans le terminal Python:**
```
📨 Données reçues:
{
  "artist": "Ren",
  "album": "Hi Ren",
  "title": "Hi Ren",
  ...
}
💾 Données sauvegardées: C:\...\queue\20250109_130821\info.json
🔍 Surveillance de la fenêtre 'Save As' démarrée...
```

**Dans le chat de l'extension:**
```
✅ Python: Données sauvegardées
📁 Dossier: 20250109_130821
```

**Fichier créé:**
```
queue/
└── 20250109_130821/
    └── info.json
```

---

**C'est tout ! Beaucoup plus simple que Native Messaging ! 🎉**
