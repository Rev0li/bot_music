#!/bin/bash
# ============================================
# 🎵 SongSurf - Démarrage Docker
# ============================================
# Script simplifié pour démarrer avec Docker
# ============================================

set -e

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

clear
echo ""
echo -e "${PURPLE}============================================${NC}"
echo -e "${PURPLE}🎵 SongSurf - Démarrage Docker${NC}"
echo -e "${PURPLE}============================================${NC}"
echo ""

# Vérifier Docker
echo -e "${CYAN}▶ Vérification de Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas installé${NC}"
    echo -e "${YELLOW}ℹ️  Installez Docker: https://docs.docker.com/get-docker/${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
    echo -e "${RED}❌ Docker Compose n'est pas installé${NC}"
    echo -e "${YELLOW}ℹ️  Installez Docker Compose${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker détecté${NC}"
echo ""

# Créer les dossiers nécessaires
echo -e "${CYAN}▶ Création des dossiers...${NC}"
mkdir -p temp music
echo -e "${GREEN}✅ Dossiers créés${NC}"
echo ""

# Construire et démarrer les conteneurs
echo -e "${CYAN}▶ Construction de l'image Docker...${NC}"
echo ""

# Utiliser docker compose (v2) ou docker-compose (v1)
if docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

$DOCKER_COMPOSE build

echo ""
echo -e "${GREEN}✅ Image construite${NC}"
echo ""

echo -e "${CYAN}▶ Démarrage des conteneurs...${NC}"
echo ""

$DOCKER_COMPOSE up -d

echo ""
echo -e "${GREEN}✅ Conteneurs démarrés${NC}"
echo ""

# Attendre que le serveur soit prêt
echo -e "${CYAN}▶ Vérification du serveur...${NC}"
sleep 3

if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Serveur prêt !${NC}"
else
    echo -e "${YELLOW}⚠️  Le serveur démarre...${NC}"
fi

echo ""
echo -e "${PURPLE}============================================${NC}"
echo -e "${GREEN}✅ SongSurf est démarré !${NC}"
echo -e "${PURPLE}============================================${NC}"
echo ""
echo -e "${CYAN}🌐 Dashboard :${NC}"
echo -e "  ${GREEN}http://localhost:8080${NC}"
echo ""
echo -e "${CYAN}📱 Extension Chrome :${NC}"
echo "  1. Installez l'extension depuis chrome-extension/"
echo "  2. Allez sur YT Music"
echo "  3. Cliquez sur le widget SongSurf"
echo ""
echo -e "${CYAN}📊 Commandes utiles :${NC}"
echo -e "  ${GREEN}$DOCKER_COMPOSE logs -f${NC}        # Voir les logs"
echo -e "  ${GREEN}$DOCKER_COMPOSE stop${NC}           # Arrêter"
echo -e "  ${GREEN}$DOCKER_COMPOSE restart${NC}        # Redémarrer"
echo -e "  ${GREEN}$DOCKER_COMPOSE down${NC}           # Arrêter et supprimer"
echo ""
echo -e "${PURPLE}============================================${NC}"
echo ""
