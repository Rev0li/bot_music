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
    copyAction: 1500,  // Augmenté pour laisser le temps au clipboard
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
  autoAccept: false
};

let statusPollingInterval = null;
let downloadHistory = []; // Historique des téléchargements (max 5)
let previousHistoryLength = 0; // Pour détecter les suppressions
let lastRenderedState = null; // Pour éviter les re-renders inutiles

// Charger les settings
function loadSettings() {
  chrome.storage.local.get(['grabsong_settings'], (result) => {
    if (result.grabsong_settings) {
      settings = { ...settings, ...result.grabsong_settings };
    }
    applySettings();
    
    // Mettre à jour le toggle si on est dans les settings
    const autoAcceptToggle = document.getElementById('auto-accept-toggle');
    if (autoAcceptToggle) {
      autoAcceptToggle.checked = settings.autoAccept || false;
      if (window.updateToggleStyle) {
        window.updateToggleStyle();
      }
    }
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
    <div id="grabsong-header" style="padding: 10px 12px; text-align: center; border-bottom: 1px solid rgba(0,0,0,0.06); position: relative;">
      <div style="display: flex; align-items: center; justify-content: center; gap: 6px; color: #1d1d1f;">
        <span style="font-size: 18px;">🎵</span>
        <span style="font-weight: 600; font-size: 14px; letter-spacing: -0.3px;">SurfSong</span>
      </div>
      <button id="grabsong-close-btn" style="
        position: absolute;
        top: 50%;
        right: 12px;
        transform: translateY(-50%);
        background: none;
        border: none;
        color: #86868b;
        font-size: 18px;
        cursor: pointer;
        padding: 4px;
        line-height: 1;
        transition: color 0.2s;
      ">×</button>
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
      <div id="grabsong-messages" style="padding: 10px; max-height: 400px; background: #f5f5f7; overflow-y: auto; display: flex; flex-direction: column; gap: 6px;">
        <div class="grabsong-message system" style="background: white; padding: 10px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
          <div style="font-size: 12px; color: #86868b;">Prêt à télécharger</div>
        </div>
      </div>
    </div>
    
    <!-- Contenu Settings -->
    <div id="grabsong-content-settings" style="display: none; padding: 15px; background: #f5f5f7; max-height: 450px; overflow-y: auto;">
      <div style="background: white; padding: 12px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
        <strong style="color: #1d1d1f; font-size: 13px; font-weight: 600;">📍 Position</strong>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px;">
          <button class="position-btn" data-position="top-left" style="padding: 10px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; background: white; cursor: pointer; font-size: 11px; color: #1d1d1f; font-weight: 500; transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);">↖ Haut G.</button>
          <button class="position-btn" data-position="top-right" style="padding: 10px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; background: white; cursor: pointer; font-size: 11px; color: #1d1d1f; font-weight: 500; transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);">↗ Haut D.</button>
          <button class="position-btn" data-position="bottom-left" style="padding: 10px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; background: white; cursor: pointer; font-size: 11px; color: #1d1d1f; font-weight: 500; transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);">↙ Bas G.</button>
          <button class="position-btn" data-position="bottom-right" style="padding: 10px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; background: white; cursor: pointer; font-size: 11px; color: #1d1d1f; font-weight: 500; transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);">↘ Bas D.</button>
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
      
      <div style="background: white; padding: 12px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <div>
            <strong style="color: #1d1d1f; font-size: 13px; font-weight: 600;">⚡ Accepter auto</strong>
            <p style="margin: 5px 0 0 0; font-size: 11px; color: #86868b;">Valider automatiquement les métadonnées</p>
          </div>
          <label style="position: relative; display: inline-block; width: 44px; height: 24px;">
            <input type="checkbox" id="auto-accept-toggle" style="opacity: 0; width: 0; height: 0;">
            <span id="toggle-slider" style="
              position: absolute;
              cursor: pointer;
              top: 0;
              left: 0;
              right: 0;
              bottom: 0;
              background-color: #ccc;
              transition: 0.3s;
              border-radius: 24px;
            ">
              <span id="toggle-dot" style="
                position: absolute;
                content: '';
                height: 18px;
                width: 18px;
                left: 3px;
                bottom: 3px;
                background-color: white;
                transition: 0.3s;
                border-radius: 50%;
              "></span>
            </span>
          </label>
        </div>
      </div>
    </div>
    
    <!-- Footer -->
    <div id="grabsong-footer" style="display: none; padding: 10px; background: white; border-top: 1px solid rgba(0,0,0,0.06);">
      <button id="grabsong-surf-again-btn" style="
        width: 100%;
        padding: 10px;
        background: rgba(102, 126, 234, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.2);
        color: #667eea;
        border-radius: 10px;
        font-weight: 600;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
      ">
        <span>🏄</span>
        <span>Surf Again</span>
      </button>
    </div>
  `;
  
  container.appendChild(widget);
  document.body.appendChild(container);
  
  // Event Listeners
  document.getElementById('grabsong-dl-btn').addEventListener('click', showDownloadView);
  document.getElementById('grabsong-settings-btn').addEventListener('click', showSettingsView);
  
  // Bouton × en haut à droite pour revenir au menu
  const closeBtn = document.getElementById('grabsong-close-btn');
  closeBtn.addEventListener('click', showMenuView);
  closeBtn.addEventListener('mouseenter', (e) => {
    e.target.style.color = '#1d1d1f';
  });
  closeBtn.addEventListener('mouseleave', (e) => {
    e.target.style.color = '#86868b';
  });
  
  // Bouton "Surf Again" dans le footer
  const surfAgainBtn = document.getElementById('grabsong-surf-again-btn');
  surfAgainBtn.addEventListener('click', () => {
    performDownload();
  });
  surfAgainBtn.addEventListener('mouseenter', (e) => {
    e.target.style.background = 'rgba(102, 126, 234, 0.15)';
  });
  surfAgainBtn.addEventListener('mouseleave', (e) => {
    e.target.style.background = 'rgba(102, 126, 234, 0.08)';
  });
  
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
  
  // Toggle auto-accept
  const autoAcceptToggle = document.getElementById('auto-accept-toggle');
  const toggleSlider = document.getElementById('toggle-slider');
  const toggleDot = document.getElementById('toggle-dot');
  
  autoAcceptToggle.addEventListener('change', (e) => {
    settings.autoAccept = e.target.checked;
    saveSettings();
    updateToggleStyle();
  });
  
  function updateToggleStyle() {
    if (settings.autoAccept) {
      toggleSlider.style.backgroundColor = '#34C759';
      toggleDot.style.transform = 'translateX(20px)';
    } else {
      toggleSlider.style.backgroundColor = '#ccc';
      toggleDot.style.transform = 'translateX(0)';
    }
  }
  
  // Exposer la fonction pour l'utiliser ailleurs
  window.updateToggleStyle = updateToggleStyle;
  
  loadSettings();
  updatePositionButtons();
  
  log('✅', 'Chat container created');
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
  document.getElementById('grabsong-container').style.width = '280px';
  
  // Initialiser la liste des téléchargements
  updateDownloadList({ queue_size: 0, in_progress: false });
}

// Afficher la vue Settings
function showSettingsView() {
  document.getElementById('grabsong-menu').style.display = 'none';
  document.getElementById('grabsong-content-dl').style.display = 'none';
  document.getElementById('grabsong-content-settings').style.display = 'block';
  document.getElementById('grabsong-footer').style.display = 'none';
  document.getElementById('grabsong-container').style.width = '280px';
}

// Afficher la liste des téléchargements (remplace les messages)
function updateDownloadList(status) {
  const messagesContainer = document.getElementById('grabsong-messages');
  if (!messagesContainer) return;
  
  // Ne pas mettre à jour si le formulaire de validation est affiché
  if (document.getElementById('grabsong-edit-form')) return;
  
  // Créer la liste des items
  const items = [];
  
  // 1. Historique (5 derniers terminés) - en haut (plus ancien en premier)
  downloadHistory.slice(-5).forEach(item => {
    items.push({
      state: 'song',
      metadata: item.metadata,
      canCancel: false,
      isHistory: true
    });
  });
  
  // 2. En cours - au milieu
  if (status.in_progress && status.current_download) {
    items.push({
      state: 'surf',
      metadata: status.current_download.metadata,
      canCancel: true
    });
  }
  
  // 3. En attente - en bas (simulé avec queue_size)
  for (let i = 0; i < status.queue_size; i++) {
    items.push({
      state: 'extract',
      metadata: { artist: 'En attente', title: `Position ${i + 1}` },
      canCancel: false
    });
  }
  
  // Générer le HTML
  const stateConfig = {
    extract: { icon: '📝', label: 'Extraction', color: '#007AFF', bg: 'rgba(0, 122, 255, 0.08)' },
    surf: { icon: '🔄', label: 'Conversion', color: '#FF9500', bg: 'rgba(255, 149, 0, 0.08)' },
    song: { icon: '✓', label: 'Rangé', color: '#34C759', bg: 'rgba(52, 199, 89, 0.1)' }
  };
  
  // Construire le HTML avec les items + bouton permanent
  let html = '';
  
  // Ajouter les items s'il y en a
  if (items.length > 0) {
    html += items.map((item, index) => {
      const config = stateConfig[item.state];
      
      // Effet cascade : minimiser les anciens téléchargements
      const isMinimized = item.isHistory;
      
      // Pour l'historique (Rangé), afficher seulement l'icône + titre
      if (item.state === 'song') {
        return `
          <div class="download-item history-item" style="
            background: white;
            border-radius: 10px;
            padding: 6px 10px;
            margin-bottom: 4px;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
            border: 1px solid rgba(0, 0, 0, 0.04);
            display: flex;
            align-items: center;
            gap: 10px;
            opacity: 0.7;
          ">
            <div style="
              width: 24px;
              height: 24px;
              border-radius: 8px;
              background: ${config.bg};
              display: flex;
              align-items: center;
              justify-content: center;
              font-size: 14px;
              flex-shrink: 0;
              color: ${config.color};
            ">${config.icon}</div>
            <div style="
              flex: 1;
              min-width: 0;
              font-size: 12px;
              color: #1d1d1f;
              font-weight: 500;
              overflow: hidden;
              text-overflow: ellipsis;
              white-space: nowrap;
            ">${item.metadata.title}</div>
          </div>
        `;
      }
      
      // Pour les items actifs (Extraction, Conversion)
      return `
        <div class="download-item" data-state="${item.state}" style="
          background: white;
          border-radius: 10px;
          padding: 8px 10px;
          margin-bottom: 4px;
          box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
          border: 1px solid rgba(0, 0, 0, 0.04);
          display: flex;
          align-items: center;
          gap: 10px;
          transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        ">
          <div style="
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: ${config.bg};
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
          ">${config.icon}</div>
          <div style="flex: 1; min-width: 0;">
            <div style="
              font-size: 10px;
              font-weight: 600;
              color: ${config.color};
              margin-bottom: 2px;
              text-transform: uppercase;
              letter-spacing: 0.5px;
            ">${config.label}</div>
            <div style="
              font-size: 12px;
              color: #1d1d1f;
              font-weight: 600;
              overflow: hidden;
              text-overflow: ellipsis;
              white-space: nowrap;
            ">${item.metadata.title}</div>
            <div style="
              font-size: 10px;
              color: #86868b;
              overflow: hidden;
              text-overflow: ellipsis;
              white-space: nowrap;
              margin-top: 1px;
            ">${item.metadata.artist}</div>
          </div>
          ${item.canCancel ? `
            <button onclick="event.stopPropagation(); cancelCurrentDownload();" style="
              background: rgba(244, 67, 54, 0.1);
              border: 1px solid rgba(244, 67, 54, 0.2);
              color: #f44336;
              width: 28px;
              height: 28px;
              border-radius: 6px;
              cursor: pointer;
              display: flex;
              align-items: center;
              justify-content: center;
              transition: all 0.2s;
              font-size: 12px;
            ">❌</button>
          ` : ''}
        </div>
      `;
    }).join('');
  }
  
  // Si aucun item, afficher un message d'accueil
  if (items.length === 0) {
    html = `
      <div style="
        padding: 30px 20px;
        text-align: center;
        color: #86868b;
      ">
        <div style="font-size: 40px; margin-bottom: 12px; opacity: 0.5;">🎵</div>
        <div style="font-size: 13px; font-weight: 500;">Prêt à télécharger</div>
        <div style="font-size: 11px; margin-top: 6px;">Cliquez sur "Surf Again" en bas</div>
      </div>
    `;
  }
  
  // Créer une signature de l'état actuel pour détecter les vrais changements
  const currentState = JSON.stringify({
    historyCount: downloadHistory.length,
    historyTitles: downloadHistory.map(h => h.metadata.title),
    inProgress: status.in_progress,
    currentTitle: status.current_download?.metadata?.title,
    queueSize: status.queue_size
  });
  
  // Mettre à jour seulement si l'état a vraiment changé
  if (lastRenderedState !== currentState) {
    const existingItems = messagesContainer.querySelectorAll('.download-item');
    
    // Si le nombre d'items est différent, on doit recréer (nouveau téléchargement ou suppression)
    if (existingItems.length !== items.length) {
      messagesContainer.innerHTML = html;
    } else {
      // Sinon, mettre à jour uniquement les données qui changent (sans recréer le DOM)
      items.forEach((item, index) => {
        const existingItem = existingItems[index];
        if (!existingItem) return;
        
        const config = stateConfig[item.state];
        
        // Pour l'historique (une seule div de texte)
        if (item.state === 'song') {
          const titleEl = existingItem.querySelector('div:nth-child(2)');
          if (titleEl && titleEl.textContent !== item.metadata.title) {
            titleEl.textContent = item.metadata.title;
          }
        } else {
          // Pour les items actifs (3 divs : état, titre, artiste)
          const stateEl = existingItem.querySelector('div:nth-child(2) > div:nth-child(1)');
          const titleEl = existingItem.querySelector('div:nth-child(2) > div:nth-child(2)');
          const artistEl = existingItem.querySelector('div:nth-child(2) > div:nth-child(3)');
          
          if (stateEl && stateEl.textContent !== config.label) {
            stateEl.textContent = config.label;
            stateEl.style.color = config.color;
          }
          if (titleEl && titleEl.textContent !== item.metadata.title) {
            titleEl.textContent = item.metadata.title;
          }
          if (artistEl && artistEl.textContent !== item.metadata.artist) {
            artistEl.textContent = item.metadata.artist;
          }
        }
      });
    }
    
    lastRenderedState = currentState;
  }
}

// Fonction globale pour annuler
window.cancelCurrentDownload = async function() {
  try {
    await chrome.runtime.sendMessage({ action: 'cancel_download' });
  } catch (error) {
    console.error('Cancel error:', error);
  }
}

// Ajouter un message au chat (gardé pour les erreurs uniquement)
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
      transform: translateY(20px) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }
  
  @keyframes slideOut {
    0% {
      opacity: 1;
      transform: translateY(0) scale(1);
      max-height: 100px;
      margin-bottom: 4px;
    }
    50% {
      opacity: 0.5;
      transform: translateY(-20px) scale(0.97);
    }
    100% {
      opacity: 0;
      transform: translateY(-40px) scale(0.9);
      max-height: 0;
      margin-bottom: 0;
      padding-top: 0;
      padding-bottom: 0;
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
  
  .download-item {
    animation: slideIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  .download-item.removing {
    animation: slideOut 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }
  
  #grabsong-messages {
    scroll-behavior: smooth;
  }
  
  .grabsong-message {
    animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  #grabsong-edit-form {
    animation: scaleIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  button {
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  }
  
  #grabsong-container {
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
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
    
    // Détecter le mode album (contient "lectures", "vues", "J'aime", etc.)
    const isAlbumMode = /lectures|vues|j'aime|views|likes/i.test(fullText);
    
    if (isAlbumMode) {
      log('⚠️', '🎵 MODE ALBUM DÉTECTÉ');
      songData.albumMode = true;
      
      // En mode album, extraire l'artiste (premier élément qui n'est pas un nombre)
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
          
          // Chercher une année (4 chiffres)
          const yearMatch = subtitleText.match(/\b(19|20)\d{2}\b/);
          if (yearMatch) {
            songData.year = yearMatch[0];
            log('📅', 'Year (from header):', songData.year);
          }
        }
      }
      
      if (!songData.album || !songData.year) {
        log('⚠️', 'Album ou année non trouvés dans le header');
      }
    } else {
      // Mode normal (chanson individuelle)
      songData.albumMode = false;
      
      if (parts[0]) songData.artist = parts[0];
      if (parts[1]) songData.album = parts[1];
      if (parts[2] && /^\d{4}$/.test(parts[2])) songData.year = parts[2];
    }
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

  // Étape 3: Récupérer l'URL depuis le champ de texte du dialog
  log('🔍', 'Looking for share URL input field...');
  
  // Chercher le champ input qui contient l'URL
  const urlInput = document.querySelector('input[type="text"]');
  
  if (urlInput && urlInput.value && urlInput.value.includes('youtube.com')) {
    const shareLink = urlInput.value;
    log('✅', 'Share link obtained from input field:', shareLink);
    
    // Fermer le dialog
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
    
    log('🎵', 'Link will be sent to yt-dlp with noplaylist=true');
    return shareLink;
  }
  
  // Fallback: essayer de trouver l'URL dans le DOM
  log('🔍', 'Input field not found, trying alternative methods...');
  
  const shareContainer = document.querySelector('ytmusic-unified-share-panel-renderer');
  if (shareContainer) {
    const allInputs = shareContainer.querySelectorAll('input');
    log('🔍', `Found ${allInputs.length} inputs in share panel`);
    
    for (const input of allInputs) {
      log('🔍', `Input value: "${input.value}"`);
      if (input.value && input.value.includes('youtube.com')) {
        const shareLink = input.value;
        log('✅', 'Share link found:', shareLink);
        
        // Fermer le dialog
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
        
        return shareLink;
      }
    }
  }
  
  // Dernier recours: utiliser window.location
  log('⚠️', 'Could not find share link, using page URL');
  
  // Fermer le dialog
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
  
  return window.location.href;
}

// ============================================
// TÉLÉCHARGEMENT
// ============================================

async function performDownload() {
  log('🚀', '=== Starting SongSurf ===');
  
  try {
    // Extraction silencieuse
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
    
    // Si auto-accept est activé, télécharger directement
    if (settings.autoAccept) {
      // Lancer directement le téléchargement
      startDownload(songData);
      return;
    }
    
    // Sinon, afficher le formulaire de vérification
    showEditForm(songData);
    
  } catch (error) {
    log('❌', 'Error:', error);
    addChatMessage(
      `<div style="background: #ffebee; border: 2px solid #f44336; border-radius: 10px; padding: 15px; text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">❌</div>
        <strong style="color: #c62828; font-size: 16px;">Erreur</strong>
        <p style="margin: 10px 0; color: #666; font-size: 14px;">
          ${error.message}
        </p>
      </div>`,
      'error'
    );
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
    // Retour à la liste
    updateDownloadList({ queue_size: 0, in_progress: false });
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
    // Envoyer au serveur Python (ajout silencieux à la queue)
    const response = await chrome.runtime.sendMessage({
      action: 'download_song',
      data: songData
    });
    
    if (!response || !response.success) {
      throw new Error(response?.error || 'Serveur Python non accessible');
    }
    
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
      
      // Ajouter à l'historique si un téléchargement vient de se terminer
      if (status.last_completed && status.last_completed.metadata) {
        const lastInHistory = downloadHistory[downloadHistory.length - 1];
        // Vérifier si ce n'est pas déjà dans l'historique
        if (!lastInHistory || 
            lastInHistory.metadata.title !== status.last_completed.metadata.title ||
            lastInHistory.metadata.artist !== status.last_completed.metadata.artist) {
          
          // Si on va dépasser 5, animer la suppression du premier
          if (downloadHistory.length >= 5) {
            const messagesContainer = document.getElementById('grabsong-messages');
            if (messagesContainer) {
              const firstItem = messagesContainer.querySelector('.download-item');
              if (firstItem) {
                firstItem.classList.add('removing');
                // Attendre la fin de l'animation avant de supprimer (800ms pour laisser l'animation complète)
                setTimeout(() => {
                  downloadHistory.shift();
                  downloadHistory.push({
                    metadata: status.last_completed.metadata,
                    timestamp: Date.now()
                  });
                  updateDownloadList(status);
                }, 800);
                return; // Ne pas mettre à jour tout de suite
              }
            }
          }
          
          downloadHistory.push({
            metadata: status.last_completed.metadata,
            timestamp: Date.now()
          });
          // Garder seulement les 5 derniers
          if (downloadHistory.length > 5) {
            downloadHistory.shift();
          }
        }
      }
      
      // Mettre à jour la liste des téléchargements
      updateDownloadList(status);
      
      // Gérer les erreurs
      if (status.last_error) {
        addChatMessage(
          `<div style="background: #ffebee; border: 2px solid #f44336; border-radius: 10px; padding: 15px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 10px;">❌</div>
            <strong style="color: #c62828; font-size: 16px;">Erreur</strong>
            <p style="margin: 10px 0; color: #666; font-size: 14px;">
              ${status.last_error.error}
            </p>
          </div>`,
          'error'
        );
      }
    } catch (error) {
      log('❌', 'Polling error:', error);
    }
  }, CONFIG.delays.statusPoll);
}

// Mettre à jour l'affichage de la queue (OBSOLETE - remplacé par updateDownloadList)
function updateQueueDisplay(status) {
  // Cette fonction n'est plus utilisée
  return;
  
  if (status.queue_size > 0 || status.in_progress || status.last_completed) {
    if (!queueDisplay) {
      const messagesContainer = document.getElementById('grabsong-messages');
      
      queueDisplay = document.createElement('div');
      queueDisplay.id = 'queue-display';
      queueDisplay.style.cssText = `
        position: sticky;
        top: 0;
        z-index: 100;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 12px 16px;
        margin-bottom: 10px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        color: white;
        transition: all 0.3s ease;
      `;
      
      messagesContainer.insertBefore(queueDisplay, messagesContainer.firstChild);
    }
    
    const currentSong = status.current_download ? status.current_download.metadata : null;
    const completedSong = status.last_completed ? status.last_completed.metadata : null;
    const queueCount = status.queue_size;
    
    // Déterminer l'état à afficher
    let displayState = '';
    let displaySong = null;
    let bgColor = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    
    if (completedSong && !status.in_progress && queueCount === 0) {
      // Terminé - afficher 3 secondes puis disparaître
      displayState = '✓ Terminé';
      displaySong = completedSong;
      bgColor = 'linear-gradient(135deg, #34C759 0%, #30D158 100%)';
      queueDisplay.style.background = bgColor;
      
      setTimeout(() => {
        if (queueDisplay && !status.in_progress && status.queue_size === 0) {
          queueDisplay.style.opacity = '0';
          queueDisplay.style.transform = 'translateY(-10px)';
          setTimeout(() => queueDisplay.remove(), 300);
        }
      }, 3000);
    } else if (status.in_progress) {
      displayState = '🎵 En cours';
      displaySong = currentSong;
      queueDisplay.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    } else if (queueCount > 0) {
      displayState = '⏸️ En attente';
      queueDisplay.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    }
    
    queueDisplay.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px;">
        <div style="flex: 1;">
          <div style="font-size: 13px; font-weight: 600; margin-bottom: 4px;">
            ${displayState}
          </div>
          ${displaySong ? `
            <div style="font-size: 11px; opacity: 0.9;">
              ${displaySong.artist} - ${displaySong.title}
            </div>
          ` : ''}
          ${queueCount > 0 ? `
            <div style="font-size: 11px; opacity: 0.8; margin-top: 4px;">
              📋 ${queueCount} en attente
            </div>
          ` : ''}
        </div>
        ${status.in_progress ? `
          <button id="cancel-download-btn" style="
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
          ">
            ❌ Annuler
          </button>
        ` : ''}
      </div>
    `;
    
    // Ajouter l'événement au bouton d'annulation
    if (status.in_progress) {
      const cancelBtn = document.getElementById('cancel-download-btn');
      if (cancelBtn) {
        cancelBtn.addEventListener('click', async () => {
          try {
            await chrome.runtime.sendMessage({ action: 'cancel_download' });
            addChatMessage('<strong>🛑</strong> Téléchargement annulé', 'warning');
          } catch (error) {
            log('❌', 'Cancel error:', error);
          }
        });
        
        cancelBtn.addEventListener('mouseenter', () => {
          cancelBtn.style.background = 'rgba(255, 255, 255, 0.3)';
        });
        cancelBtn.addEventListener('mouseleave', () => {
          cancelBtn.style.background = 'rgba(255, 255, 255, 0.2)';
        });
      }
    }
  } else if (queueDisplay) {
    // Supprimer l'affichage si la queue est vide
    queueDisplay.remove();
  }
}

// Ces fonctions ne sont plus utilisées avec le nouveau système de liste

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
