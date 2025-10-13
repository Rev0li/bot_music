# 📊 SongSurf Dashboard

Dashboard minimaliste en Python Flask pour surveiller vos téléchargements musicaux en temps réel.

## 🚀 Démarrage

### 1. Lancer le serveur Python

```bash
cd SongSurf/python-server
python app.py
```

### 2. Accéder au dashboard

Ouvrez votre navigateur et allez sur:
```
http://localhost:5000
```

## ✨ Fonctionnalités

### 📈 Statistiques en temps réel
- **Artistes** - Nombre total d'artistes dans votre bibliothèque
- **Albums** - Nombre total d'albums
- **Chansons** - Nombre total de chansons téléchargées
- **En attente** - Nombre de téléchargements dans la queue

### 🔄 Téléchargement en cours
- Affichage du titre, artiste et album en cours de téléchargement
- Barre de progression en temps réel
- Pourcentage de complétion

### 📝 File d'attente
- Liste des téléchargements en attente
- Position dans la queue
- Métadonnées de chaque élément

### ✅ Derniers téléchargements
- Historique des 10 derniers téléchargements
- Horodatage relatif (il y a X minutes)
- Métadonnées complètes

### 🛠️ Actions
- **Actualiser** - Rafraîchir manuellement les données
- **Nettoyer temp/** - Supprimer les fichiers temporaires

## 🎨 Design

- **Style minimaliste** - Interface épurée et moderne
- **Dark mode** - Thème sombre pour réduire la fatigue oculaire
- **Responsive** - Adapté aux différentes tailles d'écran
- **Auto-refresh** - Mise à jour automatique toutes les 2 secondes

## 🔧 Configuration

### Modifier l'intervalle de rafraîchissement

Éditez `static/dashboard.js`:
```javascript
const REFRESH_INTERVAL = 2000; // en millisecondes (2000 = 2 secondes)
```

### Modifier le nombre de téléchargements récents

Éditez `static/dashboard.js`:
```javascript
if (recentDownloads.length > 10) {  // Changer 10 par le nombre souhaité
    recentDownloads = recentDownloads.slice(0, 10);
}
```

## 📂 Structure des fichiers

```
python-server/
├── app.py                    # Serveur Flask avec route dashboard
├── templates/
│   └── dashboard.html        # Template HTML du dashboard
└── static/
    ├── dashboard.css         # Styles minimalistes
    └── dashboard.js          # Logique JavaScript + auto-refresh
```

## 🌐 Endpoints API utilisés

- `GET /` - Dashboard principal
- `GET /status` - Statut des téléchargements + queue
- `GET /stats` - Statistiques de la bibliothèque
- `POST /cleanup` - Nettoyage du dossier temp/

## 💡 Astuces

1. **Gardez le dashboard ouvert** pendant que vous utilisez l'extension Chrome pour voir les téléchargements en temps réel

2. **Utilisez plusieurs onglets** - Le dashboard et YouTube Music peuvent être ouverts côte à côte

3. **Surveillez la queue** - Vérifiez que les téléchargements ne s'accumulent pas

4. **Nettoyez régulièrement** - Utilisez le bouton "Nettoyer temp/" pour libérer de l'espace

## 🎯 Utilisation typique

1. Ouvrez le dashboard dans votre navigateur
2. Lancez l'extension Chrome sur YouTube Music
3. Téléchargez vos chansons favorites
4. Observez en temps réel:
   - La progression du téléchargement
   - La queue qui se remplit
   - Les statistiques qui augmentent
   - L'historique qui se construit

## 🔒 Sécurité

Le dashboard est accessible uniquement en **local** (`localhost:5000`). Il n'est pas exposé sur Internet, ce qui garantit la confidentialité de vos données.

## 🐛 Dépannage

### Le dashboard ne s'affiche pas
- Vérifiez que le serveur Python est bien lancé
- Vérifiez l'URL: `http://localhost:5000` (pas `https`)
- Consultez les logs du serveur dans le terminal

### Les données ne se mettent pas à jour
- Vérifiez la console du navigateur (F12)
- Vérifiez que le serveur répond: `http://localhost:5000/ping`
- Essayez de rafraîchir manuellement avec le bouton "Actualiser"

### Erreur "Hors ligne"
- Le serveur Python n'est pas démarré
- Lancez `python app.py` dans le dossier `python-server/`

---

**Profitez de votre dashboard personnel ! 🎵**
