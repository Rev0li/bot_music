/**
 * content-simple.js - SongSurf Extension Simplifiée
 * 
 * WORKFLOW SIMPLIFIÉ:
 *   1. Récupérer l'URL de la page YouTube Music
 *   2. Envoyer au backend pour extraction des métadonnées
 *   3. Afficher un formulaire de confirmation (optionnel)
 *   4. Lancer le téléchargement
 *   5. Afficher la progression en temps réel
 */

console.log('🎵 [SongSurf] Extension simplifiée chargée');

// ============================================
// CONFIGURATION
// ============================================

const CONFIG = {
  serverUrl: 'http://localhost:8080',
  statusPollInterval: 1000, // 1 seconde
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

// Détecte le type de page YouTube Music
function detectPageType() {
  const url = window.location.href;
  
  // Playlist
  if (url.includes('/playlist?list=')) {
    return {
      type: 'playlist',
      url: url,
      id: new URLSearchParams(window.location.search).get('list')
    };
  }
  
  // Album
  if (url.includes('/browse/') && url.includes('MPREb_')) {
    return {
      type: 'album',
      url: url,
      id: url.match(/MPREb_[a-zA-Z0-9_-]+/)?.[0]
    };
  }
  
  // Musique simple
  if (url.includes('/watch?v=')) {
    return {
      type: 'song',
      url: url,
      id: new URLSearchParams(window.location.search).get('v')
    };
  }
  
  return {
    type: 'unknown',
    url: url,
    id: null
  };
}

// ============================================
// API BACKEND
// ============================================

async function extractMetadata(url) {
  try {
    const response = await fetch(`${CONFIG.serverUrl}/api/extract-metadata`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    return await response.json();
  } catch (error) {
    log('❌', 'Erreur extraction métadonnées:', error);
    return { success: false, error: error.message };
  }
}

async function startDownload(url, metadata) {
  try {
    const response = await fetch(`${CONFIG.serverUrl}/download`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, ...metadata })
    });
    return await response.json();
  } catch (error) {
    log('❌', 'Erreur démarrage téléchargement:', error);
    return { success: false, error: error.message };
  }
}

async function getStatus() {
  try {
    const response = await fetch(`${CONFIG.serverUrl}/status`);
    return await response.json();
  } catch (error) {
    log('❌', 'Erreur récupération statut:', error);
    return { in_progress: false };
  }
}

async function pingServer() {
  try {
    console.log('🔍 Test connexion serveur:', CONFIG.serverUrl);
    const response = await fetch(`${CONFIG.serverUrl}/ping`);
    console.log('📡 Réponse serveur:', response.status, response.statusText);
    const data = await response.json();
    console.log('📦 Data:', data);
    const isOk = data.status === 'ok';
    console.log('✅ Serveur OK:', isOk);
    return isOk;
  } catch (error) {
    console.error('❌ Erreur ping serveur:', error);
    console.error('   Message:', error.message);
    console.error('   Type:', error.name);
    return false;
  }
}

// ============================================
// INTERFACE UTILISATEUR
// ============================================

let statusPollingInterval = null;
let widgetPosition = null; // Sauvegarder la position du widget

// Rendre un élément déplaçable
function makeDraggable(element) {
  let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  
  // Restaurer la position sauvegardée si elle existe
  if (widgetPosition) {
    element.style.top = widgetPosition.top;
    element.style.left = widgetPosition.left;
    element.style.bottom = "auto";
    element.style.right = "auto";
  }
  
  element.onmousedown = dragMouseDown;
  
  function dragMouseDown(e) {
    // Ne pas déplacer si on clique sur un bouton ou input
    if (e.target.tagName === 'BUTTON' || e.target.tagName === 'INPUT') {
      return;
    }
    
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
  }
  
  function elementDrag(e) {
    e.preventDefault();
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    
    // Calculer la nouvelle position
    let newTop = element.offsetTop - pos2;
    let newLeft = element.offsetLeft - pos1;
    
    // Limites de l'écran
    newTop = Math.max(0, Math.min(newTop, window.innerHeight - element.offsetHeight));
    newLeft = Math.max(0, Math.min(newLeft, window.innerWidth - element.offsetWidth));
    
    element.style.top = newTop + "px";
    element.style.left = newLeft + "px";
    element.style.bottom = "auto";
    element.style.right = "auto";
    
    // Sauvegarder la position
    widgetPosition = {
      top: element.style.top,
      left: element.style.left
    };
  }
  
  function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
  }
}

