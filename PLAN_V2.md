# 🎯 Plan de Développement - Music Organizer V2

**Date:** 2025-10-09  
**Objectif:** Créer une V2 plus propre, configurable et avec un système de debug/logs complet

---

## 📊 Analyse de l'Architecture Actuelle (V1)

### Structure du Projet
```
python-organizer/
├── app.py                          # Interface graphique principale (520 lignes)
├── music_organizer/                # Package principal
│   ├── __init__.py                 # Exports des modules
│   ├── parser.py                   # Parsing des métadonnées (140 lignes)
│   ├── organizer.py                # Organisation des fichiers (260 lignes)
│   ├── monitor.py                  # Surveillance téléchargements (392 lignes)
│   ├── auto_saver.py               # Automatisation Save As (427 lignes)
│   ├── process_activator.py        # Activation fenêtres (464 lignes)
│   ├── background_saver.py         # Sauvegarde en arrière-plan
│   └── notification_helper.py      # Notifications intelligentes
├── docs/                           # Documentation complète (11 fichiers)
├── requirements.txt                # Dépendances
└── tests/                          # Fichiers de test
```

### Modules Principaux

#### 1. **MetadataParser** (`parser.py`)
- **Rôle:** Parse les noms de fichiers au format `art=Artist alb=Album N=Title Y=Year.mp3`
- **Fonctionnalités:**
  - Extraction des métadonnées (artiste, album, titre, année)
  - Validation des formats
  - Valeurs par défaut pour champs optionnels
- **Points forts:** Simple, bien testé, regex efficaces
- **Points à améliorer:** Logging minimal

#### 2. **MusicOrganizer** (`organizer.py`)
- **Rôle:** Organise les fichiers MP3 en structure Artiste/Album/
- **Fonctionnalités:**
  - Scan récursif des dossiers
  - Mise à jour des tags ID3
  - Création de structure de dossiers
  - Déplacement des fichiers
  - Statistiques (artistes, albums)
- **Points forts:** Robuste, gestion d'erreurs
- **Points à améliorer:** Logs basiques, pas de rollback

#### 3. **DownloadMonitor** (`monitor.py`)
- **Rôle:** Surveille les fenêtres "Save As" pour détecter les téléchargements
- **Fonctionnalités:**
  - Détection via win32gui ou PowerShell
  - Filtrage intelligent des fenêtres
  - Cooldown anti-spam
  - Mode debug
  - Auto-paste et auto-save
- **Points forts:** Deux méthodes de détection, mode debug
- **Points à améliorer:** Logs dispersés, configuration hardcodée

#### 4. **AutoSaver** (`auto_saver.py`)
- **Rôle:** Automatise le collage et la sauvegarde dans "Save As"
- **Fonctionnalités:**
  - Activation de fenêtre
  - Collage automatique (Ctrl+V)
  - Vérification de chemin
  - Clic sur bouton Save
- **Points forts:** Notifications intelligentes
- **Points à améliorer:** Complexe, beaucoup de dépendances

#### 5. **ProcessActivator** (`process_activator.py`)
- **Rôle:** Active les fenêtres par nom de processus
- **Fonctionnalités:**
  - Recherche de processus navigateur
  - Activation multi-méthodes
  - SimpleAutoSaver pour tests
- **Points forts:** Approche simple et efficace
- **Points à améliorer:** Logs verbeux

### Interface Graphique (app.py)

**Composants:**
- Sélection de dossier
- Scanner de téléchargement (ON/OFF)
- Boutons d'action (Scanner, Organiser)
- Zone de logs (ScrolledText)
- Boutons de test et debug
- Switch Auto-Save

**Points forts:**
- Interface claire et intuitive
- Logs en temps réel
- Mode debug intégré

**Points à améliorer:**
- Logs non filtrables
- Pas de sauvegarde des logs
- Configuration hardcodée
- Pas de niveaux de log (INFO, WARNING, ERROR)

---

## 🎯 Objectifs de la V2

