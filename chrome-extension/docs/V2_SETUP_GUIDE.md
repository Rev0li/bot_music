# 🚀 V2 Setup Guide - Auto Share Extension

## 📋 What's New in V2?

### **V1 (Old):**
- ✅ Click menu → Click "Partager" → Click "Copier"
- ❌ Manual: You had to paste the link yourself

### **V2 (New):**
- ✅ Extract song info (title, artist, album)
- ✅ Get share link automatically
- ✅ Open target page
- ✅ Auto-fill form with data
- ✅ Everything automatic!

---

## 🗂️ New File Structure

```
bot/
├── manifest-v2.json          → New manifest with more permissions
├── background.js             → NEW: Handles tab opening
├── config.js                 → NEW: Central configuration
├── content-v2.js             → NEW: Main orchestrator
├── modules/
│   ├── utils.js              → NEW: Helper functions
│   ├── data-extractor.js     → NEW: Extract song data
│   └── page-opener.js        → NEW: Open and fill target page
├── content.js                → OLD: V1 version (keep for reference)
├── manifest.json             → OLD: V1 manifest
├── styles.css                → UI styling (unchanged)
└── popup_script.js           → Popup script (unchanged)
```

---

## ⚙️ Configuration Required

### **Step 1: Edit `config.js`**

Open `config.js` and change these values:

```javascript
// 🌐 TARGET PAGE - Page où coller les données
targetPage: {
  url: 'https://example.com/submit',  // 🔧 CHANGE THIS to your target URL
  selectors: {
    titleInput: '#song-title',         // 🔧 CHANGE THIS
    artistInput: '#artist-name',       // 🔧 CHANGE THIS
    linkInput: '#song-link',           // 🔧 CHANGE THIS
    submitButton: '#submit-btn',       // 🔧 CHANGE THIS (optional)
  }
},
```

#### **How to Find Selectors:**

1. **Open your target page** in Chrome
2. **Right-click on the input field** → "Inspect"
3. **Look for:**
   - `id="something"` → Use `#something`
   - `class="something"` → Use `.something`
   - `name="something"` → Use `[name="something"]`

**Example:**
```html
<input id="song-title" type="text" />
```
→ Selector: `#song-title`

```html
<input class="title-input" type="text" />
```
→ Selector: `.title-input`

---

## 🚀 Installation

### **Option A: Test V2 (Recommended)**

1. **Rename files:**
   ```
   manifest.json → manifest-v1-backup.json
   manifest-v2.json → manifest.json
   ```

2. **Reload extension:**
   - Go to `chrome://extensions/`
   - Click "Reload" on your extension

3. **Test it:**
   - Go to YouTube Music
   - Click "🎯 Auto Share V2"
   - Watch the magic! ✨

### **Option B: Keep Both Versions**

Create two separate folders:
```
bot-v1/  → Old version
bot-v2/  → New version
```

Load both as separate extensions.

---

## 🧪 Testing Checklist

### **Test 1: Data Extraction**
- [ ] Open YouTube Music
- [ ] Play a song
- [ ] Open Console (F12)
- [ ] Click "🎯 Auto Share V2"
- [ ] Check console for:
  ```
  🎵 Extracting song data...
  📝 Title: [song name]
  🎤 Artist: [artist name]
  🔗 Getting share link...
  ✅ Share link obtained: https://...
  ```

### **Test 2: Tab Opening**
- [ ] Click "🎯 Auto Share V2"
- [ ] New tab should open with your target URL
- [ ] Check console on new tab

### **Test 3: Auto-Fill**
- [ ] On the new tab, check if fields are filled
- [ ] Open Console (F12)
- [ ] Look for:
  ```
  📝 Filling target page fields...
  ✅ Title filled
  ✅ Artist filled
  ✅ Link filled
  ```

---

## 🐛 Troubleshooting

### **Problem 1: "CONFIG is not defined"**

**Cause:** Files loaded in wrong order.

**Solution:** Check `manifest-v2.json` - `config.js` must be first:
```json
"js": [
  "config.js",        ← Must be first!
  "modules/utils.js",
  ...
]
```

### **Problem 2: "Cannot read property 'debug' of undefined"**

**Cause:** CONFIG not loaded yet.

**Solution:** Add this to top of each module file:
```javascript
if (typeof CONFIG === 'undefined') {
  console.error('CONFIG not loaded!');
}
```

### **Problem 3: Fields not filling on target page**

**Cause:** Wrong selectors in `config.js`.

**Solution:**
1. Open target page
2. Open Console (F12)
3. Test selectors manually:
   ```javascript
   document.querySelector('#song-title')  // Should return the input
   ```
4. Update `config.js` with correct selectors

### **Problem 4: "chrome.storage is not defined"**

**Cause:** Missing permissions.

**Solution:** Check `manifest-v2.json` has:
```json
"permissions": [
  "storage",
  ...
]
```

### **Problem 5: Tab doesn't open**

**Cause:** Background service worker not loaded.

**Solution:**
1. Go to `chrome://extensions/`
2. Click "Service worker" under your extension
3. Check for errors
4. Make sure `background.js` exists

---

## 🎓 How It Works (Technical)

### **Flow Diagram:**

```
YouTube Music Page:
  1. User clicks "🎯 Auto Share V2"
  2. extractAllData() runs:
     ├─ Extract title, artist, album from DOM
     └─ Click menu → Share → Copy → Get link from clipboard
  3. saveSongDataToStorage(data)
     └─ Save to chrome.storage.local
  4. chrome.runtime.sendMessage('openTab')
     └─ Tell background.js to open new tab

Background Service Worker:
  5. Receive 'openTab' message
  6. chrome.tabs.create(targetUrl)
     └─ Open new tab

Target Page:
  7. content-v2.js detects isTargetPage = true
  8. fillTargetPageFields() runs:
     ├─ Read data from chrome.storage.local
     ├─ Find input fields
     ├─ Fill with data
     └─ Trigger 'input' events
  9. Done! ✅
```

### **Key Technologies:**

1. **Chrome Storage API** - Pass data between tabs
2. **Chrome Runtime Messaging** - Communication between scripts
3. **Chrome Tabs API** - Open new tabs
4. **Content Scripts** - Run on multiple pages
5. **Background Service Worker** - Handle tab operations

---

## 📚 Learning Resources

### **Chrome Extension APIs:**
- [Storage API](https://developer.chrome.com/docs/extensions/reference/storage/)
- [Tabs API](https://developer.chrome.com/docs/extensions/reference/tabs/)
- [Runtime Messaging](https://developer.chrome.com/docs/extensions/mv3/messaging/)

### **JavaScript Concepts:**
- [Async/Await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
- [Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- [DOM Manipulation](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model)

---

## 🎯 Next Steps

1. **Configure `config.js`** with your target page
2. **Test data extraction** on YouTube Music
3. **Test tab opening**
4. **Test auto-fill** on target page
5. **Adjust delays** in `config.js` if needed
6. **Add custom features** (submit button, validation, etc.)

---

## 💡 Tips

- **Start with `debug: true`** in `config.js` to see all logs
- **Test each step separately** before testing the full flow
- **Use Console (F12)** extensively to debug
- **Check both tabs** (YouTube Music and target page) for errors
- **Adjust delays** if things happen too fast/slow

---

## 🎉 You're Ready!

Your V2 extension is now organized, modular, and powerful!

**What you learned:**
- ✅ Modular code organization
- ✅ Chrome Extension APIs (storage, tabs, messaging)
- ✅ Async/await patterns
- ✅ Cross-page communication
- ✅ DOM manipulation and data extraction

Happy coding! 🚀