function createWidget() {
  if (document.getElementById('songsurf-widget')) {
    return;
  }
  
  const widget = document.createElement('div');
  widget.id = 'songsurf-widget';
  widget.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 999999;
    width: 320px;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(20px);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    border: 1px solid rgba(0, 0, 0, 0.06);
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    cursor: move;
  `;
  
  // Rendre le widget déplaçable
  makeDraggable(widget);
  
  widget.innerHTML = `
    <style>
      @keyframes spin {
        to { transform: rotate(360deg); }
      }
      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
      }
    </style>
    
    <!-- Header -->
    <div style="padding: 16px; text-align: center; border-bottom: 1px solid rgba(0,0,0,0.06);">
      <div style="display: flex; align-items: center; justify-content: center; gap: 8px; color: #1d1d1f;">
        <span style="font-size: 20px;">🎵</span>
        <span style="font-weight: 600; font-size: 15px; letter-spacing: -0.3px;">SongSurf</span>
      </div>
    </div>
    
    <!-- Content -->
    <div id="songsurf-content" style="padding: 20px;">
      <!-- Détection du type de page -->
      <div id="page-type-info" style="
        margin-bottom: 12px;
        padding: 8px 12px;
        background: #f5f5f7;
        border-radius: 8px;
        font-size: 12px;
        color: #86868b;
        text-align: center;
      "></div>
      
      <!-- Bouton Télécharger Musique -->
      <button id="download-song-btn" style="
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 14px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        margin-bottom: 10px;
      ">
        🎵 Télécharger cette musique
      </button>
      
      <!-- Bouton Télécharger Album/Playlist -->
      <button id="download-album-btn" style="
        width: 100%;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 14px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);
        display: none;
      ">
        💿 Télécharger l'album/playlist
      </button>
      
      <div id="status-message" style="
        margin-top: 12px;
        padding: 12px;
        background: #f5f5f7;
        border-radius: 8px;
        font-size: 13px;
        color: #86868b;
        text-align: center;
        display: none;
      "></div>
    </div>
  `;
  
  document.body.appendChild(widget);
  
  // Détecter le type de page
  const pageInfo = detectPageType();
  updateWidgetForPageType(pageInfo);
  
  // Event listeners
  const downloadSongBtn = document.getElementById('download-song-btn');
  const downloadAlbumBtn = document.getElementById('download-album-btn');
  
  downloadSongBtn.addEventListener('click', () => handleDownloadSong(pageInfo));
  downloadAlbumBtn.addEventListener('click', () => handleDownloadAlbum(pageInfo));
  
  // Hover effects - Song button
  downloadSongBtn.addEventListener('mouseenter', () => {
    downloadSongBtn.style.transform = 'translateY(-2px)';
    downloadSongBtn.style.boxShadow = '0 6px 16px rgba(102, 126, 234, 0.4)';
  });
  downloadSongBtn.addEventListener('mouseleave', () => {
    downloadSongBtn.style.transform = 'translateY(0)';
    downloadSongBtn.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.3)';
  });
  
  // Hover effects - Album button
  downloadAlbumBtn.addEventListener('mouseenter', () => {
    downloadAlbumBtn.style.transform = 'translateY(-2px)';
    downloadAlbumBtn.style.boxShadow = '0 6px 16px rgba(240, 147, 251, 0.4)';
  });
  downloadAlbumBtn.addEventListener('mouseleave', () => {
    downloadAlbumBtn.style.transform = 'translateY(0)';
    downloadAlbumBtn.style.boxShadow = '0 4px 12px rgba(240, 147, 251, 0.3)';
  });
  
  log('✅', 'Widget créé', pageInfo);
}

function showStatus(message, type = 'info') {
  const statusDiv = document.getElementById('status-message');
  if (!statusDiv) return;
  
  const colors = {
    info: { bg: '#f5f5f7', text: '#86868b' },
    success: { bg: '#d1f4e0', text: '#1d8348' },
    error: { bg: '#ffebee', text: '#c62828' },
    warning: { bg: '#fff3cd', text: '#856404' }
  };
  
  const color = colors[type] || colors.info;
  
  statusDiv.style.background = color.bg;
  statusDiv.style.color = color.text;
  statusDiv.innerHTML = message;
  statusDiv.style.display = 'block';
}

function showPlaylistConfirmation(playlistData, url) {
  const content = document.getElementById('songsurf-content');
  if (!content) return;
  
  const totalSongs = playlistData.total_songs || 0;
  const totalDuration = playlistData.total_duration || 0;
  const durationMin = Math.floor(totalDuration / 60);
  const durationSec = totalDuration % 60;
  
  content.innerHTML = `
    <div style="padding: 20px 0;">
      <h3 style="margin: 0 0 16px 0; font-size: 16px; color: #1d1d1f; font-weight: 600;">
        ${playlistData.type === 'album' ? '💿 Album' : '📋 Playlist'} détecté
      </h3>
      
      <div style="background: #f5f5f7; padding: 16px; border-radius: 12px; margin-bottom: 16px;">
        <div style="font-size: 14px; color: #1d1d1f; margin-bottom: 8px;">
          <strong>${playlistData.title}</strong>
        </div>
        <div style="font-size: 13px; color: #86868b; margin-bottom: 4px;">
          🎤 ${playlistData.artist}
        </div>
        <div style="font-size: 13px; color: #86868b; margin-bottom: 4px;">
          🎵 ${totalSongs} chanson${totalSongs > 1 ? 's' : ''}
        </div>
        <div style="font-size: 13px; color: #86868b;">
          ⏱️ ${durationMin}min ${durationSec}s
        </div>
      </div>
      
      <div style="background: #fff3cd; padding: 12px; border-radius: 8px; margin-bottom: 16px; border: 1px solid #ffc107;">
        <div style="font-size: 12px; color: #856404;">
          ⚠️ ${totalSongs} chansons seront téléchargées
        </div>
      </div>
      
      <div style="display: flex; gap: 10px;">
        <button id="cancel-playlist-btn" style="
          flex: 1;
          padding: 12px;
          background: rgba(0,0,0,0.04);
          color: #1d1d1f;
          border: none;
          border-radius: 10px;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
        ">
          ❌ Annuler
        </button>
        
        <button id="confirm-playlist-btn" style="
          flex: 2;
          padding: 12px;
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
          border: none;
          border-radius: 10px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
          box-shadow: 0 2px 8px rgba(240, 147, 251, 0.3);
        ">
          💿 Télécharger tout
        </button>
      </div>
    </div>
  `;
  
  // Event listeners
  document.getElementById('cancel-playlist-btn').addEventListener('click', () => {
    // Supprimer le widget existant
    const existingWidget = document.getElementById('songsurf-widget');
    if (existingWidget) {
      existingWidget.remove();
    }
    // Recréer le widget initial
    createWidget();
  });
  
  document.getElementById('confirm-playlist-btn').addEventListener('click', async () => {
    showStatus('Envoi de la playlist au serveur...', 'info');
    
    // Envoyer au backend pour téléchargement
    try {
      const response = await fetch(`${CONFIG.serverUrl}/api/download-playlist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: url,
          playlist_metadata: playlistData
        })
      });
      
      const result = await response.json();
      console.log('📦 Réponse téléchargement playlist:', result);
      
      if (result.success) {
        showStatus(`✅ ${result.added} chansons ajoutées à la queue`, 'success');
        // Démarrer le polling du statut
        startStatusPolling();
      } else {
        showError(result.error || 'Erreur lors du téléchargement de la playlist');
      }
    } catch (error) {
      showError('Erreur de connexion au serveur');
      console.error('Erreur:', error);
    }
  });
}

