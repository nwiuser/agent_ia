"""
Script de démonstration - Test de l'API
"""
import requests
import json
from typing import Dict, Any


def print_section(title: str):
    """Affiche une section formatée"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def test_health():
    """Test du endpoint health"""
    print_section("TEST: Health Check")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_query(query: str):
    """Test d'une requête"""
    print_section(f"TEST: {query}")
    
    try:
        response = requests.post(
            "http://localhost:8000/run",
            json={"query": query},
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        result = response.json()
        
        print("\n📝 Requête originale:")
        print(f"  {result['query']}")
        
        print("\n🔧 JSON Parsé:")
        print(json.dumps(result['parsed_tasks'], indent=2, ensure_ascii=False))
        
        print("\n✅ Résultats:")
        for i, action_result in enumerate(result['results'], 1):
            status_icon = "✅" if action_result['status'] in ['success', 'mock'] else "❌"
            print(f"  {status_icon} Action {i}: {action_result['message']}")
        
        print(f"\n⏱️ Temps d'exécution: {result['execution_time']:.2f}s")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Programme principal"""
    print("\n" + "🎓" * 30)
    print("  ASSISTANT ÉTUDIANT IA - DÉMONSTRATION")
    print("🎓" * 30)
    
    # Test de santé
    if not test_health():
        print("\n❌ L'API n'est pas accessible. Lancez le backend avec: python main.py")
        return
    
    # Tests des requêtes
    test_queries = [
        "Ajoute un examen de maths mardi à 10h",
        "Ajoute un examen de maths mardi à 10h et crée une page Notion pour réviser",
        "Crée une tâche urgente pour rendre le projet vendredi",
        "Planifie une réunion de groupe jeudi à 16h",
        "Ajoute un cours de physique demain à 14h30 durant 2 heures"
    ]
    
    for query in test_queries:
        test_query(query)
        input("\n⏸️  Appuyez sur Entrée pour continuer...")
    
    print_section("FIN DE LA DÉMONSTRATION")
    print("✅ Tous les tests sont terminés!")
    print("\n💡 Conseil: Lancez l'interface Streamlit pour une meilleure expérience:")
    print("   streamlit run ui/app.py\n")


if __name__ == "__main__":
    main()
