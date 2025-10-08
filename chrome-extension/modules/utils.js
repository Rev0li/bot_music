// modules/utils.js - Fonctions utilitaires réutilisables

/**
 * Attendre un certain temps (version Promise de setTimeout)
 * @param {number} ms - Millisecondes à attendre
 * @returns {Promise}
 */
function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Logger avec emoji (seulement si debug est activé)
 * @param {string} emoji - Emoji à afficher
 * @param {string} message - Message à logger
 * @param {any} data - Données optionnelles à logger
 */
function log(emoji, message, data = null) {
  if (CONFIG.debug) {
    if (data) {
      console.log(`${emoji} ${message}`, data);
    } else {
      console.log(`${emoji} ${message}`);
    }
  }
}

/**
 * Trouver un élément avec retry (réessayer plusieurs fois)
 * @param {string} selector - Sélecteur CSS
 * @param {number} maxAttempts - Nombre maximum de tentatives
 * @param {number} delayMs - Délai entre chaque tentative
 * @returns {Promise<Element|null>}
 */
async function findElementWithRetry(selector, maxAttempts = 5, delayMs = 500) {
  for (let i = 0; i < maxAttempts; i++) {
    const element = document.querySelector(selector);
    if (element) {
      log('✅', `Element found: ${selector}`);
      return element;
    }
    log('🔄', `Attempt ${i + 1}/${maxAttempts} - Element not found: ${selector}`);
    await wait(delayMs);
  }
  log('❌', `Element not found after ${maxAttempts} attempts: ${selector}`);
  return null;
}

/**
 * Cliquer sur un élément de manière sûre
 * @param {Element} element - Élément à cliquer
 * @param {string} description - Description de l'action
 * @returns {boolean} - True si le clic a réussi
 */
function safeClick(element, description = 'element') {
  if (!element) {
    log('❌', `Cannot click ${description}: element is null`);
    return false;
  }
  
  try {
    element.click();
    log('🎯', `Clicked: ${description}`);
    return true;
  } catch (error) {
    log('❌', `Error clicking ${description}:`, error);
    return false;
  }
}

/**
 * Trouver un bouton par son texte
 * @param {string} text - Texte à chercher
 * @param {string} tag - Tag HTML (par défaut 'button')
 * @returns {Element|null}
 */
function findButtonByText(text, tag = 'button') {
  const elements = document.querySelectorAll(tag);
  for (let element of elements) {
    if (element.textContent.includes(text)) {
      return element;
    }
  }
  return null;
}

/**
 * Extraire le texte d'un élément de manière sûre
 * @param {string} selector - Sélecteur CSS
 * @returns {string} - Texte extrait ou chaîne vide
 */
function safeGetText(selector) {
  const element = document.querySelector(selector);
  if (element) {
    return element.textContent.trim();
  }
  return '';
}

/**
 * Afficher une notification temporaire
 * @param {string} message - Message à afficher
 * @param {string} type - Type de notification (success, error, warning)
 */
function showNotification(message, type = 'success') {
  const notification = document.createElement('div');
  notification.className = `auto-click-notification ${type}`;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, CONFIG.ui.notificationDuration);
}

/**
 * Copier du texte dans le presse-papiers
 * @param {string} text - Texte à copier
 * @returns {Promise<boolean>}
 */
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    log('📋', 'Copied to clipboard:', text);
    return true;
  } catch (error) {
    log('❌', 'Failed to copy to clipboard:', error);
    return false;
  }
}

/**
 * Lire le contenu du presse-papiers
 * @returns {Promise<string>}
 */
async function readFromClipboard() {
  try {
    const text = await navigator.clipboard.readText();
    log('📋', 'Read from clipboard:', text);
    return text;
  } catch (error) {
    log('❌', 'Failed to read from clipboard:', error);
    return '';
  }
}
