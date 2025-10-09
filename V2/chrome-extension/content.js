/**
 * content.js - GrabSong avec Autoclicker
 * 
 * FONCTIONNALITÉ:
 *   - Autoclicker pour YouTube Music → Y2Mate
 *   - Extraction automatique des métadonnées
 *   - Téléchargement automatique MP3
 *   - Pas de gestion d'images (manuel)
 * 
 * WORKFLOW:
 *   1. Bouton sur YouTube Music
 *   2. Extraction des données (titre, artiste, album, année)
 *   3. Ouverture Y2Mate en arrière-plan
 *   4. Workflow automatique: paste → convert → download
 *   5. Fermeture automatique de l'onglet
 */

console.log('🎵 [GrabSong] content.js chargé');

// ============================================
// CONFIGURATION
// ============================================

const CONFIG = {
  delays: {
    menuOpen: 1000,
    shareDialog: 1000,
    copyAction: 500,
    pageLoad: 2000,
  },
  
  selectors: {
    ytMusic: {
      menuButton: 'ytmusic-player-bar ytmusic-menu-renderer #button-shape button',
      menuItems: 'ytmusic-menu-navigation-item-renderer',
      shareLink: 'a#navigation-endpoint',
      songTitle: 'ytmusic-player-bar .title',
      artistName: 'ytmusic-player-bar .byline',
      albumName: 'ytmusic-player-bar .subtitle',
    },
  },
  
  targetPage: {
    url: 'https://y2mate.nu/',
  },
  
  ui: {
    buttonText: '🎯 GrabSong',
    notificationDuration: 3000,
  },
  
  debug: true,
};

// ============================================
// UTILITAIRES
// ============================================

function log(emoji, message, data = null) {
  if (CONFIG.debug) {
    if (data) {
      console.log(`${emoji} ${message}`, data);
    } else {
      console.log(`${emoji} ${message}`);
    }
  }
}

function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function safeClick(element, description = 'element') {
  if (!element) {
    log('❌', `Cannot click ${description}: element is null`);
    return false;
  }
  
  try {
    element.click();
    log('🎯', `Clicked: ${description}`);
    return true;
  } catch (error) {
    log('❌', `Error clicking ${description}:`, error);
    return false;
  }
}

function findButtonByText(text, tag = 'button') {
  const elements = document.querySelectorAll(tag);
  for (let element of elements) {
    if (element.textContent.includes(text)) {
      return element;
    }
  }
  return null;
}

async function findElementWithRetry(selector, maxAttempts = 5, delayMs = 500) {
  for (let i = 0; i < maxAttempts; i++) {
    const element = document.querySelector(selector);
    if (element) {
      log('✅', `Element found: ${selector}`);
      return element;
    }
    log('🔄', `Attempt ${i + 1}/${maxAttempts} - Element not found: ${selector}`);
    await wait(delayMs);
  }
  log('❌', `Element not found after ${maxAttempts} attempts: ${selector}`);
  return null;
}

// Fonction showNotification supprimée - on utilise le chat maintenant

async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    log('📋', 'Copied to clipboard:', text);
    return true;
  } catch (error) {
    log('❌', 'Failed to copy to clipboard:', error);
    return false;
  }
}

async function readFromClipboard() {
  try {
    const text = await navigator.clipboard.readText();
    log('📋', 'Read from clipboard:', text);
    return text;
  } catch (error) {
    log('❌', 'Failed to read from clipboard:', error);
    return '';
  }
}

// ============================================
// DÉTECTION DE LA PAGE
// ============================================

const isYouTubeMusic = window.location.hostname.includes('music.youtube.com');
const isY2Mate = window.location.hostname.includes('y2mate.nu');

log('🌐', `Page detected - YouTube Music: ${isYouTubeMusic}, Y2Mate: ${isY2Mate}`);

// ============================================
// YOUTUBE MUSIC - INTERFACE
// ============================================

