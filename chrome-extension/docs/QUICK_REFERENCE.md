# 🚀 Quick Reference Card

## 📁 File Purpose

| File | Purpose | Edit? |
|------|---------|-------|
| **config.js** | Configuration (URLs, selectors, delays) | ✅ YES |
| **content-v2.js** | Main orchestrator | ⚠️ Rarely |
| **background.js** | Tab management | ❌ No |
| **modules/utils.js** | Helper functions | ⚠️ Add new functions |
| **modules/data-extractor.js** | Extract song data | ⚠️ Modify selectors |
| **modules/page-opener.js** | Open & fill page | ⚠️ Modify fill logic |
| **manifest-v2.json** | Extension config | ⚠️ Add permissions |

---

## ⚙️ Configuration Checklist

### **1. Target Page URL** (config.js line 26)
```javascript
url: 'https://YOUR-SITE.com/submit',
```

### **2. Input Selectors** (config.js lines 28-31)
```javascript
titleInput: '#title',      // CSS selector for title field
artistInput: '#artist',    // CSS selector for artist field
linkInput: '#link',        // CSS selector for link field
```

### **3. Delays** (config.js lines 7-11)
```javascript
menuOpen: 1000,      // Wait for menu to open
shareDialog: 1000,   // Wait for share dialog
copyAction: 500,     // Wait after copy click
pageLoad: 2000,      // Wait for target page to load
```

---

## 🔍 How to Find Selectors

1. Open target page
2. Right-click input field → Inspect
3. Look for:
   - `id="something"` → Use `#something`
   - `class="something"` → Use `.something`
   - `name="something"` → Use `[name="something"]`

---

## 🧪 Testing Commands

### **Test Selector in Console:**
```javascript
document.querySelector('#song-title')  // Should return element
```

### **Test All Selectors:**
```javascript
// Run in console on target page
document.querySelector('#song-title')
document.querySelector('#artist-name')
document.querySelector('#song-link')
```

### **Check Storage:**
```javascript
// Run in console
chrome.storage.local.get(['pendingSongData'], (result) => {
  console.log(result);
});
```

---

## 🐛 Common Issues & Fixes

### **Issue: CONFIG is not defined**
**Fix:** Check manifest-v2.json - config.js must be first in js array

### **Issue: Fields not filling**
**Fix:** Check selectors in config.js, test in console

### **Issue: Tab doesn't open**
**Fix:** Check background.js is loaded (chrome://extensions/)

### **Issue: Link not copied**
**Fix:** Increase delays.shareDialog in config.js

---

## 📝 Useful Code Snippets

### **Add New Data Field:**
```javascript
// In data-extractor.js
songData.genre = safeGetText('.genre-selector');
```

### **Add New Input Field:**
```javascript
// In config.js
genreInput: '#genre',

// In page-opener.js
const genreInput = await findElementWithRetry(CONFIG.targetPage.selectors.genreInput);
if (genreInput) {
  genreInput.value = data.genre;
  genreInput.dispatchEvent(new Event('input', { bubbles: true }));
}
```

### **Add Notification:**
```javascript
showNotification('✅ Success!', 'success');
showNotification('❌ Error!', 'error');
showNotification('⚠️ Warning!', 'warning');
```

---

## 🎯 Workflow

```
1. Edit config.js (target URL + selectors)
2. Reload extension (chrome://extensions/)
3. Go to YouTube Music
4. Play a song
5. Click "🎯 Auto Share V2"
6. Check console (F12) for logs
7. Verify data on target page
```

---

## 🔧 Customization Examples

### **Change Button Text:**
```javascript
// config.js line 38
buttonText: '🎵 Your Text Here',
```

### **Add Submit Button Click:**
```javascript
// In page-opener.js after filling fields
const submitBtn = document.querySelector(CONFIG.targetPage.selectors.submitButton);
if (submitBtn) {
  submitBtn.click();
  log('✅', 'Form submitted');
}
```

### **Change Notification Duration:**
```javascript
// config.js line 39
notificationDuration: 5000,  // 5 seconds
```

---

## 📊 Debug Checklist

- [ ] Open Console (F12) on YouTube Music
- [ ] Click button
- [ ] Check for errors (red text)
- [ ] Verify logs appear
- [ ] Open Console on target page
- [ ] Check for errors
- [ ] Verify fields filled

---

## 🚀 Quick Commands

### **Reload Extension:**
1. Go to `chrome://extensions/`
2. Click reload button

### **View Service Worker:**
1. Go to `chrome://extensions/`
2. Click "Service worker" under extension

### **Clear Storage:**
```javascript
chrome.storage.local.clear();
```

---

## 📚 Key Functions

| Function | Purpose | File |
|----------|---------|------|
| `wait(ms)` | Wait X milliseconds | utils.js |
| `log(emoji, msg)` | Debug logging | utils.js |
| `safeClick(element)` | Click safely | utils.js |
| `findButtonByText(text)` | Find button by text | utils.js |
| `extractSongData()` | Get song info | data-extractor.js |
| `getShareLink()` | Get share link | data-extractor.js |
| `openTargetPageWithData()` | Open new tab | page-opener.js |
| `fillTargetPageFields()` | Fill form | page-opener.js |

---

## 🎓 Learning Path

1. ✅ Understand V1 (simple clicking)
2. ✅ Read V2_SETUP_GUIDE.md
3. ✅ Configure config.js
4. ✅ Test data extraction
5. ✅ Test tab opening
6. ✅ Test auto-fill
7. ✅ Customize for your needs

---

## 💡 Pro Tips

- Always test selectors in console first
- Use `CONFIG.debug = true` during development
- Check both tabs (YouTube Music + target) for errors
- Start with longer delays, optimize later
- Keep V1 as backup while testing V2

---

## 📞 Need Help?

1. Check console for errors
2. Read V2_SETUP_GUIDE.md
3. Review V1_VS_V2_COMPARISON.md
4. Test each step individually
5. Check manifest-v2.json permissions

---

**Happy coding! 🚀**
