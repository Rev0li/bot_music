#!/bin/bash
# ============================================
# 🔍 SongSurf - Vérification de l'Installation
# ============================================

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}🔍 Vérification de l'Installation${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

ERRORS=0

# 1. Python
echo -n "Python 3............... "
if command -v python3 &> /dev/null; then
    VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✅ $VERSION${NC}"
else
    echo -e "${RED}❌ Non installé${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 2. FFmpeg
echo -n "FFmpeg................. "
if command -v ffmpeg &> /dev/null; then
    VERSION=$(ffmpeg -version 2>&1 | head -n1 | awk '{print $3}')
    echo -e "${GREEN}✅ $VERSION${NC}"
elif [ -d "$HOME/.local/ffmpeg" ]; then
    FFMPEG_DIR=$(find "$HOME/.local/ffmpeg" -name "ffmpeg-*-static" -type d 2>/dev/null | head -n 1)
    if [ -n "$FFMPEG_DIR" ] && [ -f "$FFMPEG_DIR/ffmpeg" ]; then
        VERSION=$("$FFMPEG_DIR/ffmpeg" -version 2>&1 | head -n1 | awk '{print $3}')
        echo -e "${GREEN}✅ $VERSION (local)${NC}"
    else
        echo -e "${YELLOW}⚠️  Non trouvé${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Non installé${NC}"
fi

# 3. Environnement virtuel
echo -n "Environnement virtuel.. "
if [ -d "venv" ]; then
    echo -e "${GREEN}✅ Présent${NC}"
else
    echo -e "${RED}❌ Manquant${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 4. Dépendances Python
echo -n "Dépendances Python..... "
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null
    
    MISSING=""
    for pkg in flask yt-dlp mutagen Pillow; do
        if ! python3 -c "import ${pkg//-/_}" 2>/dev/null; then
            MISSING="$MISSING $pkg"
        fi
    done
    
    if [ -z "$MISSING" ]; then
        echo -e "${GREEN}✅ Toutes installées${NC}"
    else
        echo -e "${RED}❌ Manquantes:$MISSING${NC}"
        ERRORS=$((ERRORS + 1))
    fi
    
    deactivate 2>/dev/null
else
    echo -e "${YELLOW}⚠️  Venv manquant${NC}"
fi

# 5. Dossiers
echo -n "Dossiers............... "
cd ..
MISSING_DIRS=""
[ ! -d "music" ] && MISSING_DIRS="$MISSING_DIRS music"
[ ! -d "temp" ] && MISSING_DIRS="$MISSING_DIRS temp"

if [ -z "$MISSING_DIRS" ]; then
    echo -e "${GREEN}✅ Présents${NC}"
else
    echo -e "${YELLOW}⚠️  Manquants:$MISSING_DIRS${NC}"
fi
cd python-server

echo ""
echo -e "${CYAN}============================================${NC}"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Installation complète et fonctionnelle !${NC}"
    echo ""
    echo -e "${CYAN}🚀 Pour démarrer :${NC}"
    echo "   ./start.sh"
else
    echo -e "${RED}❌ $ERRORS erreur(s) détectée(s)${NC}"
    echo ""
    echo -e "${CYAN}💡 Pour réinstaller :${NC}"
    echo "   ./install.sh"
fi

echo -e "${CYAN}============================================${NC}"
echo ""