### 1. **Système de Logging Professionnel**
- ✅ Logs centralisés avec niveaux (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- ✅ Filtrage par niveau et par module
- ✅ Sauvegarde automatique dans fichiers
- ✅ Horodatage précis
- ✅ Rotation des logs
- ✅ Export des logs (TXT, JSON)

### 2. **Interface de Debug Avancée**
- ✅ Panneau de logs avec filtres
- ✅ Statistiques en temps réel
- ✅ Visualisation de l'état des modules
- ✅ Console de commandes
- ✅ Graphiques de performance (optionnel)

### 3. **Configuration Flexible**
- ✅ Fichier de configuration (JSON/YAML)
- ✅ Interface de paramètres dans le GUI
- ✅ Profils de configuration
- ✅ Import/Export de configuration

### 4. **Architecture Propre**
- ✅ Séparation claire des responsabilités
- ✅ Design patterns (Observer, Factory, Singleton)
- ✅ Injection de dépendances
- ✅ Tests unitaires complets

### 5. **Expérience Utilisateur**
- ✅ Interface moderne et responsive
- ✅ Thèmes (clair/sombre)
- ✅ Raccourcis clavier
- ✅ Tooltips et aide contextuelle
- ✅ Notifications non-intrusives

---

## 🏗️ Architecture de la V2

### Structure Proposée

```
python-organizer-v2/
├── app.py                          # Point d'entrée principal
├── config.yaml                     # Configuration par défaut
├── requirements.txt                # Dépendances
│
├── core/                           # Cœur de l'application
│   ├── __init__.py
│   ├── logger.py                   # ⭐ Système de logging centralisé
│   ├── config.py                   # Gestionnaire de configuration
│   ├── events.py                   # Système d'événements (Observer)
│   └── exceptions.py               # Exceptions personnalisées
│
├── modules/                        # Modules métier (refactorisés)
│   ├── __init__.py
│   ├── parser.py                   # Parser de métadonnées (amélioré)
│   ├── organizer.py                # Organisateur (avec rollback)
│   ├── monitor.py                  # Moniteur (simplifié)
│   └── automation.py               # Automatisation (unifié)
│
├── ui/                             # Interface utilisateur
│   ├── __init__.py
│   ├── main_window.py              # Fenêtre principale
│   ├── debug_panel.py              # ⭐ Panneau de debug/logs
│   ├── settings_dialog.py          # Dialogue de paramètres
│   ├── components/                 # Composants réutilisables
│   │   ├── log_viewer.py           # ⭐ Visualiseur de logs
│   │   ├── filter_bar.py           # Barre de filtres
│   │   └── status_bar.py           # Barre de statut
│   └── themes/                     # Thèmes visuels
│       ├── dark.py
│       └── light.py
│
├── utils/                          # Utilitaires
│   ├── __init__.py
│   ├── file_utils.py               # Gestion de fichiers
│   ├── window_utils.py             # Gestion de fenêtres
│   └── validators.py               # Validateurs
│
├── tests/                          # Tests unitaires
│   ├── test_logger.py              # ⭐ Tests du logger
│   ├── test_parser.py
│   ├── test_organizer.py
│   └── test_monitor.py
│
├── logs/                           # Dossier des logs (auto-créé)
│   ├── app.log                     # Log principal
│   ├── debug.log                   # Logs de debug
│   └── error.log                   # Logs d'erreurs
│
└── docs/                           # Documentation
    ├── V2_ARCHITECTURE.md          # Architecture détaillée
    ├── V2_LOGGING.md               # Guide du système de logs
    └── V2_MIGRATION.md             # Guide de migration V1→V2
```

---

## 🔧 Système de Logging Centralisé (Priorité 1)

### Fonctionnalités

#### 1. **Niveaux de Log**
```python
DEBUG    = 10  # Informations détaillées pour le debug
INFO     = 20  # Informations générales
WARNING  = 30  # Avertissements
ERROR    = 40  # Erreurs récupérables
CRITICAL = 50  # Erreurs critiques
```

#### 2. **Format des Logs**
```
[2025-10-09 10:07:18.123] [INFO] [monitor] Fenêtre détectée: Save As
[2025-10-09 10:07:19.456] [DEBUG] [automation] Activation de Brave...
[2025-10-09 10:07:20.789] [ERROR] [organizer] Erreur lors du déplacement: Permission denied
```

#### 3. **Destinations**
- **Console** (temps réel dans l'UI)
- **Fichier** (logs/app.log)
- **Fichier d'erreurs** (logs/error.log)
- **Fichier de debug** (logs/debug.log, optionnel)

#### 4. **Rotation**
- Taille max: 10 MB par fichier
- Nombre de backups: 5
- Format: `app.log`, `app.log.1`, `app.log.2`, etc.

### API du Logger

```python
from core.logger import Logger

# Initialisation (Singleton)
logger = Logger.get_instance()

# Configuration
logger.configure(
    level=Logger.DEBUG,
    console=True,
    file=True,
    file_path="logs/app.log",
    max_size=10*1024*1024,  # 10 MB
    backup_count=5
)

# Utilisation
logger.debug("Message de debug", module="parser")
logger.info("Opération réussie", module="organizer")
logger.warning("Avertissement", module="monitor")
logger.error("Erreur", module="automation", exception=e)
logger.critical("Erreur critique", module="core")

# Filtrage
logger.set_filter(level=Logger.INFO, modules=["monitor", "automation"])

# Callbacks pour l'UI
logger.add_callback(ui_log_callback)

# Export
logger.export_logs("export.txt", format="text")
logger.export_logs("export.json", format="json")
```

---

## 🎨 Interface de Debug (Priorité 1)

### Composants

#### 1. **Panneau de Logs** (`debug_panel.py`)
```
┌─────────────────────────────────────────────────────────────┐
│ 🐛 Debug Panel                                    [X] Close │
├─────────────────────────────────────────────────────────────┤
│ Filters: [All Levels ▼] [All Modules ▼] [Search: _______]  │
├─────────────────────────────────────────────────────────────┤
│ [2025-10-09 10:07:18] [INFO] [monitor] Scanner activé      │
│ [2025-10-09 10:07:19] [DEBUG] [automation] Brave activé    │
│ [2025-10-09 10:07:20] [ERROR] [organizer] Permission denied│
│ ...                                                          │
├─────────────────────────────────────────────────────────────┤
│ [Clear] [Export] [Pause] [Resume]    Lines: 1234 | Errors: 2│
└─────────────────────────────────────────────────────────────┘
```

#### 2. **Statistiques en Temps Réel**
```
┌─────────────────────────────────────┐
│ 📊 Statistics                       │
├─────────────────────────────────────┤
│ Total Logs:        1234             │
│ DEBUG:             890              │
│ INFO:              300              │
│ WARNING:           42               │
│ ERROR:             2                │
│ CRITICAL:          0                │
│                                     │
│ Active Modules:                     │
│ • monitor         (234 logs)        │
│ • automation      (189 logs)        │
│ • organizer       (156 logs)        │
│ • parser          (89 logs)         │
└─────────────────────────────────────┘
```

#### 3. **État des Modules**
```
┌─────────────────────────────────────┐
│ 🔧 Module Status                    │
├─────────────────────────────────────┤
│ ✅ Parser         [OK]              │
│ ✅ Organizer      [OK]              │
│ ✅ Monitor        [RUNNING]         │
│ ⚠️  Automation    [WARNING]         │
│ ❌ Config         [ERROR]           │
└─────────────────────────────────────┘
```

---

## 📝 Plan de Développement par Étapes

### **Étape 1: Système de Logging** (Priorité: HAUTE)
**Objectif:** Créer le système de logging centralisé

**Tâches:**
1. ✅ Créer `core/logger.py` avec classe Logger (Singleton)
2. ✅ Implémenter les niveaux de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
3. ✅ Implémenter la rotation des fichiers
4. ✅ Ajouter le système de callbacks pour l'UI
5. ✅ Créer les tests unitaires (`tests/test_logger.py`)

**Livrables:**
- `core/logger.py` (200 lignes)
- `tests/test_logger.py` (100 lignes)
- Documentation `docs/V2_LOGGING.md`

**Durée estimée:** 2-3 heures

---

### **Étape 2: Interface de Debug** (Priorité: HAUTE)
**Objectif:** Créer le panneau de debug avec visualisation des logs

**Tâches:**
1. ✅ Créer `ui/components/log_viewer.py` (visualiseur de logs)
2. ✅ Créer `ui/components/filter_bar.py` (filtres)
3. ✅ Créer `ui/debug_panel.py` (panneau principal)
4. ✅ Intégrer avec le Logger
5. ✅ Ajouter les statistiques en temps réel
6. ✅ Ajouter l'export de logs

**Livrables:**
- `ui/components/log_viewer.py` (150 lignes)
- `ui/components/filter_bar.py` (100 lignes)
- `ui/debug_panel.py` (250 lignes)

**Durée estimée:** 3-4 heures

---

### **Étape 3: Système de Configuration** (Priorité: MOYENNE)
**Objectif:** Rendre l'application configurable

**Tâches:**
1. ✅ Créer `core/config.py` (gestionnaire de configuration)
2. ✅ Créer `config.yaml` (configuration par défaut)
3. ✅ Créer `ui/settings_dialog.py` (dialogue de paramètres)
4. ✅ Intégrer avec les modules existants

**Livrables:**
- `core/config.py` (150 lignes)
- `config.yaml` (50 lignes)
- `ui/settings_dialog.py` (200 lignes)

**Durée estimée:** 2-3 heures

---

### **Étape 4: Refactorisation des Modules** (Priorité: MOYENNE)
**Objectif:** Intégrer le Logger dans tous les modules

**Tâches:**
1. ✅ Refactoriser `parser.py` avec Logger
2. ✅ Refactoriser `organizer.py` avec Logger
3. ✅ Refactoriser `monitor.py` avec Logger
4. ✅ Refactoriser `automation.py` (unifier auto_saver + process_activator)
5. ✅ Mettre à jour les tests

**Livrables:**
- Modules refactorisés avec logging intégré
- Tests mis à jour

**Durée estimée:** 4-5 heures

---

### **Étape 5: Interface Principale V2** (Priorité: BASSE)
**Objectif:** Moderniser l'interface principale

**Tâches:**
1. ✅ Créer `ui/main_window.py` (nouvelle interface)
2. ✅ Intégrer le debug panel
3. ✅ Ajouter les thèmes (clair/sombre)
4. ✅ Ajouter les raccourcis clavier
5. ✅ Améliorer l'UX

**Livrables:**
- `ui/main_window.py` (400 lignes)
- `ui/themes/` (thèmes)

**Durée estimée:** 5-6 heures

---

### **Étape 6: Tests et Documentation** (Priorité: BASSE)
**Objectif:** Finaliser la V2

**Tâches:**
1. ✅ Tests unitaires complets
2. ✅ Documentation complète
3. ✅ Guide de migration V1→V2
4. ✅ Vidéo de démonstration

**Livrables:**
- Tests complets (>80% coverage)
- Documentation complète
- Guide de migration

**Durée estimée:** 3-4 heures

---

## 🎓 Approche Pédagogique (Étape par Étape)

Comme tu veux **apprendre**, nous allons procéder par **petites étapes** :

### **Session 1: Comprendre le Logging**
1. Expliquer les niveaux de log et leur utilité
2. Créer un logger simple (20 lignes)
3. Tester dans un script de démonstration
4. Ajouter la rotation de fichiers

### **Session 2: Créer le Logger Complet**
1. Implémenter le Singleton pattern
2. Ajouter les callbacks pour l'UI
3. Implémenter le filtrage
4. Créer les tests unitaires

### **Session 3: Interface de Debug Basique**
1. Créer un visualiseur de logs simple (ScrolledText)
2. Connecter au Logger
3. Ajouter les filtres de base
4. Tester en temps réel

### **Session 4: Interface de Debug Avancée**
1. Ajouter les statistiques
2. Ajouter l'export
3. Améliorer le design
4. Intégrer dans l'app principale

### **Session 5+: Suite du développement**
Continuer avec les étapes 3-6 selon ton rythme.

---

## 🚀 Prochaine Étape

**Commençons par l'Étape 1 - Session 1:**

1. Je vais créer un **logger simple** pour que tu comprennes les concepts
2. Nous allons le tester ensemble
3. Puis nous l'améliorerons progressivement

**Question:** Es-tu prêt à commencer avec la création du système de logging ?

---

## 📚 Ressources

### Concepts à Apprendre
- **Logging:** Pourquoi et comment logger
- **Singleton Pattern:** Un seul logger pour toute l'app
- **Observer Pattern:** Callbacks pour l'UI
- **Rotation de fichiers:** Éviter les logs trop gros
- **Threading:** Logs thread-safe

### Documentation Python
- `logging` module (standard library)
- `tkinter.scrolledtext` (pour les logs UI)
- `threading.Lock` (pour thread-safety)

---

## ✅ Résumé

**V1 (Actuel):**
- ✅ Fonctionnel et robuste
- ⚠️ Logs basiques et dispersés
- ⚠️ Configuration hardcodée
- ⚠️ Pas de système de debug avancé

**V2 (Objectif):**
- ✅ Logging professionnel centralisé
- ✅ Interface de debug complète
- ✅ Configuration flexible
- ✅ Architecture propre et testable
- ✅ Expérience utilisateur améliorée

**Approche:**
- 📚 Apprentissage progressif
- 🔧 Développement par étapes
- 🧪 Tests à chaque étape
- 📖 Documentation au fur et à mesure

---

**Prêt à commencer ? 🚀**
