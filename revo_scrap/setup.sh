#!/bin/bash

# Script d'installation automatique pour le projet Web Scraper
# Usage: chmod +x setup.sh && ./setup.sh

echo "🚀 INSTALLATION DU PROJET WEB SCRAPER"
echo "======================================"

# Fonction pour vérifier si une commande existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Vérifier Node.js
echo -e "${BLUE}📋 Vérification des prérequis...${NC}"
if command_exists node; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js trouvé: ${NODE_VERSION}${NC}"
    
    # Vérifier si la version est suffisante (>= 14)
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    if [ "$NODE_MAJOR" -lt 14 ]; then
        echo -e "${YELLOW}⚠️  Version Node.js ancienne. Recommandé: >= 14.0.0${NC}"
    fi
else
    echo -e "${RED}❌ Node.js non trouvé!${NC}"
    echo -e "${YELLOW}📥 Installation de Node.js requise: https://nodejs.org/${NC}"
    exit 1
fi

# 2. Vérifier npm
if command_exists npm; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✅ npm trouvé: v${NPM_VERSION}${NC}"
else
    echo -e "${RED}❌ npm non trouvé!${NC}"
    exit 1
fi

echo ""

# 3. Initialiser le projet si package.json n'existe pas
if [ ! -f "package.json" ]; then
    echo -e "${BLUE}📦 Initialisation du projet Node.js...${NC}"
    npm init -y
    echo -e "${GREEN}✅ package.json créé${NC}"
else
    echo -e "${GREEN}✅ package.json existe déjà${NC}"
fi

echo ""

# 4. Installer les dépendances avec versions spécifiques
echo -e "${BLUE}📥 Installation des dépendances...${NC}"

# Liste des packages avec versions testées
PACKAGES=(
    "axios@1.6.0"
    "cheerio@1.0.0-rc.10"
    "fs-extra@11.1.1"
)

for package in "${PACKAGES[@]}"; do
    echo -e "${YELLOW}📦 Installation de ${package}...${NC}"
    npm install "$package"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ ${package} installé avec succès${NC}"
    else
        echo -e "${RED}❌ Erreur lors de l'installation de ${package}${NC}"
        exit 1
    fi
done

echo ""

# 5. Créer la structure de dossiers
echo -e "${BLUE}📁 Création de la structure du projet...${NC}"

DIRS=(
    "src"
    "data"
    "output"
    "logs"
    "config"
)

for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "${GREEN}✅ Dossier ${dir}/ créé${NC}"
    else
        echo -e "${YELLOW}ℹ️  Dossier ${dir}/ existe déjà${NC}"
    fi
done

# 6. Créer les fichiers de configuration
echo -e "${BLUE}⚙️  Création des fichiers de configuration...${NC}"

# .gitignore
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << EOL
# Dépendances
node_modules/
npm-debug.log*

# Données sensibles
config/secrets.json
*.env

# Logs
logs/*.log

# Données temporaires
data/temp/
output/temp/

# OS
.DS_Store
Thumbs.db
EOL
    echo -e "${GREEN}✅ .gitignore créé${NC}"
fi

# Configuration par défaut
if [ ! -f "config/default.json" ]; then
    cat > config/default.json << EOL
{
  "scraper": {
    "delay": 1000,
    "timeout": 10000,
    "userAgent": "Mozilla/5.0 (compatible; WebScraper/1.0)",
    "maxRetries": 3
  },
  "output": {
    "format": "json",
    "directory": "./output",
    "filename": "scraped_data.json"
  },
  "logging": {
    "level": "info",
    "directory": "./logs"
  }
}
EOL
    echo -e "${GREEN}✅ Configuration par défaut créée${NC}"
fi

echo ""

# 7. Test final
echo -e "${BLUE}🧪 Test de l'installation...${NC}"

# Créer un script de test temporaire
cat > test_install.js << EOL
console.log('🚀 Test des dépendances...');

try {
    const axios = require('axios');
    console.log('✅ axios: OK');
} catch (e) {
    console.log('❌ axios: ERREUR');
    process.exit(1);
}

try {
    const cheerio = require('cheerio');
    console.log('✅ cheerio: OK');
} catch (e) {
    console.log('❌ cheerio: ERREUR');
    process.exit(1);
}

try {
    const fs = require('fs-extra');
    console.log('✅ fs-extra: OK');
} catch (e) {
    console.log('❌ fs-extra: ERREUR');
    process.exit(1);
}

console.log('🎉 Tous les tests sont passés !');
EOL

# Exécuter le test
node test_install.js

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Test d'installation réussi !${NC}"
    # Supprimer le fichier de test
    rm test_install.js
else
    echo -e "${RED}❌ Test d'installation échoué${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 INSTALLATION TERMINÉE AVEC SUCCÈS !${NC}"
echo -e "${BLUE}📂 Structure du projet:${NC}"
echo "   ├── src/          (code source)"
echo "   ├── data/         (données brutes)"
echo "   ├── output/       (résultats)"
echo "   ├── logs/         (fichiers de log)"
echo "   ├── config/       (configuration)"
echo "   └── package.json  (dépendances)"
echo ""
echo -e "${YELLOW}💡 Prochaines étapes:${NC}"
echo "   1. Créer tes scripts dans src/"
echo "   2. Modifier config/default.json si nécessaire"
echo "   3. Commencer à coder ton scraper !"
echo ""
echo -e "${BLUE}📖 Pour relancer ce script: ./setup.sh${NC}"
