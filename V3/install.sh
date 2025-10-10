#!/bin/bash
# install.sh - Script d'installation automatique pour GrabSong V3
# Usage: bash install.sh

set -e  # Arrêter en cas d'erreur

echo "============================================================"
echo "🎵 Installation de GrabSong V3"
echo "============================================================"
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Détecter l'OS
info "Détection du système d'exploitation..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    success "Linux détecté"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    success "macOS détecté"
else
    error "Système d'exploitation non supporté: $OSTYPE"
    exit 1
fi

echo ""
echo "============================================================"
echo "📦 Étape 1/4: Installation de FFmpeg"
echo "============================================================"

# Vérifier si FFmpeg est déjà installé
if command -v ffmpeg &> /dev/null; then
    success "FFmpeg est déjà installé"
    ffmpeg -version | head -n 1
else
    info "Installation de FFmpeg..."
    
    if [[ "$OS" == "linux" ]]; then
        # Détecter la distribution Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y ffmpeg
        elif command -v yum &> /dev/null; then
            sudo yum install -y ffmpeg
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm ffmpeg
        else
            error "Gestionnaire de paquets non supporté"
            exit 1
        fi
    elif [[ "$OS" == "macos" ]]; then
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            error "Homebrew n'est pas installé. Installez-le depuis https://brew.sh"
            exit 1
        fi
    fi
    
    success "FFmpeg installé avec succès"
fi

echo ""
echo "============================================================"
echo "🐍 Étape 2/4: Vérification de Python"
echo "============================================================"

# Vérifier Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    success "Python3 détecté: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    success "Python détecté: $(python --version)"
else
    error "Python n'est pas installé"
    info "Installez Python 3.8+ depuis https://www.python.org"
    exit 1
fi

# Vérifier la version de Python
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    error "Python 3.8+ requis (version actuelle: $PYTHON_VERSION)"
    exit 1
fi

success "Version Python OK: $PYTHON_VERSION"

echo ""
echo "============================================================"
echo "📚 Étape 3/4: Installation des dépendances Python"
echo "============================================================"

# Aller dans le dossier python-server
cd "$(dirname "$0")/python-server"

# Vérifier si un environnement virtuel existe déjà
if [ -d "venv" ]; then
    info "Environnement virtuel existant détecté"
else
    info "Création d'un environnement virtuel Python..."
    $PYTHON_CMD -m venv venv
    success "Environnement virtuel créé"
fi

# Activer l'environnement virtuel
info "Activation de l'environnement virtuel..."
source venv/bin/activate

# Mettre à jour pip
info "Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances
info "Installation des dépendances depuis requirements.txt..."
pip install -r requirements.txt

success "Dépendances Python installées dans l'environnement virtuel"

echo ""
echo "============================================================"
echo "📁 Étape 4/4: Création des dossiers"
echo "============================================================"

# Créer les dossiers nécessaires
cd ..
mkdir -p temp
mkdir -p music

success "Dossiers créés:"
info "  - temp/  (téléchargements temporaires)"
info "  - music/ (bibliothèque musicale)"

echo ""
echo "============================================================"
echo "✅ Installation terminée avec succès !"
echo "============================================================"
echo ""
echo "🚀 Pour lancer le serveur:"
echo "   cd python-server"
echo "   source venv/bin/activate  # Activer l'environnement virtuel"
echo "   python app.py"
echo ""
echo "💡 Ou utilisez le script de lancement:"
echo "   bash start.sh"
echo ""
echo "🌐 Pour installer l'extension Chrome:"
echo "   1. Ouvrir chrome://extensions/"
echo "   2. Activer 'Mode développeur'"
echo "   3. Charger 'chrome-extension/'"
echo ""
echo "📖 Documentation complète: README.md"
echo ""
echo "============================================================"
