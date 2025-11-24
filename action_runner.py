"""
Module Action Runner - Exécute les actions parsées par le LLM
"""
from typing import Dict, Any, List
import logging
from datetime import datetime

from models import ActionResult
from actions.notion import get_notion_manager

logger = logging.getLogger(__name__)


class ActionRunner:
    """Exécute les actions définies dans le JSON"""
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.notion_manager = get_notion_manager(demo_mode)
    
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
        
        # Router vers le bon gestionnaire - Tout utilise Notion maintenant
        if app in ["notion", "notion_calendar", "calendar", "tasks"]:
            return await self._handle_notion_action(action, task)
        else:
            return ActionResult(
                action=action,
                app=app,
                status="error",
                message=f"Application inconnue: {app}"
            )
    

    
    async def _handle_notion_action(self, action: str, task: Dict[str, Any]) -> ActionResult:
        """Gère toutes les actions Notion (pages, tâches, événements)"""
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
            elif action == "create_event":
                # Créer un événement comme une tâche avec date/heure
                title = task.get("title")
                date = task.get("date")
                time = task.get("time")
                result = await self.notion_manager.create_task(
                    title=f"📅 {title}",
                    due_date=date,
                    priority="medium",
                    description=f"Événement le {date} à {time}\n{task.get('description', '')}"
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
