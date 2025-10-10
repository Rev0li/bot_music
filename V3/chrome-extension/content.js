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
  opacity: 0.95
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
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    overflow: hidden;
    transition: all 0.3s ease;
  `;
  
  widget.innerHTML = `
    <!-- Header -->
    <div id="grabsong-header" style="padding: 12px 15px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.2);">
      <div style="display: flex; align-items: center; justify-content: center; gap: 8px; color: white;">
        <span style="font-size: 20px;">🎵</span>
        <span style="font-weight: 600; font-size: 16px;">GrabSong V3</span>
      </div>
    </div>
    
    <!-- Menu principal -->
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
    
    <!-- Contenu Download -->
    <div id="grabsong-content-dl" style="display: none;">
      <div id="grabsong-messages" style="padding: 15px; max-height: 450px; background: #f5f5f5; overflow-y: auto; display: flex; flex-direction: column; gap: 10px;">
        <div class="grabsong-message system" style="background: white; padding: 12px; border-radius: 8px; border-left: 4px solid #667eea;">
          <strong>👋 Bienvenue !</strong><br>
          <small>Prêt à télécharger...</small>
        </div>
      </div>
    </div>
    
    <!-- Contenu Settings -->
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
    
    <!-- Footer -->
    <div id="grabsong-footer" style="display: none; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-top: 1px solid rgba(255,255,255,0.2);">
      <button id="grabsong-close-btn" style="width: 100%; padding: 10px; background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s;">
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
  
  loadSettings();
  updatePositionButtons();
  
  log('✅', 'Chat container created');
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
  
  // Lancer le téléchargement
  const messages = document.getElementById('grabsong-messages');
  if (messages.children.length === 1) {
    performDownload();
  }
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
    
    <button id="save-and-download" style="
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
      💾 Télécharger
    </button>
  `;
  
  messagesContainer.appendChild(formDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
  
  // Bouton télécharger
  document.getElementById('save-and-download').addEventListener('click', () => {
    songData.artist = document.getElementById('edit-artist').value;
    songData.album = document.getElementById('edit-album').value;
    songData.title = document.getElementById('edit-title').value;
    songData.year = document.getElementById('edit-year').value;
    
    formDiv.remove();
    startDownload(songData);
  });
}

// Lancer le téléchargement
async function startDownload(songData) {
  try {
    // Étape 3: Téléchargement
    addChatMessage('<div style="font-size: 14px; font-weight: 600; color: #667eea; margin-bottom: 5px;">⬇️ Étape 3/3 : Téléchargement</div>Envoi au serveur Python...', 'info');
    
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
  const existingProgress = document.getElementById('progress-message');
  if (existingProgress) {
    existingProgress.remove();
  }
  
  const percent = progress.percent || 0;
  const status = progress.status || 'downloading';
  
  let message = '';
  if (status === 'downloading') {
    message = `⏳ Téléchargement en cours... ${percent}%`;
  } else if (status === 'processing') {
    message = `🔄 Conversion en MP3... ${percent}%`;
  }
  
  const messageDiv = document.createElement('div');
  messageDiv.id = 'progress-message';
  messageDiv.className = 'grabsong-message info';
  messageDiv.style.cssText = `
    background: white;
    border-left: 4px solid #2196F3;
    padding: 12px;
    margin-bottom: 10px;
    border-radius: 8px;
    font-size: 14px;
  `;
  messageDiv.innerHTML = `<strong>${message}</strong>`;
  
  const messagesContainer = document.getElementById('grabsong-messages');
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Gérer le succès
function handleSuccess(result) {
  addChatMessage(
    `<div style="background: #e8f5e9; border: 2px solid #4CAF50; border-radius: 10px; padding: 15px; text-align: center;">
      <div style="font-size: 32px; margin-bottom: 10px;">✅</div>
      <strong style="color: #2e7d32; font-size: 18px;">Téléchargement terminé !</strong>
      <p style="margin: 10px 0; color: #666; font-size: 14px;">
        📁 ${result.file_path}
      </p>
      <p style="margin: 10px 0 0 0; font-size: 12px; color: #999;">
        Le fichier a été organisé automatiquement
      </p>
    </div>`,
    'success'
  );
  
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
