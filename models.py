"""
Modèles Pydantic pour définir les structures de données utilisées par l'agent
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class Action(BaseModel):
    """Modèle de base pour une action à exécuter"""
    action: Literal[
        "create_event", 
        "create_page", 
        "create_task",
        "update_event",
        "delete_event"
    ] = Field(..., description="Type d'action à exécuter")
    app: Literal["google_calendar", "notion", "google_tasks"] = Field(
        ..., description="Application cible"
    )


class GoogleCalendarAction(Action):
    """Action pour Google Calendar"""
    app: Literal["google_calendar"] = "google_calendar"
    title: str = Field(..., description="Titre de l'événement")
    date: str = Field(..., description="Date au format YYYY-MM-DD")
    time: str = Field(..., description="Heure au format HH:MM")
    duration_minutes: Optional[int] = Field(60, description="Durée en minutes")
    description: Optional[str] = Field(None, description="Description de l'événement")
    location: Optional[str] = Field(None, description="Lieu de l'événement")


class NotionPageAction(Action):
    """Action pour créer une page Notion"""
    app: Literal["notion"] = "notion"
    action: Literal["create_page"] = "create_page"
    title: str = Field(..., description="Titre de la page")
    content: Optional[str] = Field(None, description="Contenu de la page")
    database_id: Optional[str] = Field(None, description="ID de la base de données")


class NotionTaskAction(Action):
    """Action pour créer une tâche Notion"""
    app: Literal["notion"] = "notion"
    action: Literal["create_task"] = "create_task"
    title: str = Field(..., description="Titre de la tâche")
    due_date: Optional[str] = Field(None, description="Date d'échéance YYYY-MM-DD")
    priority: Optional[Literal["low", "medium", "high"]] = Field(
        "medium", description="Priorité de la tâche"
    )
    description: Optional[str] = Field(None, description="Description de la tâche")


class TaskList(BaseModel):
    """Liste des tâches à exécuter"""
    tasks: List[Action] = Field(..., description="Liste des actions à effectuer")


class UserQuery(BaseModel):
    """Requête utilisateur"""
    query: str = Field(..., description="Instruction en langage naturel")


class ActionResult(BaseModel):
    """Résultat de l'exécution d'une action"""
    action: str
    app: str
    status: Literal["success", "error", "mock"]
    message: str
    details: Optional[dict] = None


class AgentResponse(BaseModel):
    """Réponse complète de l'agent"""
    query: str
    parsed_tasks: dict
    results: List[ActionResult]
    execution_time: float
