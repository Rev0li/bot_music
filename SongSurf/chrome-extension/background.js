/**
 * background-simple.js - Service Worker simplifié pour SongSurf
 * 
 * Plus besoin de gérer les messages complexes, tout passe par fetch direct
 */

console.log('🎵 [SongSurf] Background service worker chargé');

// Écouter l'installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('✅ SongSurf extension installée');
});

// Optionnel : Écouter les messages si besoin
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('📨 Message reçu:', request);
  
  // Répondre immédiatement pour éviter les timeouts
  sendResponse({ received: true });
  
  return true; // Garder le canal ouvert pour les réponses asynchrones
});
