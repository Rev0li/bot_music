# 🚀 V2 Roadmap - YouTube Music Auto-Share Extension

## 📋 V2 Goals

1. **Copy song information** from YouTube Music
2. **Open a new page** (target website)
3. **Paste the information** automatically

---

## 🗂️ New Project Structure

```
bot/
├── manifest.json           → Extension configuration
├── content.js              → Main orchestrator (V2)
├── modules/
│   ├── youtube-music.js    → YouTube Music specific actions
│   ├── data-extractor.js   → Extract song info (title, artist, link)
│   ├── page-opener.js      → Open new tab and paste data
│   └── utils.js            → Helper functions (wait, click, etc.)
├── config.js               → Configuration (URLs, selectors, delays)
├── styles.css              → UI styling
└── docs/
    ├── LEARNING_GUIDE.md
    └── STEP2_EXPLANATION.md
```

---

## 🎯 V2 Workflow

```
Step 1: Extract Song Info
├─ Get song title
├─ Get artist name
├─ Get album name
└─ Get share link (via copy button)

Step 2: Store Data
└─ Save to chrome.storage or variable

Step 3: Open Target Page
└─ Open new tab with target URL

Step 4: Paste Data
├─ Wait for page to load
├─ Find input fields
└─ Fill with extracted data
```

---

## 📊 Data Structure

```javascript
const songData = {
  title: "Song Name",
  artist: "Artist Name",
  album: "Album Name",
  link: "https://music.youtube.com/watch?v=...",
  timestamp: Date.now()
};
```

---

## 🔧 Implementation Plan

### **Phase 1: Refactor Current Code** ✅
- [x] Organize into modules
- [x] Separate concerns (UI, actions, data)
- [x] Add configuration file

### **Phase 2: Data Extraction** 🔄
- [ ] Extract song title
- [ ] Extract artist name
- [ ] Extract album name
- [ ] Get share link from clipboard

### **Phase 3: Page Navigation** 🔄
- [ ] Open new tab
- [ ] Pass data to new tab
- [ ] Detect when page is ready

### **Phase 4: Auto-Fill** 🔄
- [ ] Find input fields on target page
- [ ] Fill with extracted data
- [ ] Submit form (optional)

---

## 🎓 Key Concepts You'll Learn

1. **Chrome Storage API** - Store data between pages
2. **Chrome Tabs API** - Open and control tabs
3. **Message Passing** - Communication between tabs
4. **DOM Manipulation** - Extract and insert data
5. **Async/Await** - Handle timing properly

---

## 📝 Next Steps

1. Create modular structure
2. Extract song information
3. Test data extraction
4. Implement tab opening
5. Implement auto-fill
