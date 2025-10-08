# Script d'installation des dépendances
# Music Organizer Pro

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation des dependances" -ForegroundColor Cyan
Write-Host "Music Organizer Pro" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/4] Mise a jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host ""

Write-Host "[2/4] Installation de mutagen..." -ForegroundColor Yellow
pip install mutagen>=1.45.1
Write-Host ""

Write-Host "[3/4] Installation de pyautogui et pyperclip..." -ForegroundColor Yellow
pip install pyautogui>=0.9.53 pyperclip>=1.8.2
Write-Host ""

Write-Host "[4/4] Installation de pywin32..." -ForegroundColor Yellow
pip install pywin32>=305
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verification de l'installation..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérification mutagen
try {
    python -c "import mutagen"
    Write-Host "[OK] mutagen installe" -ForegroundColor Green
} catch {
    Write-Host "[ERREUR] mutagen manquant" -ForegroundColor Red
}

# Vérification pyautogui
try {
    python -c "import pyautogui"
    Write-Host "[OK] pyautogui installe" -ForegroundColor Green
} catch {
    Write-Host "[ERREUR] pyautogui manquant" -ForegroundColor Red
}

# Vérification pyperclip
try {
    python -c "import pyperclip"
    Write-Host "[OK] pyperclip installe" -ForegroundColor Green
} catch {
    Write-Host "[ERREUR] pyperclip manquant" -ForegroundColor Red
}

# Vérification pywin32
try {
    python -c "import win32gui"
    Write-Host "[OK] pywin32 installe" -ForegroundColor Green
} catch {
    Write-Host "[ERREUR] pywin32 manquant" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation terminee!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Lancez l'application avec: python app.py" -ForegroundColor Yellow
Write-Host ""
