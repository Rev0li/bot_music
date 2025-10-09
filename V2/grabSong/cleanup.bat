@echo off
REM Script de nettoyage automatique - GrabSong v1.0

echo ========================================
echo Nettoyage GrabSong v1.0
echo ========================================
echo.

REM Confirmation
set /p confirm="Voulez-vous nettoyer les fichiers obsoletes ? (O/N): "
if /i not "%confirm%"=="O" (
    echo Nettoyage annule.
    pause
    exit /b
)

echo.
echo Nettoyage en cours...
echo.

REM Supprimer les fichiers obsolètes
echo [1/4] Suppression des fichiers Native Messaging...
del /Q native_host.py 2>nul
del /Q com.musicorganizer.grabsong.json 2>nul
del /Q install_native_host.bat 2>nul
del /Q autoclicker.js 2>nul

REM Supprimer les dossiers obsolètes
echo [2/4] Suppression des dossiers obsoletes...
rmdir /S /Q modules 2>nul
rmdir /S /Q _archive 2>nul

REM Supprimer la documentation obsolète
echo [3/4] Suppression de la documentation obsolete...
del /Q DEBUG_NO_DETECTION.md 2>nul
del /Q FIX_PERMISSIONS.md 2>nul
del /Q NEXT_STEPS.md 2>nul
del /Q PROGRESS.md 2>nul
del /Q README.md 2>nul
del /Q READY_TO_TEST.md 2>nul
del /Q SIMPLIFICATION.md 2>nul
del /Q STEP2_CLIPBOARD_MONITOR.md 2>nul
del /Q STEP_BY_STEP_SUMMARY.md 2>nul
del /Q TESTING_GUIDE.md 2>nul
del /Q FIX_UNDERSCORE.md 2>nul
del /Q FIX_OPENTAB.md 2>nul
del /Q FIX_DRAG_CLICK.md 2>nul
del /Q NEW_FEATURES.md 2>nul
del /Q EXPANDABLE_CHAT.md 2>nul
del /Q FINAL_VERSION.md 2>nul
del /Q EDIT_FORM.md 2>nul
del /Q SMOOTH_DRAG.md 2>nul
del /Q PYTHON_INTEGRATION.md 2>nul
del /Q PYTHON_SETUP.md 2>nul

REM Supprimer les fichiers de test
echo [4/4] Suppression des fichiers de test...
del /Q test-*.html 2>nul

echo.
echo ========================================
echo Nettoyage termine !
echo ========================================
echo.
echo Fichiers conserves:
echo - manifest.json
echo - background.js
echo - content.js
echo - popup.html
echo - popup.js
echo - icons/
echo - app.py
echo - requirements.txt
echo - VERSION_1.0_STABLE.md
echo - START_HERE.md
echo - CLEANUP.md
echo - cleanup.bat
echo.

pause
