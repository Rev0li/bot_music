// popup.js - Script pour la popup de l'extension

document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('startAutoClick');
    
    startButton.addEventListener('click', function() {
        // Envoyer un message au content script pour démarrer l'auto-click
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'performClick'
            }, function(response) {
                if (response && response.success) {
                    // Fermer la popup après avoir envoyé le message
                    window.close();
                }
            });
        });
    });
});