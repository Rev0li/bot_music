// background.js - Service worker pour gérer l'ouverture de tabs

// Écouter les messages pour ouvrir des tabs
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'openTab') {
    // Ouvrir un nouvel onglet EN ARRIÈRE-PLAN
    chrome.tabs.create({
      url: request.url,
      active: false  // ✅ NE PAS mettre le focus (reste en arrière-plan)
    }, (tab) => {
      console.log('✅ New tab opened in background:', tab.id);
      sendResponse({ success: true, tabId: tab.id });
    });
    
    return true;  // Indique que la réponse sera asynchrone
  }
  
  if (request.action === 'closeCurrentTab') {
    // Fermer l'onglet qui a envoyé le message
    if (sender.tab && sender.tab.id) {
      chrome.tabs.remove(sender.tab.id, () => {
        console.log('✅ Tab closed:', sender.tab.id);
        sendResponse({ success: true });
      });
    }
    
    return true;
  }
});

console.log('🚀 Background service worker loaded');