if (isYouTubeMusic) {
  
  // Ancien code supprimé - maintenant on utilise createChatContainer()
  
  // Variables pour le chat dépliant
  let chatExpanded = false;
  let statusPollingInterval = null;
  let settingsExpanded = false;
  
  // Paramètres par défaut
  let settings = {
    position: 'bottom-right', // top-left, top-right, bottom-left, bottom-right
    opacity: 0.95 // 0.5 à 1
  };
  
  // Charger les settings
  function loadSettings() {
    chrome.storage.local.get(['grabsong_settings'], (result) => {
      if (result.grabsong_settings) {
        settings = { ...settings, ...result.grabsong_settings };
      }
      applySettings();
    });
  }
  
  // Appliquer les settings
  function applySettings() {
    const container = document.getElementById('grabsong-container');
    if (!container) return;
    
    // Position
    container.style.top = settings.position.includes('top') ? '20px' : 'auto';
    container.style.bottom = settings.position.includes('bottom') ? '20px' : 'auto';
    container.style.left = settings.position.includes('left') ? '20px' : 'auto';
    container.style.right = settings.position.includes('right') ? '20px' : 'auto';
    
    // Opacité
    container.style.opacity = settings.opacity;
  }
  
  // Créer le conteneur qui combine bouton et chat
  function createChatContainer() {
    if (document.getElementById('grabsong-container')) {
      return;
    }
    
    const container = document.createElement('div');
    container.id = 'grabsong-container';
    container.style.cssText = `
      position: fixed;
      z-index: 999999;
      transition: all 0.3s ease;
      width: 220px;
      display: flex;
      flex-direction: column;
      align-items: stretch;
    `;
    
    // Widget principal
    const widget = document.createElement('div');
    widget.id = 'grabsong-widget';
    widget.style.cssText = `
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 15px;
      box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
      overflow: hidden;
      transition: all 0.3s ease;
    `;
    
    widget.innerHTML = `
      <!-- Header (toujours visible) -->
      <div id="grabsong-header" style="padding: 12px 15px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.2);">
        <div style="display: flex; align-items: center; justify-content: center; gap: 8px; color: white;">
          <span style="font-size: 20px;">🎵</span>
          <span style="font-weight: 600; font-size: 16px;">GrabSong</span>
        </div>
      </div>
      
      <!-- Menu principal (boutons) -->
      <div id="grabsong-menu" style="display: flex; flex-direction: column; gap: 8px; padding: 12px;">
        <button id="grabsong-dl-btn" style="background: rgba(255,255,255,0.9); color: #667eea; border: none; padding: 12px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.2s;">
          <span style="font-size: 18px;">⬇️</span>
          <span>Télécharger</span>
        </button>
        <button id="grabsong-settings-btn" style="background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); padding: 12px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.2s;">
          <span style="font-size: 18px;">⚙️</span>
          <span>Paramètres</span>
        </button>
      </div>
      
      <!-- Contenu Download (caché par défaut) -->
      <div id="grabsong-content-dl" style="display: none;">
        <div id="grabsong-messages" style="padding: 15px; max-height: 450px; background: #f5f5f5; overflow-y: auto; display: flex; flex-direction: column; gap: 10px;">
          <div class="grabsong-message system" style="background: white; padding: 12px; border-radius: 8px; border-left: 4px solid #667eea;">
            <strong>👋 Bienvenue !</strong><br>
            <small>Lancement du téléchargement...</small>
          </div>
        </div>
      </div>
      
      <!-- Contenu Settings (caché par défaut) -->
      <div id="grabsong-content-settings" style="display: none; padding: 15px; background: white;">
        <div style="margin-bottom: 15px;">
          <strong style="color: #667eea;">📍 Position</strong>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px;">
            <button class="position-btn" data-position="top-left" style="padding: 10px; border: 2px solid #ddd; border-radius: 8px; background: white; cursor: pointer; font-size: 12px;">↖️ Haut Gauche</button>
            <button class="position-btn" data-position="top-right" style="padding: 10px; border: 2px solid #ddd; border-radius: 8px; background: white; cursor: pointer; font-size: 12px;">↗️ Haut Droite</button>
            <button class="position-btn" data-position="bottom-left" style="padding: 10px; border: 2px solid #ddd; border-radius: 8px; background: white; cursor: pointer; font-size: 12px;">↙️ Bas Gauche</button>
            <button class="position-btn" data-position="bottom-right" style="padding: 10px; border: 2px solid #ddd; border-radius: 8px; background: white; cursor: pointer; font-size: 12px;">↘️ Bas Droite</button>
          </div>
        </div>
        
        <div style="margin-bottom: 15px;">
          <strong style="color: #667eea;">🎨 Transparence</strong>
          <div style="margin-top: 8px;">
            <input type="range" id="opacity-slider" min="50" max="100" value="95" style="width: 100%;">
            <div style="text-align: center; font-size: 12px; color: #666; margin-top: 5px;">
              <span id="opacity-value">95</span>%
            </div>
          </div>
        </div>
      </div>
      
      <!-- Footer avec bouton Fermer (caché par défaut) -->
      <div id="grabsong-footer" style="display: none; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-top: 1px solid rgba(255,255,255,0.2);">
        <button id="grabsong-close-btn" style="width: 100%; padding: 10px; background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s;">
          Fermer
        </button>
      </div>
    `;
    
    container.appendChild(widget);
    document.body.appendChild(container);
    
    // Event Listeners
    
    // Bouton Download
    document.getElementById('grabsong-dl-btn').addEventListener('click', () => {
      showDownloadView();
    });
    
    // Bouton Settings
    document.getElementById('grabsong-settings-btn').addEventListener('click', () => {
      showSettingsView();
    });
    
    // Bouton Fermer
    document.getElementById('grabsong-close-btn').addEventListener('click', () => {
      showMenuView();
    });
    
    // Boutons position
    document.querySelectorAll('.position-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        settings.position = btn.dataset.position;
        saveSettings();
        applySettings();
        updatePositionButtons();
      });
    });
    
    // Slider opacité
    document.getElementById('opacity-slider').addEventListener('input', (e) => {
      settings.opacity = e.target.value / 100;
      document.getElementById('opacity-value').textContent = e.target.value;
      applySettings();
    });
    
    document.getElementById('opacity-slider').addEventListener('change', () => {
      saveSettings();
    });
    
    // Charger et appliquer les settings
    loadSettings();
    updatePositionButtons();
    
    log('✅', 'Chat container created');
  }
  
  // Sauvegarder les settings
  function saveSettings() {
    chrome.storage.local.set({ grabsong_settings: settings });
  }
  
  // Mettre à jour les boutons de position
  function updatePositionButtons() {
    document.querySelectorAll('.position-btn').forEach(btn => {
      if (btn.dataset.position === settings.position) {
        btn.style.borderColor = '#667eea';
        btn.style.background = '#f0f7ff';
        btn.style.fontWeight = '600';
      } else {
        btn.style.borderColor = '#ddd';
        btn.style.background = 'white';
        btn.style.fontWeight = 'normal';
      }
    });
  }
  
  // Afficher la vue Menu (état initial)
  function showMenuView() {
    const menu = document.getElementById('grabsong-menu');
    const contentDl = document.getElementById('grabsong-content-dl');
    const contentSettings = document.getElementById('grabsong-content-settings');
    const footer = document.getElementById('grabsong-footer');
    const container = document.getElementById('grabsong-container');
    
    menu.style.display = 'flex';
    contentDl.style.display = 'none';
    contentSettings.style.display = 'none';
    footer.style.display = 'none';
    
    // Réduire la largeur
    container.style.width = '220px';
    
    chatExpanded = false;
    settingsExpanded = false;
  }
  
  // Afficher la vue Download
  function showDownloadView() {
    const menu = document.getElementById('grabsong-menu');
    const contentDl = document.getElementById('grabsong-content-dl');
    const contentSettings = document.getElementById('grabsong-content-settings');
    const footer = document.getElementById('grabsong-footer');
    const container = document.getElementById('grabsong-container');
    
    menu.style.display = 'none';
    contentDl.style.display = 'block';
    contentSettings.style.display = 'none';
    footer.style.display = 'block';
    
    // Élargir le widget
    container.style.width = '380px';
    
    chatExpanded = true;
    settingsExpanded = false;
    
    // Lancer le téléchargement si première fois
    const messages = document.getElementById('grabsong-messages');
    if (messages.children.length === 1) {
      performAutoShare();
    }
  }
  
  // Afficher la vue Settings
  function showSettingsView() {
    const menu = document.getElementById('grabsong-menu');
    const contentDl = document.getElementById('grabsong-content-dl');
    const contentSettings = document.getElementById('grabsong-content-settings');
    const footer = document.getElementById('grabsong-footer');
    const container = document.getElementById('grabsong-container');
    
    menu.style.display = 'none';
    contentDl.style.display = 'none';
    contentSettings.style.display = 'block';
    footer.style.display = 'block';
    
    // Largeur moyenne pour settings
    container.style.width = '280px';
    
    chatExpanded = false;
    settingsExpanded = true;
  }
  
  
  // Ajouter un message au chat
  function addChatMessage(message, type = 'info') {
    const messagesContainer = document.getElementById('grabsong-messages');
    if (!messagesContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `grabsong-message ${type}`;
    messageDiv.style.cssText = `
      background: ${type === 'error' ? '#ffebee' : type === 'success' ? '#e8f5e9' : type === 'warning' ? '#fff3e0' : 'white'};
      border-left: 4px solid ${type === 'error' ? '#f44336' : type === 'success' ? '#4CAF50' : type === 'warning' ? '#ff9800' : '#2196F3'};
      padding: 12px;
      margin-bottom: 10px;
      border-radius: 8px;
      font-size: 14px;
      line-height: 1.5;
      animation: slideIn 0.3s ease-out;
    `;
    
    messageDiv.innerHTML = message;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
  
  // Ajouter les styles CSS pour les animations
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideIn {
      from {
        opacity: 0;
        transform: translateX(20px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }
    
    .grabsong-message.system {
      background: #e3f2fd;
      border-left: 4px solid #2196F3;
      padding: 12px;
      margin-bottom: 10px;
      border-radius: 8px;
      font-size: 14px;
      line-height: 1.5;
    }
  `;
  document.head.appendChild(style);

  // Extraire les données de la chanson
  async function extractSongData() {
    log('🎵', 'Extracting song data...');
    
    const songData = {
      title: '',
      artist: '',
      album: '',
      year: '',
      link: '',
      timestamp: Date.now(),
    };

    // Extraire le titre
    const titleElement = document.querySelector(CONFIG.selectors.ytMusic.songTitle);
    if (titleElement) {
      songData.title = titleElement.textContent.trim();
      log('📝', 'Title:', songData.title);
    }

    // Extraire l'artiste, album et année depuis le byline
    const bylineElement = document.querySelector('ytmusic-player-bar .byline.complex-string');
    if (bylineElement) {
      const fullText = bylineElement.textContent.trim();
      log('🔍', 'Full byline text:', fullText);
      
      // Détecter le mode album (contient "lectures", "vues", "J'aime", etc.)
      const isAlbumMode = /lectures|vues|j'aime|views|likes/i.test(fullText);
      
      if (isAlbumMode) {
        log('⚠️', '🎵 MODE ALBUM DÉTECTÉ');
        songData.albumMode = true;
        
        // En mode album, on a généralement juste l'artiste
        const parts = fullText.split('•').map(part => part.trim());
        
        // Le premier élément qui n'est pas un nombre de vues/lectures est l'artiste
        for (let part of parts) {
          if (!/lectures|vues|j'aime|views|likes|k |M /i.test(part)) {
            songData.artist = part.trim();
            log('🎤', 'Artist (album mode):', songData.artist);
            break;
          }
        }
        
        // Chercher l'album et l'année dans le header de la page
        const albumHeader = document.querySelector('ytmusic-responsive-header-renderer');
        if (albumHeader) {
          // Nom de l'album
          const albumTitle = albumHeader.querySelector('h1 .title');
          if (albumTitle) {
            songData.album = albumTitle.textContent.trim();
            log('💿', 'Album (from header):', songData.album);
          }
          
          // Année (dans le subtitle: "Album • 2022")
          const subtitle = albumHeader.querySelector('.subtitle');
          if (subtitle) {
            const subtitleText = subtitle.textContent.trim();
            log('🔍', 'Subtitle text:', subtitleText);
            
            // Séparer par • et chercher l'année
            const subtitleParts = subtitleText.split('•').map(p => p.trim());
            for (let part of subtitleParts) {
              // Chercher une année (4 chiffres uniquement)
              if (/^\d{4}$/.test(part)) {
                songData.year = part;
                log('📅', 'Year (from header):', songData.year);
                break;
              }
            }
          }
        }
        
        if (!songData.album || !songData.year) {
          log('⚠️', 'Album ou année non trouvés dans le header');
        }
      } else {
        // Mode normal (chanson individuelle)
        songData.albumMode = false;
        const parts = fullText.split('•').map(part => part.trim());
        log('📋', 'Byline parts:', parts);
        
        if (parts[0]) {
          songData.artist = parts[0].trim();
          log('🎤', 'Artist:', songData.artist);
        }
        
        if (parts[1]) {
          songData.album = parts[1].trim();
          log('💿', 'Album:', songData.album);
        }
        
        if (parts[2]) {
          const yearText = parts[2].trim();
          if (/^\d{4}$/.test(yearText)) {
            songData.year = yearText;
            log('📅', 'Year:', songData.year);
          }
        }
      }
    }

    return songData;
  }

  // Obtenir le lien de partage
  async function getShareLink() {
    log('🔗', 'Getting share link...');
    
    const previousClipboard = await readFromClipboard();
    
    const menuButton = await findElementWithRetry(CONFIG.selectors.ytMusic.menuButton);
    if (!menuButton) {
      log('❌', 'Menu button not found');
      return '';
    }
    
    safeClick(menuButton, 'menu button');
    await wait(CONFIG.delays.menuOpen);

    const menuItems = document.querySelectorAll(CONFIG.selectors.ytMusic.menuItems);
    let shareClicked = false;
    
    for (let item of menuItems) {
      if (item.textContent.includes('Partager')) {
        const shareLink = item.querySelector(CONFIG.selectors.ytMusic.shareLink);
        if (shareLink) {
          safeClick(shareLink, 'share button');
          shareClicked = true;
          break;
        }
      }
    }

    if (!shareClicked) {
      log('❌', 'Share button not found');
      return '';
    }

    await wait(CONFIG.delays.shareDialog);

    const copyButton = findButtonByText('Copier') || findButtonByText('Copy');
    if (!copyButton) {
      log('❌', 'Copy button not found');
      return '';
    }

    safeClick(copyButton, 'copy button');
    await wait(CONFIG.delays.copyAction);

    const shareLink = await readFromClipboard();
    
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
    
    log('✅', 'Share link obtained:', shareLink);
    return shareLink;
  }

  // Fonction principale
  async function performAutoShare() {
    log('🚀', '=== Starting GrabSong ===');
    
    try {
      // Étape 1: Extraction
      addChatMessage('<div style="font-size: 14px; font-weight: 600; color: #667eea; margin-bottom: 5px;">🎵 Étape 1/4 : Extraction</div>Récupération des métadonnées de la chanson...', 'info');
      const songData = await extractSongData();
      
      songData.link = await getShareLink();
      
      if (!songData.link || !songData.title) {
        // Aucune musique en cours ou erreur d'extraction
        addChatMessage(
          `<div style="background: #fff3e0; border: 2px solid #ff9800; border-radius: 10px; padding: 15px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 10px;">⚠️</div>
            <strong style="color: #e65100; font-size: 16px;">Aucune musique détectée</strong>
            <p style="margin: 10px 0; color: #666; font-size: 14px;">
              Assurez-vous qu'une musique est en cours de lecture sur YouTube Music
            </p>
            <button id="retry-btn" style="background: #ff9800; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 14px; margin-top: 10px; transition: all 0.2s;">
              🔄 Réessayer
            </button>
            <p style="margin: 10px 0 0 0; font-size: 12px; color: #999;">
              💡 N'oubliez pas de lancer une musique !
            </p>
          </div>`,
          'warning'
        );
        
        // Event listener pour le bouton Retry
        setTimeout(() => {
          const retryBtn = document.getElementById('retry-btn');
          if (retryBtn) {
            retryBtn.addEventListener('click', () => {
              // Clear les messages et recommencer
              const messages = document.getElementById('grabsong-messages');
              while (messages.children.length > 1) {
                messages.removeChild(messages.lastChild);
              }
              performAutoShare();
            });
            
            retryBtn.addEventListener('mouseenter', () => {
              retryBtn.style.background = '#f57c00';
              retryBtn.style.transform = 'scale(1.05)';
            });
            retryBtn.addEventListener('mouseleave', () => {
              retryBtn.style.background = '#ff9800';
              retryBtn.style.transform = 'scale(1)';
            });
          }
        }, 100);
        
        return;
      }
      
      addChatMessage('<strong>✅</strong> Données extraites avec succès !', 'success');
      
      // Étape 2: Afficher le formulaire d'édition
      addChatMessage('<div style="font-size: 14px; font-weight: 600; color: #667eea; margin-bottom: 5px;">✏️ Étape 2/4 : Vérification</div>Vérifiez les informations ci-dessous', 'info');
      
      // Notification si mode album
      if (songData.albumMode) {
        addChatMessage(
          '<strong>⚠️ Mode Album détecté</strong><br><small>Album et Année extraits automatiquement</small>',
          'warning'
        );
      }
      
      showEditForm(songData);
      
    } catch (error) {
      log('❌', 'Error in performAutoShare:', error);
      addChatMessage(`<strong>❌ Erreur:</strong> ${error.message}`, 'error');
    }
  }
  
  // Afficher le formulaire d'édition
  function showEditForm(songData) {
    const messagesContainer = document.getElementById('grabsong-messages');
    if (!messagesContainer) return;
    
    const formDiv = document.createElement('div');
    formDiv.id = 'grabsong-edit-form';
    formDiv.style.cssText = `
      background: white;
      border: 2px solid #667eea;
      border-radius: 10px;
      padding: 15px;
      margin-bottom: 10px;
    `;
    
    formDiv.innerHTML = `
      <div style="margin-bottom: 15px;">
        <strong style="color: #667eea;">✏️ Modifier les informations</strong>
      </div>
      
      ${songData.albumMode ? `
      <div style="background: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; padding: 12px; margin-bottom: 15px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 20px;">⚠️</span>
          <div>
            <strong style="color: #856404; font-size: 14px;">Mode Album Détecté</strong>
            <p style="margin: 5px 0 0 0; font-size: 12px; color: #856404;">
              Les informations Album et Année ne sont pas disponibles automatiquement.<br>
              Veuillez les remplir manuellement.
            </p>
          </div>
        </div>
      </div>
      ` : ''}
      
      <div style="margin-bottom: 10px;">
        <label style="display: block; font-size: 12px; color: #666; margin-bottom: 5px;">🎤 Artiste</label>
        <input type="text" id="edit-artist" value="${songData.artist || ''}" 
               style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px;">
      </div>
      
      <div style="margin-bottom: 10px;">
        <label style="display: block; font-size: 12px; color: #666; margin-bottom: 5px;">💿 Album</label>
        <input type="text" id="edit-album" value="${songData.album || ''}" 
               style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px;">
      </div>
      
      <div style="margin-bottom: 10px;">
        <label style="display: block; font-size: 12px; color: #666; margin-bottom: 5px;">🎵 Titre</label>
        <input type="text" id="edit-title" value="${songData.title || ''}" 
               style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px;">
      </div>
      
      <div style="margin-bottom: 15px;">
        <label style="display: block; font-size: 12px; color: #666; margin-bottom: 5px;">📅 Année</label>
        <input type="text" id="edit-year" value="${songData.year || ''}" 
               style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px;">
      </div>
      
      <div style="margin-bottom: 10px;">
        <strong style="font-size: 12px; color: #666;">📝 Aperçu du nom de fichier:</strong>
        <div id="filename-preview" style="background: #f0f0f0; padding: 8px; border-radius: 5px; margin-top: 5px; font-size: 12px; word-break: break-all; font-family: monospace;">
          ${generateFilename(songData)}
        </div>
      </div>
      
      <button id="save-and-continue" style="
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.2s;
      ">
        💾 Sauvegarder et Continuer
      </button>
    `;
    
    messagesContainer.appendChild(formDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Mettre à jour l'aperçu en temps réel
    const inputs = ['edit-artist', 'edit-album', 'edit-title', 'edit-year'];
    inputs.forEach(id => {
      document.getElementById(id).addEventListener('input', () => {
        updateFilenamePreview();
      });
    });
    
    // Bouton sauvegarder
    document.getElementById('save-and-continue').addEventListener('click', () => {
      saveAndContinue(songData);
    });
    
    // Effet hover sur le bouton
    const saveBtn = document.getElementById('save-and-continue');
    saveBtn.addEventListener('mouseenter', () => {
      saveBtn.style.transform = 'scale(1.02)';
    });
    saveBtn.addEventListener('mouseleave', () => {
      saveBtn.style.transform = 'scale(1)';
    });
  }
  
  // Générer le nom de fichier
  function generateFilename(data) {
    const parts = [];
    if (data.artist) parts.push(`art=${data.artist}`);
    if (data.album) parts.push(`alb=${data.album}`);
    if (data.title) parts.push(`N=${data.title}`);
    if (data.year) parts.push(`Y=${data.year}`);
    
    const filename = parts.join(' ') + '.mp3';
    return filename.replace(/[<>"/\\|?*]/g, '');
  }
  
  // Mettre à jour l'aperçu du nom de fichier
  function updateFilenamePreview() {
    const data = {
      artist: document.getElementById('edit-artist').value,
      album: document.getElementById('edit-album').value,
      title: document.getElementById('edit-title').value,
      year: document.getElementById('edit-year').value,
    };
    
    const preview = document.getElementById('filename-preview');
    if (preview) {
      preview.textContent = generateFilename(data);
    }
  }
  
  // Sauvegarder et continuer
  async function saveAndContinue(songData) {
    // Récupérer les valeurs modifiées
    songData.artist = document.getElementById('edit-artist').value;
    songData.album = document.getElementById('edit-album').value;
    songData.title = document.getElementById('edit-title').value;
    songData.year = document.getElementById('edit-year').value;
    
    // Supprimer le formulaire
    const form = document.getElementById('grabsong-edit-form');
    if (form) {
      form.remove();
    }
    
    // Afficher les données validées
    addChatMessage(
      `<strong>✅ Données validées:</strong><br>
      🎤 Artiste: ${songData.artist || 'N/A'}<br>
      💿 Album: ${songData.album || 'N/A'}<br>
      🎵 Titre: ${songData.title || 'N/A'}<br>
      📅 Année: ${songData.year || 'N/A'}`,
      'success'
    );
    
    // Continuer avec le workflow
    continueWorkflow(songData);
  }
  
  // Continuer le workflow après validation
  async function continueWorkflow(songData) {
    try {
      // Étape 3: Sauvegarde Python
      addChatMessage('<div style="font-size: 14px; font-weight: 600; color: #667eea; margin-bottom: 5px;">💾 Étape 3/4 : Sauvegarde</div>Envoi des données au serveur Python...', 'info');
      
      const parts = [];
      if (songData.artist) parts.push(`art=${songData.artist}`);
      if (songData.album) parts.push(`alb=${songData.album}`);
      if (songData.title) parts.push(`N=${songData.title}`);
      if (songData.year) parts.push(`Y=${songData.year}`);
      
      const filename = parts.join(' ') + '.mp3';
      const cleanFilename = filename.replace(/[<>"/\\|?*]/g, '');
      
      log('📝', 'Filename created:', cleanFilename);
      
      await copyToClipboard(cleanFilename);
      
      songData.filename = cleanFilename;
      
      // Sauvegarder dans le storage
      chrome.storage.local.set({ pendingSongData: songData }, () => {
        log('💾', 'Data saved to storage');
      });
      
      // Envoyer via background script (pour éviter CORS)
      chrome.runtime.sendMessage({
        action: 'send_to_flask',
        data: songData
      }, (response) => {
        if (response && response.success) {
          log('✅', 'Données envoyées à Python:', response);
          // Message supprimé - pas besoin d'afficher
        } else {
          log('⚠️', 'Python non connecté:', response);
          addChatMessage(
            '<strong>⚠️ Serveur Python non accessible</strong><br>' +
            '<small>Lancez: <code>python app.py</code></small>',
            'warning'
          );
        }
      });
      
      // Étape 4: Téléchargement
      addChatMessage('<div style="font-size: 14px; font-weight: 600; color: #667eea; margin-bottom: 5px;">⬇️ Étape 4/4 : Téléchargement</div>Lancement du téléchargement automatique...', 'info');
      
      chrome.runtime.sendMessage({
        action: 'openTab',
        url: CONFIG.targetPage.url,
        data: songData
      });
      
      // Animation loading en attente
      addChatMessage(
        `<div style="text-align: center; padding: 20px;">
          <div style="display: inline-block; width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; animation: spin 1s linear infinite;"></div>
          <div style="margin-top: 10px; color: #667eea; font-weight: 600;">En attente de la fenêtre de téléchargement...</div>
          <style>
            @keyframes spin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
          </style>
        </div>`,
        'info'
      );
      
      // Démarrer le polling du statut Python
      startStatusPolling();
      
      log('✅', '=== GrabSong Complete ===');
      
    } catch (error) {
      log('❌', 'Error in continueWorkflow:', error);
      addChatMessage(`<strong>❌ Erreur:</strong> ${error.message}`, 'error');
    }
  }

  // Initialiser
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      createChatContainer();
    });
  } else {
    createChatContainer();
  }

  // Polling du statut Python
  function startStatusPolling() {
    log('🔄', 'Démarrage du polling du statut Python...');
    
    // Arrêter un éventuel polling en cours
    if (statusPollingInterval) {
      clearInterval(statusPollingInterval);
    }
    
    // Vérifier le statut toutes les 3 secondes
    statusPollingInterval = setInterval(() => {
      chrome.runtime.sendMessage({
        action: 'check_python_status'
      }, (response) => {
        if (response && response.last_completed) {
          // Téléchargement terminé !
          log('🎉', 'Téléchargement confirmé:', response.last_completed);
          
          // Arrêter le polling
          clearInterval(statusPollingInterval);
          statusPollingInterval = null;
          
          // Supprimer l'animation loading
          const messages = document.getElementById('grabsong-messages');
          if (messages) {
            const loadingDivs = messages.querySelectorAll('div');
            loadingDivs.forEach(div => {
              if (div.textContent.includes('En attente de la fenêtre')) {
                div.remove();
              }
            });
          }
          
          // Extraire artiste et album du filename
          const filename = response.last_completed.filename;
          let artist = 'Unknown';
          let album = 'Unknown';
          
          const artistMatch = filename.match(/art=([^]+?)(?:\s+alb=|$)/);
          const albumMatch = filename.match(/alb=([^]+?)(?:\s+N=|$)/);
          
          if (artistMatch) artist = artistMatch[1].trim();
          if (albumMatch) album = albumMatch[1].trim();
          
          // Clear tous les messages sauf le premier (bienvenue)
          while (messages.children.length > 1) {
            messages.removeChild(messages.lastChild);
          }
          
          // Message final unique avec toutes les infos
          const finalDiv = document.createElement('div');
          finalDiv.className = 'grabsong-message success';
          finalDiv.setAttribute('data-final-message', 'true');
          finalDiv.innerHTML = `
            <div style="background: linear-gradient(135deg, #e8f5e9 0%, #f1f8f4 100%); border: 2px solid #4caf50; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);">
              <div style="text-align: center; margin-bottom: 15px;">
                <span style="font-size: 32px;">✅</span>
                <div style="font-size: 18px; font-weight: 700; color: #2e7d32; margin-top: 8px;">Téléchargement terminé !</div>
              </div>
              
              <div style="background: white; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                <div style="font-size: 12px; color: #666; margin-bottom: 4px;">📁 Fichier</div>
                <div style="font-size: 13px; font-weight: 600; color: #333; word-break: break-all;">${filename}</div>
              </div>
              
              <div style="background: white; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
                <div style="font-size: 12px; color: #666; margin-bottom: 4px;">📂 Organisé dans</div>
                <div style="font-size: 14px; font-weight: 600; color: #667eea;">${artist} / ${album}</div>
              </div>
              
              <div style="text-align: center; padding-top: 12px; border-top: 2px solid #e0e0e0;">
                <div style="font-size: 13px; color: #666; margin-bottom: 8px;">Reset dans <span id="countdown">3</span> secondes...</div>
                <div style="background: #e0e0e0; height: 6px; border-radius: 3px; overflow: hidden;">
                  <div id="progress-bar" style="background: linear-gradient(90deg, #4caf50, #66bb6a); height: 100%; width: 100%; transition: width 0.1s linear;"></div>
                </div>
              </div>
            </div>
          `;
          messages.appendChild(finalDiv);
          
          // Scroll vers le message
          messages.scrollTop = messages.scrollHeight;
          
          // Animation countdown + barre de progression
          let secondsLeft = 3;
          const countdownEl = document.getElementById('countdown');
          const progressBar = document.getElementById('progress-bar');
          
          const countdownInterval = setInterval(() => {
            secondsLeft -= 0.1;
            
            if (secondsLeft <= 0) {
              clearInterval(countdownInterval);
              resetExtension();
            } else {
              // Afficher le nombre de secondes (arrondi supérieur, mais afficher 0 quand < 0.5)
              if (countdownEl) {
                const displaySeconds = secondsLeft < 0.5 ? 0 : Math.ceil(secondsLeft);
                countdownEl.textContent = displaySeconds;
              }
              
              // Barre de progression
              if (progressBar) {
                const percentage = Math.max(0, (secondsLeft / 3) * 100);
                progressBar.style.width = `${percentage}%`;
              }
            }
          }, 100);
        }
        
        if (response && response.last_error) {
          // Erreur détectée
          log('❌', 'Erreur Python:', response.last_error);
          
          // Arrêter le polling
          clearInterval(statusPollingInterval);
          statusPollingInterval = null;
          
          addChatMessage(
            `<strong>❌ Erreur Python:</strong><br>${response.last_error}`,
            'error'
          );
        }
      });
    }, 3000); // Vérifier toutes les 3 secondes
  }
  
  // Fonction de reset de l'extension
  function resetExtension() {
    log('🔄', 'Reset de l\'extension...');
    
    // Fermer le chat
    if (chatExpanded) {
      toggleChat();
    }
    
    // Vider les messages (garder seulement le message de bienvenue)
    const messagesContainer = document.getElementById('grabsong-messages');
    if (messagesContainer) {
      messagesContainer.innerHTML = `
        <div class="grabsong-message system">
          <strong>👋 Bienvenue !</strong><br>
          Cliquez pour télécharger une chanson depuis YouTube Music.
        </div>
      `;
    }
    
    log('✅', 'Extension réinitialisée - Prête pour un nouveau téléchargement');
  }
  
  // Écouter les messages de la popup et du background
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'performClick') {
      performAutoShare();
      sendResponse({ success: true });
    }
    
    if (request.action === 'download_complete') {
      // Python a terminé le téléchargement
      log('🎉', 'Téléchargement terminé:', request.data);
      
      // Afficher le message de succès
      addChatMessage(
        `<strong>🎉 Téléchargement terminé !</strong><br><br>
        📁 Fichier: <strong>${request.data.filename}</strong><br>
        📂 Dossier: ${request.data.path || 'Downloads'}<br><br>
        <em>✨ L'extension va se réinitialiser dans 3 secondes...</em>`,
        'success'
      );
      
      // Reset après 3 secondes
      setTimeout(() => {
        resetExtension();
      }, 3000);
      
      sendResponse({ success: true });
    }
    
    return true;
  });
}

