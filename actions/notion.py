import os
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NotionManager:
    """Gestionnaire pour Notion API"""
    
    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY")
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.client = None
        self._client_initialized = False
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Notion client"""
        try:
            from notion_client import AsyncClient
            
            if not self.api_key:
                raise ValueError("NOTION_API_KEY not found in environment")
            
            self.client = AsyncClient(auth=self.api_key)
            self._client_initialized = True
            logger.info("Notion client initialized")
            
        except Exception as e:
            logger.error(f"Error initializing Notion client: {e}")
            raise
    
    async def __aenter__(self):
        """Context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        await self.close()
    
    async def close(self):
        """Close the Notion client properly"""
        if self.client and self._client_initialized:
            try:
                await self.client.aclose()
                logger.debug("Notion client closed")
            except Exception as e:
                # Ignore errors during cleanup
                logger.debug(f"Error closing Notion client: {e}")
            finally:
                self._client_initialized = False
    
  
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
        try:
            if not self.database_id:
                return {
                    "status": "error",
                    "message": "Database ID not configured for tasks"
                }
            
            # Structure de base de la tâche
            new_task = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "Name": {
                        "title": [{"text": {"content": title}}]
                    }
                }
            }
            
            # Ajouter date si présente
            if due_date:
                new_task["properties"]["Due Date"] = {"date": {"start": due_date}}
            
            # Ajouter statut par défaut
            new_task["properties"]["Status"] = {"select": {"name": "Not started"}}
            
            # Ajouter priorité
            priority_values = {"low": "Low", "medium": "Medium", "high": "High"}
            new_task["properties"]["Priority"] = {
                "select": {"name": priority_values.get(priority.lower(), "Medium")}
            }
            
            # Ajouter description si présente
            if description:
                new_task["children"] = [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": description}}]
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


# Instance globale
_notion_manager = None


def get_notion_manager() -> NotionManager:
    """Récupère ou crée l'instance du gestionnaire Notion"""
    global _notion_manager
    
    # Force refresh pour éviter le cache
    _notion_manager = None
    
    if _notion_manager is None:
        _notion_manager = NotionManager()
    
    return _notion_manager
