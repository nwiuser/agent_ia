"""
Module Action Runner - Exécute les actions parsées par le LLM
"""
from typing import Dict, Any, List
import logging
from datetime import datetime

from models import ActionResult
from actions.google_calendar import get_calendar_manager
from actions.notion import get_notion_manager
from actions.google_tasks import get_google_tasks_manager

logger = logging.getLogger(__name__)


class ActionRunner:
    """Exécute les actions définies dans le JSON"""
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.calendar_manager = get_calendar_manager(demo_mode)
        self.notion_manager = get_notion_manager(demo_mode)
        self.tasks_manager = get_google_tasks_manager(demo_mode)
    
    async def execute_tasks(self, tasks_json: Dict[str, Any]) -> List[ActionResult]:
        """
        Exécute toutes les tâches du JSON
        
        Args:
            tasks_json: Dict contenant la clé "tasks" avec la liste des actions
            
        Returns:
            Liste des résultats d'exécution
        """
        tasks = tasks_json.get("tasks", [])
        results = []
        
        logger.info(f"Executing {len(tasks)} task(s)")
        
        for i, task in enumerate(tasks):
            logger.info(f"Task {i+1}/{len(tasks)}: {task.get('action')} on {task.get('app')}")
            
            try:
                result = await self._execute_single_task(task)
                results.append(result)
            except Exception as e:
                logger.error(f"Error executing task {i+1}: {e}")
                results.append(ActionResult(
                    action=task.get("action", "unknown"),
                    app=task.get("app", "unknown"),
                    status="error",
                    message=f"Erreur: {str(e)}"
                ))
        
        return results
    
    async def _execute_single_task(self, task: Dict[str, Any]) -> ActionResult:
        """
        Exécute une seule tâche
        
        Args:
            task: Dict représentant l'action à effectuer
            
        Returns:
            ActionResult avec le résultat de l'exécution
        """
        action = task.get("action")
        app = task.get("app")
        
        # Router vers le bon gestionnaire
        if app == "google_calendar":
            return await self._handle_calendar_action(action, task)
        elif app == "notion":
            return await self._handle_notion_action(action, task)
        elif app == "google_tasks":
            return await self._handle_google_tasks_action(action, task)
        else:
            return ActionResult(
                action=action,
                app=app,
                status="error",
                message=f"Application inconnue: {app}"
            )
    
    async def _handle_calendar_action(self, action: str, task: Dict[str, Any]) -> ActionResult:
        """Gère les actions Google Calendar"""
        try:
            if action == "create_event":
                result = await self.calendar_manager.create_event(
                    title=task.get("title"),
                    date=task.get("date"),
                    time=task.get("time"),
                    duration_minutes=task.get("duration_minutes", 60),
                    description=task.get("description"),
                    location=task.get("location")
                )
            elif action == "update_event":
                result = await self.calendar_manager.update_event(
                    event_id=task.get("event_id"),
                    **task
                )
            elif action == "delete_event":
                result = await self.calendar_manager.delete_event(
                    event_id=task.get("event_id")
                )
            else:
                result = {
                    "status": "error",
                    "message": f"Action inconnue: {action}"
                }
            
            return ActionResult(
                action=action,
                app="google_calendar",
                status=result.get("status"),
                message=result.get("message"),
                details=result
            )
            
        except Exception as e:
            logger.error(f"Calendar action error: {e}")
            return ActionResult(
                action=action,
                app="google_calendar",
                status="error",
                message=f"Erreur: {str(e)}"
            )
    
    async def _handle_notion_action(self, action: str, task: Dict[str, Any]) -> ActionResult:
        """Gère les actions Notion"""
        try:
            if action == "create_page":
                result = await self.notion_manager.create_page(
                    title=task.get("title"),
                    content=task.get("content"),
                    database_id=task.get("database_id")
                )
            elif action == "create_task":
                result = await self.notion_manager.create_task(
                    title=task.get("title"),
                    due_date=task.get("due_date"),
                    priority=task.get("priority", "medium"),
                    description=task.get("description")
                )
            else:
                result = {
                    "status": "error",
                    "message": f"Action inconnue: {action}"
                }
            
            return ActionResult(
                action=action,
                app="notion",
                status=result.get("status"),
                message=result.get("message"),
                details=result
            )
            
        except Exception as e:
            logger.error(f"Notion action error: {e}")
            return ActionResult(
                action=action,
                app="notion",
                status="error",
                message=f"Erreur: {str(e)}"
            )
    
    async def _handle_google_tasks_action(self, action: str, task: Dict[str, Any]) -> ActionResult:
        """Gère les actions Google Tasks"""
        try:
            if action == "create_task":
                result = await self.tasks_manager.create_task(
                    title=task.get("title"),
                    due_date=task.get("due_date"),
                    notes=task.get("notes")
                )
            else:
                result = {
                    "status": "error",
                    "message": f"Action inconnue: {action}"
                }
            
            return ActionResult(
                action=action,
                app="google_tasks",
                status=result.get("status"),
                message=result.get("message"),
                details=result
            )
            
        except Exception as e:
            logger.error(f"Google Tasks action error: {e}")
            return ActionResult(
                action=action,
                app="google_tasks",
                status="error",
                message=f"Erreur: {str(e)}"
            )


# Instance globale
_action_runner = None


def get_action_runner(demo_mode: bool = None) -> ActionRunner:
    """Récupère ou crée l'instance de l'action runner"""
    global _action_runner
    
    import os
    if demo_mode is None:
        demo_mode = os.getenv("DEMO_MODE", "True").lower() == "true"
    
    if _action_runner is None:
        _action_runner = ActionRunner(demo_mode=demo_mode)
    
    return _action_runner
