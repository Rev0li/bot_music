# 🤝 Contribuer à GrabSong V3

Merci de votre intérêt pour contribuer à GrabSong ! Voici comment vous pouvez aider.

## 📋 Comment Contribuer

### 1. Signaler un Bug

Ouvrez une [issue](https://github.com/votre-username/grabsong-v3/issues) avec :
- Description claire du problème
- Étapes pour reproduire
- Comportement attendu vs actuel
- Version de Python, OS, navigateur
- Logs d'erreur si disponibles

### 2. Proposer une Fonctionnalité

Ouvrez une [issue](https://github.com/votre-username/grabsong-v3/issues) avec :
- Description de la fonctionnalité
- Cas d'usage
- Exemples si possible

### 3. Soumettre du Code

1. **Fork** le projet
2. **Clone** votre fork
   ```bash
   git clone https://github.com/votre-username/grabsong-v3.git
   cd grabsong-v3
   ```

3. **Créer une branche**
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```

4. **Faire vos modifications**
   - Suivre le style de code existant
   - Ajouter des commentaires si nécessaire
   - Tester vos changements

5. **Commit**
   ```bash
   git add .
   git commit -m "feat: description de la fonctionnalité"
   ```

6. **Push**
   ```bash
   git push origin feature/ma-fonctionnalite
   ```

7. **Pull Request**
   - Ouvrir une PR vers `main`
   - Décrire vos changements
   - Lier les issues concernées

## 📝 Conventions de Commit

Utiliser [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage, pas de changement de code
- `refactor:` Refactoring
- `test:` Ajout de tests
- `chore:` Maintenance

Exemples :
```
feat: ajouter support des playlists
fix: corriger l'extraction de l'année
docs: mettre à jour le README
```

## 🧪 Tests

Avant de soumettre :

1. **Tester localement**
   ```bash
   cd python-server
   source venv/bin/activate
   python app.py
   ```

2. **Tester avec Docker**
   ```bash
   docker-compose up --build
   ```

3. **Tester l'extension Chrome**
   - Recharger l'extension
   - Tester sur plusieurs chansons
   - Vérifier les logs (F12)

## 🎨 Style de Code

### Python
- PEP 8
- Docstrings pour les fonctions
- Type hints si possible

### JavaScript
- ES6+
- Commentaires clairs
- Noms de variables descriptifs

## 🌟 Domaines d'Amélioration

Voici des idées de contribution :

### Fonctionnalités
- [ ] Support des playlists complètes
- [ ] Interface web pour gérer la bibliothèque
- [ ] API pour applications tierces
- [ ] Support Spotify/Deezer
- [ ] Détection automatique des doublons

### Améliorations
- [ ] Tests unitaires
- [ ] CI/CD complet
- [ ] Documentation API
- [ ] Traductions (i18n)
- [ ] Mode sombre pour l'extension

### Bugs Connus
- [ ] Gestion des caractères spéciaux dans les noms
- [ ] Timeout sur vidéos très longues
- [ ] Améliorer la détection de l'année

## 📞 Contact

- Issues : [GitHub Issues](https://github.com/votre-username/grabsong-v3/issues)
- Discussions : [GitHub Discussions](https://github.com/votre-username/grabsong-v3/discussions)

## 📄 Licence

En contribuant, vous acceptez que vos contributions soient sous licence MIT.

---

**Merci de contribuer à GrabSong ! 🎵**
