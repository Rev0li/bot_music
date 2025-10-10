#!/bin/bash
# ============================================
# 🎵 GrabSong V3 - Script d'installation
# ============================================
# 
# Ce script configure automatiquement :
#   - Environnement virtuel Python
#   - Installation des dépendances
#   - Vérification de FFmpeg
#
# Usage:
#   chmod +x install.sh
#   ./install.sh
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

print_header "🎵 GrabSong V3 - Installation"

# ============================================
# 1. Vérifier Python
# ============================================

print_step "Vérification de Python..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 n'est pas installé"
    echo ""
    print_info "Installation sur WSL/Ubuntu:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python $PYTHON_VERSION détecté"

# ============================================
# 2. Vérifier FFmpeg
# ============================================

print_step "Vérification de FFmpeg..."

if ! command -v ffmpeg &> /dev/null; then
    print_warning "FFmpeg n'est pas installé"
    echo ""
    print_info "FFmpeg est requis pour la conversion MP3"
    print_info "Installation sur WSL/Ubuntu:"
    echo "  sudo apt update"
    echo "  sudo apt install ffmpeg"
    echo ""
    read -p "Voulez-vous continuer sans FFmpeg ? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
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
    print_warning "L'environnement virtuel existe déjà"
    read -p "Voulez-vous le recréer ? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_step "Suppression de l'ancien environnement..."
        rm -rf venv
        print_step "Création d'un nouvel environnement..."
        python3 -m venv venv
        print_success "Environnement virtuel recréé"
    else
        print_info "Utilisation de l'environnement existant"
    fi
else
    python3 -m venv venv
    print_success "Environnement virtuel créé"
fi

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
print_info "Pour démarrer le serveur:"
echo -e "  ${GREEN}source venv/bin/activate${NC}"
echo -e "  ${GREEN}python app.py${NC}"
echo ""

print_info "Pour désactiver l'environnement virtuel:"
echo -e "  ${GREEN}deactivate${NC}"
echo ""

print_info "Endpoints disponibles:"
echo "  GET  http://localhost:5000/ping"
echo "  POST http://localhost:5000/download"
echo "  GET  http://localhost:5000/status"
echo "  POST http://localhost:5000/cleanup"
echo "  GET  http://localhost:5000/stats"
echo ""

print_success "Prêt à télécharger de la musique ! 🎵"
echo ""
