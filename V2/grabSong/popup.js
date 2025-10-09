/**
 * popup.js - Interface popup de l'extension
 * 
 * FONCTIONNALITÉ:
 *   - Affiche l'état de la connexion Python
 *   - Statistiques d'utilisation
 *   - Boutons de test et paramètres
 */

console.log('🎵 GrabSong popup.js chargé');

// Éléments DOM
const statusDiv = document.getElementById('status');
const testButton = document.getElementById('testConnection');
const settingsButton = document.getElementById('openSettings');
const imageCountSpan = document.getElementById('imageCount');
const lastActionSpan = document.getElementById('lastAction');

// État
let isConnected = false;
let stats = {
  imageCount: 0,
  lastAction: 'Aucune'
};

/**
 * Initialisation
 */
document.addEventListener('DOMContentLoaded', () => {
  console.log('📱 Popup initialisé');
  
  // Charger les statistiques depuis le storage
  loadStats();
  
  // Vérifier l'état de la connexion
  checkConnection();
  
  // Event listeners
  testButton.addEventListener('click', testConnection);
  settingsButton.addEventListener('click', openSettings);
});

/**
 * Charge les statistiques depuis chrome.storage
 */
function loadStats() {
  chrome.storage.local.get(['stats'], (result) => {
    if (result.stats) {
      stats = result.stats;
      updateStatsDisplay();
    }
  });
}

/**
 * Sauvegarde les statistiques
 */
function saveStats() {
  chrome.storage.local.set({ stats: stats });
}

/**
 * Met à jour l'affichage des statistiques
 */
function updateStatsDisplay() {
  imageCountSpan.textContent = stats.imageCount;
  lastActionSpan.textContent = stats.lastAction;
}

/**
 * Vérifie l'état de la connexion
 */
function checkConnection() {
  // Envoyer un message au background pour vérifier
  chrome.runtime.sendMessage({ action: 'check_connection' }, (response) => {
    if (chrome.runtime.lastError) {
      console.error('Erreur:', chrome.runtime.lastError);
      updateConnectionStatus(false);
      return;
    }
    
    updateConnectionStatus(response && response.connected);
  });
}

/**
 * Met à jour l'affichage de l'état de connexion
 */
function updateConnectionStatus(connected) {
  isConnected = connected;
  
  if (connected) {
    statusDiv.className = 'status connected';
    statusDiv.textContent = '✅ Connecté à Python';
  } else {
    statusDiv.className = 'status disconnected';
    statusDiv.textContent = '⭕ Déconnecté de Python';
  }
}

/**
 * Teste la connexion
 */
function testConnection() {
  console.log('🔌 Test de connexion...');
  testButton.disabled = true;
  testButton.textContent = '⏳ Test en cours...';
  
  // Envoyer un message de test
  chrome.runtime.sendMessage({ 
    action: 'test_connection' 
  }, (response) => {
    testButton.disabled = false;
    testButton.textContent = '🔌 Tester la connexion';
    
    if (response && response.success) {
      updateConnectionStatus(true);
      stats.lastAction = 'Test connexion réussi';
    } else {
      updateConnectionStatus(false);
      stats.lastAction = 'Test connexion échoué';
    }
    
    updateStatsDisplay();
    saveStats();
  });
}

/**
 * Ouvre les paramètres
 */
function openSettings() {
  // TODO: Ouvrir une page de paramètres
  chrome.tabs.create({ 
    url: 'chrome://extensions/?id=' + chrome.runtime.id 
  });
}

/**
 * Écoute les messages du background
 */
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'stats_update') {
    stats = message.stats;
    updateStatsDisplay();
    saveStats();
  }
  
  if (message.action === 'connection_status') {
    updateConnectionStatus(message.connected);
  }
});

console.log('✅ Popup initialisé');
