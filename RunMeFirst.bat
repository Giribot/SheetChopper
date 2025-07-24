@echo off

REM Vérifier si Python est installé
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installé. Veuillez installer Python avant d'exécuter ce script.
    pause
    exit /b
)

REM Installer les bibliothèques nécessaires
echo Installation des bibliothèques Python requises...
pip install opencv-python opencv-python-headless numpy >nul 2>&1

REM Vérifier si le fichier Python existe
SET SCRIPT=decoup.py
IF NOT EXIST "%SCRIPT%" (
    echo Le fichier %SCRIPT% est introuvable. Assurez-vous qu'il est dans le même répertoire que ce fichier batch.
    pause
    exit /b
)

REM Exécuter le script Python
echo Exécution du script Python...
python "%SCRIPT%"
pause
