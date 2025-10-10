#!/bin/bash
# start.sh - Script pour lancer le serveur GrabSong V3

set -e

echo "============================================================"
echo "🎵 Démarrage de GrabSong V3"
echo "============================================================"
echo ""

# Aller dans le dossier python-server
cd "$(dirname "$0")/python-server"

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé"
    echo "💡 Lancez d'abord: bash install.sh"
    exit 1
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Vérifier que les dépendances sont installées
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ Dépendances non installées"
    echo "💡 Lancez d'abord: bash install.sh"
    exit 1
fi

# Lancer le serveur
echo "🚀 Lancement du serveur..."
echo ""
python app.py
