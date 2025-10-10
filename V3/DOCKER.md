# 🐳 Docker - GrabSong V3

Guide pour utiliser GrabSong V3 avec Docker.

## 🚀 Quick Start avec Docker

### Option 1: Docker Compose (Recommandé)

```bash
# Construire et lancer
docker-compose up -d

# Vérifier les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

### Option 2: Docker seul

```bash
# Construire l'image
docker build -t grabsong-v3 .

# Lancer le conteneur
docker run -d \
  --name grabsong-v3 \
  -p 5000:5000 \
  -v $(pwd)/temp:/app/temp \
  -v $(pwd)/music:/app/music \
  grabsong-v3

# Vérifier les logs
docker logs -f grabsong-v3

# Arrêter
docker stop grabsong-v3
docker rm grabsong-v3
```

## 📁 Structure des Volumes

```
V3/
├── temp/     → /app/temp   (téléchargements temporaires)
└── music/    → /app/music  (bibliothèque musicale)
```

Les fichiers sont **persistés** sur votre machine hôte.

## 🔧 Configuration

### Variables d'Environnement

Vous pouvez personnaliser le serveur avec des variables d'environnement dans `docker-compose.yml`:

```yaml
environment:
  - FLASK_ENV=production
  - FLASK_HOST=0.0.0.0
  - FLASK_PORT=5000
```

### Ports

Par défaut, le serveur écoute sur le port **5000**. Pour changer:

```yaml
ports:
  - "8080:5000"  # Accès via http://localhost:8080
```

## 🩺 Health Check

Le conteneur inclut un health check qui vérifie toutes les 30 secondes que le serveur répond:

```bash
# Vérifier le statut
docker ps

# Devrait afficher "healthy" dans la colonne STATUS
```

## 📊 Commandes Utiles

### Logs

```bash
# Tous les logs
docker-compose logs

# Logs en temps réel
docker-compose logs -f

# Dernières 100 lignes
docker-compose logs --tail=100
```

### Redémarrage

```bash
# Redémarrer le service
docker-compose restart

# Reconstruire et redémarrer
docker-compose up -d --build
```

### Nettoyage

```bash
# Arrêter et supprimer
docker-compose down

# Supprimer aussi les volumes (⚠️ perte de données)
docker-compose down -v

# Supprimer l'image
docker rmi grabsong-v3
```

## 🌐 Accès depuis l'Extension Chrome

L'extension Chrome doit pointer vers:
```
http://localhost:5000
```

Si vous changez le port, modifiez `chrome-extension/background.js`:
```javascript
const PYTHON_SERVER = 'http://localhost:8080';  // Votre port
```

## 🔒 Sécurité

### Production

Pour un déploiement en production:

1. **Utiliser HTTPS** (avec un reverse proxy comme Nginx)
2. **Limiter l'accès** (firewall, authentification)
3. **Surveiller les logs**

Exemple avec Nginx:

```nginx
server {
    listen 443 ssl;
    server_name grabsong.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 Performance

### Optimisations

1. **Limiter les ressources**:

```yaml
services:
  grabsong-server:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

2. **Utiliser une image multi-stage** (pour réduire la taille):

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

## 🐛 Dépannage

### Le conteneur ne démarre pas

```bash
# Vérifier les logs
docker-compose logs

# Vérifier que le port 5000 est libre
netstat -an | grep 5000
```

### FFmpeg non trouvé

FFmpeg est installé automatiquement dans l'image Docker. Si vous avez une erreur:

```bash
# Vérifier que FFmpeg est présent
docker exec grabsong-v3 which ffmpeg

# Devrait afficher: /usr/bin/ffmpeg
```

### Problèmes de permissions

```bash
# Donner les permissions aux dossiers
chmod -R 777 temp/ music/
```

## 🚀 Déploiement

### Sur un serveur distant

1. **Copier les fichiers**:
```bash
scp -r V3/ user@server:/path/to/
```

2. **Se connecter au serveur**:
```bash
ssh user@server
cd /path/to/V3
```

3. **Lancer Docker**:
```bash
docker-compose up -d
```

### Avec Docker Hub

1. **Tag l'image**:
```bash
docker tag grabsong-v3 username/grabsong-v3:latest
```

2. **Push vers Docker Hub**:
```bash
docker push username/grabsong-v3:latest
```

3. **Pull sur un autre serveur**:
```bash
docker pull username/grabsong-v3:latest
docker run -d -p 5000:5000 username/grabsong-v3:latest
```

## 📝 Notes

- Les téléchargements sont **persistés** dans `./music/`
- Les fichiers temporaires dans `./temp/` sont nettoyés automatiquement
- Le serveur redémarre automatiquement en cas d'erreur (`restart: unless-stopped`)

## 🎉 Avantages de Docker

✅ **Isolation** - Pas de conflit avec d'autres applications  
✅ **Portabilité** - Fonctionne partout (Linux, macOS, Windows)  
✅ **Reproductibilité** - Même environnement pour tous  
✅ **Simplicité** - Une commande pour tout installer  
✅ **Scalabilité** - Facile à déployer sur plusieurs serveurs  

## 📚 Ressources

- [Documentation Docker](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
