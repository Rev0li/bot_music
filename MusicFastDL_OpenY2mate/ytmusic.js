(function() {
    'use strict';
    const wait = ms => new Promise(r => setTimeout(r, ms));
    const log = (...args) => console.log('[MusicFastDL]', ...args);

    async function waitForElementByClass(className, timeout = 10000) {
        return new Promise((resolve, reject) => {
            const start = Date.now();
            const interval = setInterval(() => {
                const elements = document.getElementsByClassName(className);
                if (elements.length > 0) {
                    clearInterval(interval);
                    resolve(elements[0]);
                }
                if (Date.now() - start > timeout) {
                    clearInterval(interval);
                    reject('Timeout: ' + className);
                }
            }, 300);
        });
    }

    async function injectButton() {
        try {
            const refNode = await waitForElementByClass('menu style-scope ytmusic-player-bar');
            if (!refNode || document.querySelector('#fastdl-button')) return;

            const btn = document.createElement('button');
            btn.id = 'fastdl-button';
            btn.innerText = '🎵 DL';
            btn.style.cssText = 'margin-left: 4px; padding: 4px 8px; border-radius: 5px; background: #c00000; color: white; border: none; cursor: pointer; font-weight: bold;';
            btn.title = 'Télécharger automatiquement';

            btn.onclick = async () => {
                log('DL bouton activé');

                const actionBtn = refNode.querySelector('button');
                if (actionBtn) actionBtn.click();
                await wait(500);

                const shareBtn = [...document.querySelectorAll('ytmusic-menu-navigation-item-renderer')]
                    .find(el => el.innerText.toLowerCase().includes('partager'));
                if (shareBtn) shareBtn.click();
                await wait(500);
                const copyBtn = [...document.querySelectorAll('button')].find(b => b.innerText.toLowerCase().includes('copier'));
                if (copyBtn) copyBtn.click();
                log('✅ Lien copié dans presse-papiers');
                
                chrome.runtime.sendMessage({ action: "switchToY2mate" }, (res) => {
                console.log("[YTMusic] Onglet Y2mate lancé, tabId:", res.tabId);
                });
                // chrome.runtime.sendMessage({ action: "runY2mateInBackground" }, (res) => {
                // console.log("[YTMusic] Onglet Y2mate lancé, tabId:", res.tabId);
                // });
            };

            refNode.parentNode.insertBefore(btn, refNode.nextSibling);
            log('✔️ Bouton injecté');
        } catch (e) {
            log('Erreur injection bouton', e);
        }
    }

    const observer = new MutationObserver(() => injectButton());
    observer.observe(document.body, { childList: true, subtree: true });
})();