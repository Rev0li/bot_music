# Dockerfile pour GrabSong V3
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="GrabSong V3"
LABEL description="Serveur Python pour télécharger et organiser de la musique depuis YouTube Music"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Installer FFmpeg et dépendances système
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements
COPY python-server/requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY python-server/ .

# Créer les dossiers pour les données
RUN mkdir -p /app/temp /app/music

# Exposer le port
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/ping')" || exit 1

# Commande de démarrage
CMD ["python", "app.py"]
