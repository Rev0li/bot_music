// modules/page-opener.js - Ouvrir une nouvelle page et remplir les données

/**
 * Sauvegarder les données dans chrome.storage pour les passer à la nouvelle page
 * @param {Object} songData - Données de la chanson
 */
async function saveSongDataToStorage(songData) {
  return new Promise((resolve) => {
    chrome.storage.local.set({ pendingSongData: songData }, () => {
      log('💾', 'Data saved to storage:', songData);
      resolve();
    });
  });
}

/**
 * Ouvrir une nouvelle page avec les données
 * @param {Object} songData - Données de la chanson
 */
async function openTargetPageWithData(songData) {
  log('🌐', 'Opening target page...');
  
  // Sauvegarder les données
  await saveSongDataToStorage(songData);
  
  // Ouvrir la nouvelle page
  chrome.runtime.sendMessage({
    action: 'openTab',
    url: CONFIG.targetPage.url,
    data: songData
  });
  
  showNotification('✅ Page ouverte avec les données!');
}

/**
 * Workflow Y2Mate - Automatiser tout le processus
 */
async function fillTargetPageFields() {
  log('📝', 'Starting Y2Mate workflow...');
  
  // Récupérer les données depuis le storage
  const data = await new Promise((resolve) => {
    chrome.storage.local.get(['pendingSongData'], (result) => {
      resolve(result.pendingSongData || null);
    });
  });
  
  if (!data) {
    log('❌', 'No data found in storage');
    return;
  }
  
  log('📦', 'Data retrieved:', data);
  
  try {
    // STEP 1: Paste YouTube link
    await pasteYouTubeLink(data.link);
    
    // STEP 2: Select MP3 format if needed
    await selectMP3Format();
    
    // STEP 3: Click Convert button
    await clickConvertButton();
    
    // STEP 4: Wait for conversion to complete
    await waitForConversion();
    
    // STEP 5: Click Download button
    await clickDownloadButton();
    
    // Nettoyer le storage
    chrome.storage.local.remove(['pendingSongData']);
    
    showNotification('✅ Download started!');
    log('🎉', 'Y2Mate workflow complete!');
    
  } catch (error) {
    log('❌', 'Error in Y2Mate workflow:', error);
    showNotification('❌ Error: ' + error.message, 'error');
  }
}

/**
 * STEP 1: Coller le lien YouTube
 */
async function pasteYouTubeLink(link) {
  log('🔗', 'Step 1: Pasting YouTube link...');
  
  await wait(2000); // Wait longer for page to load
  
  // Debug: Log all inputs on the page
  const allInputs = document.querySelectorAll('input, textarea');
  log('📋', `Found ${allInputs.length} input/textarea elements on page`);
  allInputs.forEach((input, index) => {
    log('🔍', `Input ${index}: type="${input.type}", placeholder="${input.placeholder}", id="${input.id}", class="${input.className}"`);
  });
  
  // Try multiple selectors
  const selectors = [
    'input[type="text"]',
    'input[placeholder*="YouTube"]',
    'input[placeholder*="youtube"]',
    'input[placeholder*="video"]',
    'input[placeholder*="URL"]',
    'input[placeholder*="url"]',
    'input.form-control',
    'input#url',
    'input#search',
    'textarea'
  ];
  
  let linkInput = null;
  for (const selector of selectors) {
    linkInput = document.querySelector(selector);
    if (linkInput) {
      log('✅', `Found input with selector: ${selector}`);
      break;
    }
  }
  
  if (!linkInput) {
    // Last resort: find first visible input
    log('⚠️', 'Trying to find first visible input...');
    for (const input of allInputs) {
      const isVisible = input.offsetParent !== null && 
                       input.type !== 'hidden' &&
                       window.getComputedStyle(input).display !== 'none';
      if (isVisible) {
        linkInput = input;
        log('✅', 'Found first visible input');
        break;
      }
    }
  }
  
  if (!linkInput) {
    log('❌', 'No input found. Available inputs:', allInputs);
    throw new Error('Link input not found - check console for available inputs');
  }
  
  // Paste the link
  log('📝', 'Pasting link into input...');
  linkInput.focus();
  linkInput.value = link;
  
  // Trigger multiple events to ensure the page detects the change
  linkInput.dispatchEvent(new Event('input', { bubbles: true }));
  linkInput.dispatchEvent(new Event('change', { bubbles: true }));
  linkInput.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
  linkInput.dispatchEvent(new Event('paste', { bubbles: true }));
  
  log('✅', 'Link pasted:', link);
  log('📊', 'Input value after paste:', linkInput.value);
  
  await wait(1500);
}

