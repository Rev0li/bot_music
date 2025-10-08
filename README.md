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

## 📚 Documentation

### **Chrome Extension**
- [`chrome-extension/README.md`](chrome-extension/README.md) - Setup and usage guide

### **Python Organizer**
- [`python-organizer/docs/00_INDEX.md`](python-organizer/docs/00_INDEX.md) - Complete documentation
- [`python-organizer/docs/01_QUICK_START.md`](python-organizer/docs/01_QUICK_START.md) - 5-minute setup
- [`python-organizer/docs/02_INSTALLATION.md`](python-organizer/docs/02_INSTALLATION.md) - Detailed installation
- [`python-organizer/docs/03_USER_GUIDE.md`](python-organizer/docs/03_USER_GUIDE.md) - How to use

---

## 🎵 Example Result

**Before:**
```
Downloads/
└── art=Drake alb=Views N=OneDance Y=2016.mp3
```

**After:**
```
Music/
└── Drake/
    └── Views/
        └── OneDance.mp3 (with ID3 tags)
```

---

## 🛠️ Tech Stack

- **Chrome Extension:** JavaScript ES6+, Chrome APIs
- **Python Organizer:** Python 3.8+, Tkinter, mutagen, pyautogui

---

## 🐛 Troubleshooting

### Chrome Extension
- **Button not visible:** Refresh YouTube Music page
- **Y2Mate not opening:** Check popup blockers
- **Download not starting:** Try different song

### Python Organizer
- **Scanner not detecting:** `pip install pywin32`
- **Auto-paste not working:** `pip install pyautogui pyperclip`
- **No songs found:** Check filename format

---

## ✅ Success Indicators

You know it's working when:
- ✅ Chrome extension shows "🎯 Auto Share V2" button
- ✅ Y2Mate opens in background and converts automatically
- ✅ Python monitor detects "Save As" dialog
- ✅ Filename is pasted automatically
- ✅ Files are organized into Artist/Album structure
- ✅ MP3 tags are updated correctly

---

## 🎉 Result

**A completely automated music downloading and organizing system!**

From YouTube Music to perfectly organized library in just a few clicks.

**Happy music organizing! 🎵**
