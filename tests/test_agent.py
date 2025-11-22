"""
Tests unitaires pour l'Assistant Étudiant IA
"""
import pytest
from datetime import datetime, timedelta
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import UserQuery, ActionResult
from llm import LLMParser
from action_runner import ActionRunner


class TestLLMParser:
    """Tests pour le parser LLM"""
    
    @pytest.fixture
    def parser(self):
        """Fixture pour créer un parser en mode demo"""
        return LLMParser(demo_mode=True)
    
    @pytest.mark.asyncio
    async def test_parse_simple_event(self, parser):
        """Test parsing d'un événement simple"""
        query = "Ajoute un examen de maths mardi à 10h"
        result = await parser.parse_query(query)
        
        assert "tasks" in result
        assert len(result["tasks"]) > 0
        
        task = result["tasks"][0]
        assert task["action"] == "create_event"
        assert task["app"] == "google_calendar"
        assert "maths" in task["title"].lower()
    
    @pytest.mark.asyncio
    async def test_parse_event_with_notion(self, parser):
        """Test parsing événement + page Notion"""
        query = "Ajoute un examen de maths mardi à 10h et crée une page Notion pour réviser"
        result = await parser.parse_query(query)
        
        assert len(result["tasks"]) >= 2
        
        # Vérifier l'événement
        event_task = next(t for t in result["tasks"] if t["action"] == "create_event")
        assert event_task["app"] == "google_calendar"
        
        # Vérifier la page Notion
        notion_task = next(t for t in result["tasks"] if t["action"] == "create_page")
        assert notion_task["app"] == "notion"
    
    @pytest.mark.asyncio
    async def test_parse_task_creation(self, parser):
        """Test parsing de création de tâche"""
        query = "Ajoute une tâche urgente pour rendre le projet vendredi"
        result = await parser.parse_query(query)
        
        assert "tasks" in result
        task = result["tasks"][0]
        
        assert task["action"] == "create_task"
        assert task["priority"] == "high"
    
    def test_extract_datetime_tomorrow(self, parser):
        """Test extraction date pour 'demain'"""
        query = "Ajoute un cours demain à 14h30"
        date_str, time_str = parser._extract_datetime(query)
        
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        assert date_str == tomorrow
        assert time_str == "14:30"
    
    def test_extract_datetime_day_of_week(self, parser):
        """Test extraction pour jour de la semaine"""
        query = "Ajoute un cours mardi à 10h"
        date_str, time_str = parser._extract_datetime(query)
        
        assert time_str == "10:00"
        # La date devrait être un mardi futur
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        assert parsed_date.weekday() == 1  # 1 = mardi


class TestActionRunner:
    """Tests pour l'exécuteur d'actions"""
    
    @pytest.fixture
    def runner(self):
        """Fixture pour créer un action runner en mode demo"""
        return ActionRunner(demo_mode=True)
    
    @pytest.mark.asyncio
    async def test_execute_calendar_event(self, runner):
        """Test création d'événement Google Calendar"""
        tasks_json = {
            "tasks": [
                {
                    "action": "create_event",
                    "app": "google_calendar",
                    "title": "Test Exam",
                    "date": "2025-01-20",
                    "time": "10:00",
                    "duration_minutes": 60
                }
            ]
        }
        
        results = await runner.execute_tasks(tasks_json)
        
        assert len(results) == 1
        assert results[0].status in ["success", "mock"]
        assert results[0].app == "google_calendar"
    
    @pytest.mark.asyncio
    async def test_execute_notion_page(self, runner):
        """Test création de page Notion"""
        tasks_json = {
            "tasks": [
                {
                    "action": "create_page",
                    "app": "notion",
                    "title": "Test Page",
                    "content": "Test content"
                }
            ]
        }
        
        results = await runner.execute_tasks(tasks_json)
        
        assert len(results) == 1
        assert results[0].status in ["success", "mock"]
        assert results[0].app == "notion"
    
    @pytest.mark.asyncio
    async def test_execute_notion_task(self, runner):
        """Test création de tâche Notion"""
        tasks_json = {
            "tasks": [
                {
                    "action": "create_task",
                    "app": "notion",
                    "title": "Test Task",
                    "priority": "high",
                    "due_date": "2025-01-20"
                }
            ]
        }
        
        results = await runner.execute_tasks(tasks_json)
        
        assert len(results) == 1
        assert results[0].status in ["success", "mock"]
    
    @pytest.mark.asyncio
    async def test_execute_multiple_tasks(self, runner):
        """Test exécution de plusieurs tâches"""
        tasks_json = {
            "tasks": [
                {
                    "action": "create_event",
                    "app": "google_calendar",
                    "title": "Exam",
                    "date": "2025-01-20",
                    "time": "10:00"
                },
                {
                    "action": "create_page",
                    "app": "notion",
                    "title": "Notes"
                }
            ]
        }
        
        results = await runner.execute_tasks(tasks_json)
        
        assert len(results) == 2
        assert all(r.status in ["success", "mock", "error"] for r in results)
    
    @pytest.mark.asyncio
    async def test_execute_invalid_action(self, runner):
        """Test avec une action invalide"""
        tasks_json = {
            "tasks": [
                {
                    "action": "invalid_action",
                    "app": "google_calendar",
                    "title": "Test"
                }
            ]
        }
        
        results = await runner.execute_tasks(tasks_json)
        
        assert len(results) == 1
        assert results[0].status == "error"


class TestModels:
    """Tests pour les modèles Pydantic"""
    
    def test_user_query_model(self):
        """Test modèle UserQuery"""
        query = UserQuery(query="Test query")
        assert query.query == "Test query"
    
    def test_action_result_model(self):
        """Test modèle ActionResult"""
        result = ActionResult(
            action="create_event",
            app="google_calendar",
            status="success",
            message="Event created"
        )
        
        assert result.action == "create_event"
        assert result.app == "google_calendar"
        assert result.status == "success"


class TestIntegration:
    """Tests d'intégration"""
    
    @pytest.mark.asyncio
    async def test_full_pipeline(self):
        """Test du pipeline complet"""
        # Parse
        parser = LLMParser(demo_mode=True)
        query = "Ajoute un examen de maths mardi à 10h"
        parsed = await parser.parse_query(query)
        
        # Execute
        runner = ActionRunner(demo_mode=True)
        results = await runner.execute_tasks(parsed)
        
        # Verify
        assert len(results) > 0
        assert all(r.status in ["success", "mock", "error"] for r in results)


def run_tests():
    """Lance les tests"""
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])


if __name__ == "__main__":
    run_tests()
