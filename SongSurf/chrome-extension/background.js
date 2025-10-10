/**
 * background.js - Service Worker pour GrabSong V3
 * 
 * FONCTIONNALITÉ:
 *   - Gère la communication avec le serveur Python
 *   - Pas de gestion d'onglets (plus besoin de Y2Mate)
 */

console.log('🎵 [GrabSong V3] Service Worker démarré');

// Configuration
const PYTHON_SERVER = 'http://localhost:5000';

// ============================================
// MESSAGE HANDLERS
// ============================================

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('📨 Message reçu:', message);
  
  if (message.action === 'download_song') {
    handleDownload(message.data)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Indique que la réponse sera asynchrone
  }
  
  if (message.action === 'get_status') {
    getStatus()
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
  
  if (message.action === 'cleanup') {
    cleanup()
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
  
  if (message.action === 'cancel_download') {
    cancelDownload()
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
  
});

// ============================================
// FONCTIONS
// ============================================

/**
 * Lance un téléchargement via le serveur Python
 */
async function handleDownload(data) {
  try {
    console.log('🚀 Lancement du téléchargement:', data);
    
    const response = await fetch(`${PYTHON_SERVER}/download`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error(`Erreur serveur: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('✅ Réponse du serveur:', result);
    
    return result;
    
  } catch (error) {
    console.error('❌ Erreur lors du téléchargement:', error);
    throw error;
  }
}

/**
 * Récupère le statut du téléchargement en cours
 */
async function getStatus() {
  try {
    const response = await fetch(`${PYTHON_SERVER}/status`);
    
    if (!response.ok) {
      throw new Error(`Erreur serveur: ${response.status}`);
    }
    
    const result = await response.json();
    return result;
    
  } catch (error) {
    console.error('❌ Erreur lors de la récupération du statut:', error);
    throw error;
  }
}

/**
 * Nettoie le dossier temporaire
 */
async function cleanup() {
  try {
    const response = await fetch(`${PYTHON_SERVER}/cleanup`, {
      method: 'POST'
    });
    
    if (!response.ok) {
      throw new Error(`Erreur serveur: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('✅ Nettoyage effectué:', result);
    
    return result;
    
  } catch (error) {
    console.error('❌ Erreur lors du nettoyage:', error);
    throw error;
  }
}

/**
 * Annule le téléchargement en cours
 */
async function cancelDownload() {
  try {
    const response = await fetch(`${PYTHON_SERVER}/cancel`, {
      method: 'POST'
    });
    
    if (!response.ok) {
      throw new Error(`Erreur serveur: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('✅ Téléchargement annulé:', result);
    
    return result;
    
  } catch (error) {
    console.error('❌ Erreur lors de l\'annulation:', error);
    throw error;
  }
}

/**
 * Test de connexion au serveur Python
 */
async function testConnection() {
  try {
    const response = await fetch(`${PYTHON_SERVER}/ping`);
    
    if (!response.ok) {
      return false;
    }
    
    const result = await response.json();
    console.log('✅ Serveur Python accessible:', result);
    return true;
    
  } catch (error) {
    console.error('❌ Serveur Python non accessible:', error);
    return false;
  }
}

// Test de connexion au démarrage
testConnection();
