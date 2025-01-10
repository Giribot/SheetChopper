@echo off

:: Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installé sur ce système. Veuillez l'installer et réessayer.
    pause
    exit /b
)

:: Installer les bibliothèques nécessaires
pip install opencv-python pillow numpy

:: Lancer le script Python
python decoup.py

pause
