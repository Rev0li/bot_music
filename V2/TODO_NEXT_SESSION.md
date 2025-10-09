# 🔧 TODO - Prochaine Session

## 🐛 Bugs à Corriger

### 1. **Serveur Python Non Accessible - Gestion Améliorée**

**Problème:**
- Quand le serveur Python n'est pas accessible, le processus continue
- L'onglet Y2Mate reste ouvert
- Pas de possibilité de retry facilement

**Solution à Implémenter:**
```javascript
// Détecter l'erreur serveur Python
if (!response || !response.success) {
  // 1. Arrêter le processus
  stopPolling();
  
  // 2. Fermer l'onglet Y2Mate ouvert
  chrome.runtime.sendMessage({ action: 'close_y2mate_tab' });
  
  // 3. Afficher message d'erreur avec bouton Retry
  showErrorWithRetry({
    title: "⚠️ Serveur Python non accessible",
    message: "Lancez: python app.py",
    retryAction: () => continueWorkflow(songData)
  });
}
```

**Fichiers à Modifier:**
- `content.js` - Fonction `continueWorkflow()` ligne ~910
- `background.js` - Ajouter action `close_y2mate_tab`

---

### 2. **Countdown Ne Déclenche Pas le Reset**

**Problème:**
- Le countdown affiche "Reset dans 0 secondes..."
- Mais le reset ne se déclenche pas
- L'extension reste bloquée sur le message final

**Cause Probable:**
```javascript
if (secondsLeft <= 0) {
  clearInterval(countdownInterval);
  resetExtension();  // ← Ne se déclenche pas ?
}
```

**Solutions à Tester:**
1. Vérifier que `resetExtension()` existe et fonctionne
2. Ajouter des logs pour debug
3. Peut-être un problème de timing (secondsLeft jamais exactement 0)

**Code à Modifier:**
```javascript
// Option 1: Condition plus large
if (secondsLeft <= 0.05) {  // Au lieu de <= 0
  clearInterval(countdownInterval);
  resetExtension();
}

// Option 2: Forcer le reset après 3.5s
setTimeout(() => {
  clearInterval(countdownInterval);
  resetExtension();
}, 3500);
```

**Fichier à Modifier:**
- `content.js` - Ligne ~1044-1046

---

## 📝 Notes

- **Screen 1:** Montre le serveur Python non accessible mais le processus continue
- **Screen 2:** Montre le countdown bloqué à "0 secondes" sans reset

## ✅ Tests à Faire

1. Lancer l'extension SANS serveur Python → Vérifier que l'onglet se ferme et retry proposé
2. Attendre le countdown complet → Vérifier que le reset se déclenche à 0
3. Tester plusieurs fois de suite pour vérifier la stabilité

---

**Date:** 2025-10-09
**Priorité:** Haute (bloque l'UX)
