# ============================================
# 🎵 SongSurf - Dockerfile
# ============================================
# Image Python optimisée avec FFmpeg inclus
# ============================================

FROM python:3.11-slim

# Métadonnées
LABEL maintainer="SongSurf"
LABEL description="SongSurf - YT Music Downloader Server"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installer les dépendances système (FFmpeg + outils)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de l'application
WORKDIR /app

# Copier requirements.txt en premier (pour le cache Docker)
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app.py .
COPY downloader.py .
COPY organizer.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Créer les dossiers de données
RUN mkdir -p /data/temp /data/music /data/music/artist_photos

# Exposer le port
EXPOSE 8080

# Vérifier que tout est bien installé
RUN python -c "import flask, yt_dlp, mutagen; from PIL import Image; print('✅ All modules OK')" && \
    ffmpeg -version | head -n1

# Commande de démarrage
CMD ["python", "app.py"]