function showMetadataForm(metadata) {
  const content = document.getElementById('songsurf-content');
  if (!content) return;
  
  content.innerHTML = `
    <div style="margin-bottom: 16px;">
      <h3 style="margin: 0 0 12px 0; font-size: 14px; color: #1d1d1f; font-weight: 600;">
        Vérifier les métadonnées
      </h3>
    </div>
    
    <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 16px;">
      <div>
        <label style="display: block; font-size: 12px; color: #86868b; margin-bottom: 4px;">🎵 Titre</label>
        <input type="text" id="meta-title" value="${metadata.title || ''}" style="
          width: 100%;
          padding: 10px;
          border: 1px solid rgba(0,0,0,0.1);
          border-radius: 8px;
          font-size: 14px;
          box-sizing: border-box;
        ">
      </div>
      
      <div>
        <label style="display: block; font-size: 12px; color: #86868b; margin-bottom: 4px;">🎤 Artiste</label>
        <input type="text" id="meta-artist" value="${metadata.artist || ''}" style="
          width: 100%;
          padding: 10px;
          border: 1px solid rgba(0,0,0,0.1);
          border-radius: 8px;
          font-size: 14px;
          box-sizing: border-box;
        ">
      </div>
      
      <div>
        <label style="display: block; font-size: 12px; color: #86868b; margin-bottom: 4px;">💿 Album</label>
        <input type="text" id="meta-album" value="${metadata.album || ''}" style="
          width: 100%;
          padding: 10px;
          border: 1px solid rgba(0,0,0,0.1);
          border-radius: 8px;
          font-size: 14px;
          box-sizing: border-box;
        ">
      </div>
      
      <div>
        <label style="display: block; font-size: 12px; color: #86868b; margin-bottom: 4px;">📅 Année</label>
        <input type="text" id="meta-year" value="${metadata.year || ''}" style="
          width: 100%;
          padding: 10px;
          border: 1px solid rgba(0,0,0,0.1);
          border-radius: 8px;
          font-size: 14px;
          box-sizing: border-box;
        ">
      </div>
    </div>
    
    <div style="display: flex; gap: 10px;">
      <button id="cancel-btn" style="
        flex: 1;
        padding: 12px;
        background: rgba(0,0,0,0.04);
        color: #1d1d1f;
        border: none;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
      ">
        ❌ Annuler
      </button>
      
      <button id="confirm-btn" style="
        flex: 2;
        padding: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
      ">
        💾 Télécharger
      </button>
    </div>
  `;
  
  // Event listeners
  document.getElementById('cancel-btn').addEventListener('click', () => {
    createWidget(); // Recréer le widget initial
  });
  
  document.getElementById('confirm-btn').addEventListener('click', () => {
    const updatedMetadata = {
      title: document.getElementById('meta-title').value,
      artist: document.getElementById('meta-artist').value,
      album: document.getElementById('meta-album').value,
      year: document.getElementById('meta-year').value,
    };
    confirmDownload(window.location.href, updatedMetadata);
  });
}

