"""
Module Google Tasks (optionnel) - Gestion des tâches Google
"""
import os
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GoogleTasksManager:
    """Gestionnaire pour Google Tasks API"""
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.service = None
        
        # Google Tasks est toujours en mode démo pour simplifier
        logger.info("Google Tasks module initialized in demo mode")
    
    async def create_task(
        self,
        title: str,
        due_date: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crée une tâche Google
        
        Args:
            title: Titre de la tâche
            due_date: Date d'échéance (YYYY-MM-DD)
            notes: Notes de la tâche
            
        Returns:
            Dict avec le statut et les détails
        """
        logger.info(f"[MOCK] Creating Google Task: {title}")
        
        return {
            "status": "mock",
            "message": f"✅ [DEMO] Tâche Google '{title}' créée",
            "task_id": f"mock_gtask_{datetime.now().timestamp()}",
            "details": {
                "title": title,
                "due_date": due_date or "Pas de date",
                "notes": notes or "Pas de notes"
            }
        }


def get_google_tasks_manager(demo_mode: bool = True) -> GoogleTasksManager:
    """Récupère le gestionnaire Google Tasks"""
    return GoogleTasksManager(demo_mode=demo_mode)
