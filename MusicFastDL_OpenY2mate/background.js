
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "switchToY2mate") {
    chrome.tabs.query({}, (tabs) => {
      const y2mateTab = tabs.find(tab =>
        tab.url && tab.url.includes("y2mate.nu")
      );

      if (y2mateTab) {
        chrome.tabs.update(y2mateTab.id, { active: true }, () => {
          console.log("✅ Switched to existing y2mate tab");
          sendResponse({ success: true });
        });
      } else {
        chrome.tabs.create({ url: "https://y2mate.nu/" }, () => {
          console.log("🆕 Opened new y2mate tab");
          sendResponse({ success: true });
        });
      }
    });

    return true; // Keep the message channel open
  }
});
// chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
//   if (request.action === "runY2mateInBackground") {
//     chrome.tabs.create({ url: "https://y2mate.nu/", active: false }, (tab) => {
//       console.log("[BG] Onglet Y2mate ouvert en arrière-plan :", tab.id);
//       sendResponse({ tabId: tab.id });
//     });
//     return true;
//   }
// });
// chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
//   if (
//     changeInfo.status === "complete" &&
//     tab.url && tab.url.includes("y2mate.nu")
//   ) {
//     // Injecte ton script y2mate.js dans cet onglet
//     chrome.scripting.executeScript({
//       target: { tabId: tabId },
//       files: ["y2mate.js"]
//     }, () => {
//       console.log("[BG] Script y2mate.js injecté dans l'onglet", tabId);
//     });
//   }
// });