// ============================================
// Y2MATE - AUTO-WORKFLOW
// ============================================

if (isY2Mate) {
  log('🎯', 'Y2Mate page detected, starting workflow...');
  
  setTimeout(() => {
    fillY2MateFields();
  }, 500);
}

async function fillY2MateFields() {
  log('📝', 'Starting Y2Mate workflow...');
  
  const data = await new Promise((resolve) => {
    chrome.storage.local.get(['pendingSongData'], (result) => {
      resolve(result.pendingSongData || null);
    });
  });
  
  if (!data) {
    log('❌', 'No data found in storage');
    return;
  }
  
  log('📦', 'Data retrieved:', data);
  
  try {
    await pasteYouTubeLink(data.link);
    await selectMP3Format();
    await clickConvertButton();
    await waitForConversion();
    await clickDownloadButton(data.filename);
    
    chrome.storage.local.remove(['pendingSongData']);
    
    log('🎉', 'Y2Mate workflow complete!');
    
  } catch (error) {
    log('❌', 'Error in Y2Mate workflow:', error);
  }
}

async function pasteYouTubeLink(link) {
  log('🔗', 'Step 1: Pasting YouTube link...');
  
  await wait(2000);
  
  const selectors = [
    'input[type="text"]',
    'input[placeholder*="YouTube"]',
    'input[placeholder*="youtube"]',
    'input[placeholder*="video"]',
    'input[placeholder*="URL"]',
    'input[placeholder*="url"]',
    'input.form-control',
    'input#url',
    'input#search',
    'textarea'
  ];
  
  let linkInput = null;
  for (const selector of selectors) {
    linkInput = document.querySelector(selector);
    if (linkInput) {
      log('✅', `Found input with selector: ${selector}`);
      break;
    }
  }
  
  if (!linkInput) {
    const allInputs = document.querySelectorAll('input, textarea');
    for (const input of allInputs) {
      const isVisible = input.offsetParent !== null && 
                       input.type !== 'hidden' &&
                       window.getComputedStyle(input).display !== 'none';
      if (isVisible) {
        linkInput = input;
        log('✅', 'Found first visible input');
        break;
      }
    }
  }
  
  if (!linkInput) {
    throw new Error('Link input not found');
  }
  
  linkInput.focus();
  linkInput.value = link;
  
  linkInput.dispatchEvent(new Event('input', { bubbles: true }));
  linkInput.dispatchEvent(new Event('change', { bubbles: true }));
  linkInput.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
  linkInput.dispatchEvent(new Event('paste', { bubbles: true }));
  
  log('✅', 'Link pasted:', link);
  
  await wait(1500);
}

