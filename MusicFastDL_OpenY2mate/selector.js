// selector.js - Content script for interactive element selection with floating button

(function() {
    let selecting = false;
    let lastElement = null;
    const HIGHLIGHT_STYLE = 'outline: 2px solid #ff0000 !important; background: rgba(255,0,0,0.05) !important;';
    const SERVER_URL = 'http://127.0.0.1:5000/command';
    const SECRET_TOKEN = 'changeme123'; // Must match your Python app

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
})(); 