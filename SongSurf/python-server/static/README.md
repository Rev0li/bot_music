# 📁 Fichiers Statiques du Dashboard

Ce dossier contient les assets du dashboard SongSurf.

## Fichiers

### `dashboard.css`
- Styles minimalistes avec thème sombre
- Design moderne et épuré
- Responsive (adapté mobile/tablette/desktop)
- Animations fluides

### `dashboard.js`
- Logique de mise à jour en temps réel
- Auto-refresh toutes les 2 secondes
- Gestion de l'historique des téléchargements
- Interactions avec l'API Flask

## Personnalisation

### Changer les couleurs

Éditez `dashboard.css` et modifiez les variables CSS:

```css
:root {
    --bg-primary: #0a0a0a;      /* Fond principal */
    --bg-secondary: #1a1a1a;    /* Fond secondaire */
    --bg-card: #222222;         /* Fond des cartes */
    --text-primary: #ffffff;    /* Texte principal */
    --text-secondary: #a0a0a0;  /* Texte secondaire */
    --accent: #667eea;          /* Couleur d'accent */
    --success: #34c759;         /* Couleur de succès */
}
```

### Changer l'intervalle de rafraîchissement

Éditez `dashboard.js`:

```javascript
const REFRESH_INTERVAL = 2000; // en millisecondes
```

## Technologies

- **CSS3** - Variables CSS, Grid, Flexbox, Animations
- **JavaScript ES6+** - Fetch API, Async/Await, Template Literals
- **Responsive Design** - Media queries pour tous les écrans
