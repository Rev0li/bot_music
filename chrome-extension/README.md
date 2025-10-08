# 🎯 Chrome Extension - Auto Share V2

Professional Chrome extension for automated music downloading from YouTube Music.

[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-green.svg)](https://developer.chrome.com/docs/extensions/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

---

## 🚀 Features

- ✅ **Background Processing** - Y2Mate runs in background tab
- ✅ **Auto MP3 Selection** - Smart format detection
- ✅ **Structured Filenames** - `art=Artist alb=Album N=Title Y=Year.mp3`
- ✅ **Clipboard Integration** - Ready for Python organizer
- ✅ **Auto-Close** - Closes Y2Mate tab after download

---

## 📦 Installation

1. **Open Chrome Extensions:** `chrome://extensions/`
2. **Enable Developer mode** (top right toggle)
3. **Click "Load unpacked"**
4. **Select this folder** (`chrome-extension/`)
5. **Go to YouTube Music** → Look for "🎯 Auto Share V2" button

---

## 🎵 Usage

1. **Go to YouTube Music**
2. **Click "🎯 Auto Share V2"** on any song
3. **Y2Mate opens in background** and processes automatically
4. **Download starts** with structured filename
5. **Tab closes automatically**

**That's it! Perfect for batch downloads! 🎉**

---

## ⚙️ Configuration

Edit `config.js` to customize:

```javascript
const CONFIG = {
    y2mateUrl: 'https://www.y2mate.com/youtube/',
    delays: {
        pageLoad: 2000,
        conversion: 3000
    }
};
```

---

## 🔄 How It Works

```
YouTube Music → Extract song data → Open Y2Mate (background)
    ↓
Paste URL → Select MP3 → Convert → Download → Close tab
    ↓
Result: "art=Drake alb=Views N=OneDance Y=2016.mp3"
```

---

## 🐛 Troubleshooting

### Button Not Visible
- Refresh YouTube Music page
- Check extension is enabled

### Y2Mate Not Opening  
- Check popup blockers
- Try different song

### Download Not Starting
- Increase delays in `config.js`
- Check browser console for errors

---

## 🎯 Integration

**Works perfectly with Python Organizer:**
1. Extension creates structured filenames
2. Python organizer detects downloads
3. Auto-organizes into Artist/Album/Title.mp3

**Complete automation! 🚀**

---

## 📁 File Structure

```
chrome-extension/
├── manifest.json           # Extension config
├── content.js             # YouTube Music integration
├── background.js          # Tab management
├── config.js              # Settings
└── modules/
    └── page-opener.js     # Y2Mate automation
```

---

## ✅ Success!

You know it's working when:
- ✅ Button appears on YouTube Music
- ✅ Y2Mate opens in background
- ✅ Download starts automatically
- ✅ Filename: `art=Artist N=Title.mp3`

**Happy downloading! 🎵**
