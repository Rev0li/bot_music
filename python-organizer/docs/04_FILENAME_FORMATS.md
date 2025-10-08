# 📝 Formats de Noms de Fichiers

## 🎯 Format Standard

```
art=Artiste alb=Album N=Titre Y=Année.mp3
```

---

## ✅ Champs Obligatoires

### `art=` - Artiste
**Obligatoire:** ✅ Oui  
**Exemple:** `art=Drake`

### `N=` - Titre
**Obligatoire:** ✅ Oui  
**Exemple:** `N=OneDance`

---

## ⚪ Champs Optionnels

### `alb=` - Album
**Obligatoire:** ⚪ Non  
**Défaut:** "Unknown Album"  
**Exemple:** `alb=Views`

### `Y=` - Année
**Obligatoire:** ⚪ Non  
**Défaut:** "Unknown"  
**Exemple:** `Y=2016`

---

## 📊 Exemples Valides

### Format Complet
```
art=Drake alb=Views N=OneDance Y=2016.mp3
→ Drake/Views/OneDance.mp3
```

### Format Minimal
```
art=Drake N=OneDance.mp3
→ Drake/Unknown Album/OneDance.mp3
```

### Sans Album
```
art=The Killers N=Mr. Brightside Y=2004.mp3
→ The Killers/Unknown Album/Mr. Brightside.mp3
```

### Sans Année
```
art=Apashe alb=Time Warp N=Time Warp.mp3
→ Apashe/Time Warp/Time Warp.mp3
```

---

## 🔄 Ordre des Balises

**L'ordre n'a PAS d'importance !**

Tous ces formats sont équivalents :
```
✅ art=Drake N=OneDance alb=Views Y=2016.mp3
✅ N=OneDance art=Drake Y=2016 alb=Views.mp3
✅ alb=Views Y=2016 art=Drake N=OneDance.mp3
✅ Y=2016 N=OneDance alb=Views art=Drake.mp3
```

**Résultat identique:** `Drake/Views/OneDance.mp3`

---

## ❌ Formats Invalides

### Manque l'Artiste
```
❌ alb=Views N=OneDance Y=2016.mp3
```
**Erreur:** `⚠️ Ignoré (manque art= ou N=)`

### Manque le Titre
```
❌ art=Drake alb=Views Y=2016.mp3
```
**Erreur:** `⚠️ Ignoré (manque art= ou N=)`

### Aucune Balise
```
❌ Drake - OneDance.mp3
```
**Erreur:** `⚠️ Ignoré (manque art= ou N=)`

---

## 🧹 Caractères Spéciaux

### Caractères Supprimés
Les caractères suivants sont automatiquement supprimés :
```
< > : " / \ | ? *
```

### Exemple
```
Avant: art=AC/DC N=Back:in:Black.mp3
Après: ACDC/Unknown Album/BackinBlack.mp3
```

---

## 🎓 Intégration Chrome Extension

### Extension V2 Génère Automatiquement

**Format complet (si toutes les infos disponibles):**
```javascript
art=Drake alb=Views N=OneDance Y=2016.mp3
```

**Format partiel (si infos manquantes):**
```javascript
// Si album manquant
art=Drake N=OneDance Y=2016.mp3

// Si année manquante
art=Drake alb=Views N=OneDance.mp3

// Minimal
art=Drake N=OneDance.mp3
```

**Tous sont acceptés ! ✅**

---

## 📋 Tableau Récapitulatif

| Balise | Nom | Obligatoire | Défaut | Exemple |
|--------|-----|-------------|--------|---------|
| `art=` | Artiste | ✅ Oui | - | `art=Drake` |
| `N=` | Titre | ✅ Oui | - | `N=OneDance` |
| `alb=` | Album | ⚪ Non | "Unknown Album" | `alb=Views` |
| `Y=` | Année | ⚪ Non | "Unknown" | `Y=2016` |

---

## 🎯 Cas d'Usage

### Cas 1: Chanson Complète
```
Fichier: art=Drake alb=Views N=OneDance Y=2016.mp3

Résultat:
Drake/
└── Views/
    └── OneDance.mp3

Tags ID3:
- Artist: Drake
- Album: Views
- Title: OneDance
- Year: 2016
```

### Cas 2: Chanson Simple
```
Fichier: art=Drake N=OneDance.mp3

Résultat:
Drake/
└── Unknown Album/
    └── OneDance.mp3

Tags ID3:
- Artist: Drake
- Album: Unknown Album
- Title: OneDance
- Year: Unknown
```

---

## 💡 Conseils

### Conseil 1: Format Minimal pour Tests
```
art=TestArtist N=TestSong.mp3
```
Parfait pour tester rapidement !

### Conseil 2: Format Complet pour Production
```
art=Artiste alb=Album N=Titre Y=2024.mp3
```
Meilleur pour une bibliothèque organisée !

### Conseil 3: Vérifier le Format
Avant d'organiser, vérifiez que vos fichiers ont au minimum `art=` et `N=`.

---

## ✅ Résumé

**Obligatoire:**
- `art=` (Artiste)
- `N=` (Titre)

**Optionnel:**
- `alb=` (Album) → défaut: "Unknown Album"
- `Y=` (Année) → défaut: "Unknown"

**Ordre:** Peu importe !

**Résultat:** Fichiers organisés en `Artiste/Album/Titre.mp3` avec tags ID3 ! 🎉