function showProgress() {
  const content = document.getElementById('songsurf-content');
  if (!content) return;
  
  content.innerHTML = `
    <div style="text-align: center; padding: 20px 0;">
      <div style="
        width: 60px;
        height: 60px;
        margin: 0 auto 16px;
        border: 4px solid rgba(102, 126, 234, 0.2);
        border-top-color: #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      "></div>
      
      <div style="font-size: 14px; color: #1d1d1f; font-weight: 500; margin-bottom: 8px;">
        Téléchargement en cours...
      </div>
      
      <div id="progress-details" style="font-size: 12px; color: #86868b;">
        Veuillez patienter
      </div>
    </div>
  `;
}

function updateProgressDetails(progress) {
  const detailsDiv = document.getElementById('progress-details');
  if (!detailsDiv) return;
  
  if (progress.status === 'downloading') {
    detailsDiv.innerHTML = `${progress.percent}% • ${progress.speed}`;
  } else if (progress.status === 'processing') {
    detailsDiv.innerHTML = 'Conversion en MP3...';
  }
}

function showSuccess(result) {
  const content = document.getElementById('songsurf-content');
  if (!content) return;
  
  content.innerHTML = `
    <div style="text-align: center; padding: 20px 0;">
      <div style="
        width: 60px;
        height: 60px;
        margin: 0 auto 16px;
        background: #34C759;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
      ">
        ✓
      </div>
      
      <div style="font-size: 15px; color: #1d1d1f; font-weight: 600; margin-bottom: 8px;">
        Téléchargement terminé !
      </div>
      
      <div style="font-size: 12px; color: #86868b; margin-bottom: 20px;">
        📁 ${result.file_path}
      </div>
      
      <button id="download-another-btn" style="
        width: 100%;
        padding: 12px;
        background: #007AFF;
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
      ">
        Télécharger une autre chanson
      </button>
    </div>
  `;
  
  document.getElementById('download-another-btn').addEventListener('click', () => {
    // Supprimer le widget existant
    const existingWidget = document.getElementById('songsurf-widget');
    if (existingWidget) {
      existingWidget.remove();
    }
    // Recréer le widget initial
    createWidget();
  });
}

