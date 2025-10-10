#!/bin/bash

# Script de push pour GrabSong V3 - Linux/WSL Edition

echo "🎵 GrabSong V3 - Préparation du push"
echo "===================================="

# Vérifier qu'on est dans le bon dossier
if [ ! -f "README.md" ]; then
    echo "❌ Erreur: Exécutez ce script depuis le dossier V3/"
    exit 1
fi

# Afficher le statut
echo ""
echo "📊 Statut Git:"
git status --short

# Demander confirmation
echo ""
read -p "Voulez-vous continuer avec le commit et push? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Annulé"
    exit 1
fi

# Commit
echo ""
echo "📝 Création du commit..."
git commit -F COMMIT_MESSAGE.txt

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors du commit"
    exit 1
fi

# Créer/basculer sur la branche linux
echo ""
echo "🌿 Création de la branche 'linux'..."
git checkout -b linux 2>/dev/null || git checkout linux

# Push
echo ""
echo "🚀 Push vers origin/linux..."
git push -u origin linux

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Push réussi!"
    echo ""
    echo "🎉 GrabSong V3 (Linux/WSL Edition) est maintenant sur GitHub!"
    echo ""
    echo "📋 Prochaines étapes:"
    echo "  1. Vérifier le repo sur GitHub"
    echo "  2. Créer une release v3.0.0"
    echo "  3. Préparer la branche 'windows' pour la version native"
else
    echo ""
    echo "❌ Erreur lors du push"
    exit 1
fi
