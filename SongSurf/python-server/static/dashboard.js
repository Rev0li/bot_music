// Configuration
const API_BASE = 'http://localhost:5000';
const REFRESH_INTERVAL = 2000; // 2 secondes

let refreshTimer = null;
let recentDownloads = [];

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎵 Dashboard SongSurf initialisé');
    loadData();
    loadLibrary(); // Charger la bibliothèque musicale
    startAutoRefresh();
    startLibraryAutoRefresh(); // Auto-refresh de la bibliothèque
});

// Chargement des données
async function loadData() {
    try {
        // Charger les stats
        const statsResponse = await fetch(`${API_BASE}/stats`);
        const stats = await statsResponse.json();
        updateStats(stats);

        // Charger le statut
        const statusResponse = await fetch(`${API_BASE}/status`);
        const status = await statusResponse.json();
        updateStatus(status);

        // Mettre à jour le timestamp
        updateTimestamp();

    } catch (error) {
        console.error('❌ Erreur lors du chargement des données:', error);
        // Ne pas afficher "Hors ligne" si c'est juste une erreur JS
        // showError();
    }
}

// Mettre à jour les statistiques
function updateStats(stats) {
    document.getElementById('total-artists').textContent = stats.artists || 0;
    document.getElementById('total-albums').textContent = stats.albums || 0;
    document.getElementById('total-songs').textContent = stats.songs || 0;
}

// Mettre à jour le compteur de queue
function updateQueueCount(count) {
    document.getElementById('queue-count').textContent = count || 0;
}

// Variables pour l'organisateur
let libraryData = null;
let expandedItems = new Set();
let lastSongCount = 0; // Pour détecter les changements

// Charger la bibliothèque
async function loadLibrary() {
    try {
        const response = await fetch(`${API_BASE}/api/library`);
        const newData = await response.json();
        
        // Détecter si le nombre de chansons a changé
        const newSongCount = newData.songs ? newData.songs.length : 0;
        const hasChanged = lastSongCount > 0 && newSongCount !== lastSongCount;
        
        if (hasChanged) {
            console.log(`🔔 Bibliothèque mise à jour: ${lastSongCount} → ${newSongCount} chansons`);
            // Afficher une notification
            showNotification(`📥 ${newSongCount - lastSongCount > 0 ? 'Nouvelle' : 'Mise à jour'} chanson détectée !`);
        }
        
        lastSongCount = newSongCount;
        libraryData = newData;
        
        analyzeSuggestions(); // Analyser AVANT de rendre
        renderLibraryTree(); // Rendre APRÈS avoir analysé
    } catch (error) {
        console.error('❌ Erreur lors du chargement de la bibliothèque:', error);
    }
}

// Rendre l'arbre de la bibliothèque
function renderLibraryTree() {
    if (!libraryData || !libraryData.songs) return;
    
    if (viewMode === 'grid') {
        renderGridView();
    } else {
        renderListView();
    }
}

