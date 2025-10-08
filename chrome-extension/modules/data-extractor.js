// modules/data-extractor.js - Extraire les informations de la chanson

/**
 * Extraire toutes les informations de la chanson actuellement jouée
 * @returns {Promise<Object>} - Objet contenant les infos de la chanson
 */
async function extractSongData() {
  log('🎵', 'Extracting song data...');
  
  const songData = {
    title: '',
    artist: '',
    album: '',
    year: '',
    link: '',
    timestamp: Date.now(),
  };

  // Extraire le titre
  songData.title = safeGetText(CONFIG.selectors.ytMusic.songTitle);
  log('📝', 'Title:', songData.title);

  // Extraire l'artiste, album et année depuis le byline
  // Structure: "The Killers • Hot Fuss • 2004"
  const bylineElement = document.querySelector('ytmusic-player-bar .byline.complex-string');
  if (bylineElement) {
    // Récupérer tous les liens <a> (artiste et album)
    const links = bylineElement.querySelectorAll('a');
    
    // Premier lien = Artiste
    if (links[0]) {
      songData.artist = links[0].textContent.trim();
      log('🎤', 'Artist:', songData.artist);
    }
    
    // Deuxième lien = Album
    if (links[1]) {
      songData.album = links[1].textContent.trim();
      log('💿', 'Album:', songData.album);
    }
    
    // Année (dernier <span> sans lien)
    const spans = bylineElement.querySelectorAll('span[dir="auto"]');
    for (let span of spans) {
      const text = span.textContent.trim();
      // Vérifier si c'est une année (4 chiffres)
      if (/^\d{4}$/.test(text)) {
        songData.year = text;
        log('📅', 'Year:', songData.year);
        break;
      }
    }
  } else {
    log('⚠️', 'Byline element not found, trying fallback...');
    // Fallback: essayer l'ancienne méthode
    const artistElement = document.querySelector(CONFIG.selectors.ytMusic.artistName);
    if (artistElement) {
      const artistLink = artistElement.querySelector('a');
      songData.artist = artistLink ? artistLink.textContent.trim() : artistElement.textContent.trim();
      log('🎤', 'Artist (fallback):', songData.artist);
    }
  }

  return songData;
}

/**
 * Obtenir le lien de partage en cliquant sur le bouton copier
 * @returns {Promise<string>} - Lien de la chanson
 */
async function getShareLink() {
  log('🔗', 'Getting share link...');
  
  // Sauvegarder le contenu actuel du clipboard
  const previousClipboard = await readFromClipboard();
  
  // Cliquer sur le menu
  const menuButton = await findElementWithRetry(CONFIG.selectors.ytMusic.menuButton);
  if (!menuButton) {
    log('❌', 'Menu button not found');
    return '';
  }
  
  safeClick(menuButton, 'menu button');
  await wait(CONFIG.delays.menuOpen);

  // Trouver et cliquer sur "Partager"
  const menuItems = document.querySelectorAll(CONFIG.selectors.ytMusic.menuItems);
  let shareClicked = false;
  
  for (let item of menuItems) {
    if (item.textContent.includes('Partager')) {
      const shareLink = item.querySelector(CONFIG.selectors.ytMusic.shareLink);
      if (shareLink) {
        safeClick(shareLink, 'share button');
        shareClicked = true;
        break;
      }
    }
  }

  if (!shareClicked) {
    log('❌', 'Share button not found');
    return '';
  }

  await wait(CONFIG.delays.shareDialog);

  // Cliquer sur le bouton "Copier"
  const copyButton = findButtonByText('Copier') || findButtonByText('Copy');
  if (!copyButton) {
    log('❌', 'Copy button not found');
    return '';
  }

  safeClick(copyButton, 'copy button');
  await wait(CONFIG.delays.copyAction);

  // Lire le lien depuis le clipboard
  const shareLink = await readFromClipboard();
  
  // Fermer le dialog (appuyer sur Escape)
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
  
  log('✅', 'Share link obtained:', shareLink);
  return shareLink;
}

/**
 * Extraire toutes les données (infos + lien)
 * @returns {Promise<Object>}
 */
async function extractAllData() {
  log('🚀', 'Starting full data extraction...');
  
  // Extraire les infos de base
  const songData = await extractSongData();
  
  // Obtenir le lien de partage
  songData.link = await getShareLink();
  
  log('✅', 'Data extraction complete:', songData);
  
  return songData;
}
