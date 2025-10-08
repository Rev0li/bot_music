// content-v2.js - Version 2 organisée et modulaire
// Ce script s'exécute sur YouTube Music ET sur la page cible

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
  // Créer le bouton d'auto-click
  function createAutoClickButton() {
    // Vérifier si le bouton existe déjà
    if (document.getElementById('auto-click-btn')) {
      return;
    }

    // Créer le bouton
    const button = document.createElement('button');
    button.id = 'auto-click-btn';
    button.textContent = CONFIG.ui.buttonText;
    button.className = 'auto-click-floating-btn';
    
    // Ajouter le bouton à la page
    document.body.appendChild(button);
    
    // Ajouter l'événement de clic
    button.addEventListener('click', performAutoShare);
    
    log('✅', 'Auto-click button created');
  }

  // Fonction principale V2
  async function performAutoShare() {
    log('🚀', '=== Starting Auto-Share V2 ===');
    
    try {
      // Étape 1: Extraire toutes les données
      showNotification('📥 Extraction des données...', 'info');
      const songData = await extractAllData();
      
      if (!songData.link) {
        showNotification('❌ Impossible d\'obtenir le lien', 'error');
        return;
      }
      
      // Étape 2: Créer le nom de fichier standardisé pour Python
      // Format: art:Artist alb:Album N:Title Y:Year
      const parts = [];
      if (songData.artist) parts.push(`art=${songData.artist}`);
      if (songData.album) parts.push(`alb=${songData.album}`);
      if (songData.title) parts.push(`N=${songData.title}`);
      if (songData.year) parts.push(`Y=${songData.year}`);
      
      const filename = parts.join(' ') + '.mp3';
      // Nettoyer les caractères invalides mais garder les ':'
      const cleanFilename = filename.replace(/[<>"/\\|?*]/g, '');
      
      log('📝', 'Filename created:', cleanFilename);
      
      // Copier le nom de fichier dans le clipboard
      await copyToClipboard(cleanFilename);
      showNotification(`📋 Filename: ${cleanFilename.substring(0, 40)}...`, 'success');
      
      // Sauvegarder aussi le filename dans les données
      songData.filename = cleanFilename;
      
      // Étape 3: Ouvrir la page cible avec les données
      showNotification('🌐 Ouverture de Y2Mate...', 'info');
      await openTargetPageWithData(songData);
      
      log('✅', '=== Auto-Share V2 Complete ===');
      
    } catch (error) {
      log('❌', 'Error in performAutoShare:', error);
      showNotification('❌ Erreur: ' + error.message, 'error');
    }
  }

  // Initialiser l'extension quand la page est chargée
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createAutoClickButton);
  } else {
    createAutoClickButton();
  }

  // Écouter les messages de la popup
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'performClick') {
      performAutoShare();
      sendResponse({ success: true });
    }
  });
}

// ============================================
// Y2MATE - AUTO-WORKFLOW
// ============================================

if (isY2Mate) {
  log('🎯', 'Y2Mate page detected, checking for data...');
  
  // Attendre un peu puis démarrer le workflow
  setTimeout(() => {
    fillTargetPageFields();
  }, 500);
}

// ============================================
// FALLBACK - Autres pages
// ============================================

if (!isYouTubeMusic && !isY2Mate) {
  log('ℹ️', 'Extension loaded but not on YouTube Music or Y2Mate');
}