// Render Grid View (4 colonnes)
function renderGridView() {
    const container = document.getElementById('library-tree');
    
    // Grouper par artiste avec le premier album
    const artistsMap = new Map();
    libraryData.songs.forEach(song => {
        if (!artistsMap.has(song.artist)) {
            // Chercher la pochette dans différents champs possibles
            const albumArt = song.album_art || song.albumArt || song.cover || song.artwork || null;
            
            artistsMap.set(song.artist, {
                albums: new Set(),
                songCount: 0,
                firstAlbum: song.album,
                albumArt: albumArt,
                firstSong: song
            });
        }
        artistsMap.get(song.artist).albums.add(song.album);
        artistsMap.get(song.artist).songCount++;
    });
    
    let html = '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">';
    
    Array.from(artistsMap.entries()).sort().forEach(([artist, data]) => {
        const albumCount = data.albums.size;
        const songCount = data.songCount;
        const albumArt = data.albumArt;
        
        // Échapper les guillemets pour onclick
        const escapedArtist = artist.replace(/'/g, "\\'");
        
        html += `
            <div class="grid-card" onclick="openArtistModal('${escapedArtist}')" style="
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: var(--radius-md);
                padding: 0;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                overflow: hidden;
            ">
                <div style="
                    aspect-ratio: 1;
                    background: ${albumArt ? `url('${albumArt}') center/cover` : 'linear-gradient(135deg, rgba(138, 180, 248, 0.2) 0%, rgba(174, 203, 250, 0.1) 100%)'};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 56px;
                    overflow: hidden;
                    position: relative;
                ">
                    ${albumArt ? '' : '<span style="opacity: 0.6;">🎤</span>'}
                    <div style="
                        position: absolute;
                        inset: 0;
                        background: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.4) 100%);
                    "></div>
                </div>
                <div style="padding: 16px;">
                    <h3 style="
                        font-size: 15px;
                        font-weight: 600;
                        color: var(--text-primary);
                        margin: 0 0 6px 0;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        letter-spacing: -0.01em;
                    ">${artist}</h3>
                    <p style="
                        font-size: 13px;
                        color: var(--text-secondary);
                        margin: 0;
                        font-weight: 400;
                    ">
                        ${albumCount} album${albumCount > 1 ? 's' : ''} • ${songCount} chanson${songCount > 1 ? 's' : ''}
                    </p>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
    
    // Add hover effect
    container.querySelectorAll('.grid-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.background = 'var(--bg-hover)';
            card.style.borderColor = 'var(--border-hover)';
            card.style.transform = 'translateY(-6px)';
            card.style.boxShadow = 'var(--shadow-md)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.background = 'var(--bg-card)';
            card.style.borderColor = 'var(--border)';
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = 'none';
        });
    });
}
function openArtistModal(artist) {
    // Bloquer le scroll de la page principale
    document.body.style.overflow = 'hidden';
    
    // Créer la modale
    const modal = document.createElement('div');
    modal.id = 'artist-modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--bg-primary);
        z-index: 10000;
        overflow-y: auto;
        animation: fadeIn 0.3s ease;
    `;
    
    // Filtrer les chansons de cet artiste
    const artistSongs = libraryData.songs.filter(s => s.artist === artist);
    
    // Organiser par album
    const albums = {};
    artistSongs.forEach(song => {
        if (!albums[song.album]) {
            albums[song.album] = [];
        }
        albums[song.album].push(song);
    });
    
    // Compter le total de chansons
    const totalSongs = artistSongs.length;
    
    // Construire le HTML
    let html = `
        <div class="modal-container" style="max-width: 1400px; margin: 0 auto; padding: 48px 40px;">
            <!-- Header -->
            <div class="header" style="
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                margin-bottom: 48px;
                padding-bottom: 24px;
                border-bottom: 1px solid var(--border);
            ">
                <div>
                    <h1 style="
                        font-size: 36px; 
                        margin: 0 0 8px 0;
                        font-weight: 700;
                        letter-spacing: -0.02em;
                        background: linear-gradient(135deg, #f9fafb 0%, #a5b4fc 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                    ">🎤 ${artist}</h1>
                    <p style="
                        font-size: 15px;
                        color: var(--text-secondary);
                        margin: 0;
                    ">${Object.keys(albums).length} album${Object.keys(albums).length > 1 ? 's' : ''} • ${totalSongs} chanson${totalSongs > 1 ? 's' : ''}</p>
                </div>
                <button class="close-btn" onclick="closeArtistModal()" style="
                    width: 44px;
                    height: 44px;
                    background: var(--bg-card);
                    border: 1px solid var(--border);
                    border-radius: 50%;
                    color: var(--text-primary);
                    font-size: 20px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.2s;
                " onmouseover="this.style.background='var(--bg-hover)'; this.style.borderColor='var(--border-hover)'; this.style.transform='rotate(90deg)'" onmouseout="this.style.background='var(--bg-card)'; this.style.borderColor='var(--border)'; this.style.transform='rotate(0deg)'">
                    ✕
                </button>
            </div>
            
            <!-- Albums Grid (2 colonnes responsive) -->
            <div class="albums-grid" style="
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(520px, 1fr));
                gap: 32px;
            ">
    `;
    
    Object.keys(albums).sort().forEach(album => {
        const songs = albums[album];
        // Chercher la pochette dans différents champs possibles
        const albumArt = songs[0].album_art || songs[0].albumArt || songs[0].cover || songs[0].artwork || null;
        
        html += `
            <div class="album-card" style="
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                overflow: hidden;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
            " onmouseover="this.style.borderColor='var(--accent)'; this.style.boxShadow='0 20px 40px rgba(0, 0, 0, 0.5)'; this.style.transform='translateY(-4px)'" onmouseout="this.style.borderColor='var(--border)'; this.style.boxShadow='none'; this.style.transform='translateY(0)'">
                <!-- Pochette Album -->
                <div class="album-cover-container" style="
                    position: relative;
                    padding: 32px;
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 240px;
                ">
                    <div class="album-cover-wrapper" style="
                        position: relative;
                        width: 180px;
                        height: 180px;
                        border-radius: var(--radius-md);
                        overflow: hidden;
                        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                    " onmouseover="this.style.transform='scale(1.05) rotate(2deg)'" onmouseout="this.style.transform='scale(1) rotate(0deg)'">
                        ${albumArt ? `
                            <img src="${albumArt}" style="
                                width: 100%;
                                height: 100%;
                                object-fit: cover;
                            " onerror="this.parentElement.innerHTML='<div style=\\'width:100%;height:100%;background:linear-gradient(135deg,rgba(138,180,248,0.3) 0%,rgba(174,203,250,0.15) 100%);display:flex;align-items:center;justify-content:center;font-size:64px;position:relative\\'><span style=\\'opacity:0.5\\'>💿</span></div>'">
                        ` : `
                            <div class="album-placeholder" style="
                                width: 100%;
                                height: 100%;
                                background: linear-gradient(135deg, rgba(138, 180, 248, 0.3) 0%, rgba(174, 203, 250, 0.15) 100%);
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                font-size: 64px;
                                position: relative;
                            ">
                                <span style="opacity: 0.5;">💿</span>
                            </div>
                        `}
                    </div>
                </div>
                
                <!-- Info Album -->
                <div class="album-info" style="padding: 28px 32px;">
                    <div class="album-header" style="
                        display: flex;
                        justify-content: space-between;
                        align-items: start;
                        margin-bottom: 24px;
                        gap: 16px;
                    ">
                        <div>
                            <h2 class="album-title" style="
                                font-size: 22px; 
                                margin: 0 0 8px 0; 
                                font-weight: 700;
                                letter-spacing: -0.02em;
                                color: var(--text-primary);
                            ">${album}</h2>
                            <div class="album-meta" style="
                                display: flex;
                                align-items: center;
                                gap: 12px;
                                font-size: 13px;
                                color: var(--text-secondary);
                            ">
                                <span class="album-badge" style="
                                    background: rgba(99, 102, 241, 0.15);
                                    color: var(--accent);
                                    padding: 4px 12px;
                                    border-radius: 20px;
                                    font-weight: 600;
                                    font-size: 12px;
                                    white-space: nowrap;
                                ">${songs.length} chanson${songs.length > 1 ? 's' : ''}</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Chansons -->
                    <div class="songs-list" style="
                        display: flex;
                        flex-direction: column;
                        gap: 2px;
                    ">
        `;
        
        songs.forEach((song, index) => {
            html += `
                <div class="song-item" style="
                    display: flex;
                    align-items: center;
                    gap: 14px;
                    padding: 12px 10px;
                    background: transparent;
                    border-radius: var(--radius-sm);
                    transition: all 0.2s;
                    cursor: pointer;
                    position: relative;
                    overflow: hidden;
                " onmouseover="this.style.background='var(--bg-hover)'; this.style.paddingLeft='18px'; this.querySelector('.song-icon').style.opacity='1'; this.querySelector('.song-icon').style.transform='scale(1.1)'" onmouseout="this.style.background='transparent'; this.style.paddingLeft='10px'; this.querySelector('.song-icon').style.opacity='0.6'; this.querySelector('.song-icon').style.transform='scale(1)'">
                    <span class="song-number" style="
                        color: var(--text-muted); 
                        min-width: 28px; 
                        font-size: 13px;
                        font-weight: 600;
                        text-align: center;
                    ">${index + 1}</span>
                    <span class="song-icon" style="
                        font-size: 16px;
                        opacity: 0.6;
                        transition: all 0.2s;
                    ">🎵</span>
                    <span class="song-title" style="
                        flex: 1; 
                        white-space: nowrap; 
                        overflow: hidden; 
                        text-overflow: ellipsis;
                        color: var(--text-primary);
                        font-size: 14px;
                        font-weight: 500;
                    ">${song.title}</span>
                </div>
            `;
        });
        
        html += `
                    </div>
                </div>
            </div>
        `;
    });
    
    html += `
            </div>
        </div>
    `;
    
    modal.innerHTML = html;
    document.body.appendChild(modal);
}
// Ouvrir la modale artiste (pleine page)
// function openArtistModal(artist) {
//     // Créer la modale
//     const modal = document.createElement('div');
//     modal.id = 'artist-modal';
//     modal.style.cssText = `
//         position: fixed;
//         top: 0;
//         left: 0;
//         width: 100%;
//         height: 100%;
//         background: var(--bg-primary);
//         z-index: 10000;
//         overflow-y: auto;
//         animation: fadeIn 0.2s ease;
//     `;
    
//     // Filtrer les chansons de cet artiste
//     const artistSongs = libraryData.songs.filter(s => s.artist === artist);
    
//     // Organiser par album
//     const albums = {};
//     artistSongs.forEach(song => {
//         if (!albums[song.album]) {
//             albums[song.album] = [];
//         }
//         albums[song.album].push(song);
//     });
    
//     // Construire le HTML
//     let html = `
//         <div style="max-width: 1400px; margin: 0 auto; padding: 48px 40px;">
//             <!-- Header -->
//             <div style="
//                 display: flex; 
//                 justify-content: space-between; 
//                 align-items: center; 
//                 margin-bottom: 48px;
//                 padding-bottom: 24px;
//                 border-bottom: 1px solid var(--border);
//             ">
//                 <div>
//                     <h1 style="
//                         font-size: 36px; 
//                         margin: 0 0 8px 0;
//                         font-weight: 700;
//                         letter-spacing: -0.02em;
//                     ">🎤 ${artist}</h1>
//                     <p style="
//                         font-size: 15px;
//                         color: var(--text-secondary);
//                         margin: 0;
//                     ">${Object.keys(albums).length} album${Object.keys(albums).length > 1 ? 's' : ''}</p>
//                 </div>
//                 <button onclick="closeArtistModal()" style="
//                     width: 44px;
//                     height: 44px;
//                     background: var(--bg-card);
//                     border: 1px solid var(--border);
//                     border-radius: 50%;
//                     color: var(--text-primary);
//                     font-size: 20px;
//                     cursor: pointer;
//                     display: flex;
//                     align-items: center;
//                     justify-content: center;
//                     transition: all 0.2s;
//                 " onmouseover="this.style.background='var(--bg-hover)'; this.style.borderColor='var(--border-hover)'" onmouseout="this.style.background='var(--bg-card)'; this.style.borderColor='var(--border)'">
//                     ✕
//                 </button>
//             </div>
            
//             <!-- Albums en 2 colonnes -->
//             <div style="
//                 display: grid !important; 
//                 grid-template-columns: 1fr 1fr !important; 
//                 gap: 24px;
//                 width: 100%;
//             ">
//     `;
    
//     Object.keys(albums).sort().forEach(album => {
//         const songs = albums[album];
//         // Chercher la pochette dans différents champs possibles
//         const albumArt = songs[0].album_art || songs[0].albumArt || songs[0].cover || songs[0].artwork || null;
        
//         html += `
//             <div class="album-card-modal" style="
//                 background: var(--bg-card);
//                 border: 1px solid var(--border);
//                 border-radius: var(--radius-lg);
//                 overflow: hidden;
//                 transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
//                 position: relative;
//             ">
//                 <!-- Pochette Album (centrée, style moderne) -->
//                 <div style="
//                     position: relative;
//                     padding: 32px;
//                     background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
//                     display: flex;
//                     justify-content: center;
//                     align-items: center;
//                     min-height: 240px;
//                 ">
//                     <div class="album-cover-wrapper" style="
//                         position: relative;
//                         width: 180px;
//                         height: 180px;
//                         border-radius: var(--radius-md);
//                         overflow: hidden;
//                         box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
//                         transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
//                     ">
//                         ${albumArt ? `
//                             <img src="${albumArt}" style="
//                                 width: 100%;
//                                 height: 100%;
//                                 object-fit: cover;
//                             ">
//                         ` : `
//                             <div style="
//                                 width: 100%;
//                                 height: 100%;
//                                 background: linear-gradient(135deg, rgba(138, 180, 248, 0.3) 0%, rgba(174, 203, 250, 0.15) 100%);
//                                 display: flex;
//                                 align-items: center;
//                                 justify-content: center;
//                                 font-size: 64px;
//                                 position: relative;
//                             ">
//                                 <span style="opacity: 0.5;">💿</span>
//                             </div>
//                         `}
//                     </div>
//                 </div>
                
//                 <!-- Info Album -->
//                 <div style="padding: 28px 32px;">
//                     <div style="margin-bottom: 24px;">
//                         <h2 style="
//                             font-size: 22px; 
//                             margin: 0 0 8px 0; 
//                             font-weight: 700;
//                             letter-spacing: -0.02em;
//                             color: var(--text-primary);
//                         ">${album}</h2>
//                         <div style="display: flex; align-items: center; gap: 12px;">
//                             <span style="
//                                 background: rgba(99, 102, 241, 0.15);
//                                 color: var(--accent);
//                                 padding: 4px 12px;
//                                 border-radius: 20px;
//                                 font-weight: 600;
//                                 font-size: 12px;
//                             ">${songs.length} chanson${songs.length > 1 ? 's' : ''}</span>
//                         </div>
//                     </div>
                    
//                     <!-- Chansons -->
//                     <div style="display: flex; flex-direction: column; gap: 2px;">
//         `;
        
//         songs.forEach((song, index) => {
//             html += `
//                 <div class="song-item-modal" style="
//                     display: flex;
//                     align-items: center;
//                     gap: 14px;
//                     padding: 12px 10px;
//                     background: transparent;
//                     border-radius: var(--radius-sm);
//                     transition: all 0.2s;
//                     cursor: pointer;
//                     position: relative;
//                     overflow: hidden;
//                 " onmouseover="this.style.background='var(--bg-hover)'; this.style.paddingLeft='18px'" onmouseout="this.style.background='transparent'; this.style.paddingLeft='10px'">
//                     <span style="
//                         color: var(--text-muted); 
//                         min-width: 28px; 
//                         font-size: 13px;
//                         font-weight: 600;
//                         text-align: center;
//                     ">${index + 1}</span>
//                     <span style="
//                         font-size: 16px;
//                         opacity: 0.6;
//                         transition: all 0.2s;
//                     ">🎵</span>
//                     <span style="
//                         flex: 1; 
//                         white-space: nowrap; 
//                         overflow: hidden; 
//                         text-overflow: ellipsis;
//                         color: var(--text-primary);
//                         font-size: 14px;
//                         font-weight: 500;
//                     ">${song.title}</span>
//                 </div>
//             `;
//         });
        
//         html += `
//                 </div>
//             </div>
//         `;
//     });
    
//     html += `
//             </div>
//         </div>
//     `;
    
//     modal.innerHTML = html;
// }

// Fermer la modale artiste
function closeArtistModal() {
    // Réactiver le scroll de la page principale
    document.body.style.overflow = 'auto';
    
    const modal = document.getElementById('artist-modal');
    if (modal) {
        modal.style.animation = 'fadeOut 0.2s ease';
        setTimeout(() => {
            modal.remove();
        }, 200);
    }
}

// Render List View (arbre actuel)
function renderListView() {
    if (!libraryData || !libraryData.artists) {
        document.getElementById('library-tree').innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-secondary);">Aucune musique</div>';
        return;
    }
    
    // Organiser par artiste > album > chansons SANS regrouper (afficher l'état actuel)
    const tree = {};
    
    // Créer une map des chansons qui seront déplacées (pour les afficher grisées à leur future position)
    const futurePositions = new Map();
    selectedSuggestions.forEach(index => {
        const suggestion = suggestions[index];
        const targetArtist = suggestion.to;
        const targetAlbum = suggestion.song.album;
        const newTitle = `${suggestion.song.title} (feat. ${suggestion.featArtist})`;
        
        if (!futurePositions.has(targetArtist)) {
            futurePositions.set(targetArtist, new Map());
        }
        if (!futurePositions.get(targetArtist).has(targetAlbum)) {
            futurePositions.get(targetArtist).set(targetAlbum, []);
        }
        futurePositions.get(targetArtist).get(targetAlbum).push({
            title: newTitle,
            originalSong: suggestion.song
        });
    });
    
    libraryData.songs.forEach(song => {
        const artist = song.artist; // Garder l'artiste tel quel (avec "et" si présent)
        
        // Créer la structure
        if (!tree[artist]) tree[artist] = {};
        if (!tree[artist][song.album]) tree[artist][song.album] = [];
        
        tree[artist][song.album].push(song);
    });
    
    let html = '';
    Object.keys(tree).sort().forEach(artist => {
        const artistId = `artist-${artist.replace(/[^a-zA-Z0-9]/g, '-')}`;
        const isExpanded = expandedItems.has(artistId);
        
        html += `
            <div class="tree-item">
                <div class="tree-line" onclick="toggleItem('${artistId}')">
                    <span class="tree-icon">${isExpanded ? '📂' : '📁'}</span>
                    <span class="tree-label">${artist}</span>
                    <span class="tree-count">${Object.keys(tree[artist]).length} album(s)</span>
                </div>
                <div id="${artistId}" class="tree-children" style="display: ${isExpanded ? 'block' : 'none'};">
        `;
        
        Object.keys(tree[artist]).sort().forEach(album => {
            const albumId = `album-${artist}-${album}`.replace(/[^a-zA-Z0-9]/g, '-');
            const isAlbumExpanded = expandedItems.has(albumId);
            const songs = tree[artist][album];
            
            // URL de la pochette
            const coverUrl = `${API_BASE}/api/album-cover/${encodeURIComponent(artist)}/${encodeURIComponent(album)}`;
            
            html += `
                <div class="tree-item">
                    <div class="tree-line album-line" 
                         onclick="toggleItem('${albumId}')" 
                         data-artist="${artist}" 
                         data-album="${album}"
                         style="padding-left: 20px; display: flex; align-items: center; gap: 8px; cursor: pointer;">
                        <img src="${coverUrl}" 
                             onerror="this.style.display='none'; this.nextElementSibling.style.display='inline';"
                             style="width: 32px; height: 32px; border-radius: 4px; object-fit: cover; flex-shrink: 0;"
                             alt="Album cover">
                        <span class="tree-icon" style="display: none;">💿</span>
                        <span class="tree-label" style="flex: 1;">${album}</span>
                        <span class="tree-count">${tree[artist][album].length} chanson(s)</span>
                    </div>
                    <div id="${albumId}" class="tree-children" style="display: ${isAlbumExpanded ? 'block' : 'none'};">
            `;
            
            // Afficher d'abord les chansons existantes
            tree[artist][album].forEach((song, index) => {
                // Détecter si la chanson a besoin d'être corrigée
                const needsCorrection = song.artist.includes(' et ');
                
                if (needsCorrection) {
                    // Trouver l'index de la suggestion correspondante
                    const suggestionIndex = suggestions.findIndex(s => 
                        s.song.title === song.title && s.song.artist === song.artist
                    );
                    
                    const isChecked = suggestionIndex >= 0 && selectedSuggestions.has(suggestionIndex);
                    const grayedStyle = 'opacity: 0.6; background: rgba(255, 149, 0, 0.08);';
                    
                    // Badge : soit "À CORRIGER" soit "→ Vers Artiste"
                    let badge = '';
                    let destinationArrow = '';
                    
                    if (isChecked && suggestionIndex >= 0) {
                        const suggestion = suggestions[suggestionIndex];
                        // Badge inline avec la destination
                        badge = `<span style="margin-left: 8px; padding: 2px 8px; background: rgba(52, 199, 89, 0.15); color: #34c759; border-radius: 4px; font-size: 10px; font-weight: 600;">→ 📁 ${suggestion.to}</span>`;
                        
                        // Flèche visuelle en dessous (sans le rond)
                        destinationArrow = `
                            <div style="
                                margin-left: 60px; 
                                margin-top: 4px; 
                                margin-bottom: 4px; 
                                padding-left: 14px;
                                border-left: 3px dashed #34c759;
                            ">
                            </div>
                        `;
                    } else if (suggestionIndex >= 0) {
                        // Pas coché : badge orange "À CORRIGER"
                        badge = '<span style="margin-left: 8px; padding: 2px 6px; background: rgba(255, 149, 0, 0.2); color: #ff9500; border-radius: 4px; font-size: 10px; font-weight: 600;">⚠️ À CORRIGER</span>';
                    }
                    
                    html += `
                        <div class="tree-line song-line" style="padding-left: 40px; ${grayedStyle}">
                            <input type="checkbox" ${isChecked ? 'checked' : ''} onchange="toggleSong(${suggestionIndex})" style="margin-right: 8px; cursor: pointer;">
                            <span class="tree-icon">🎵</span>
                            <span class="tree-label">${song.title}${badge}</span>
                        </div>
                        ${destinationArrow}
                    `;
                } else {
                    // Chanson normale (sans feat) - DRAGGABLE
                    html += `
                        <div class="tree-line song-line" 
                             draggable="true" 
                             data-song-path="${song.path}"
                             data-song-title="${song.title}"
                             style="padding-left: 40px; display: flex; align-items: center; gap: 8px;">
                            <span class="tree-icon" style="margin-left: 28px;">🎵</span>
                            <span class="tree-label" style="flex: 1;">${song.title}</span>
                            <button class="rename-btn" 
                                    onclick="event.stopPropagation(); renameSongFromButton('${song.path}', '${song.title.replace(/'/g, "\\'")}');"
                                    style="
                                        opacity: 0;
                                        padding: 4px 8px;
                                        background: rgba(102, 126, 234, 0.1);
                                        border: 1px solid rgba(102, 126, 234, 0.3);
                                        border-radius: 6px;
                                        color: #667eea;
                                        font-size: 12px;
                                        cursor: pointer;
                                        transition: all 0.2s;
                                    ">✏️</button>
                        </div>
                    `;
                }
            });
            
            // Afficher les chansons qui seront déplacées ICI (grisées)
            if (futurePositions.has(artist) && futurePositions.get(artist).has(album)) {
                const futureSongs = futurePositions.get(artist).get(album);
                futureSongs.forEach(futureSong => {
                    html += `
                        <div class="tree-line song-line" style="
                            padding-left: 40px; 
                            opacity: 0.4; 
                            background: rgba(52, 199, 89, 0.05);
                            border-left: 3px solid #34c759;
                        ">
                            <span class="tree-icon" style="margin-left: 28px;">🎵</span>
                            <span class="tree-label">${futureSong.title}</span>
                            <span style="margin-left: 8px; padding: 2px 6px; background: rgba(52, 199, 89, 0.2); color: #34c759; border-radius: 4px; font-size: 10px; font-weight: 600;">✨ FUTUR</span>
                        </div>
                    `;
                });
            }
            
            html += `</div></div>`;
        });
        
        html += `</div></div>`;
    });
    
    document.getElementById('library-tree').innerHTML = html;
    
    // Initialiser le drag & drop après le rendu
    if (typeof initDragAndDrop === 'function') {
        initDragAndDrop();
    }
}

// Toggle expand/collapse
function toggleItem(id) {
    const element = document.getElementById(id);
    if (element.style.display === 'none') {
        element.style.display = 'block';
        expandedItems.add(id);
    } else {
        element.style.display = 'none';
        expandedItems.delete(id);
    }
}

// Tout ouvrir
function expandAll() {
    document.querySelectorAll('.tree-children').forEach(el => {
        el.style.display = 'block';
        expandedItems.add(el.id);
    });
    renderLibraryTree();
}

// Tout fermer
function collapseAll() {
    expandedItems.clear();
    renderLibraryTree();
}

// Normaliser le texte (enlever accents, minuscules)
function normalizeText(text) {
    return text
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, ''); // Enlever les accents
}

// Filtrer la bibliothèque (recherche intelligente)
function filterLibrary(query) {
    if (!query || query.trim() === '') {
        // Réafficher tout
        document.querySelectorAll('.tree-item, .tree-line').forEach(el => {
            el.style.display = '';
        });
        return;
    }
    
    const normalizedQuery = normalizeText(query.trim());
    
    // Filtrer les éléments
    document.querySelectorAll('.tree-item').forEach(item => {
        const text = normalizeText(item.textContent);
        const matches = text.includes(normalizedQuery);
        item.style.display = matches ? '' : 'none';
        
        // Si un élément correspond, montrer aussi ses parents
        if (matches) {
            let parent = item.parentElement;
            while (parent && parent.classList.contains('tree-children')) {
                parent.style.display = 'block';
                parent = parent.parentElement;
            }
        }
    });
}

// Renommer une chanson
function renameSong(path) {
    const song = libraryData.songs.find(s => s.path === path);
    if (!song) return;
    
    const newTitle = prompt('Nouveau titre:', song.title);
    if (newTitle && newTitle !== song.title) {
        alert(`Fonctionnalité à implémenter: Renommer "${song.title}" en "${newTitle}"`);
        // TODO: Appel API
    }
}

// Déplacer une chanson
function moveSong(path) {
    const song = libraryData.songs.find(s => s.path === path);
    if (!song) return;
    
    const newArtist = prompt('Nouvel artiste:', song.artist);
    if (newArtist && newArtist !== song.artist) {
        alert(`Fonctionnalité à implémenter: Déplacer vers "${newArtist}"`);
        // TODO: Appel API
    }
}

// Afficher les infos d'une chanson
function showSongInfo(path) {
    const song = libraryData.songs.find(s => s.path === path);
    if (!song) return;
    
    alert(`🎵 ${song.title}\n🎤 ${song.artist}\n💿 ${song.album}\n📁 ${song.path}`);
}

// Renommer depuis le bouton
async function renameSongFromButton(songPath, currentTitle) {
    // Utiliser la même logique que le double-click
    const newTitle = await showRenameDialog(0, 0, currentTitle);
    
    if (!newTitle || newTitle === currentTitle) {
        return;
    }
    
    console.log(`✏️ Rename: "${currentTitle}" → "${newTitle}"`);
    
    // Appeler l'API
    try {
        const response = await fetch(`${API_BASE}/api/rename-song`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                song_path: songPath,
                new_title: newTitle
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log(`✅ Chanson renommée: "${newTitle}"`);
            await loadLibrary();
        } else {
            console.error(`❌ Erreur: ${result.error}`);
            showNotification(`❌ ${result.error}`, 'error');
        }
        
    } catch (error) {
        console.error('❌ Erreur:', error);
        showNotification('❌ Erreur lors du renommage', 'error');
    }
}

// Variables pour les suggestions
let suggestions = [];
let selectedSuggestions = new Set();

// View mode
let viewMode = 'grid'; // 'grid' ou 'list'

function setViewMode(mode) {
    viewMode = mode;
    
    // Update buttons
    const gridBtn = document.getElementById('grid-view-btn');
    const listBtn = document.getElementById('list-view-btn');
    
    if (mode === 'grid') {
        gridBtn.style.background = 'var(--accent)';
        gridBtn.style.color = 'white';
        listBtn.style.background = 'transparent';
        listBtn.style.color = 'var(--text-secondary)';
    } else {
        listBtn.style.background = 'var(--accent)';
        listBtn.style.color = 'white';
        gridBtn.style.background = 'transparent';
        gridBtn.style.color = 'var(--text-secondary)';
    }
    
    // Re-render
    renderLibraryTree();
}

// Analyser et proposer des modifications
function analyzeSuggestions() {
    if (!libraryData || !libraryData.songs) return;
    
    suggestions = [];
    
    // Créer un Set des artistes qui existent seuls dans la bibliothèque
    const soloArtists = new Set();
    libraryData.songs.forEach(song => {
        if (!song.artist.includes(' et ')) {
            soloArtists.add(song.artist);
        }
    });
    
    // Détecter les artistes avec "et" (feats à corriger)
    libraryData.songs.forEach(song => {
        if (song.artist.includes(' et ')) {
            const parts = song.artist.split(' et ');
            const artist1 = parts[0].trim();
            const artist2 = parts[1].trim();
            
            let mainArtist, featArtist;
            
            // Logique intelligente : celui qui existe seul est l'artiste principal
            if (soloArtists.has(artist1) && !soloArtists.has(artist2)) {
                // artist1 existe seul → c'est l'artiste principal
                mainArtist = artist1;
                featArtist = artist2;
            } else if (soloArtists.has(artist2) && !soloArtists.has(artist1)) {
                // artist2 existe seul → c'est l'artiste principal
                mainArtist = artist2;
                featArtist = artist1;
            } else {
                // Par défaut : le premier est l'artiste principal
                mainArtist = artist1;
                featArtist = artist2;
            }
            
            suggestions.push({
                type: 'move_feat',
                song: song,
                from: song.artist,
                to: mainArtist,
                featArtist: featArtist,
                description: `Déplacer "${song.title}" de "${song.artist}" vers "${mainArtist}" et ajouter (feat. ${featArtist})`
            });
        }
    });
    
    // Mettre à jour le compteur "À corriger"
    const issuesCountEl = document.getElementById('issues-count');
    if (issuesCountEl) {
        issuesCountEl.textContent = suggestions.length;
    }
}



// Toggle une chanson
function toggleSong(suggestionIndex) {
    if (suggestionIndex === -1 || suggestionIndex === undefined) {
        console.error('❌ Index invalide');
        return;
    }
    
    if (selectedSuggestions.has(suggestionIndex)) {
        selectedSuggestions.delete(suggestionIndex);
        console.log('✅ Décochée:', suggestions[suggestionIndex].song.title);
    } else {
        selectedSuggestions.add(suggestionIndex);
        console.log('✅ Cochée:', suggestions[suggestionIndex].song.title, '→', suggestions[suggestionIndex].to);
    }
    
    updateSuggestionCount();
    renderLibraryTree(); // Re-render pour afficher/masquer la flèche
}

// Mettre à jour le compteur
function updateSuggestionCount() {
    const count = selectedSuggestions.size;
    
    // Mettre à jour le compteur dans le header
    const selectedCountHeader = document.getElementById('selected-count-header');
    if (selectedCountHeader) {
        selectedCountHeader.textContent = count;
    }
    
    // Afficher/masquer les éléments dans le header
    const selectionInfo = document.getElementById('selection-info');
    const applyBtnHeader = document.getElementById('apply-btn-header');
    
    if (selectionInfo && applyBtnHeader) {
        if (count > 0) {
            selectionInfo.style.display = 'block';
            applyBtnHeader.style.display = 'block';
        } else {
            selectionInfo.style.display = 'none';
            applyBtnHeader.style.display = 'none';
        }
    }
}

// Appliquer les suggestions sélectionnées
async function applySuggestions() {
    if (selectedSuggestions.size === 0) return;
    
    const selected = Array.from(selectedSuggestions).map(i => suggestions[i]);
    
    if (!confirm(`Voulez-vous vraiment appliquer ${selected.length} correction(s) ?\n\n` + 
                 selected.map(s => `• ${s.song.title} → ${s.to} (feat. ${s.featArtist})`).join('\n'))) {
        return;
    }
    
    console.log('🚀 Application des corrections...', selected);
    
    try {
        // Préparer les données pour l'API
        const corrections = selected.map(s => ({
            song_path: s.song.path,
            target_artist: s.to,
            feat_artist: s.featArtist
        }));
        
        const response = await fetch(`${API_BASE}/api/apply-corrections`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ corrections })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(`✅ ${result.success_count}/${result.total} correction(s) appliquée(s) avec succès !`);
            
            // Réinitialiser les sélections
            selectedSuggestions.clear();
            
            // Recharger la bibliothèque
            await loadLibrary();
            await loadData();
        } else {
            alert(`❌ Erreur: ${result.error}`);
        }
        
    } catch (error) {
        console.error('❌ Erreur:', error);
        alert('❌ Erreur lors de l\'application des corrections');
    }
}

