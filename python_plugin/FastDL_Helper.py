import pyautogui
import time
import pygetwindow as gw

# Chemin cible
destination = r"C:\Users\Molim\Music\DlRevo"

print("[FastDL Helper] En attente d'une fenêtre de téléchargement...")

# Attente de la fenêtre Windows "Enregistrer sous"
target_window = None
while not target_window:
    time.sleep(1)
    for win in gw.getWindowsWithTitle("Enregistrer sous"):
        if win.isActive or win.isVisible:
            target_window = win
            break

print("[FastDL Helper] Fenêtre détectée :", target_window.title)

# Saisir le chemin
time.sleep(0.5)
pyautogui.write(destination)
pyautogui.press("enter")

# Valider la fenêtre
time.sleep(0.5)
pyautogui.press("enter")

print("[FastDL Helper] Fichier en cours de téléchargement.")
