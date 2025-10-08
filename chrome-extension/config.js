// config.js - Configuration centrale pour l'extension

const CONFIG = {
  // ⏱️ TIMING - Délais en millisecondes
  delays: {
    menuOpen: 1000,        // Attendre que le menu s'ouvre
    shareDialog: 1000,     // Attendre que le dialog de partage s'ouvre
    copyAction: 500,       // Attendre après avoir cliqué sur copier
    pageLoad: 2000,        // Attendre que la nouvelle page charge
  },

  // 🎯 SELECTORS - Sélecteurs CSS pour YouTube Music
  selectors: {
    ytMusic: {
      menuButton: 'ytmusic-player-bar ytmusic-menu-renderer #button-shape button',
      menuItems: 'ytmusic-menu-navigation-item-renderer',
      shareLink: 'a#navigation-endpoint',
      
      // Informations de la chanson
      songTitle: 'ytmusic-player-bar .title',
      artistName: 'ytmusic-player-bar .byline',
      albumName: 'ytmusic-player-bar .subtitle',
    },
  },

  // 🌐 TARGET PAGE - Y2Mate configuration
  targetPage: {
    url: 'https://y2mate.nu/',
    selectors: {
      // Step 1: Paste link - Try multiple selectors
      linkInput: 'input[type="text"]',  // Generic text input
      
      // Step 2: Check format and click if not MP3
      mp3Button: 'button:contains("MP3")',  // Button with text "MP3"
      convertButton: 'button:contains("Convert")',  // Button with text "Convert"
      
      // Step 3: Wait for conversion
      progressDiv: '#progress',  // <div id="progress">
      
      // Step 4: Click Download
      downloadButton: 'button[type="button"]:contains("Download")',  // Download button
    }
  },

  // 🎨 UI - Configuration de l'interface
  ui: {
    buttonText: '🎯 Auto Share V2',
    notificationDuration: 3000,  // 3 secondes
  },

  // 🐛 DEBUG - Mode débogage
  debug: true,  // Mettre à false en production
};

// Export pour utilisation dans d'autres fichiers
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CONFIG;
}