/**
 * STEP 2: Sélectionner le format MP3 (seulement si MP4 est sélectionné)
 */
async function selectMP3Format() {
  log('🎵', 'Step 2: Checking format...');
  
  await wait(1000);
  
  // Chercher le bouton MP4 pour voir s'il est sélectionné
  const mp4Button = findButtonByText('MP4');
  
  if (mp4Button) {
    const mp4IsSelected = mp4Button.classList.contains('active') || 
                          mp4Button.classList.contains('selected') ||
                          mp4Button.getAttribute('aria-selected') === 'true';
    
    if (mp4IsSelected) {
      log('⚠️', 'MP4 is selected, switching to MP3...');
      
      // Chercher et cliquer sur MP3
      const mp3Button = findButtonByText('MP3');
      if (mp3Button) {
        safeClick(mp3Button, 'MP3 button');
        log('✅', 'Switched to MP3');
        await wait(500);
      } else {
        log('❌', 'MP3 button not found');
      }
    } else {
      log('✅', 'MP4 not selected, no need to change');
    }
  } else {
    log('ℹ️', 'MP4 button not found, assuming MP3 is default');
  }
}

/**
 * STEP 3: Cliquer sur Convert
 */
async function clickConvertButton() {
  log('⚙️', 'Step 3: Clicking Convert button...');
  
  await wait(500);
  
  const convertButton = findButtonByText('Convert');
  if (!convertButton) {
    throw new Error('Convert button not found');
  }
  
  safeClick(convertButton, 'Convert button');
  log('✅', 'Convert button clicked');
  
  await wait(1000);
}

/**
 * STEP 4: Attendre la fin de la conversion
 */
async function waitForConversion() {
  log('⏳', 'Step 4: Waiting for conversion...');
  
  // Attendre que le div #progress apparaisse
  const progressDiv = await findElementWithRetry('#progress', 30, 1000);
  
  if (progressDiv) {
    log('🔄', 'Conversion in progress...');
    
    // Attendre que le div disparaisse ou change
    let attempts = 0;
    const maxAttempts = 60; // 60 secondes max
    
    while (attempts < maxAttempts) {
      await wait(1000);
      
      const stillConverting = document.querySelector('#progress');
      if (!stillConverting || stillConverting.style.display === 'none') {
        log('✅', 'Conversion complete!');
        break;
      }
      
      attempts++;
      if (attempts % 5 === 0) {
        log('⏳', `Still converting... (${attempts}s)`);
      }
    }
    
    if (attempts >= maxAttempts) {
      throw new Error('Conversion timeout');
    }
  }
  
  await wait(2000); // Attendre un peu plus pour être sûr
}

/**
 * STEP 5: Cliquer sur Download
 */
async function clickDownloadButton() {
  log('⬇️', 'Step 5: Clicking Download button...');
  
  // Récupérer le filename depuis le storage (déjà créé sur YouTube Music)
  const data = await new Promise((resolve) => {
    chrome.storage.local.get(['pendingSongData'], (result) => {
      resolve(result.pendingSongData || null);
    });
  });
  
  const filename = data?.filename || 'download.mp3';
  log('📝', 'Using filename:', filename);
  
  // Chercher le bouton Download
  const downloadButton = findButtonByText('Download');
  
  if (!downloadButton) {
    throw new Error('Download button not found');
  }
  
  // Vérifier si c'est un lien <a> avec download attribute
  if (downloadButton.tagName === 'A' && downloadButton.hasAttribute('href')) {
    // Modifier l'attribut download pour suggérer le nom de fichier
    downloadButton.setAttribute('download', filename);
    log('✅', 'Download attribute set to:', filename);
  }
  
  safeClick(downloadButton, 'Download button');
  log('✅', 'Download button clicked!');
  
  // Attendre un peu pour que le téléchargement commence
  await wait(2000);
  
  // Fermer l'onglet Y2Mate
  log('🔒', 'Closing Y2Mate tab...');
  
  // Envoyer un message au background pour fermer l'onglet
  chrome.runtime.sendMessage({
    action: 'closeCurrentTab'
  });
}