// Mettre à jour le statut
function updateStatus(status) {
    // Mettre à jour le compteur de queue
    updateQueueCount(status.queue_size || 0);
    
    // Dernier téléchargement complété
    if (status.last_completed && status.last_completed.success) {
        addToRecent(status.last_completed);
    }

    // Afficher les téléchargements récents
    updateRecentList();
    
    // Recharger la bibliothèque si un téléchargement est terminé
    if (status.last_completed && status.last_completed.success) {
        loadLibrary();
    }
}

// Ajouter aux téléchargements récents
function addToRecent(download) {
    // Vérifier si déjà présent (éviter les doublons)
    const exists = recentDownloads.some(d => 
        d.metadata.title === download.metadata.title &&
        d.metadata.artist === download.metadata.artist
    );

    if (!exists) {
        recentDownloads.unshift(download);
        // Garder seulement les 10 derniers
        if (recentDownloads.length > 10) {
            recentDownloads = recentDownloads.slice(0, 10);
        }
    }
}

// Mettre à jour la liste des téléchargements récents
function updateRecentList() {
    const recentList = document.getElementById('recent-list');
    
    if (recentDownloads.length === 0) {
        recentList.innerHTML = '<div class="empty-state">Aucun téléchargement récent</div>';
        return;
    }

    recentList.innerHTML = recentDownloads.map(download => {
        const metadata = download.metadata;
        const time = formatTime(download.timestamp);
        
        return `
            <div class="recent-item">
                <div class="recent-icon">✓</div>
                <div class="recent-info">
                    <div class="recent-title">${metadata.title || '-'}</div>
                    <div class="recent-artist">${metadata.artist || '-'}</div>
                </div>
                <div class="recent-time">${time}</div>
            </div>
        `;
    }).join('');
}