function showError(error) {
  const content = document.getElementById('songsurf-content');
  if (!content) return;
  
  content.innerHTML = `
    <div style="text-align: center; padding: 20px 0;">
      <div style="font-size: 48px; margin-bottom: 12px;">❌</div>
      
      <div style="font-size: 15px; color: #c62828; font-weight: 600; margin-bottom: 8px;">
        Erreur
      </div>
      
      <div style="font-size: 13px; color: #86868b; margin-bottom: 20px;">
        ${error}
      </div>
      
      <button id="retry-btn" style="
        width: 100%;
        padding: 12px;
        background: rgba(0,0,0,0.04);
        color: #1d1d1f;
        border: none;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
      ">
        Réessayer
      </button>
    </div>
  `;
  
  document.getElementById('retry-btn').addEventListener('click', () => {
    // Supprimer le widget existant
    const existingWidget = document.getElementById('songsurf-widget');
    if (existingWidget) {
      existingWidget.remove();
    }
    // Recréer le widget initial
    createWidget();
  });
}

// ============================================
// LOGIQUE PRINCIPALE
// ============================================

// Met à jour le widget en fonction du type de page
function updateWidgetForPageType(pageInfo) {
  const pageTypeInfo = document.getElementById('page-type-info');
  const downloadSongBtn = document.getElementById('download-song-btn');
  const downloadAlbumBtn = document.getElementById('download-album-btn');
  
  if (!pageTypeInfo) return;
  
  const typeEmojis = {
    'song': '🎵',
    'album': '💿',
    'playlist': '📋',
    'unknown': '❓'
  };
  
  const typeLabels = {
    'song': 'Musique détectée',
    'album': 'Album détecté',
    'playlist': 'Playlist détectée',
    'unknown': 'Page non reconnue'
  };
  
  pageTypeInfo.innerHTML = `${typeEmojis[pageInfo.type]} ${typeLabels[pageInfo.type]}`;
  
  // Afficher/masquer les boutons selon le type
  if (pageInfo.type === 'song') {
    downloadSongBtn.style.display = 'block';
    downloadAlbumBtn.style.display = 'none';
  } else if (pageInfo.type === 'album' || pageInfo.type === 'playlist') {
    downloadSongBtn.style.display = 'block';
    downloadAlbumBtn.style.display = 'block';
  } else {
    downloadSongBtn.style.display = 'none';
    downloadAlbumBtn.style.display = 'none';
    pageTypeInfo.style.background = '#ffebee';
    pageTypeInfo.style.color = '#c62828';
  }
  
  log('📍', 'Type de page détecté:', pageInfo);
}

// Gère le clic sur "Télécharger cette musique"
async function handleDownloadSong(pageInfo) {
  console.log('🎵 ========================================');
  console.log('🎵 TÉLÉCHARGER MUSIQUE');
  console.log('🎵 ========================================');
  console.log('📍 Type:', pageInfo.type);
  console.log('🔗 URL:', pageInfo.url);
  console.log('🆔 ID:', pageInfo.id);
  console.log('🎵 ========================================');
  
  // Vérifier la connexion au serveur
  showStatus('Connexion au serveur...', 'info');
  const serverOnline = await pingServer();
  
  if (!serverOnline) {
    showStatus('❌ Serveur non accessible. Lancez: python app.py', 'error');
    return;
  }
  
  // Extraire les métadonnées
  showStatus('Extraction des métadonnées...', 'info');
  console.log('📡 Envoi au backend:', pageInfo.url);
  
  const metadataResult = await extractMetadata(pageInfo.url);
  console.log('📦 Réponse du backend:', metadataResult);
  
  if (!metadataResult.success) {
    showError(metadataResult.error || 'Erreur lors de l\'extraction des métadonnées');
    return;
  }
  
  log('✅', 'Métadonnées extraites:', metadataResult.metadata);
  
  // Afficher le formulaire de confirmation
  showMetadataForm(metadataResult.metadata);
}

