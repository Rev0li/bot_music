/**
 * content.js - GrabSong V3 avec yt-dlp
 * 
 * FONCTIONNALITÉ:
 *   - Interface utilisateur sur YouTube Music
 *   - Extraction automatique des métadonnées
 *   - Communication avec le serveur Python (yt-dlp)
 *   - Pas de Y2Mate, pas de Save As, tout en direct !
 * 
 * WORKFLOW:
 *   1. Bouton sur YouTube Music
 *   2. Extraction des données (titre, artiste, album, année)
 *   3. Envoi au serveur Python
 *   4. Téléchargement via yt-dlp
 *   5. Organisation automatique
 */

console.log('🎵 [GrabSong V3] content.js chargé');

// ============================================
// CONFIGURATION
// ============================================

const CONFIG = {
  delays: {
    menuOpen: 1000,
    shareDialog: 1000,
    copyAction: 500,
    statusPoll: 1000, // Polling toutes les secondes
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
// INTERFACE UTILISATEUR
// ============================================

// Variables globales
let settings = {
  position: 'bottom-right',
  opacity: 0.95,
  customFolder: '' // Dossier personnalisé pour sauvegarder la musique
};

let statusPollingInterval = null;

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
  
  container.style.top = settings.position.includes('top') ? '20px' : 'auto';
  container.style.bottom = settings.position.includes('bottom') ? '20px' : 'auto';
  container.style.left = settings.position.includes('left') ? '20px' : 'auto';
  container.style.right = settings.position.includes('right') ? '20px' : 'auto';
  container.style.opacity = settings.opacity;
}

// Sauvegarder les settings
function saveSettings() {
  chrome.storage.local.set({ grabsong_settings: settings });
}

// Créer le conteneur principal
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
  
  const widget = document.createElement('div');
  widget.id = 'grabsong-widget';
  widget.style.cssText = `
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.06);
    overflow: hidden;
    transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  `;
  
  widget.innerHTML = `
    <!-- Header -->
    <div id="grabsong-header" style="padding: 16px; text-align: center; border-bottom: 1px solid rgba(0,0,0,0.06);">
      <div style="display: flex; align-items: center; justify-content: center; gap: 8px; color: #1d1d1f;">
        <span style="font-size: 20px;">🎵</span>
        <span style="font-weight: 600; font-size: 15px; letter-spacing: -0.3px;">GrabSong</span>
      </div>
    </div>
    
    <!-- Menu principal -->
    <div id="grabsong-menu" style="display: flex; flex-direction: column; gap: 8px; padding: 12px;">
      <button id="grabsong-dl-btn" style="background: #007AFF; color: white; border: none; padding: 12px; border-radius: 10px; font-size: 14px; font-weight: 500; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: 0 2px 8px rgba(0, 122, 255, 0.25);">
        <span style="font-size: 16px;">↓</span>
        <span>Télécharger</span>
      </button>
      <button id="grabsong-settings-btn" style="background: rgba(0,0,0,0.04); color: #1d1d1f; border: none; padding: 12px; border-radius: 10px; font-size: 14px; font-weight: 500; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);">
        <span style="font-size: 16px;">⚙</span>
        <span>Paramètres</span>
      </button>
    </div>
    
    <!-- Contenu Download -->
    <div id="grabsong-content-dl" style="display: none;">
      <div id="grabsong-messages" style="padding: 15px; max-height: 450px; background: #f5f5f7; overflow-y: auto; display: flex; flex-direction: column; gap: 10px;">
        <div class="grabsong-message system" style="background: white; padding: 14px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
          <div style="font-size: 13px; color: #86868b;">Prêt à télécharger</div>
        </div>
      </div>
    </div>
    
    <!-- Contenu Settings -->
    <div id="grabsong-content-settings" style="display: none; padding: 15px; background: #f5f5f7; max-height: 450px; overflow-y: auto;">
      <div style="background: white; padding: 12px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
        <strong style="color: #1d1d1f; font-size: 13px; font-weight: 600;">📍 Position</strong>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px;">
          <button class="position-btn" data-position="top-left" style="padding: 10px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; background: white; cursor: pointer; font-size: 11px; color: #1d1d1f; font-weight: 500; transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1);">↖ Haut G.</button>
          <button class="position-btn" data-position="top-right" style="padding: 10px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; background: white; cursor: pointer; font-size: 11px; color: #1d1d1f; font-weight: 500; transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1);">↗ Haut D.</button>
          <button class="position-btn" data-position="bottom-left" style="padding: 10px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; background: white; cursor: pointer; font-size: 11px; color: #1d1d1f; font-weight: 500; transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1);">↙ Bas G.</button>
          <button class="position-btn" data-position="bottom-right" style="padding: 10px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; background: white; cursor: pointer; font-size: 11px; color: #1d1d1f; font-weight: 500; transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1);">↘ Bas D.</button>
        </div>
      </div>
      
      <div style="background: white; padding: 12px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
        <strong style="color: #1d1d1f; font-size: 13px; font-weight: 600;">🎨 Transparence</strong>
        <div style="margin-top: 10px;">
          <input type="range" id="opacity-slider" min="50" max="100" value="95" style="width: 100%; accent-color: #007AFF;">
          <div style="text-align: center; font-size: 12px; color: #86868b; margin-top: 5px;">
            <span id="opacity-value">95</span>%
          </div>
        </div>
      </div>
      
      <div style="background: white; padding: 12px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); overflow: hidden;">
        <strong style="color: #1d1d1f; font-size: 13px; font-weight: 600;">📁 Dossier de sauvegarde</strong>
        <div style="margin-top: 10px;">
          <div style="position: relative;">
            <input type="text" id="custom-folder-input" placeholder="/mnt/c/Users/Molim/Music" 
                   style="width: 100%; padding: 10px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; font-size: 12px; color: #1d1d1f; background: #f5f5f7; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
            <div id="custom-folder-display" style="display: none; width: 100%; padding: 10px; border: 1px solid rgba(52, 199, 89, 0.3); border-radius: 8px; font-size: 12px; color: #1d1d1f; background: rgba(52, 199, 89, 0.05); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
            </div>
          </div>
          <div style="font-size: 11px; color: #86868b; margin-top: 6px; line-height: 1.4; overflow: hidden; text-overflow: ellipsis;">
            ⚠️ Chemin absolu WSL (ex: /mnt/c/Users/...)<br>
            Laissez vide pour music/ par défaut
          </div>
          <div style="margin-top: 10px; display: flex; gap: 8px;">
            <button id="validate-folder-btn" style="
              flex: 1;
              padding: 10px;
              background: #34C759;
              color: white;
              border: none;
              border-radius: 8px;
              font-size: 13px;
              font-weight: 500;
              cursor: pointer;
              transition: all 2.4s cubic-bezier(0.16, 1, 0.3, 1);
            ">
              ✓ Valider
            </button>
            <button id="modify-folder-btn" style="
              flex: 1;
              padding: 10px;
              background: rgba(0,0,0,0.04);
              color: #1d1d1f;
              border: none;
              border-radius: 8px;
              font-size: 13px;
              font-weight: 500;
              cursor: pointer;
              transition: all 2.4s cubic-bezier(0.16, 1, 0.3, 1);
              display: none;
            ">
              ✏️ Modifier
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Footer -->
    <div id="grabsong-footer" style="display: none; padding: 12px; background: white; border-top: 1px solid rgba(0,0,0,0.06);">
      <button id="grabsong-close-btn" style="width: 100%; padding: 11px; background: rgba(0,0,0,0.04); color: #1d1d1f; border: none; border-radius: 10px; font-weight: 500; font-size: 14px; cursor: pointer; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);">
        Fermer
      </button>
    </div>
  `;
  
  container.appendChild(widget);
  document.body.appendChild(container);
  
  // Event Listeners
  document.getElementById('grabsong-dl-btn').addEventListener('click', showDownloadView);
  document.getElementById('grabsong-settings-btn').addEventListener('click', showSettingsView);
  document.getElementById('grabsong-close-btn').addEventListener('click', showMenuView);
  
  document.querySelectorAll('.position-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      settings.position = btn.dataset.position;
      saveSettings();
      applySettings();
      updatePositionButtons();
    });
  });
  
  document.getElementById('opacity-slider').addEventListener('input', (e) => {
    settings.opacity = e.target.value / 100;
    document.getElementById('opacity-value').textContent = e.target.value;
    applySettings();
  });
  
  document.getElementById('opacity-slider').addEventListener('change', saveSettings);
  
  // Custom folder - Bouton Valider
  const validateBtn = document.getElementById('validate-folder-btn');
  validateBtn.addEventListener('click', () => {
    const input = document.getElementById('custom-folder-input');
    const display = document.getElementById('custom-folder-display');
    const modifyBtn = document.getElementById('modify-folder-btn');
    
    const folderPath = input.value.trim();
    settings.customFolder = folderPath;
    saveSettings();
    
    // Afficher le chemin validé
    display.textContent = folderPath || 'music/ (par défaut)';
    display.style.display = 'block';
    input.style.display = 'none';
    
    // Inverser les boutons
    validateBtn.style.display = 'none';
    modifyBtn.style.display = 'block';
    
    log('✅', 'Custom folder locked:', settings.customFolder);
  });
  
  // Effet hover - Valider
  validateBtn.addEventListener('mouseenter', () => {
    validateBtn.style.background = '#30B350';
    validateBtn.style.transform = 'scale(1.02)';
  });
  validateBtn.addEventListener('mouseleave', () => {
    validateBtn.style.background = '#34C759';
    validateBtn.style.transform = 'scale(1)';
  });
  
  // Custom folder - Bouton Modifier
  const modifyBtn = document.getElementById('modify-folder-btn');
  modifyBtn.addEventListener('click', () => {
    const input = document.getElementById('custom-folder-input');
    const display = document.getElementById('custom-folder-display');
    
    // Afficher l'input pour modification
    input.style.display = 'block';
    display.style.display = 'none';
    
    // Inverser les boutons
    validateBtn.style.display = 'block';
    modifyBtn.style.display = 'none';
    
    // Focus sur l'input
    input.focus();
    
    log('✏️', 'Custom folder unlocked for editing');
  });
  
  // Effet hover - Modifier
  modifyBtn.addEventListener('mouseenter', () => {
    modifyBtn.style.background = 'rgba(0,0,0,0.08)';
    modifyBtn.style.transform = 'scale(1.02)';
  });
  modifyBtn.addEventListener('mouseleave', () => {
    modifyBtn.style.background = 'rgba(0,0,0,0.04)';
    modifyBtn.style.transform = 'scale(1)';
  });
  
  loadSettings();
  updatePositionButtons();
  updateCustomFolderInput();
  
  log('✅', 'Chat container created');
}

