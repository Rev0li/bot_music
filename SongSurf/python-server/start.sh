#!/bin/bash
# ============================================
# 🎵 GrabSong V3 - Script de démarrage
# ============================================
# 
# Ce script démarre le serveur Python
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

# Vérifier que l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ L'environnement virtuel n'existe pas${NC}"
    echo -e "${CYAN}ℹ️  Exécutez d'abord: ./install.sh${NC}"
    exit 1
fi

# Activer l'environnement virtuel
echo -e "${CYAN}▶ Activation de l'environnement virtuel...${NC}"
source venv/bin/activate

if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}❌ Impossible d'activer l'environnement virtuel${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Environnement virtuel activé${NC}"
echo ""

# Afficher la bannière
echo -e "${PURPLE}============================================${NC}"
echo -e "${PURPLE}🎵 GrabSong V3 - Serveur Python${NC}"
echo -e "${PURPLE}============================================${NC}"
echo ""

# Démarrer le serveur
echo -e "${CYAN}▶ Démarrage du serveur...${NC}"
echo ""

# Utiliser python.exe sur Windows
if command -v python.exe &> /dev/null; then
    python.exe app.py
elif command -v python3 &> /dev/null; then
    python3 app.py
elif command -v python &> /dev/null; then
    python app.py
else
    echo -e "${RED}❌ Python n'est pas installé ou n'est pas dans le PATH${NC}"
    exit 1
fi
