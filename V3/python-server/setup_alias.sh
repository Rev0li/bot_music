#!/bin/bash
# ============================================
# 🎵 GrabSong V3 - Configuration des alias
# ============================================
# 
# Ce script ajoute des alias pratiques à votre shell
#
# Usage:
#   source setup_alias.sh
# ============================================

# Couleurs
GREEN='\033[0;32m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Déterminer le fichier de configuration du shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    echo "Shell non supporté. Utilisez bash ou zsh."
    exit 1
fi

# Obtenir le chemin absolu du dossier python-server
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${PURPLE}============================================${NC}"
echo -e "${PURPLE}🎵 Configuration des alias GrabSong${NC}"
echo -e "${PURPLE}============================================${NC}"
echo ""
echo -e "${CYAN}Shell détecté: $SHELL_NAME${NC}"
echo -e "${CYAN}Fichier de config: $SHELL_RC${NC}"
echo -e "${CYAN}Dossier: $SCRIPT_DIR${NC}"
echo ""

# Créer les alias
ALIAS_CONTENT="
# ============================================
# 🎵 GrabSong V3 - Alias
# ============================================
alias grabsong-install='cd \"$SCRIPT_DIR\" && ./install.sh'
alias grabsong-start='cd \"$SCRIPT_DIR\" && ./start.sh'
alias grabsong-cd='cd \"$SCRIPT_DIR\"'
alias grabsong-ping='curl http://localhost:5000/ping'
alias grabsong-stats='curl http://localhost:5000/stats'
alias grabsong-cleanup='curl -X POST http://localhost:5000/cleanup'
"

# Vérifier si les alias existent déjà
if grep -q "GrabSong V3 - Alias" "$SHELL_RC" 2>/dev/null; then
    echo -e "${GREEN}✅ Les alias existent déjà dans $SHELL_RC${NC}"
    echo ""
    echo "Voulez-vous les mettre à jour ? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        # Supprimer les anciens alias
        sed -i '/# GrabSong V3 - Alias/,/^$/d' "$SHELL_RC"
        echo "$ALIAS_CONTENT" >> "$SHELL_RC"
        echo -e "${GREEN}✅ Alias mis à jour${NC}"
    else
        echo "Annulé."
        exit 0
    fi
else
    # Ajouter les alias
    echo "$ALIAS_CONTENT" >> "$SHELL_RC"
    echo -e "${GREEN}✅ Alias ajoutés à $SHELL_RC${NC}"
fi

echo ""
echo -e "${PURPLE}============================================${NC}"
echo -e "${PURPLE}📝 Alias disponibles:${NC}"
echo -e "${PURPLE}============================================${NC}"
echo ""
echo -e "${CYAN}grabsong-install${NC}  → Installer les dépendances"
echo -e "${CYAN}grabsong-start${NC}    → Démarrer le serveur"
echo -e "${CYAN}grabsong-cd${NC}       → Aller dans le dossier python-server"
echo -e "${CYAN}grabsong-ping${NC}     → Tester la connexion au serveur"
echo -e "${CYAN}grabsong-stats${NC}    → Voir les statistiques"
echo -e "${CYAN}grabsong-cleanup${NC}  → Nettoyer le dossier temp/"
echo ""
echo -e "${GREEN}Pour activer les alias, exécutez:${NC}"
echo -e "  ${CYAN}source $SHELL_RC${NC}"
echo ""
echo -e "${GREEN}Ou redémarrez votre terminal${NC}"
echo ""