// Mettre à jour le champ custom folder
function updateCustomFolderInput() {
  const input = document.getElementById('custom-folder-input');
  const display = document.getElementById('custom-folder-display');
  const validateBtn = document.getElementById('validate-folder-btn');
  const modifyBtn = document.getElementById('modify-folder-btn');
  
  if (input && settings.customFolder) {
    input.value = settings.customFolder;
    
    // Si un chemin est déjà sauvegardé, l'afficher en mode "validé"
    display.textContent = settings.customFolder;
    display.style.display = 'block';
    input.style.display = 'none';
    validateBtn.style.display = 'none';
    modifyBtn.style.display = 'block';
  }
}

// Mettre à jour les boutons de position
function updatePositionButtons() {
  document.querySelectorAll('.position-btn').forEach(btn => {
    if (btn.dataset.position === settings.position) {
      btn.style.borderColor = '#007AFF';
      btn.style.background = 'rgba(0, 122, 255, 0.08)';
      btn.style.color = '#007AFF';
      btn.style.fontWeight = '600';
    } else {
      btn.style.borderColor = 'rgba(0,0,0,0.1)';
      btn.style.background = 'white';
      btn.style.color = '#1d1d1f';
      btn.style.fontWeight = '500';
    }
  });
}

// Afficher la vue Menu
function showMenuView() {
  document.getElementById('grabsong-menu').style.display = 'flex';
  document.getElementById('grabsong-content-dl').style.display = 'none';
  document.getElementById('grabsong-content-settings').style.display = 'none';
  document.getElementById('grabsong-footer').style.display = 'none';
  document.getElementById('grabsong-container').style.width = '220px';
  
  // Arrêter le polling
  if (statusPollingInterval) {
    clearInterval(statusPollingInterval);
    statusPollingInterval = null;
  }
}