// Gère le clic sur "Télécharger l'album/playlist"
async function handleDownloadAlbum(pageInfo) {
  console.log('💿 ========================================');
  console.log('💿 TÉLÉCHARGER ALBUM/PLAYLIST');
  console.log('💿 ========================================');
  console.log('📍 Type:', pageInfo.type);
  console.log('🔗 URL:', pageInfo.url);
  console.log('🆔 ID:', pageInfo.id);
  console.log('💿 ========================================');
  
  // Vérifier la connexion au serveur
  showStatus('Connexion au serveur...', 'info');
  const serverOnline = await pingServer();
  
  if (!serverOnline) {
    showStatus('❌ Serveur non accessible. Lancez: python app.py', 'error');
    return;
  }
  
  // Extraire les métadonnées de la playlist/album
  showStatus('Extraction de l\'album/playlist...', 'info');
  console.log('📡 Envoi au backend:', pageInfo.url);
  
  const playlistResult = await extractMetadata(pageInfo.url);
  console.log('📦 Réponse du backend:', playlistResult);
  
  if (!playlistResult.success) {
    showError(playlistResult.error || 'Erreur lors de l\'extraction de l\'album/playlist');
    return;
  }
  
  log('✅', 'Playlist/Album extrait:', playlistResult);
  
  // Afficher un résumé et demander confirmation
  showPlaylistConfirmation(playlistResult, pageInfo.url);
}

async function handleDownload() {
  const downloadBtn = document.getElementById('download-btn');
  if (!downloadBtn) return;
  
  // Désactiver le bouton
  downloadBtn.disabled = true;
  downloadBtn.style.opacity = '0.6';
  downloadBtn.style.cursor = 'not-allowed';
  
  // Vérifier la connexion au serveur
  showStatus('Connexion au serveur...', 'info');
  const serverOnline = await pingServer();
  
  if (!serverOnline) {
    showStatus('❌ Serveur non accessible. Lancez: python app.py', 'error');
    downloadBtn.disabled = false;
    downloadBtn.style.opacity = '1';
    downloadBtn.style.cursor = 'pointer';
    return;
  }
  
  // Récupérer l'URL de la page
  const url = window.location.href;
  log('📍', 'URL actuelle:', url);
  
  // Vérifier que c'est une URL valide
  if (!url.includes('music.youtube.com/watch')) {
    showStatus('⚠️ Veuillez ouvrir une chanson sur YouTube Music', 'warning');
    downloadBtn.disabled = false;
    downloadBtn.style.opacity = '1';
    downloadBtn.style.cursor = 'pointer';
    return;
  }
  
  // Extraire les métadonnées
  showStatus('Extraction des métadonnées...', 'info');
  const metadataResult = await extractMetadata(url);
  
  if (!metadataResult.success) {
    showError(metadataResult.error || 'Erreur lors de l\'extraction des métadonnées');
    return;
  }
  
  log('✅', 'Métadonnées extraites:', metadataResult.metadata);
  
  // Afficher le formulaire de confirmation
  showMetadataForm(metadataResult.metadata);
}

async function confirmDownload(url, metadata) {
  // Afficher la progression
  showProgress();
  
  // Démarrer le téléchargement
  const downloadResult = await startDownload(url, metadata);
  
  if (!downloadResult.success) {
    showError(downloadResult.error || 'Erreur lors du démarrage du téléchargement');
    return;
  }
  
  log('✅', 'Téléchargement démarré');
  
  // Démarrer le polling du statut
  startStatusPolling();
}

function updateProgressDetails(progress) {
  const content = document.getElementById('songsurf-content');
  if (!content) return;
  
  const queueRemaining = progress.queue_remaining || 0;
  const currentSong = progress.current_song || {};
  
  // Les métadonnées sont dans current_song.metadata
  const metadata = currentSong.metadata || {};
  
  content.innerHTML = `
    <div style="padding: 20px 0; text-align: center;">
      <div style="font-size: 48px; margin-bottom: 12px; animation: pulse 1.5s ease-in-out infinite;">
        ⬇️
      </div>
      
      <div style="font-size: 15px; color: #1d1d1f; font-weight: 600; margin-bottom: 8px;">
        Téléchargement en cours...
      </div>
      
      <div style="font-size: 13px; color: #1d1d1f; font-weight: 500; margin-bottom: 16px;">
        ${metadata.title || 'Chargement...'}
      </div>
      
      <div style="background: #f5f5f7; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
        <div style="font-size: 12px; color: #86868b; margin-bottom: 4px;">
          🎤 ${metadata.artist || '...'}
        </div>
        <div style="font-size: 12px; color: #86868b;">
          💿 ${metadata.album || '...'}
        </div>
      </div>
      
      ${queueRemaining > 0 ? `
        <div style="background: #e3f2fd; padding: 10px; border-radius: 8px; border: 1px solid #2196f3;">
          <div style="font-size: 13px; color: #1976d2; font-weight: 500;">
            📋 ${queueRemaining} chanson${queueRemaining > 1 ? 's' : ''} en attente
          </div>
        </div>
      ` : ''}
    </div>
  `;
}

