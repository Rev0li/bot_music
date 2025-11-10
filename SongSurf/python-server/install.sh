#!/bin/bash
# ============================================
# 🎵 SongSurf - Installation Automatique
# ============================================
# 
# Ce script installe tout automatiquement :
#   ✅ Environnement virtuel Python
#   ✅ Toutes les dépendances
#   ✅ FFmpeg (si nécessaire)
#   ✅ Dossiers de travail
#
# Usage: ./install.sh
# ============================================

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonction d'affichage
print_header() {
    echo -e "${PURPLE}============================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}============================================${NC}"
}

print_step() {
    echo -e "${CYAN}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# ============================================
# DÉBUT DE L'INSTALLATION
# ============================================

clear
print_header "🎵 SongSurf - Installation Automatique"

# ============================================
# 1. Vérifier Python
# ============================================

print_step "Vérification de Python..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 n'est pas installé"
    echo ""
    print_info "Installation automatique..."
    
    # Détecter l'OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y python3 python3-venv python3-pip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python3
    else
        print_error "OS non supporté. Installez Python 3 manuellement."
        exit 1
    fi
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python $PYTHON_VERSION détecté"

# ============================================
# 2. Vérifier FFmpeg
# ============================================

print_step "Vérification de FFmpeg..."

if ! command -v ffmpeg &> /dev/null; then
    print_warning "FFmpeg n'est pas installé"
    print_info "Installation automatique de FFmpeg..."
    
    # Détecter l'OS et installer FFmpeg
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y ffmpeg
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ffmpeg
    else
        print_warning "Installation manuelle requise: sudo apt install ffmpeg"
    fi
    
    # Vérifier à nouveau
    if command -v ffmpeg &> /dev/null; then
        print_success "FFmpeg installé avec succès"
    else
        print_error "Impossible d'installer FFmpeg automatiquement"
        print_info "Installez-le manuellement: sudo apt install ffmpeg"
        exit 1
    fi
else
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n1 | awk '{print $3}')
    print_success "FFmpeg $FFMPEG_VERSION détecté"
fi

# ============================================
# 3. Créer l'environnement virtuel
# ============================================

print_step "Création de l'environnement virtuel..."

if [ -d "venv" ]; then
    print_info "Environnement virtuel existant détecté"
    print_step "Suppression et recréation..."
    rm -rf venv
fi

python3 -m venv venv
print_success "Environnement virtuel créé"

# ============================================
# 4. Activer l'environnement virtuel
# ============================================

print_step "Activation de l'environnement virtuel..."

source venv/bin/activate

if [ -z "$VIRTUAL_ENV" ]; then
    print_error "Impossible d'activer l'environnement virtuel"
    exit 1
fi

print_success "Environnement virtuel activé"

# ============================================
# 5. Mettre à jour pip
# ============================================

print_step "Mise à jour de pip..."

pip install --upgrade pip --quiet

PIP_VERSION=$(pip --version | awk '{print $2}')
print_success "pip $PIP_VERSION"

# ============================================
# 6. Installer les dépendances
# ============================================

print_step "Installation des dépendances..."

if [ ! -f "requirements.txt" ]; then
    print_error "Le fichier requirements.txt est introuvable"
    exit 1
fi

echo ""
print_info "Dépendances à installer:"
cat requirements.txt | grep -v '^#' | grep -v '^$' | sed 's/^/  - /'
echo ""

pip install -r requirements.txt

print_success "Dépendances installées"

# ============================================
# 7. Vérifier les installations
# ============================================

print_step "Vérification des installations..."

echo ""
print_info "Packages installés:"
pip list | grep -E "(flask|yt-dlp|mutagen|Pillow)" | sed 's/^/  /'
echo ""

# ============================================
# 8. Créer les dossiers nécessaires
# ============================================

print_step "Création des dossiers..."

cd ..

mkdir -p temp
mkdir -p music

print_success "Dossiers créés (temp/, music/)"

# ============================================
# 9. Test du serveur
# ============================================

print_step "Test de l'importation des modules..."

cd python-server

python3 << EOF
try:
    import flask
    import yt_dlp
    import mutagen
    from PIL import Image
    print("✅ Tous les modules sont importables")
except ImportError as e:
    print(f"❌ Erreur d'importation: {e}")
    exit(1)
EOF

if [ $? -eq 0 ]; then
    print_success "Tous les modules fonctionnent"
else
    print_error "Certains modules ne fonctionnent pas"
    exit 1
fi

# ============================================
# INSTALLATION TERMINÉE
# ============================================

echo ""
print_header "✅ Installation terminée avec succès !"

echo ""
print_info "🚀 Pour démarrer SongSurf:"
echo -e "  ${GREEN}./start.sh${NC}"
echo ""

print_info "📱 Ensuite:"
echo "  1. Installez l'extension Chrome"
echo "  2. Allez sur YouTube Music"
echo "  3. Cliquez sur le widget SongSurf"
echo "  4. Téléchargez vos musiques !"
echo ""

print_info "🌐 Dashboard:"
echo "  http://localhost:8080"
echo ""

print_success "Installation terminée ! Prêt à télécharger de la musique ! 🎵"
echo ""