// Afficher la vue Download
function showDownloadView() {
  document.getElementById('grabsong-menu').style.display = 'none';
  document.getElementById('grabsong-content-dl').style.display = 'block';
  document.getElementById('grabsong-content-settings').style.display = 'none';
  document.getElementById('grabsong-footer').style.display = 'block';
  document.getElementById('grabsong-container').style.width = '380px';
  
  // Afficher le bouton de démarrage
  const messages = document.getElementById('grabsong-messages');
  if (messages.children.length === 1) {
    showStartButton();
  }
}

// Afficher le bouton de démarrage
function showStartButton() {
  const messagesContainer = document.getElementById('grabsong-messages');
  
  messagesContainer.innerHTML = `
    <div style="
      background: white;
      border-radius: 16px;
      padding: 32px 20px;
      text-align: center;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    ">
      <div style="font-size: 56px; margin-bottom: 16px; opacity: 0.9;">🎵</div>
      <strong style="font-size: 17px; display: block; margin-bottom: 8px; color: #1d1d1f; font-weight: 600; letter-spacing: -0.3px;">
        Prêt à télécharger
      </strong>
      <p style="font-size: 13px; color: #86868b; margin-bottom: 24px; line-height: 1.4;">
        Extrait et télécharge la chanson<br>en cours de lecture
      </p>
      <button id="start-download-btn" style="
        padding: 13px 28px;
        background: #007AFF;
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 500;
        cursor: pointer;
        font-size: 15px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
        letter-spacing: -0.2px;
      ">
        Télécharger
      </button>
    </div>
  `;
  
  // Ajouter l'événement au bouton
  const btn = document.getElementById('start-download-btn');
  btn.addEventListener('click', () => {
    messagesContainer.innerHTML = '<div style="padding: 10px; text-align: center; color: #999; font-size: 12px;">Extraction en cours...</div>';
    performDownload();
  });
  
  // Effet hover subtil
  btn.addEventListener('mouseenter', () => {
    btn.style.transform = 'scale(1.02)';
    btn.style.boxShadow = '0 6px 16px rgba(0, 122, 255, 0.4)';
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = 'scale(1)';
    btn.style.boxShadow = '0 4px 12px rgba(0, 122, 255, 0.3)';
  });
}

