@echo off
REM Script pour lancer l'interface Streamlit

echo ========================================
echo   INTERFACE STREAMLIT
echo ========================================
echo.

REM Activer l'environnement virtuel
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Environnement virtuel active
) else (
    echo [!] Environnement virtuel non trouve
    echo [!] Executez d'abord start.bat
    pause
    exit
)

echo.
echo [*] Demarrage de l'interface Streamlit...
echo [*] L'interface sera accessible sur http://localhost:8501
echo.
echo [i] Assurez-vous que le backend est lance (start.bat)
echo.
echo ========================================
echo.

streamlit run ui/app.py

pause
