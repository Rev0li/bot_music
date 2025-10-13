# 🎉 Nouveauté: Dashboard SongSurf

## 📊 Qu'est-ce que c'est ?

Un **dashboard web minimaliste** intégré à votre serveur Python Flask pour surveiller vos téléchargements musicaux en temps réel.

## ✨ Fonctionnalités

### 📈 Vue d'ensemble
- **Statistiques globales** - Artistes, Albums, Chansons, Queue
- **Mise à jour automatique** - Rafraîchissement toutes les 2 secondes
- **Design minimaliste** - Thème sombre élégant

### 🔄 Activité en temps réel
- **Téléchargement actuel** avec barre de progression
- **File d'attente** avec détails de chaque élément
- **Historique** des 10 derniers téléchargements

### 🛠️ Actions
- **Actualiser** - Rafraîchir manuellement les données
- **Nettoyer temp/** - Supprimer les fichiers temporaires

## 🚀 Comment l'utiliser ?

### Méthode 1: Fichier batch (Windows)
```bash
# Double-cliquer sur:
start_dashboard.bat
```

### Méthode 2: Ligne de commande
```bash
cd SongSurf/python-server
python app.py
```

### Accès
```
http://localhost:5000
```

## 📁 Fichiers créés

```
SongSurf/
├── start_dashboard.bat              # Lancement rapide (Windows)
├── DASHBOARD.md                     # Documentation complète
├── LANCEMENT_RAPIDE.md             # Guide de démarrage
├── DASHBOARD_PREVIEW.txt           # Aperçu visuel
└── python-server/
    ├── app.py                      # ✅ Modifié (route dashboard ajoutée)
    ├── templates/
    │   └── dashboard.html          # 🆕 Template HTML
    └── static/
        ├── dashboard.css           # 🆕 Styles minimalistes
        ├── dashboard.js            # 🆕 Logique + auto-refresh
        └── README.md               # 🆕 Documentation des assets
```

## 🎨 Aperçu du Design

### Palette de couleurs
- **Fond principal:** Noir profond (#0a0a0a)
- **Cartes:** Gris foncé (#222222)
- **Accent:** Violet doux (#667eea)
- **Succès:** Vert (#34c759)

### Sections
1. **Header** - Logo + Statut du serveur
2. **Stats Grid** - 4 cartes (Artistes, Albums, Chansons, Queue)
3. **Téléchargement actuel** - Titre, artiste, album + progression
4. **File d'attente** - Liste numérotée des téléchargements en attente
5. **Historique** - 10 derniers téléchargements avec horodatage
6. **Footer** - Dernière mise à jour + Actions

## 🔧 Personnalisation

### Changer l'intervalle de rafraîchissement
Éditez `static/dashboard.js`:
```javascript
const REFRESH_INTERVAL = 2000; // 2 secondes (2000 ms)
```

### Modifier les couleurs
Éditez `static/dashboard.css`:
```css
:root {
    --accent: #667eea;  /* Votre couleur préférée */
}
```

### Changer le nombre d'éléments dans l'historique
Éditez `static/dashboard.js`:
```javascript
if (recentDownloads.length > 10) {  // Changer 10
    recentDownloads = recentDownloads.slice(0, 10);
}
```

## 💡 Cas d'usage

### Scénario 1: Surveillance passive
1. Lancez le dashboard sur un second écran
2. Utilisez l'extension Chrome normalement
3. Observez les téléchargements en temps réel

### Scénario 2: Vérification rapide
1. Ouvrez le dashboard
2. Consultez les statistiques
3. Vérifiez que tout fonctionne bien

### Scénario 3: Gestion de la queue
1. Surveillez la file d'attente
2. Vérifiez qu'elle ne déborde pas
3. Nettoyez temp/ si nécessaire

## 🎯 Avantages

✅ **Visibilité** - Voir ce qui se passe en temps réel  
✅ **Contrôle** - Surveiller la queue et les téléchargements  
✅ **Statistiques** - Connaître la taille de votre bibliothèque  
✅ **Simplicité** - Interface minimaliste et intuitive  
✅ **Performance** - Léger et rapide  
✅ **Local** - Aucune donnée n'est envoyée sur Internet  

## 🔒 Sécurité

Le dashboard est accessible **uniquement en local** (`localhost:5000`).  
Aucune donnée n'est exposée sur Internet.

## 📖 Documentation

- **[DASHBOARD.md](DASHBOARD.md)** - Documentation complète
- **[LANCEMENT_RAPIDE.md](LANCEMENT_RAPIDE.md)** - Guide de démarrage
- **[DASHBOARD_PREVIEW.txt](DASHBOARD_PREVIEW.txt)** - Aperçu visuel

## 🐛 Dépannage

### Le dashboard ne s'affiche pas
```
❌ Problème: Page blanche ou erreur 404

✅ Solution:
   1. Vérifier que le serveur est lancé (python app.py)
   2. Vérifier l'URL: http://localhost:5000 (pas https)
   3. Consulter les logs du serveur
```

### Les données ne se mettent pas à jour
```
❌ Problème: Dashboard figé

✅ Solution:
   1. Ouvrir la console du navigateur (F12)
   2. Vérifier les erreurs JavaScript
   3. Tester l'API: http://localhost:5000/status
   4. Cliquer sur "Actualiser" manuellement
```

### Erreur "Hors ligne"
```
❌ Problème: Indicateur rouge "Hors ligne"

✅ Solution:
   Le serveur Python n'est pas démarré
   → Lancer: python app.py
```

## 🎵 Profitez-en !

Le dashboard est maintenant prêt à l'emploi. Lancez-le et profitez d'une vue complète sur vos téléchargements musicaux !

---

**Créé le:** 12 octobre 2025  
**Version:** 1.0.0  
**Compatibilité:** SongSurf V3 (Windows Edition)