// Afficher la vue Settings
function showSettingsView() {
  document.getElementById('grabsong-menu').style.display = 'none';
  document.getElementById('grabsong-content-dl').style.display = 'none';
  document.getElementById('grabsong-content-settings').style.display = 'block';
  document.getElementById('grabsong-footer').style.display = 'block';
  document.getElementById('grabsong-container').style.width = '280px';
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

// Ajouter les styles CSS
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
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(15px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes scaleIn {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  .grabsong-message {
    animation: fadeIn 3.6s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  #grabsong-edit-form {
    animation: scaleIn 3.0s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  button {
    transition: all 2.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
  }
  
  #grabsong-container {
    transition: all 3.0s cubic-bezier(0.16, 1, 0.3, 1) !important;
  }
`;
document.head.appendChild(style);

// ============================================
// EXTRACTION DES DONNÉES
// ============================================

async function extractSongData() {
  log('🎵', 'Extracting song data...');
  
  const songData = {
    title: '',
    artist: '',
    album: '',
    year: '',
    url: '',
  };

  // Extraire le titre
  const titleElement = document.querySelector(CONFIG.selectors.ytMusic.songTitle);
  if (titleElement) {
    songData.title = titleElement.textContent.trim();
  }

  // Extraire l'artiste, album et année
  const bylineElement = document.querySelector('ytmusic-player-bar .byline.complex-string');
  if (bylineElement) {
    const fullText = bylineElement.textContent.trim();
    const parts = fullText.split('•').map(part => part.trim());
    
    if (parts[0]) songData.artist = parts[0];
    if (parts[1]) songData.album = parts[1];
    if (parts[2] && /^\d{4}$/.test(parts[2])) songData.year = parts[2];
  }

  // Récupérer l'URL
  songData.url = await getShareLink();

  log('✅', 'Song data extracted:', songData);
  return songData;
}

async function getShareLink() {
  log('🔗', 'Getting share link via menu...');
  
  const previousClipboard = await readFromClipboard();
  
  // Étape 1: Ouvrir le menu
  const menuButton = document.querySelector(CONFIG.selectors.ytMusic.menuButton);
  if (!menuButton) {
    log('❌', 'Menu button not found');
    return '';
  }
  
  log('🖱️', 'Click 1/3: Opening menu...');
  menuButton.click();
  await wait(CONFIG.delays.menuOpen);

  // Étape 2: Cliquer sur "Partager"
  const menuItems = document.querySelectorAll(CONFIG.selectors.ytMusic.menuItems);
  let shareClicked = false;
  
  for (let item of menuItems) {
    if (item.textContent.includes('Partager')) {
      const shareLink = item.querySelector(CONFIG.selectors.ytMusic.shareLink);
      if (shareLink) {
        log('🖱️', 'Click 2/3: Opening share dialog...');
        shareLink.click();
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

  // Étape 3: Cliquer sur "Copier"
  const copyButton = Array.from(document.querySelectorAll('button')).find(btn => 
    btn.textContent.includes('Copier') || btn.textContent.includes('Copy')
  );
  
  if (!copyButton) {
    log('❌', 'Copy button not found');
    return '';
  }

  log('🖱️', 'Click 3/3: Copying link...');
  copyButton.click();
  await wait(CONFIG.delays.copyAction);

  // Récupérer le lien depuis le clipboard
  const shareLink = await readFromClipboard();
  
  // Fermer le dialog
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
  
  log('✅', 'Share link obtained:', shareLink);
  log('🎵', 'Link will be sent to yt-dlp with noplaylist=true');
  
  return shareLink;
}

// ============================================
// TÉLÉCHARGEMENT
// ============================================

async function performDownload() {
  log('🚀', '=== Starting GrabSong V3 ===');
  
  try {
    // Étape 1: Extraction
    addChatMessage('<div style="font-size: 14px; font-weight: 600; color: #667eea; margin-bottom: 5px;">🎵 Étape 1/3 : Extraction</div>Récupération des métadonnées...', 'info');
    
    const songData = await extractSongData();
    
    if (!songData.url || !songData.title) {
      addChatMessage(
        `<div style="background: #fff3e0; border: 2px solid #ff9800; border-radius: 10px; padding: 15px; text-align: center;">
          <div style="font-size: 24px; margin-bottom: 10px;">⚠️</div>
          <strong style="color: #e65100; font-size: 16px;">Aucune musique détectée</strong>
          <p style="margin: 10px 0; color: #666; font-size: 14px;">
            Assurez-vous qu'une musique est en cours de lecture
          </p>
        </div>`,
        'warning'
      );
      return;
    }
    
    addChatMessage('<strong>✅</strong> Données extraites avec succès !', 'success');
    
    // Étape 2: Vérification
    addChatMessage('<div style="font-size: 14px; font-weight: 600; color: #667eea; margin-bottom: 5px;">✏️ Étape 2/3 : Vérification</div>Vérifiez les informations', 'info');
    
    showEditForm(songData);
    
  } catch (error) {
    log('❌', 'Error:', error);
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
    
    <div style="display: flex; gap: 10px;">
      <button id="cancel-btn" style="
        flex: 1;
        background: #f5f5f5;
        color: #666;
        border: 1px solid #ddd;
        padding: 12px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s;
      ">
        ❌ Annuler
      </button>
      
      <button id="save-and-download" style="
        flex: 2;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s;
      ">
        💾 Télécharger
      </button>
    </div>
  `;
  
  messagesContainer.appendChild(formDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
  
  // Bouton Annuler
  document.getElementById('cancel-btn').addEventListener('click', () => {
    formDiv.remove();
    // Retour à l'écran d'accueil
    showStartButton();
  });
  
  // Effet hover sur Annuler
  const cancelBtn = document.getElementById('cancel-btn');
  cancelBtn.addEventListener('mouseenter', () => {
    cancelBtn.style.background = '#e0e0e0';
    cancelBtn.style.borderColor = '#bbb';
  });
  cancelBtn.addEventListener('mouseleave', () => {
    cancelBtn.style.background = '#f5f5f5';
    cancelBtn.style.borderColor = '#ddd';
  });
  
  // Bouton Télécharger
  document.getElementById('save-and-download').addEventListener('click', () => {
    songData.artist = document.getElementById('edit-artist').value;
    songData.album = document.getElementById('edit-album').value;
    songData.title = document.getElementById('edit-title').value;
    songData.year = document.getElementById('edit-year').value;
    
    formDiv.remove();
    startDownload(songData);
  });
  
  // Effet hover sur Télécharger
  const downloadBtn = document.getElementById('save-and-download');
  downloadBtn.addEventListener('mouseenter', () => {
    downloadBtn.style.transform = 'translateY(-2px)';
    downloadBtn.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.4)';
  });
  downloadBtn.addEventListener('mouseleave', () => {
    downloadBtn.style.transform = 'translateY(0)';
    downloadBtn.style.boxShadow = 'none';
  });
}

// Lancer le téléchargement
async function startDownload(songData) {
  try {
    // Étape 3: Téléchargement
    addChatMessage('<div style="font-size: 14px; font-weight: 600; color: #667eea; margin-bottom: 5px;">⬇️ Étape 3/3 : Téléchargement</div>Envoi au serveur Python...', 'info');
    
    // Ajouter le custom folder si défini
    if (settings.customFolder) {
      songData.custom_folder = settings.customFolder;
      log('📁', 'Using custom folder:', settings.customFolder);
    }
    
    // Envoyer au serveur Python
    const response = await chrome.runtime.sendMessage({
      action: 'download_song',
      data: songData
    });
    
    if (!response || !response.success) {
      throw new Error(response?.error || 'Serveur Python non accessible');
    }
    
    addChatMessage('<strong>✅</strong> Téléchargement démarré !', 'success');
    
    // Démarrer le polling du statut
    startStatusPolling();
    
  } catch (error) {
    log('❌', 'Error:', error);
    addChatMessage(
      `<div style="background: #ffebee; border: 2px solid #f44336; border-radius: 10px; padding: 15px; text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">❌</div>
        <strong style="color: #c62828; font-size: 16px;">Erreur</strong>
        <p style="margin: 10px 0; color: #666; font-size: 14px;">
          ${error.message}
        </p>
        <p style="margin: 10px 0 0 0; font-size: 12px; color: #999;">
          💡 Assurez-vous que le serveur Python est lancé: <code>python app.py</code>
        </p>
      </div>`,
      'error'
    );
  }
}

// Polling du statut
function startStatusPolling() {
  if (statusPollingInterval) {
    clearInterval(statusPollingInterval);
  }
  
  statusPollingInterval = setInterval(async () => {
    try {
      const status = await chrome.runtime.sendMessage({ action: 'get_status' });
      
      if (status.in_progress && status.progress) {
        updateProgress(status.progress);
      } else if (status.last_completed) {
        handleSuccess(status.last_completed);
        clearInterval(statusPollingInterval);
      } else if (status.last_error) {
        handleError(status.last_error);
        clearInterval(statusPollingInterval);
      }
    } catch (error) {
      log('❌', 'Polling error:', error);
    }
  }, CONFIG.delays.statusPoll);
}

// Mettre à jour la progression
function updateProgress(progress) {
  let progressBar = document.getElementById('progress-bar-container');
  
  // Créer la barre de progression si elle n'existe pas
  if (!progressBar) {
    const messagesContainer = document.getElementById('grabsong-messages');
    
    progressBar = document.createElement('div');
    progressBar.id = 'progress-bar-container';
    progressBar.className = 'grabsong-message info';
    progressBar.style.cssText = `
      background: white;
      padding: 16px;
      margin-bottom: 10px;
      border-radius: 12px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    `;
    
    progressBar.innerHTML = `
      <div style="margin-bottom: 12px;">
        <div style="font-size: 13px; color: #1d1d1f; font-weight: 500; margin-bottom: 4px;">
          Téléchargement en cours
        </div>
        <div style="font-size: 12px; color: #86868b;">
          Veuillez patienter...
        </div>
      </div>
      <div style="width: 100%; height: 6px; background: rgba(0, 122, 255, 0.1); border-radius: 10px; overflow: hidden;">
        <div id="progress-bar-fill" style="
          width: 0%;
          height: 100%;
          background: linear-gradient(90deg, #007AFF 0%, #5AC8FA 100%);
          border-radius: 10px;
          transition: width 0.3s ease-out;
        "></div>
      </div>
    `;
    
    messagesContainer.appendChild(progressBar);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Animation automatique sur 10 secondes avec variations aléatoires
    let currentProgress = 0;
    let targetProgress = 0;
    
    const interval = setInterval(() => {
      // Ajouter une variation aléatoire (entre 0.3% et 1.5%)
      const randomIncrement = Math.random() * 1.2 + 0.3;
      targetProgress += randomIncrement;
      
      // Limiter à 95% jusqu'à la fin réelle
      if (targetProgress >= 95) {
        targetProgress = 95;
        clearInterval(interval);
      }
      
      // Interpolation douce vers la cible
      currentProgress += (targetProgress - currentProgress) * 0.3;
      
      const fillBar = document.getElementById('progress-bar-fill');
      if (fillBar) {
        fillBar.style.width = currentProgress.toFixed(1) + '%';
      }
    }, 100); // Mise à jour toutes les 100ms
    
    // Stocker l'interval pour le nettoyer plus tard
    progressBar.dataset.interval = interval;
  }
}

// Gérer le succès
function handleSuccess(result) {
  const messagesContainer = document.getElementById('grabsong-messages');
  
  // Compléter rapidement la barre de progression à 100%
  const fillBar = document.getElementById('progress-bar-fill');
  if (fillBar) {
    // Animation rapide de la progression actuelle vers 100%
    let currentWidth = parseFloat(fillBar.style.width) || 0;
    const quickInterval = setInterval(() => {
      currentWidth += (100 - currentWidth) * 0.4; // Accélération rapide
      fillBar.style.width = currentWidth.toFixed(1) + '%';
      
      if (currentWidth >= 99.5) {
        fillBar.style.width = '100%';
        clearInterval(quickInterval);
        
        // Attendre un peu avant d'afficher le succès
        setTimeout(() => {
          const progressBar = document.getElementById('progress-bar-container');
          if (progressBar) {
            progressBar.remove();
          }
          showSuccessMessage(result, messagesContainer);
        }, 600);
      }
    }, 50);
  } else {
    showSuccessMessage(result, messagesContainer);
  }
}

function showSuccessMessage(result, messagesContainer) {
  const successDiv = document.createElement('div');
  successDiv.className = 'grabsong-message success';
  successDiv.style.cssText = `
    background: white;
    border-radius: 16px;
    padding: 28px 20px;
    text-align: center;
    margin-bottom: 10px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  `;
  
  successDiv.innerHTML = `
    <div style="width: 56px; height: 56px; margin: 0 auto 16px; background: #34C759; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px;">
      ✓
    </div>
    <strong style="color: #1d1d1f; font-size: 17px; font-weight: 600; letter-spacing: -0.3px; display: block; margin-bottom: 8px;">
      Téléchargement terminé
    </strong>
    <p style="margin: 0 0 6px 0; color: #86868b; font-size: 13px; line-height: 1.4;">
      📁 ${result.file_path}
    </p>
    <p style="margin: 0 0 20px 0; font-size: 12px; color: #86868b;">
      Organisé automatiquement
    </p>
    <button id="download-again-btn" style="
      padding: 12px 24px;
      background: #007AFF;
      color: white;
      border: none;
      border-radius: 12px;
      font-weight: 500;
      cursor: pointer;
      font-size: 14px;
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
      letter-spacing: -0.2px;
    ">
      Télécharger une autre chanson
    </button>
  `;
  
  messagesContainer.appendChild(successDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
  
  // Ajouter l'événement au bouton
  document.getElementById('download-again-btn').addEventListener('click', () => {
    // Vider les messages
    messagesContainer.innerHTML = '<div style="padding: 10px; text-align: center; color: #999; font-size: 12px;">Prêt à télécharger !</div>';
    
    // Relancer le téléchargement
    performDownload();
  });
  
  // Effet hover subtil
  const btn = document.getElementById('download-again-btn');
  btn.addEventListener('mouseenter', () => {
    btn.style.transform = 'scale(1.02)';
    btn.style.boxShadow = '0 6px 16px rgba(0, 122, 255, 0.4)';
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = 'scale(1)';
    btn.style.boxShadow = '0 4px 12px rgba(0, 122, 255, 0.3)';
  });
  
  log('✅', 'Download completed:', result);
}

// Gérer l'erreur
function handleError(error) {
  addChatMessage(
    `<div style="background: #ffebee; border: 2px solid #f44336; border-radius: 10px; padding: 15px; text-align: center;">
      <div style="font-size: 24px; margin-bottom: 10px;">❌</div>
      <strong style="color: #c62828; font-size: 16px;">Erreur</strong>
      <p style="margin: 10px 0; color: #666; font-size: 14px;">
        ${error.error}
      </p>
    </div>`,
    'error'
  );
  
  log('❌', 'Download error:', error);
}

// ============================================
// INITIALISATION
// ============================================

// Créer l'interface au chargement de la page
if (window.location.hostname.includes('music.youtube.com')) {
  // Attendre que la page soit chargée
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createChatContainer);
  } else {
    createChatContainer();
  }
}
