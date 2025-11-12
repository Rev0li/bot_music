# 🐳 SongSurf - Guide Docker

## 🚀 Démarrage Rapide

### Prérequis
- Docker installé ([Installation](https://docs.docker.com/get-docker/))
- Docker Compose installé (inclus avec Docker Desktop)

### Démarrer SongSurf

```bash
./start-docker.sh
```

Le serveur sera accessible sur **http://localhost:8080**

---

## 📋 Commandes Utiles

### Démarrer les conteneurs
```bash
docker-compose up -d
```

### Arrêter les conteneurs
```bash
docker-compose stop
```

### Redémarrer les conteneurs
```bash
docker-compose restart
```

### Voir les logs en temps réel
```bash
docker-compose logs -f
```

### Arrêter et supprimer les conteneurs
```bash
docker-compose down
```

### Reconstruire l'image (après modification du code)
```bash
docker-compose build
docker-compose up -d
```

---

## 📁 Structure des Volumes

Les données sont persistées dans les dossiers locaux :

```
SongSurf/
├── temp/          → Téléchargements temporaires
└── music/         → Bibliothèque musicale organisée
    └── artist_photos/
```

Ces dossiers sont montés dans le conteneur Docker, donc :
- ✅ Les téléchargements persistent après redémarrage
- ✅ Tu peux accéder aux fichiers directement depuis ton système
- ✅ Pas de perte de données si tu supprimes le conteneur

---

## 🔧 Configuration

### Changer le port

Édite `docker-compose.yml` :

```yaml
ports:
  - "9000:8080"  # Utiliser le port 9000 au lieu de 8080
```

### Mode développement (hot reload)

Décommente cette ligne dans `docker-compose.yml` :

```yaml
volumes:
  - ./python-server:/app  # Monter le code source
```

---

## 🐛 Dépannage

### Le serveur ne démarre pas

Vérifier les logs :
```bash
docker-compose logs songsurf-server
```

### Port déjà utilisé

Changer le port dans `docker-compose.yml` ou arrêter le processus qui utilise le port 8080 :
```bash
sudo lsof -i :8080
```

### Reconstruire complètement

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Accéder au conteneur

```bash
docker exec -it songsurf-server bash
```

---

## 🆚 Docker vs Installation Manuelle

### ✅ Avantages Docker
- Installation en 1 commande
- Pas de conflit avec ton système
- FFmpeg inclus automatiquement
- Portable (fonctionne partout)
- Facile à mettre à jour

### ❌ Inconvénients Docker
- Nécessite Docker installé
- Utilise plus de ressources
- Légèrement plus lent au démarrage

---

## 📦 Mise à jour

Pour mettre à jour SongSurf :

```bash
git pull
docker-compose build
docker-compose up -d
```

---

## 🗑️ Désinstallation

```bash
# Arrêter et supprimer les conteneurs
docker-compose down

# Supprimer l'image
docker rmi songsurf-server

# Supprimer les données (optionnel)
rm -rf temp/ music/
```

---

## 📊 Monitoring

### Vérifier l'état du conteneur
```bash
docker ps
```

### Statistiques d'utilisation
```bash
docker stats songsurf-server
```

### Health check
```bash
curl http://localhost:8080/health
```

---

## 🔐 Sécurité

⚠️ **Important** : Le serveur est accessible uniquement en local (`localhost:8080`)

Pour exposer sur le réseau, modifie `docker-compose.yml` :
```yaml
ports:
  - "0.0.0.0:8080:8080"  # Accessible depuis le réseau
```

**Attention** : N'expose pas le serveur sur Internet sans authentification !

---

## 💡 Astuces

### Nettoyer l'espace disque Docker
```bash
docker system prune -a
```

### Sauvegarder ta bibliothèque
```bash
tar -czf songsurf-backup.tar.gz music/
```

### Restaurer une sauvegarde
```bash
tar -xzf songsurf-backup.tar.gz
```

---

## 📝 Notes

- Les fichiers `install.sh` et `start.sh` ne sont plus nécessaires avec Docker
- L'environnement virtuel Python (`venv/`) n'est plus créé localement
- FFmpeg est installé automatiquement dans le conteneur
- Le serveur redémarre automatiquement en cas de crash (`restart: unless-stopped`)