async function selectMP3Format() {
  log('🎵', 'Step 2: Checking format...');
  
  await wait(1000);
  
  const mp4Button = findButtonByText('MP4');
  
  if (mp4Button) {
    const mp4IsSelected = mp4Button.classList.contains('active') || 
                          mp4Button.classList.contains('selected') ||
                          mp4Button.getAttribute('aria-selected') === 'true';
    
    if (mp4IsSelected) {
      log('⚠️', 'MP4 is selected, switching to MP3...');
      
      const mp3Button = findButtonByText('MP3');
      if (mp3Button) {
        safeClick(mp3Button, 'MP3 button');
        log('✅', 'Switched to MP3');
        await wait(500);
      }
    }
  }
}

async function clickConvertButton() {
  log('⚙️', 'Step 3: Clicking Convert button...');
  
  await wait(500);
  
  const convertButton = findButtonByText('Convert');
  if (!convertButton) {
    throw new Error('Convert button not found');
  }
  
  safeClick(convertButton, 'Convert button');
  log('✅', 'Convert button clicked');
  
  await wait(1000);
}

async function waitForConversion() {
  log('⏳', 'Step 4: Waiting for conversion...');
  
  const progressDiv = await findElementWithRetry('#progress', 30, 1000);
  
  if (progressDiv) {
    log('🔄', 'Conversion in progress...');
    
    let attempts = 0;
    const maxAttempts = 60;
    
    while (attempts < maxAttempts) {
      await wait(1000);
      
      const stillConverting = document.querySelector('#progress');
      if (!stillConverting || stillConverting.style.display === 'none') {
        log('✅', 'Conversion complete!');
        break;
      }
      
      attempts++;
      if (attempts % 5 === 0) {
        log('⏳', `Still converting... (${attempts}s)`);
      }
    }
    
    if (attempts >= maxAttempts) {
      throw new Error('Conversion timeout');
    }
  }
  
  await wait(2000);
}

async function clickDownloadButton(filename) {
  log('⬇️', 'Step 5: Clicking Download button...');
  
  const downloadButton = findButtonByText('Download');
  
  if (!downloadButton) {
    throw new Error('Download button not found');
  }
  
  if (downloadButton.tagName === 'A' && downloadButton.hasAttribute('href')) {
    downloadButton.setAttribute('download', filename);
    log('✅', 'Download attribute set to:', filename);
  }
  
  safeClick(downloadButton, 'Download button');
  log('✅', 'Download button clicked!');
  
  await wait(2000);
  
  log('🔒', 'Closing Y2Mate tab...');
  chrome.runtime.sendMessage({
    action: 'closeCurrentTab'
  });
}

// ============================================
// FALLBACK
// ============================================

if (!isYouTubeMusic && !isY2Mate) {
  log('ℹ️', 'Extension loaded but not on YouTube Music or Y2Mate');
}

console.log('✅ GrabSong content.js initialisé');
