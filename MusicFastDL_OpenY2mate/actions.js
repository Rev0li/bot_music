// actions.js - Module central pour exécuter des actions sur la page

(function() {
    // Utilitaire pour attendre
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Clic sur un élément par sélecteur CSS
    async function clickSelector(selector) {
        const el = document.querySelector(selector);
        if (el) {
            el.click();
            return { success: true };
        } else {
            return { success: false, error: 'Element not found: ' + selector };
        }
    }

    // Exécute une séquence d'actions
    async function runActions(actions) {
        for (const action of actions) {
            if (action.type === 'click') {
                const res = await clickSelector(action.selector);
                if (!res.success) return res;
            } else if (action.type === 'sleep') {
                await sleep(action.duration);
            } else if (action.type === 'extension') {
                // Action personnalisée, à adapter selon besoin
                chrome.runtime.sendMessage({ action: action.action, ...action.params });
                await sleep(200); // Petite pause pour laisser le temps à l'extension
            }
        }
        return { success: true };
    }

    // Listener pour recevoir des commandes du background ou d'autres scripts
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === 'runActions' && Array.isArray(request.actions)) {
            runActions(request.actions).then(res => sendResponse(res));
            return true; // Garde le canal ouvert pour la réponse async
        }
        if (request.action === 'clickSelector' && request.selector) {
            clickSelector(request.selector).then(res => sendResponse(res));
            return true;
        }
        if (request.action === 'sleep' && request.duration) {
            sleep(request.duration).then(() => sendResponse({ success: true }));
            return true;
        }
        // Ajoute ici d'autres actions personnalisées si besoin
    });

    // Expose les fonctions pour debug (optionnel)
    window._actions = { clickSelector, sleep, runActions };
})(); 