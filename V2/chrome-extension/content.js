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
  let chatXOffset = 0;
  let chatYOffset = 0;
  
  // Créer le conteneur qui combine bouton et chat
  function createChatContainer() {
    if (document.getElementById('grabsong-container')) {
      return;
    }
    
    const container = document.createElement('div');
    container.id = 'grabsong-container';
    container.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 999999;
      transition: all 0.3s ease;
    `;
    
    // Créer le bouton à l'intérieur
    const button = document.createElement('button');
    button.id = 'grabsong-btn';
    button.textContent = CONFIG.ui.buttonText;
    button.title = 'Clic = Ouvrir | Alt + Drag = Déplacer';
    button.style.cssText = `
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      padding: 15px 25px;
      border-radius: 50px;
      font-size: 16px;
      font-weight: bold;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
      user-select: none;
      transition: all 0.3s ease;
      width: 100%;
    `;
    
    // Créer le chat (caché par défaut) - se déplie vers le bas
    const chatPanel = document.createElement('div');
    chatPanel.id = 'grabsong-chat';
    chatPanel.style.cssText = `
      width: 350px;
      max-height: 0;
      background: white;
      border-radius: 0 0 15px 15px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.3);
      overflow: hidden;
      transition: max-height 0.3s ease, opacity 0.3s ease;
      opacity: 0;
      display: flex;
      flex-direction: column;
    `;
    
    chatPanel.innerHTML = `
      <div id="grabsong-messages" style="flex: 1; overflow-y: auto; padding: 15px; max-height: 400px; background: #f5f5f5;">
        <div class="grabsong-message system">
          <strong>👋 Bienvenue !</strong><br>
          Cliquez pour télécharger une chanson depuis YouTube Music.
        </div>
      </div>
      <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; cursor: move;" id="grabsong-footer">
        <div style="font-size: 12px; opacity: 0.9;">Alt + Drag pour déplacer</div>
        <button id="grabsong-minimize" style="background: rgba(255,255,255,0.2); border: none; color: white; width: 25px; height: 25px; border-radius: 50%; cursor: pointer; font-size: 16px;">−</button>
      </div>
    `;
    
    container.appendChild(button);
    container.appendChild(chatPanel);
    document.body.appendChild(container);
    
    // Gestion du clic sur le bouton
    button.addEventListener('click', (e) => {
      if (!e.altKey) {
        toggleChat();
      }
    });
    
    // Bouton minimiser
    document.getElementById('grabsong-minimize').addEventListener('click', (e) => {
      e.stopPropagation();
      toggleChat();
    });
    
    // Rendre le conteneur déplaçable avec Alt + drag
    setupDragging(container);
    
    log('✅', 'Chat container created');
  }
  
  // Basculer entre bouton et chat
  function toggleChat() {
    const button = document.getElementById('grabsong-btn');
    const chat = document.getElementById('grabsong-chat');
    
    if (!chatExpanded) {
      // Ouvrir le chat (vers le bas)
      button.style.borderRadius = '15px 15px 0 0';
      chat.style.maxHeight = '500px';
      chat.style.opacity = '1';
      chatExpanded = true;
      
      // Si c'est la première ouverture, lancer le téléchargement
      const messages = document.getElementById('grabsong-messages');
      if (messages.children.length === 1) {
        performAutoShare();
      }
    } else {
      // Fermer le chat
      button.style.borderRadius = '50px';
      chat.style.maxHeight = '0';
      chat.style.opacity = '0';
      chatExpanded = false;
    }
  }
  
  // Configuration du drag pour le conteneur
  function setupDragging(container) {
    let isDragging = false;
    let hasMoved = false;
    let startX, startY;
    
    const footer = document.getElementById('grabsong-footer');
    const button = document.getElementById('grabsong-btn');
    
    // Optimisation: utiliser will-change pour préparer l'animation
    container.style.willChange = 'transform';
    
    // Drag depuis le footer (quand chat ouvert) ou bouton (quand fermé)
    footer.addEventListener('mousedown', (e) => {
      if (e.altKey) {
        startDrag(e);
      }
    });
    
    button.addEventListener('mousedown', (e) => {
      if (e.altKey) {
        startDrag(e);
      }
    });
    
    function startDrag(e) {
      startX = e.clientX - chatXOffset;
      startY = e.clientY - chatYOffset;
      isDragging = true;
      hasMoved = false;
      container.style.cursor = 'grabbing';
      
      // Désactiver les transitions pendant le drag
      container.style.transition = 'none';
      
      e.preventDefault();
    }
    
    // Utiliser requestAnimationFrame pour des animations fluides
    let animationFrameId = null;
    
    document.addEventListener('mousemove', (e) => {
      if (isDragging) {
        e.preventDefault();
        
        // Annuler l'animation précédente si elle existe
        if (animationFrameId) {
          cancelAnimationFrame(animationFrameId);
        }
        
        // Planifier la mise à jour pour le prochain frame
        animationFrameId = requestAnimationFrame(() => {
          chatXOffset = e.clientX - startX;
          chatYOffset = e.clientY - startY;
          hasMoved = true;
          
          // Utiliser translate3d pour l'accélération GPU
          container.style.transform = `translate3d(${chatXOffset}px, ${chatYOffset}px, 0)`;
        });
      }
    });
    
    document.addEventListener('mouseup', () => {
      if (isDragging) {
        isDragging = false;
        container.style.cursor = '';
        
        // Réactiver les transitions
        container.style.transition = 'all 0.3s ease';
        
        // Nettoyer l'animation frame
        if (animationFrameId) {
          cancelAnimationFrame(animationFrameId);
          animationFrameId = null;
        }
      }
    });
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
      addChatMessage('<strong>📥 Étape 1/5:</strong> Extraction des données de la chanson...', 'info');
      const songData = await extractSongData();
      
      songData.link = await getShareLink();
      
      if (!songData.link) {
        addChatMessage('<strong>❌ Erreur:</strong> Impossible d\'obtenir le lien de la chanson.', 'error');
        return;
      }
      
      // Étape 2: Afficher le formulaire d'édition
      addChatMessage('<strong>✏️ Étape 2/5:</strong> Vérifiez et modifiez les données si nécessaire', 'info');
      
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
      // Étape 3: Création du nom de fichier
      addChatMessage('<strong>📝 Étape 3/5:</strong> Création du nom de fichier...', 'info');
      
      const parts = [];
      if (songData.artist) parts.push(`art=${songData.artist}`);
      if (songData.album) parts.push(`alb=${songData.album}`);
      if (songData.title) parts.push(`N=${songData.title}`);
      if (songData.year) parts.push(`Y=${songData.year}`);
      
      const filename = parts.join(' ') + '.mp3';
      const cleanFilename = filename.replace(/[<>"/\\|?*]/g, '');
      
      log('📝', 'Filename created:', cleanFilename);
      
      await copyToClipboard(cleanFilename);
      
      addChatMessage(
        `<strong>✅ Nom de fichier créé:</strong><br>
        <code style="background: #f0f0f0; padding: 5px; border-radius: 3px; display: block; margin-top: 5px; word-break: break-all;">${cleanFilename}</code>`,
        'success'
      );
      
      songData.filename = cleanFilename;
      
      // Sauvegarder dans le storage
      chrome.storage.local.set({ pendingSongData: songData }, () => {
        log('💾', 'Data saved to storage');
      });
      
      // Étape 4: Envoyer à Python via background script
      addChatMessage('<strong>🐍 Étape 4/5:</strong> Envoi des données à Python...', 'info');
      
      // Envoyer via background script (pour éviter CORS)
      chrome.runtime.sendMessage({
        action: 'send_to_flask',
        data: songData
      }, (response) => {
        if (response && response.success) {
          log('✅', 'Données envoyées à Python:', response);
          addChatMessage(
            `<strong>✅ Python:</strong> Données sauvegardées<br>
            📁 Dossier: ${response.timestamp}`,
            'success'
          );
        } else {
          log('⚠️', 'Python non connecté:', response);
          addChatMessage(
            '<strong>⚠️ Python:</strong> Non connecté<br>' +
            '<em>Lancez: python app.py</em><br>' +
            '(Le téléchargement continuera)',
            'warning'
          );
        }
      });
      
      // Étape 5: Ouverture Y2Mate
      addChatMessage('<strong>🌐 Étape 5/5:</strong> Ouverture de Y2Mate en arrière-plan...', 'info');
      
      chrome.runtime.sendMessage({
        action: 'openTab',
        url: CONFIG.targetPage.url,
        data: songData
      });
      
      // Instructions finales
      addChatMessage(
        `<strong>⏳ Conversion en cours...</strong><br><br>
        <strong>📌 Important:</strong><br>
        • Restez sur cette page YouTube Music<br>
        • Vous pouvez continuer à naviguer et écouter de la musique<br>
        • La conversion se fait en arrière-plan<br>
        • Le téléchargement démarrera automatiquement<br>
        • L'onglet Y2Mate se fermera tout seul<br><br>
        <em>⏱️ Temps estimé: 30-60 secondes</em>`,
        'warning'
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
  let statusPollingInterval = null;
  
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
          
          // Afficher le message de succès
          addChatMessage(
            `<strong>🎉 Téléchargement terminé !</strong><br><br>
            📁 Fichier: <strong>${response.last_completed.filename}</strong><br>
            📂 Dossier: ${response.last_completed.path}<br><br>
            <em>✨ L'extension va se réinitialiser dans 3 secondes...</em>`,
            'success'
          );
          
          // Reset après 3 secondes
          setTimeout(() => {
            resetExtension();
          }, 3000);
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