function startStatusPolling() {
  if (statusPollingInterval) {
    clearInterval(statusPollingInterval);
  }
  
  statusPollingInterval = setInterval(async () => {
    const status = await getStatus();
    
    if (status.in_progress && status.current_download) {
      updateProgressDetails({
        current_song: status.current_download,
        queue_remaining: status.queue_size || 0
      });
    } else if (!status.in_progress && status.queue_size === 0) {
      // Téléchargement terminé
      clearInterval(statusPollingInterval);
      if (status.last_completed) {
        showSuccess(status.last_completed);
      }
    } else if (status.last_error) {
      clearInterval(statusPollingInterval);
      showError(status.last_error.error);
    }
  }, CONFIG.statusPollInterval);
}

// ============================================
// DÉTECTION DES CHANGEMENTS D'URL
// ============================================

let lastUrl = window.location.href;

function onUrlChange() {
  const currentUrl = window.location.href;
  
  if (currentUrl !== lastUrl) {
    log('🔄', 'URL changée:', { from: lastUrl, to: currentUrl });
    lastUrl = currentUrl;
    
    // Mettre à jour le widget
    const widget = document.getElementById('songsurf-widget');
    if (widget) {
      const pageInfo = detectPageType();
      updateWidgetForPageType(pageInfo);
      
      // Mettre à jour les event listeners avec la nouvelle pageInfo
      const downloadSongBtn = document.getElementById('download-song-btn');
      const downloadAlbumBtn = document.getElementById('download-album-btn');
      
      if (downloadSongBtn && downloadAlbumBtn) {
        // Supprimer les anciens listeners en clonant les boutons
        const newSongBtn = downloadSongBtn.cloneNode(true);
        const newAlbumBtn = downloadAlbumBtn.cloneNode(true);
        
        downloadSongBtn.parentNode.replaceChild(newSongBtn, downloadSongBtn);
        downloadAlbumBtn.parentNode.replaceChild(newAlbumBtn, downloadAlbumBtn);
        
        // Ajouter les nouveaux listeners
        newSongBtn.addEventListener('click', () => handleDownloadSong(pageInfo));
        newAlbumBtn.addEventListener('click', () => handleDownloadAlbum(pageInfo));
        
        // Réappliquer les hover effects
        newSongBtn.addEventListener('mouseenter', () => {
          newSongBtn.style.transform = 'translateY(-2px)';
          newSongBtn.style.boxShadow = '0 6px 16px rgba(102, 126, 234, 0.4)';
        });
        newSongBtn.addEventListener('mouseleave', () => {
          newSongBtn.style.transform = 'translateY(0)';
          newSongBtn.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.3)';
        });
        
        newAlbumBtn.addEventListener('mouseenter', () => {
          newAlbumBtn.style.transform = 'translateY(-2px)';
          newAlbumBtn.style.boxShadow = '0 6px 16px rgba(240, 147, 251, 0.4)';
        });
        newAlbumBtn.addEventListener('mouseleave', () => {
          newAlbumBtn.style.transform = 'translateY(0)';
          newAlbumBtn.style.boxShadow = '0 4px 12px rgba(240, 147, 251, 0.3)';
        });
      }
    }
  }
}

// Observer les changements d'URL (YouTube Music est une SPA)
function observeUrlChanges() {
  // Méthode 1: MutationObserver sur le body
  const observer = new MutationObserver(() => {
    onUrlChange();
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  
  // Méthode 2: Intercepter pushState et replaceState
  const originalPushState = history.pushState;
  const originalReplaceState = history.replaceState;
  
  history.pushState = function(...args) {
    originalPushState.apply(this, args);
    onUrlChange();
  };
  
  history.replaceState = function(...args) {
    originalReplaceState.apply(this, args);
    onUrlChange();
  };
  
  // Méthode 3: Écouter l'événement popstate
  window.addEventListener('popstate', onUrlChange);
  
  log('👀', 'Observation des changements d\'URL activée');
}

// ============================================
// INITIALISATION
// ============================================

if (window.location.hostname.includes('music.youtube.com')) {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      createWidget();
      observeUrlChanges();
    });
  } else {
    createWidget();
    observeUrlChanges();
  }
  
  log('✅', 'Extension SongSurf initialisée');
}
