// selector.js - Content script for interactive element selection with floating button

(function() {
    let selecting = false;
    let lastElement = null;
    const HIGHLIGHT_STYLE = 'outline: 2px solid #ff0000 !important; background: rgba(255,0,0,0.05) !important;';
    const SERVER_URL = 'http://127.0.0.1:5000/command';
    const SECRET_TOKEN = 'changeme123'; // Must match your Python app
    let selectedFields = { artiste: null, album: null, song: null };
    let selectedSelectors = { artiste: null, album: null, song: null };

    // --- Floating Button Logic ---
    function injectFloatingButton() {
        if (document.getElementById('selector-floating-btn')) return;
        const btn = document.createElement('button');
        btn.id = 'selector-floating-btn';
        btn.innerText = 'Select Component';
        btn.style.position = 'fixed';
        btn.style.top = '20px';
        btn.style.right = '20px';
        btn.style.zIndex = 999999;
        btn.style.background = '#c00000';
        btn.style.color = 'white';
        btn.style.border = 'none';
        btn.style.padding = '8px 14px';
        btn.style.borderRadius = '6px';
        btn.style.cursor = 'pointer';
        btn.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
        btn.title = 'Click to select a component on the page';
        btn.onclick = () => {
            startSelecting();
        };
        // Add close button
        const closeBtn = document.createElement('span');
        closeBtn.innerText = '×';
        closeBtn.style.marginLeft = '10px';
        closeBtn.style.cursor = 'pointer';
        closeBtn.onclick = (e) => {
            e.stopPropagation();
            btn.remove();
        };
        btn.appendChild(closeBtn);
        document.body.appendChild(btn);

        // --- Nouveau bouton pour déclencher Save As ---
        if (!document.getElementById('trigger-save-btn')) {
            const saveBtn = document.createElement('button');
            saveBtn.id = 'trigger-save-btn';
            saveBtn.innerText = 'Déclencher Save As';
            saveBtn.style.position = 'fixed';
            saveBtn.style.top = '60px';
            saveBtn.style.right = '20px';
            saveBtn.style.zIndex = 999999;
            saveBtn.style.background = '#0077c0';
            saveBtn.style.color = 'white';
            saveBtn.style.border = 'none';
            saveBtn.style.padding = '8px 14px';
            saveBtn.style.borderRadius = '6px';
            saveBtn.style.cursor = 'pointer';
            saveBtn.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
            saveBtn.title = 'Déclencher la détection Save As côté Python';
            saveBtn.onclick = () => {
                fetch('http://127.0.0.1:5000/command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        token: 'changeme123',
                        cmd: 'trigger_save',
                        value: null
                    })
                });
            };
            document.body.appendChild(saveBtn);
        }
    }

    function highlightElement(el) {
        if (el) {
            el.setAttribute('data-selector-highlight', '1');
            el.setAttribute('style', (el.getAttribute('style') || '') + HIGHLIGHT_STYLE);
        }
    }
    function unhighlightElement(el) {
        if (el && el.hasAttribute('data-selector-highlight')) {
            el.setAttribute('style', (el.getAttribute('style') || '').replace(HIGHLIGHT_STYLE, ''));
            el.removeAttribute('data-selector-highlight');
        }
    }
    function getUniqueSelector(el) {
        if (!el) return '';
        if (el.id) return '#' + el.id;
        let path = [];
        while (el && el.nodeType === 1 && path.length < 5) {
            let selector = el.nodeName.toLowerCase();
            if (el.className) selector += '.' + el.className.trim().replace(/\s+/g, '.');
            path.unshift(selector);
            el = el.parentElement;
        }
        return path.join(' > ');
    }
    function onMouseOver(e) {
        if (!selecting) return;
        if (lastElement) unhighlightElement(lastElement);
        lastElement = e.target;
        highlightElement(lastElement);
        e.stopPropagation();
    }
    function onMouseOut(e) {
        if (!selecting) return;
        unhighlightElement(e.target);
        e.stopPropagation();
    }
    function onClick(e) {
        if (!selecting) return;
        e.preventDefault();
        e.stopPropagation();
        selecting = false;
        unhighlightElement(e.target);
        document.body.style.cursor = '';
        document.removeEventListener('mouseover', onMouseOver, true);
        document.removeEventListener('mouseout', onMouseOut, true);
        document.removeEventListener('click', onClick, true);
        const selector = getUniqueSelector(e.target);
        const info = {
            selector,
            text: e.target.innerText,
            tag: e.target.tagName,
            href: e.target.href || null
        };
        // Send to Python app
        fetch(SERVER_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                token: SECRET_TOKEN,
                cmd: 'select_component',
                value: info
            })
        });
    }
    function startSelecting() {
        if (selecting) return;
        selecting = true;
        document.body.style.cursor = 'crosshair';
        document.addEventListener('mouseover', onMouseOver, true);
        document.addEventListener('mouseout', onMouseOut, true);
        document.addEventListener('click', onClick, true);
    }
    // Listen for a message from the extension to start selecting
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === 'start_select_component') {
            startSelecting();
            sendResponse({ started: true });
        }
    });

    // Inject the floating button on every page load
    injectFloatingButton();

    function injectMusicInfoButtons() {
        if (document.getElementById('music-info-btns')) return;
        const container = document.createElement('div');
        container.id = 'music-info-btns';
        container.style.position = 'fixed';
        container.style.top = '110px';
        container.style.right = '20px';
        container.style.zIndex = 999999;
        container.style.background = '#fff';
        container.style.border = '1px solid #ccc';
        container.style.padding = '8px';
        container.style.borderRadius = '6px';
        container.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
        container.style.display = 'flex';
        container.style.flexDirection = 'column';
        container.style.gap = '6px';

        ['artiste', 'album', 'song'].forEach(field => {
            const btn = document.createElement('button');
            btn.innerText = 'Sélectionner ' + field;
            btn.style.marginBottom = '4px';
            btn.onclick = () => {
                startSelectingField(field);
            };
            container.appendChild(btn);
        });

        // Affichage des sélecteurs choisis
        const selectorsDiv = document.createElement('div');
        selectorsDiv.id = 'music-info-selectors';
        selectorsDiv.style.fontSize = '12px';
        selectorsDiv.style.marginTop = '8px';
        selectorsDiv.style.background = '#f7f7f7';
        selectorsDiv.style.padding = '4px';
        selectorsDiv.style.borderRadius = '4px';
        function updateSelectorsDisplay() {
            selectorsDiv.innerHTML =
                '<b>Sélecteurs choisis :</b><br>' +
                'Artiste : <span style="color:#0077c0">' + (selectedSelectors.artiste || '-') + '</span><br>' +
                'Album : <span style="color:#0077c0">' + (selectedSelectors.album || '-') + '</span><br>' +
                'Song : <span style="color:#0077c0">' + (selectedSelectors.song || '-') + '</span>';
        }
        updateSelectorsDisplay();
        container.appendChild(selectorsDiv);

        const sendBtn = document.createElement('button');
        sendBtn.innerText = 'Envoyer infos musique';
        sendBtn.style.background = '#0077c0';
        sendBtn.style.color = 'white';
        sendBtn.style.border = 'none';
        sendBtn.style.padding = '8px 14px';
        sendBtn.style.borderRadius = '6px';
        sendBtn.style.cursor = 'pointer';
        sendBtn.onclick = () => {
            // Récupère le texte à partir des sélecteurs
            const artiste = selectedSelectors.artiste ? (document.querySelector(selectedSelectors.artiste)?.innerText || '') : '';
            const album = selectedSelectors.album ? (document.querySelector(selectedSelectors.album)?.innerText || '') : '';
            const song = selectedSelectors.song ? (document.querySelector(selectedSelectors.song)?.innerText || '') : '';
            const payload = {
                event: 'lastDl',
                base_path: 'Music/bot/test/',
                artiste,
                album,
                song
            };
            console.log('[MusicFastDL] Envoi infos musique à Python:', payload);
            fetch('http://127.0.0.1:5000/event', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            }).then(() => {
                console.log('[MusicFastDL] Infos musique envoyées à Python:', { artiste, album, song });
            });
        };
        container.appendChild(sendBtn);
        document.body.appendChild(container);
        // Met à jour l'affichage à chaque sélection
        window._updateMusicSelectors = updateSelectorsDisplay;
    }

    function startSelectingField(field) {
        let selecting = true;
        let lastElement = null;
        const HIGHLIGHT_STYLE = 'outline: 2px solid #00c000 !important; background: rgba(0,255,0,0.05) !important;';
        function highlightElement(el) {
            if (el) {
                el.setAttribute('data-selector-highlight', '1');
                el.setAttribute('style', (el.getAttribute('style') || '') + HIGHLIGHT_STYLE);
            }
        }
        function unhighlightElement(el) {
            if (el && el.hasAttribute('data-selector-highlight')) {
                el.setAttribute('style', (el.getAttribute('style') || '').replace(HIGHLIGHT_STYLE, ''));
                el.removeAttribute('data-selector-highlight');
            }
        }
        function getUniqueSelector(el) {
            if (!el) return '';
            if (el.id) return '#' + el.id;
            let path = [];
            while (el && el.nodeType === 1 && path.length < 5) {
                let selector = el.nodeName.toLowerCase();
                if (el.className) selector += '.' + el.className.trim().replace(/\s+/g, '.');
                path.unshift(selector);
                el = el.parentElement;
            }
            return path.join(' > ');
        }
        function onMouseOver(e) {
            if (!selecting) return;
            if (lastElement) unhighlightElement(lastElement);
            lastElement = e.target;
            highlightElement(lastElement);
            e.stopPropagation();
        }
        function onMouseOut(e) {
            if (!selecting) return;
            unhighlightElement(e.target);
            e.stopPropagation();
        }
        function onClick(e) {
            if (!selecting) return;
            e.preventDefault();
            e.stopPropagation();
            selecting = false;
            unhighlightElement(e.target);
            document.body.style.cursor = '';
            document.removeEventListener('mouseover', onMouseOver, true);
            document.removeEventListener('mouseout', onMouseOut, true);
            document.removeEventListener('click', onClick, true);
            const selector = getUniqueSelector(e.target);
            selectedSelectors[field] = selector;
            selectedFields[field] = e.target.innerText;
            alert('Sélecteur pour ' + field + ' enregistré : ' + selector + '\nTexte : ' + e.target.innerText);
            console.log('[MusicFastDL] Sélecteur ' + field + ' =', selector);
            if (window._updateMusicSelectors) window._updateMusicSelectors();
        }
        document.body.style.cursor = 'crosshair';
        document.addEventListener('mouseover', onMouseOver, true);
        document.addEventListener('mouseout', onMouseOut, true);
        document.addEventListener('click', onClick, true);
    }

    injectMusicInfoButtons();
})(); 