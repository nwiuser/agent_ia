@echo off
REM Script de lancement rapide pour Windows

echo ========================================
echo   ASSISTANT ETUDIANT IA - LANCEMENT
echo ========================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\" (
    echo [!] Environnement virtuel non trouve
    echo [*] Creation de l'environnement virtuel...
    python -m venv venv
    echo [OK] Environnement virtuel cree
    echo.
)

REM Activer l'environnement virtuel
echo [*] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer/Mettre à jour les dépendances
echo [*] Installation des dependances...
pip install -r requirements.txt --quiet
echo [OK] Dependances installees
echo.

REM Vérifier le fichier .env
if not exist ".env" (
    echo [!] Fichier .env non trouve
    echo [*] Creation du fichier .env...
    copy .env.example .env
    echo [OK] Fichier .env cree
    echo.
)

echo ========================================
echo   DEMARRAGE DU BACKEND
echo ========================================
echo.
echo [*] Le backend va demarrer sur http://localhost:8000
echo [*] Documentation API : http://localhost:8000/docs
echo.
echo [i] Pour lancer l'interface Streamlit, ouvrez un nouveau terminal et executez:
echo     streamlit run ui/app.py
echo.
echo ========================================
echo.

REM Lancer le backend
python main.py

pause