// Formater le temps relatif
function formatTime(timestamp) {
    if (!timestamp) return '-';
    
    const now = new Date();
    const time = new Date(timestamp);
    const diff = Math.floor((now - time) / 1000); // secondes

    if (diff < 60) return 'À l\'instant';
    if (diff < 3600) return `Il y a ${Math.floor(diff / 60)} min`;
    if (diff < 86400) return `Il y a ${Math.floor(diff / 3600)} h`;
    return `Il y a ${Math.floor(diff / 86400)} j`;
}

// Mettre à jour le timestamp
function updateTimestamp() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
    });
    document.getElementById('last-update').textContent = timeString;
}

// Actualiser les données
function refreshData() {
    console.log('🔄 Actualisation des données...');
    loadData();
}

// Auto-refresh
function startAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
    }
    
    refreshTimer = setInterval(() => {
        loadData();
    }, REFRESH_INTERVAL);
    
    console.log(`✅ Auto-refresh activé (${REFRESH_INTERVAL / 1000}s)`);
}

// Nettoyer le dossier temp
async function clearTemp() {
    if (!confirm('Voulez-vous vraiment nettoyer le dossier temp/ ?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/cleanup`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(`✅ Nettoyage terminé: ${result.deleted_files.length} fichier(s) supprimé(s)`);
            loadData();
        } else {
            alert(`❌ Erreur: ${result.error}`);
        }
    } catch (error) {
        console.error('❌ Erreur lors du nettoyage:', error);
        alert('❌ Erreur lors du nettoyage');
    }
}

