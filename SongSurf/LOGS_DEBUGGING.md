# 📝 Système de Logs - Debugging

## 🎯 Objectif

Page de logs en temps réel pour **détecter et diagnostiquer les bugs** et suivre le cheminement complet de chaque téléchargement.

## ✨ Fonctionnalités

### 📊 Statistiques
- **Total logs** - Nombre total d'entrées
- **Erreurs** - Nombre d'erreurs détectées
- **Avertissements** - Nombre d'avertissements

### 🔍 Filtres
- **Tous** - Afficher tous les logs
- **Info** - Logs informatifs (actions normales)
- **Succès** - Opérations réussies
- **Avertissements** - Situations inhabituelles
- **Erreurs** - Problèmes détectés

### 🔄 Temps réel
- **Auto-refresh** - Mise à jour automatique toutes les 2 secondes
- **500 entrées max** - Garde les 500 derniers logs
- **Horodatage précis** - Date et heure de chaque événement

### 📋 Détails des logs
Chaque log contient:
- **Timestamp** - Date et heure exacte
- **Niveau** - INFO, SUCCESS, WARNING, ERROR
- **Message** - Description de l'événement
- **Data** - Données additionnelles (JSON)

## 🚀 Accès

### Depuis le Dashboard
Cliquez sur le bouton **"📝 Logs"** en haut à droite du dashboard

### URL directe
```
http://localhost:5000/logs
```

## 📖 Types de logs enregistrés

### 🟢 INFO
- Démarrage du serveur
- Téléchargement ajouté à la queue
- Queue worker démarré
- Actions utilisateur

### ✅ SUCCESS
- Serveur démarré avec succès
- Téléchargement terminé
- Organisation du fichier réussie
- Opérations complétées

### ⚠️ WARNING
- Queue presque pleine
- Fichier déjà existant
- Métadonnées incomplètes
- Situations inhabituelles

### ❌ ERROR
- Erreur de téléchargement
- Erreur d'organisation
- Erreur réseau
- Exceptions Python

## 🛠️ Actions disponibles

### 🔄 Actualiser
Rafraîchit manuellement les logs (en plus de l'auto-refresh)

### 🗑️ Effacer
Supprime tous les logs actuels (demande confirmation)

### ← Dashboard
Retour au dashboard principal

## 📡 API

### GET /api/logs
Récupère tous les logs en JSON

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2025-10-12T16:30:00.123456",
      "level": "INFO",
      "message": "Téléchargement ajouté à la queue",
      "data": {
        "url": "https://...",
        "metadata": {...}
      }
    }
  ],
  "total": 42,
  "max_logs": 500
}
```

### POST /api/logs/clear
Efface tous les logs

**Response:**
```json
{
  "success": true,
  "message": "Logs effacés"
}
```

## 🐛 Utilisation pour le debugging

### Scénario 1: Téléchargement qui échoue

1. Ouvrez la page des logs
2. Lancez un téléchargement
3. Filtrez par "Erreurs"
4. Analysez le message d'erreur et les données

### Scénario 2: Suivi complet d'un téléchargement

1. Effacez les logs
2. Lancez un téléchargement
3. Observez en temps réel:
   - Ajout à la queue (INFO)
   - Démarrage du téléchargement (INFO)
   - Progression (INFO)
   - Organisation (INFO)
   - Succès (SUCCESS)

### Scénario 3: Détection de problèmes

1. Laissez les logs tourner pendant vos sessions
2. Vérifiez régulièrement le compteur d'erreurs
3. Filtrez par "Erreurs" ou "Avertissements"
4. Analysez les patterns

## 💡 Conseils

### Pour un debugging efficace

1. **Effacez les logs** avant de reproduire un bug
2. **Filtrez par niveau** pour isoler les problèmes
3. **Regardez les données JSON** pour les détails techniques
4. **Notez le timestamp** pour corréler avec d'autres événements

### Logs importants à surveiller

- ❌ **ERROR** - Problèmes critiques à résoudre
- ⚠️ **WARNING** - Situations à surveiller
- ✅ **SUCCESS** - Confirme que tout fonctionne

## 🔧 Configuration

### Modifier le nombre max de logs

Éditez `app.py`:
```python
MAX_LOGS = 500  # Changer cette valeur
```

### Modifier l'intervalle de rafraîchissement

Éditez `templates/logs.html`:
```javascript
const REFRESH_INTERVAL = 2000; // en millisecondes
```

## 📊 Exemple de session de debugging

```
[16:30:00] ✅ SUCCESS - Serveur SongSurf démarré
[16:30:00] ℹ️  INFO    - Queue worker démarré
[16:30:15] ℹ️  INFO    - Téléchargement ajouté: One Dance - Drake
[16:30:16] ℹ️  INFO    - Démarrage du téléchargement
[16:30:25] ✅ SUCCESS - Téléchargement terminé
[16:30:26] ✅ SUCCESS - Organisation réussie
[16:30:45] ℹ️  INFO    - Téléchargement ajouté: Hotline Bling - Drake
[16:30:46] ❌ ERROR   - Erreur de téléchargement: Video unavailable
```

## 🎯 Avantages

✅ **Visibilité totale** - Voir tout ce qui se passe  
✅ **Debugging rapide** - Identifier les problèmes facilement  
✅ **Historique** - Garder une trace des événements  
✅ **Filtrage** - Se concentrer sur ce qui compte  
✅ **Temps réel** - Suivre en direct  
✅ **Données détaillées** - JSON pour analyse approfondie  

## 🔒 Sécurité

Les logs sont **uniquement accessibles en local** (`localhost:5000`). Aucune donnée n'est envoyée sur Internet.

---

**Utilisez cette page pour diagnostiquer tous vos problèmes ! 🐛**
