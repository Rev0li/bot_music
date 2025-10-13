@echo off
chcp 65001 > nul
echo.
echo ========================================
echo   SongSurf Dashboard
echo ========================================
echo.
echo Demarrage du serveur...
echo.
cd python-server
python app.py
pause
