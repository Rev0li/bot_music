# 🎵 Web Scraper Musical

Un projet d'apprentissage pour récupérer des informations musicales depuis des pages web et les stocker au format JSON.

## 📋 Table des matières

- [Description](#description)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Structure du projet](#structure-du-projet)
- [Utilisation](#utilisation)
- [Configuration](#configuration)
- [Exemples](#exemples)
- [Dépannage](#dépannage)
- [Contribution](#contribution)

## 📝 Description

Ce projet permet de :
- ✅ Récupérer le contenu HTML de pages web
- ✅ Extraire des informations spécifiques (titres, artistes, liens, images)
- ✅ Sauvegarder les données au format JSON
- ✅ Organiser les fichiers de sortie
- ✅ Communiquer entre JavaScript et Python (à venir)

**⚠️ Important :** Ce projet est à des fins éducatives uniquement. Respectez toujours les conditions d'utilisation des sites web et les droits d'auteur.

## 🔧 Prérequis

- **Node.js** >= 14.0.0
- **npm** >= 6.0.0
- **Git** (optionnel)

### Vérifier les prérequis

```bash
node --version
npm --version
```

## 🚀 Installation

### Installation automatique (recommandée)

```bash
# Cloner le projet
git clone https://github.com/ton-username/web-scraper-musical.git
cd web-scraper-musical

# Lancer l'installation automatique
chmod +x setup.sh
./setup.sh
```

### Installation manuelle

```bash
# Initialiser le projet
npm init -y

# Installer les dépendances
npm install axios@1.6.0 cheerio@1.0.0-rc.10 fs-extra@11.1.1

# Créer la structure de dossiers
mkdir -p src data output logs config
```

## 📂 Structure du projet

```
web-scraper-musical/
├── 📦 node_modules/          # Dépendances (auto-générées)
├── 📝 src/                   # Code source
│   ├── scraper.js           # Script principal de scraping
│   ├── parser.js            # Fonctions de parsing HTML
│   └── utils.js             # Fonctions utilitaires
├── 💾 data/                  # Données brutes récupérées
│   ├── raw/                 # HTML brut
│   └── temp/                # Fichiers temporaires
├── 📊 output/                # Résultats finaux
│   ├── json/                # Fichiers JSON
│   └── reports/             # Rapports de scraping
├── 📋 logs/                  # Fichiers de log
├── ⚙️ config/                # Configuration
│   └── default.json         # Configuration par défaut
├── 📄 package.json           # Dépendances et scripts
├── 🚫 .gitignore            # Fichiers ignorés par git
├── 🛠️ setup.sh              # Script d'installation
└── 📖 README.md             # Ce fichier
```

## 🎯 Utilisation

### Scraping basique

```bash
# Aller dans le dossier src
cd src

# Lancer le scraper
node scraper.js
```

### Avec paramètres

```javascript
// Dans ton script
const scraper = new WebScraper();

// Scraper une page
const data = await scraper.scrapeWebsite('https://example.com', {
    title: '.song-title',
    artist: '.artist-name',
    album: '.album-name'
});

// Sauvegarder en JSON
await scraper.saveToJSON('ma_musique.json');
```

## ⚙️ Configuration

Modifie le fichier `config/default.json` :

```json
{
  "scraper": {
    "delay": 1000,           // Délai entre requêtes (ms)
    "timeout": 10000,        // Timeout des requêtes (ms)
    "userAgent": "Mozilla/5.0...",
    "maxRetries": 3          // Nombre de tentatives
  },
  "output": {
    "format": "json",        // Format de sortie
    "directory": "./output", // Dossier de sortie
    "filename": "scraped_data.json"
  },
  "logging": {
    "level": "info",         // Niveau de log
    "directory": "./logs"    // Dossier des logs
  }
}
```

## 📚 Exemples

### Exemple 1 : Scraper des informations de base

```javascript
const WebScraper = require('./src/scraper');

async function exemple1() {
    const scraper = new WebScraper();
    
    const selectors = {
        title: 'h1',
        description: '.description',
        links: 'a'
    };
    
    const data = await scraper.scrapeWebsite('https://httpbin.org/html', selectors);
    console.log(data);
}

exemple1();
```

### Exemple 2 : Scraper plusieurs pages

```javascript
async function exemple2() {
    const scraper = new WebScraper();
    const urls = [
        'https://site1.com',
        'https://site2.com',
        'https://site3.com'
    ];
    
    for (const url of urls) {
        await scraper.scrapeWebsite(url, selectors);
        // Pause respectueuse entre les requêtes
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    await scraper.saveToJSON('resultats_multiples.json');
}
```

### Exemple 3 : Filtrer et nettoyer les données

```javascript
async function exemple3() {
    const scraper = new WebScraper();
    
    // Scraper des données
    await scraper.scrapeWebsite(url, selectors);
    
    // Nettoyer les données
    scraper.cleanData();
    
    // Chercher dans les données
    const results = scraper.search('rock');
    console.log(`Trouvé ${results.length} résultats pour "rock"`);
}
```

## 🧪 Tests

```bash
# Tester l'installation
node -e "console.log('Node.js fonctionne !'); require('axios'); require('cheerio'); console.log('Toutes les dépendances OK!');"

# Tester le scraper basique
cd src
node -e "const scraper = require('./scraper'); console.log('Scraper chargé avec succès!');"
```

## 🐛 Dépannage

### Erreur "Module not found"
```bash
# Réinstaller les dépendances
rm -rf node_modules package-lock.json
npm install
```

### Erreur avec Cheerio
```bash
# Installer la version compatible
npm uninstall cheerio
npm install cheerio@1.0.0-rc.10
```

### Erreur CORS ou 403
- Vérifiez le User-Agent dans la configuration
- Ajoutez des délais entre les requêtes
- Respectez les robots.txt du site

### Timeout des requêtes
- Augmentez le timeout dans `config/default.json`
- Vérifiez votre connexion internet
- Le site cible est peut-être lent

## 📈 Fonctionnalités à venir

- [ ] Interface Python pour traitement avancé
- [ ] Création automatique de dossiers organisés
- [ ] Modification des métadonnées de fichiers
- [ ] Interface web pour configuration
- [ ] Support de différents formats de sortie
- [ ] Planification automatique de scraping

## 🤝 Contribution

1. Fork le projet
2. Crée une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit tes changements (`git commit -am 'Ajoute une nouvelle fonctionnalité'`)
4. Push sur la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvre une Pull Request

## 📜 Licence

Ce projet est à des fins éducatives uniquement. 

**Rappel important :** 
- Respectez les robots.txt des sites
- Ne surchargez pas les serveurs (utilisez des délais)
- Respectez les droits d'auteur et les conditions d'utilisation
- Ce code est fourni tel quel, sans garantie

## 👤 Auteur

**Ton nom**
- GitHub: [@ton-username](https://github.com/ton-username)
- Email: ton-email@example.com

## 🙏 Remerciements

- [Axios](https://github.com/axios/axios) pour les requêtes HTTP
- [Cheerio](https://github.com/cheeriojs/cheerio) pour le parsing HTML
- [fs-extra](https://github.com/jprichardson/node-fs-extra) pour la gestion des fichiers
- La communauté Node.js pour les ressources d'apprentissage

---

**🎵 Happy scraping! (légalement et respectueusement)**
