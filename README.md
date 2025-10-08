# 🎵 Music Organizer & Chrome Extension

Complete automated solution for downloading and organizing music from YouTube Music.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-green.svg)](https://developer.chrome.com/docs/extensions/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 What This Does

**Complete automation from YouTube Music to organized library:**

1. **Chrome Extension** → Automates Y2Mate downloading
2. **Python Organizer** → Detects downloads and organizes files
3. **Result** → Perfect music library: `Artist/Album/Title.mp3`

---

## ⚡ Quick Start

### 1. Chrome Extension
```bash
# Load chrome-extension/ folder as unpacked extension
# Go to YouTube Music → Click "🎯 Auto Share V2"
```

### 2. Python Organizer
```bash
cd python-organizer
pip install -r requirements.txt
python app.py
```

**That's it! Download a song and watch the magic happen! ✨**

---

## 📁 Project Structure

```
Music-Organizer/
├── chrome-extension/               # 🌐 Chrome Extension V2
│   ├── manifest.json
│   ├── content.js
│   ├── background.js
│   └── modules/
│
├── python-organizer/               # 🐍 Python Music Organizer
│   ├── app.py                      # Main application
│   ├── music_organizer/            # Modular package
│   └── docs/                       # Complete documentation
│
└── README.md                       # This file
```

---

## 🚀 Features

### Chrome Extension
- ✅ **Background Processing** - Y2Mate runs in background
- ✅ **Auto MP3 Selection** - Smart format detection
- ✅ **Structured Filenames** - `art=Artist N=Title.mp3`
- ✅ **Clipboard Integration** - Ready for Python organizer

### Python Organizer
- ✅ **Download Detection** - Monitors "Save As" dialogs
- ✅ **Auto-Paste** - Pastes filenames automatically (Ctrl+V)
- ✅ **Auto-Organization** - Creates `Artist/Album/Title.mp3`
- ✅ **ID3 Tags** - Updates MP3 metadata
- ✅ **GUI Interface** - User-friendly with real-time logs

---

## 🔄 Complete Workflow

```
YouTube Music → Auto Share V2 → Y2Mate (background) → Download
    ↓
"Save As" dialog → Auto-paste filename → Save to Music/itunes
    ↓
Python Organizer → Scan folder → Organize into Artist/Album/
    ↓
Perfect music library! 🎉
```

---

## 💡 Tips

- **Start with V1** if you're new to Chrome extensions
- **V2 requires configuration** - edit `V2/config.js` first
- **Both versions work independently** - you can install both
- **Keep V1 as reference** while learning V2

---

## 🎉 What You'll Learn

**From V1:**
- Chrome extension basics
- DOM manipulation
- Event handling
- Debugging techniques

**From V2:**
- Modular architecture
- Chrome APIs (Storage, Tabs, Messaging)
- Async/await patterns
- Cross-page communication
- Professional code organization

---

**Happy coding! 🚀**

Choose your version and get started:
- [V1 - Simple Clicker](./V1/)
- [V2 - Full Automation](./V2/)
