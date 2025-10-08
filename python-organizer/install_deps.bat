@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║           Music Organizer Pro - Installation              ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH
    echo.
    echo Téléchargez Python depuis: https://www.python.org/downloads/
    echo N'oubliez pas de cocher "Add Python to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)

echo [✓] Python détecté
python --version
echo.

REM Mise à jour de pip
echo ┌────────────────────────────────────────────────────────────┐
echo │ [1/5] Mise à jour de pip...                                │
echo └────────────────────────────────────────────────────────────┘
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [ERREUR] Échec de la mise à jour de pip
    pause
    exit /b 1
)
echo [✓] pip mis à jour
echo.

REM Installation de mutagen
echo ┌────────────────────────────────────────────────────────────┐
echo │ [2/5] Installation de mutagen (tags ID3)...               │
echo └────────────────────────────────────────────────────────────┘
pip install mutagen>=1.45.1 --quiet
if errorlevel 1 (
    echo [ERREUR] Échec de l'installation de mutagen
    pause
    exit /b 1
)
echo [✓] mutagen installé
echo.

REM Installation de pyautogui
echo ┌────────────────────────────────────────────────────────────┐
echo │ [3/5] Installation de pyautogui (automatisation)...       │
echo └────────────────────────────────────────────────────────────┘
pip install pyautogui>=0.9.53 --quiet
if errorlevel 1 (
    echo [ERREUR] Échec de l'installation de pyautogui
    pause
    exit /b 1
)
echo [✓] pyautogui installé
echo.

REM Installation de pyperclip
echo ┌────────────────────────────────────────────────────────────┐
echo │ [4/5] Installation de pyperclip (clipboard)...            │
echo └────────────────────────────────────────────────────────────┘
pip install pyperclip>=1.8.2 --quiet
if errorlevel 1 (
    echo [ERREUR] Échec de l'installation de pyperclip
    pause
    exit /b 1
)
echo [✓] pyperclip installé
echo.

REM Installation de pywin32
echo ┌────────────────────────────────────────────────────────────┐
echo │ [5/5] Installation de pywin32 (détection fenêtres)...     │
echo └────────────────────────────────────────────────────────────┘
pip install pywin32>=305 --quiet
if errorlevel 1 (
    echo [ERREUR] Échec de l'installation de pywin32
    pause
    exit /b 1
)
echo [✓] pywin32 installé
echo.

REM Vérification de l'installation
echo ╔════════════════════════════════════════════════════════════╗
echo ║                  Vérification...                           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

set ERROR_COUNT=0

python -c "import mutagen" 2>nul
if errorlevel 1 (
    echo [✗] mutagen - ERREUR
    set /a ERROR_COUNT+=1
) else (
    echo [✓] mutagen - OK
)

python -c "import pyautogui" 2>nul
if errorlevel 1 (
    echo [✗] pyautogui - ERREUR
    set /a ERROR_COUNT+=1
) else (
    echo [✓] pyautogui - OK
)

python -c "import pyperclip" 2>nul
if errorlevel 1 (
    echo [✗] pyperclip - ERREUR
    set /a ERROR_COUNT+=1
) else (
    echo [✓] pyperclip - OK
)

python -c "import win32gui" 2>nul
if errorlevel 1 (
    echo [✗] pywin32 - ERREUR
    set /a ERROR_COUNT+=1
) else (
    echo [✓] pywin32 - OK
)

python -c "from music_organizer import MetadataParser" 2>nul
if errorlevel 1 (
    echo [✗] music_organizer - ERREUR
    set /a ERROR_COUNT+=1
) else (
    echo [✓] music_organizer - OK
)

echo.

if %ERROR_COUNT% EQU 0 (
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║                                                            ║
    echo ║          ✓ Installation terminée avec succès !            ║
    echo ║                                                            ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo Lancez l'application avec: python app.py
    echo.
) else (
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║                                                            ║
    echo ║     ✗ Installation terminée avec %ERROR_COUNT% erreur(s)              ║
    echo ║                                                            ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo Consultez la documentation: docs\02_INSTALLATION.md
    echo.
)

pause
