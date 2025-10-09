/**
 * background.js - Service Worker pour Native Messaging
 * 
 * FONCTIONNALITÉ:
 *   - Écoute les messages du content script
 *   - Communique avec Python via Native Messaging
 *   - Gère les réponses de Python
 * 
 * WORKFLOW:
 *   1. Reçoit message de content.js (image copiée)
 *   2. Envoie à Python via Native Messaging
 *   3. Reçoit confirmation de Python
 *   4. Notifie content.js pour continuer l'auto-clicker
 */

// Nom du host Python (doit correspondre au manifest Python)
const NATIVE_HOST_NAME = 'com.musicorganizer.grabsong';

// État de la connexion
let nativePort = null;
let isConnected = false;

/**
 * Initialise l'extension au démarrage
 */
chrome.runtime.onStartup.addListener(() => {
  console.log('🚀 GrabSong extension démarrée');
  // Native Messaging désactivé - On utilise Flask HTTP maintenant
  // connectToNativeHost();
});

/**
 * Connexion au host Python
 */
function connectToNativeHost() {
  console.log('🔌 Connexion au host Python...');
  
  try {
    nativePort = chrome.runtime.connectNative(NATIVE_HOST_NAME);
    
    // Écouter les messages de Python
    nativePort.onMessage.addListener((message) => {
      console.log('📨 Message reçu de Python:', message);
      handlePythonResponse(message);
    });
    
    // Gérer la déconnexion
    nativePort.onDisconnect.addListener(() => {
      console.error('❌ Déconnecté du host Python');
      isConnected = false;
      
      if (chrome.runtime.lastError) {
        console.error('Erreur:', chrome.runtime.lastError.message);
      }
      
      // Réessayer la connexion après 5 secondes
      setTimeout(connectToNativeHost, 5000);
    });
    
    isConnected = true;
    console.log('✅ Connecté au host Python');
    
  } catch (error) {
    console.error('❌ Erreur de connexion:', error);
    isConnected = false;
  }
}

/**
 * Envoie un message à Python
 */
function sendToPython(message) {
  if (!isConnected || !nativePort) {
    console.error('❌ Pas de connexion au host Python');
    connectToNativeHost();
    return false;
  }
  
  try {
    console.log('📤 Envoi à Python:', message);
    nativePort.postMessage(message);
    return true;
  } catch (error) {
    console.error('❌ Erreur d\'envoi:', error);
    return false;
  }
}

/**
 * Gère les réponses de Python
 */
function handlePythonResponse(response) {
  console.log('📨 Réponse Python:', response);
  
  if (response.action === 'download_complete') {
    // Python a terminé le téléchargement
    console.log('✅ Téléchargement terminé:', response.filename);
    
    // Notifier tous les onglets YouTube Music
    chrome.tabs.query({ url: '*://music.youtube.com/*' }, (tabs) => {
      tabs.forEach(tab => {
        chrome.tabs.sendMessage(tab.id, {
          action: 'download_complete',
          data: {
            success: response.success,
            filename: response.filename,
            path: response.path
          }
        });
      });
    });
    
  } else if (response.success) {
    console.log('✅ Python a préparé le dossier:', response.path);
    
    // Notifier le content script pour continuer l'auto-clicker
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.tabs.sendMessage(tabs[0].id, {
          action: 'python_ready',
          data: response
        });
      }
    });
    
  } else {
    console.error('❌ Erreur Python:', response.error);
  }
}

/**
 * Écoute les messages du content script
 */
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('📨 [Background] Message reçu:', message.action);
  
  // Ouvrir un nouvel onglet (pour Y2Mate)
  if (message.action === 'openTab') {
    console.log('🌐 [Background] Ouverture d\'un nouvel onglet:', message.url);
    
    chrome.tabs.create({
      url: message.url,
      active: false  // Ouvrir en arrière-plan
    }, (tab) => {
      console.log('✅ [Background] Onglet ouvert:', tab.id);
      sendResponse({ success: true, tabId: tab.id });
    });
    
    return true; // Garder le canal ouvert pour sendResponse asynchrone
  }
  
  // Fermer l'onglet actuel (après téléchargement Y2Mate)
  if (message.action === 'closeCurrentTab') {
    console.log('🔒 [Background] Fermeture de l\'onglet:', sender.tab?.id);
    
    if (sender.tab && sender.tab.id) {
      chrome.tabs.remove(sender.tab.id, () => {
        console.log('✅ [Background] Onglet fermé');
        sendResponse({ success: true });
      });
    }
    
    return true;
  }
  
  // Envoyer à Flask via HTTP
  if (message.action === 'send_to_flask') {
    console.log('📤 [Background] Envoi à Flask...');
    console.log('📦 [Background] Données:', message.data);
    
    // Faire la requête HTTP depuis le background (pas de CORS)
    fetch('http://localhost:5000/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(message.data)
    })
    .then(response => response.json())
    .then(data => {
      console.log('✅ [Background] Réponse Flask:', data);
      sendResponse(data);
    })
    .catch(error => {
      console.error('❌ [Background] Erreur Flask:', error);
      sendResponse({ 
        success: false, 
        error: 'Serveur Python non accessible. Lancez: python app.py' 
      });
    });
    
    return true; // Garder le canal ouvert pour sendResponse asynchrone
  }
  
  return true;
});

/**
 * Test de connexion au clic sur l'icône
 */
chrome.action.onClicked.addListener(() => {
  if (!isConnected) {
    console.log('🔄 Tentative de reconnexion...');
    connectToNativeHost();
  } else {
    console.log('✅ Déjà connecté au host Python');
  }
});

// Native Messaging désactivé - On utilise Flask HTTP
// connectToNativeHost();

console.log('🎵 GrabSong background.js chargé (Flask HTTP mode)');
