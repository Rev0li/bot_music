#!/bin/bash
# ============================================
# 🎵 GrabSong V3 - Script de démarrage
# ============================================
# 
# Ce script démarre le serveur Python avec FFmpeg
#
# Usage:
#   chmod +x start.sh
#   ./start.sh
# ============================================

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

# ============================================
# 1. Vérifier l'environnement virtuel
# ============================================

if [ ! -d "venv" ]; then
    echo -e "${RED}❌ L'environnement virtuel n'existe pas${NC}"
    echo -e "${CYAN}ℹ️  Exécutez d'abord: ./install.sh${NC}"
    exit 1
fi

# ============================================
# 2. Activer l'environnement virtuel
# ============================================

echo -e "${CYAN}▶ Activation de l'environnement virtuel...${NC}"
source venv/bin/activate

if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}❌ Impossible d'activer l'environnement virtuel${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Environnement virtuel activé${NC}"

# ============================================
# 3. Configurer FFmpeg
# ============================================

echo -e "${CYAN}▶ Configuration de FFmpeg...${NC}"

FFMPEG_LOCAL_DIR="$HOME/.local/ffmpeg"
FFMPEG_FOUND=false

# Vérifier FFmpeg système
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n1 | awk '{print $3}')
    echo -e "${GREEN}✅ FFmpeg $FFMPEG_VERSION (système)${NC}"
    FFMPEG_FOUND=true
# Vérifier FFmpeg local
elif [ -d "$FFMPEG_LOCAL_DIR" ]; then
    FFMPEG_STATIC=$(find "$FFMPEG_LOCAL_DIR" -name "ffmpeg-*-static" -type d 2>/dev/null | head -n 1)
    
    if [ -n "$FFMPEG_STATIC" ] && [ -f "$FFMPEG_STATIC/ffmpeg" ]; then
        # Ajouter FFmpeg au PATH
        export PATH="$FFMPEG_STATIC:$PATH"
        
        FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n1 | awk '{print $3}')
        echo -e "${GREEN}✅ FFmpeg $FFMPEG_VERSION (local)${NC}"
        echo -e "${CYAN}   Chemin: $FFMPEG_STATIC${NC}"
        FFMPEG_FOUND=true
    fi
fi

# Avertir si FFmpeg n'est pas trouvé
if [ "$FFMPEG_FOUND" = false ]; then
    echo -e "${YELLOW}⚠️  FFmpeg non trouvé${NC}"
    echo -e "${CYAN}ℹ️  La conversion MP3 ne fonctionnera pas${NC}"
    echo -e "${CYAN}ℹ️  Exécutez './install.sh' pour installer FFmpeg${NC}"
    echo ""
    read -p "Voulez-vous continuer sans FFmpeg ? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        deactivate
        exit 1
    fi
fi

# ============================================
# 4. Vérifier les dépendances Python
# ============================================

echo -e "${CYAN}▶ Vérification des dépendances...${NC}"

python3 << EOF
import sys
try:
    import flask
    import yt_dlp
    import mutagen
    from PIL import Image
    print("✅ Tous les modules Python sont disponibles")
except ImportError as e:
    print(f"❌ Module manquant: {e}")
    print("ℹ️  Exécutez './install.sh' pour installer les dépendances")
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    deactivate
    exit 1
fi

# ============================================
# 5. Afficher la bannière
# ============================================

echo ""
echo -e "${PURPLE}============================================${NC}"
echo -e "${PURPLE}🎵 GrabSong V3 - Serveur Python${NC}"
echo -e "${PURPLE}============================================${NC}"
echo ""

# ============================================
# 6. Afficher les informations de connexion
# ============================================

echo -e "${CYAN}Serveur prêt à démarrer :${NC}"
echo -e "  ${GREEN}http://localhost:5000${NC}"
echo ""
echo -e "${CYAN}Endpoints disponibles :${NC}"
echo "  GET  /ping        - Test de connexion"
echo "  POST /download    - Télécharger une vidéo"
echo "  GET  /status      - Statut du serveur"
echo "  POST /cleanup     - Nettoyer les fichiers temp"
echo "  GET  /stats       - Statistiques"
echo ""
echo -e "${CYAN}Pour arrêter le serveur :${NC}"
echo "  Ctrl+C"
echo ""
echo -e "${PURPLE}============================================${NC}"
echo ""

# ============================================
# 7. Démarrer le serveur
# ============================================

echo -e "${CYAN}▶ Démarrage du serveur...${NC}"
echo ""

# Piège pour nettoyer à la sortie
trap 'echo -e "\n${YELLOW}⚠️  Arrêt du serveur...${NC}"; deactivate; exit 0' INT TERM

python app.py

# Désactiver l'environnement virtuel à la sortie
deactivate