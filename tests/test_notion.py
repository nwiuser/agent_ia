"""
Script de test pour l'intégration Notion
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Ajouter le répertoire parent au path pour l'import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actions.notion import get_notion_manager

# Charger les variables d'environnement
load_dotenv()

async def test_notion():
    """Test des fonctionnalités Notion"""
    
    # Obtenir le gestionnaire Notion
    notion = get_notion_manager()
    
    print("=" * 60)
    print("🧪 TEST INTÉGRATION NOTION")
    print("=" * 60)
    print(f"Mode: {'DEMO' if notion.demo_mode else 'PRODUCTION'}")
    print()
    
    # Test 1: Créer une page
    print("📝 Test 1: Création d'une page Notion")
    print("-" * 60)
    result1 = await notion.create_page(
        title="Plan de révision Mathématiques",
        content="Chapitre 1: Algèbre\nChapitre 2: Géométrie\nChapitre 3: Analyse"
    )
    print(f"Status: {result1['status']}")
    print(f"Message: {result1['message']}")
    if 'page_url' in result1:
        print(f"URL: {result1['page_url']}")
    if 'details' in result1:
        print(f"Détails: {result1['details']}")
    print()
    
    # Test 2: Créer une tâche avec priorité haute
    print("✅ Test 2: Création d'une tâche prioritaire")
    print("-" * 60)
    result2 = await notion.create_task(
        title="Rendre le projet de physique",
        due_date="2025-11-30",
        priority="high",
        description="Rapport final + code Python + présentation"
    )
    print(f"Status: {result2['status']}")
    print(f"Message: {result2['message']}")
    if 'task_url' in result2:
        print(f"URL: {result2['task_url']}")
    if 'details' in result2:
        print(f"Détails: {result2['details']}")
    print()
    
    # Test 3: Créer une tâche simple
    print("📌 Test 3: Création d'une tâche simple")
    print("-" * 60)
    result3 = await notion.create_task(
        title="Réviser le cours de Python",
        priority="medium"
    )
    print(f"Status: {result3['status']}")
    print(f"Message: {result3['message']}")
    if 'details' in result3:
        print(f"Détails: {result3['details']}")
    print()
    
    print("=" * 60)
    print("✨ Tests terminés!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_notion())
