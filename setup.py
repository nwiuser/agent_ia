"""
Script de setup - Installation et configuration initiale
"""
import os
import sys
import subprocess


def print_step(step: str, status: str = "info"):
    """Affiche une étape avec un symbole"""
    symbols = {
        "info": "ℹ️",
        "success": "✅",
        "error": "❌",
        "warning": "⚠️"
    }
    print(f"{symbols.get(status, 'ℹ️')} {step}")


def check_python_version():
    """Vérifie la version de Python"""
    print_step("Vérification de la version Python...", "info")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print_step(f"Python {version.major}.{version.minor}.{version.micro} détecté", "success")
        return True
    else:
        print_step(f"Python {version.major}.{version.minor} détecté - Version 3.9+ requise", "error")
        return False


def install_requirements():
    """Installe les dépendances"""
    print_step("Installation des dépendances...", "info")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print_step("Dépendances installées avec succès", "success")
        return True
    except subprocess.CalledProcessError:
        print_step("Erreur lors de l'installation des dépendances", "error")
        return False


def create_env_file():
    """Crée le fichier .env s'il n'existe pas"""
    print_step("Configuration du fichier .env...", "info")
    
    if os.path.exists(".env"):
        print_step("Fichier .env déjà existant", "warning")
        return True
    
    try:
        with open(".env.example", "r") as src:
            content = src.read()
        
        with open(".env", "w") as dst:
            dst.write(content)
        
        print_step("Fichier .env créé avec succès", "success")
        return True
    except Exception as e:
        print_step(f"Erreur: {e}", "error")
        return False


def print_instructions():
    """Affiche les instructions finales"""
    print("\n" + "="*60)
    print("  🎉 INSTALLATION TERMINÉE")
    print("="*60 + "\n")
    
    print("📋 PROCHAINES ÉTAPES:\n")
    
    print("1️⃣  MODE DÉMO (Recommandé pour débuter):")
    print("   Le fichier .env est déjà configuré en mode démo")
    print("   Aucune configuration API n'est nécessaire\n")
    
    print("2️⃣  LANCER LE BACKEND:")
    print("   python main.py\n")
    
    print("3️⃣  LANCER L'INTERFACE (dans un nouveau terminal):")
    print("   streamlit run ui/app.py\n")
    
    print("4️⃣  OU TESTER AVEC LE SCRIPT DE DEMO:")
    print("   python demo.py\n")
    
    print("="*60 + "\n")
    
    print("💡 CONFIGURATION AVANCÉE (Optionnel):")
    print("   - Google Calendar: Voir README.md section 'Google Calendar API'")
    print("   - Notion: Voir README.md section 'Notion API'")
    print("   - OpenAI: Voir README.md section 'OpenAI API'\n")


def main():
    """Programme principal"""
    print("\n" + "🚀" * 30)
    print("  ASSISTANT ÉTUDIANT IA - SETUP")
    print("🚀" * 30 + "\n")
    
    # Vérifications
    if not check_python_version():
        sys.exit(1)
    
    # Installation
    if not install_requirements():
        print_step("Essayez manuellement: pip install -r requirements.txt", "warning")
    
    # Configuration
    create_env_file()
    
    # Instructions
    print_instructions()


if __name__ == "__main__":
    main()