// Afficher une erreur
function showError() {
    const statusIndicator = document.getElementById('server-status');
    if (statusIndicator) {
        statusIndicator.innerHTML = '<span class="dot" style="background: #ff3b30;"></span><span>Hors ligne</span>';
    }
}

// Afficher une notification
function showNotification(message) {
    // Créer l'élément de notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        font-size: 14px;
        font-weight: 600;
        animation: slideInRight 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Supprimer après 3 secondes
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Auto-refresh de la bibliothèque toutes les 5 secondes
let libraryRefreshTimer = null;

function startLibraryAutoRefresh() {
    // Rafraîchir toutes les 5 secondes
    libraryRefreshTimer = setInterval(async () => {
        await loadLibrary();
    }, 5000);
    
    console.log('🔄 Auto-refresh de la bibliothèque activé (5s)');
}

function stopLibraryAutoRefresh() {
    if (libraryRefreshTimer) {
        clearInterval(libraryRefreshTimer);
        libraryRefreshTimer = null;
        console.log('⏸️ Auto-refresh de la bibliothèque désactivé');
    }
}

// Cleanup au déchargement
window.addEventListener('beforeunload', () => {
    if (refreshTimer) {
        clearInterval(refreshTimer);
    }
    stopLibraryAutoRefresh();
});
