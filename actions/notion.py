"""
Module Notion - Gestion des pages et tâches
"""
import os
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NotionManager:
    """Gestionnaire pour Notion API"""
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.api_key = os.getenv("NOTION_API_KEY")
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.client = None
        
        if not demo_mode:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Notion client"""
        try:
            from notion_client import AsyncClient
            
            if not self.api_key:
                logger.error("NOTION_API_KEY not found in environment")
                logger.info("Falling back to demo mode")
                self.demo_mode = True
                return
            
            self.client = AsyncClient(auth=self.api_key)
            logger.info("Notion client initialized")
            
        except Exception as e:
            logger.error(f"Error initializing Notion client: {e}")
            logger.info("Falling back to demo mode")
            self.demo_mode = True
    
    async def create_page(
        self,
        title: str,
        content: Optional[str] = None,
        database_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crée une page dans Notion
        
        Args:
            title: Titre de la page
            content: Contenu de la page
            database_id: ID de la base de données (optionnel)
            
        Returns:
            Dict avec le statut et les détails
        """
        if self.demo_mode:
            return self._mock_create_page(title, content)
        
        try:
            db_id = database_id or self.database_id
            
            if not db_id:
                return {
                    "status": "error",
                    "message": "Database ID not configured"
                }
            
            # Créer la page
            new_page = {
                "parent": {"database_id": db_id},
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": title
                                }
                            }
                        ]
                    }
                }
            }
            
            # Ajouter le contenu si présent
            if content:
                new_page["children"] = [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": content
                                    }
                                }
                            ]
                        }
                    }
                ]
            
            response = await self.client.pages.create(**new_page)
            
            logger.info(f"Page created: {response.get('url')}")
            
            return {
                "status": "success",
                "message": f"Page '{title}' créée avec succès",
                "page_id": response.get("id"),
                "page_url": response.get("url")
            }
            
        except Exception as e:
            logger.error(f"Error creating Notion page: {e}")
            return {
                "status": "error",
                "message": f"Erreur lors de la création de la page: {str(e)}"
            }
    
    def _mock_create_page(self, title: str, content: Optional[str]) -> Dict[str, Any]:
        """Version mock pour la démonstration"""
        logger.info(f"[MOCK] Creating Notion page: {title}")
        
        return {
            "status": "mock",
            "message": f"✅ [DEMO] Page Notion '{title}' créée",
            "page_id": f"mock_page_{datetime.now().timestamp()}",
            "page_url": "https://www.notion.so/",
            "details": {
                "title": title,
                "content": content or "Pas de contenu"
            }
        }
    
    async def create_task(
        self,
        title: str,
        due_date: Optional[str] = None,
        priority: str = "medium",
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crée une tâche dans Notion
        
        Args:
            title: Titre de la tâche
            due_date: Date d'échéance (YYYY-MM-DD)
            priority: Priorité (low, medium, high)
            description: Description de la tâche
            
        Returns:
            Dict avec le statut et les détails
        """
        if self.demo_mode:
            return self._mock_create_task(title, due_date, priority, description)
        
        try:
            if not self.database_id:
                return {
                    "status": "error",
                    "message": "Database ID not configured for tasks"
                }
            
            # Créer la tâche
            new_task = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": title
                                }
                            }
                        ]
                    },
                    "Status": {
                        "select": {
                            "name": "À faire"
                        }
                    }
                }
            }
            
            # Ajouter la date d'échéance si présente
            if due_date:
                new_task["properties"]["Due Date"] = {
                    "date": {
                        "start": due_date
                    }
                }
            
            # Ajouter la priorité
            priority_map = {
                "low": "Basse",
                "medium": "Moyenne",
                "high": "Haute"
            }
            
            new_task["properties"]["Priority"] = {
                "select": {
                    "name": priority_map.get(priority, "Moyenne")
                }
            }
            
            # Ajouter la description si présente
            if description:
                new_task["children"] = [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": description
                                    }
                                }
                            ]
                        }
                    }
                ]
            
            response = await self.client.pages.create(**new_task)
            
            logger.info(f"Task created: {response.get('url')}")
            
            return {
                "status": "success",
                "message": f"Tâche '{title}' créée avec succès",
                "task_id": response.get("id"),
                "task_url": response.get("url")
            }
            
        except Exception as e:
            logger.error(f"Error creating Notion task: {e}")
            return {
                "status": "error",
                "message": f"Erreur lors de la création de la tâche: {str(e)}"
            }
    
    def _mock_create_task(
        self,
        title: str,
        due_date: Optional[str],
        priority: str,
        description: Optional[str]
    ) -> Dict[str, Any]:
        """Version mock pour la démonstration"""
        logger.info(f"[MOCK] Creating Notion task: {title}")
        
        priority_emoji = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🔴"
        }
        
        return {
            "status": "mock",
            "message": f"✅ [DEMO] Tâche Notion '{title}' créée",
            "task_id": f"mock_task_{datetime.now().timestamp()}",
            "task_url": "https://www.notion.so/",
            "details": {
                "title": title,
                "due_date": due_date or "Pas de date",
                "priority": f"{priority_emoji.get(priority, '🟡')} {priority}",
                "description": description or "Pas de description"
            }
        }


# Instance globale
_notion_manager = None


def get_notion_manager(demo_mode: bool = None) -> NotionManager:
    """Récupère ou crée l'instance du gestionnaire Notion"""
    global _notion_manager
    
    if demo_mode is None:
        demo_mode = os.getenv("DEMO_MODE", "True").lower() == "true"
    
    if _notion_manager is None:
        _notion_manager = NotionManager(demo_mode=demo_mode)
    
    return _notion_manager
