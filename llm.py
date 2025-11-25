import os
import json
import re
from typing import Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class LLMParser:
    """Parse les requêtes utilisateur et les convertit en actions structurées"""
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.demo_mode and not self.openai_api_key:
            logger.warning("OpenAI API key not found. Falling back to demo mode.")
            self.demo_mode = True
    
    async def parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse une requête utilisateur et retourne un JSON structuré
        
        Args:
            query: La requête en langage naturel
            
        Returns:
            Dict contenant les tasks à exécuter
        """
        if self.demo_mode:
            return self._mock_parse(query)
        else:
            return await self._openai_parse(query)
    
    def _mock_parse(self, query: str) -> Dict[str, Any]:
        """
        Mode mock pour démo - analyse basique des mots-clés avec priorités
        """
        logger.info(f"Mock parsing query: {query}")
        query_lower = query.lower()
        tasks = []
        
        # Détection par ordre de priorité (une seule action principale)
        
        # 1. Priorité haute : Événements (avec date/heure)
        if any(word in query_lower for word in ["examen", "cours", "rdv", "rendez-vous", "réunion", "meeting", "événement", "event"]):
            event_task = self._extract_event(query)
            if event_task:
                tasks.append(event_task)
                return {"tasks": tasks}  # Retourner directement
        
        # 2. Priorité moyenne : Tâches explicites
        if any(word in query_lower for word in ["tâche", "tache", "todo", "à faire", "a faire", "task", "ajoute", "crée une"]):
            # Vérifier que ce n'est pas une demande de page
            if not any(word in query_lower for word in ["page", "document"]):
                task_item = self._extract_notion_task(query)
                if task_item:
                    tasks.append(task_item)
                    return {"tasks": tasks}  # Retourner directement
        
        # 3. Priorité basse : Pages Notion
        if any(word in query_lower for word in ["page", "note", "document"]):
            page_task = self._extract_notion_page(query)
            if page_task:
                tasks.append(page_task)
                return {"tasks": tasks}  # Retourner directement
        
        # 4. Par défaut : Créer une tâche simple
        if not tasks:
            tasks.append({
                "action": "create_task",
                "app": "notion",
                "title": query[:100],
                "priority": "medium",
                "description": query
            })
        
        return {"tasks": tasks}
    
    def _extract_event(self, query: str) -> Dict[str, Any]:
        """Extrait les informations d'un événement"""
        # Extraction du titre
        title_match = re.search(r'(examen|cours|rdv|rendez-vous|réunion|meeting)\s+(?:de\s+)?([^à]+)', query, re.IGNORECASE)
        title = title_match.group(2).strip() if title_match else "Événement"
        
        # Extraction de la date
        date_str, time_str = self._extract_datetime(query)
        
        # Extraction de la durée
        duration = 60
        duration_match = re.search(r'(\d+)\s*(heure|h|minute|min)', query, re.IGNORECASE)
        if duration_match:
            value = int(duration_match.group(1))
            unit = duration_match.group(2).lower()
            if 'h' in unit:
                duration = value * 60
            else:
                duration = value
        
        return {
            "action": "create_event",
            "app": "notion",
            "title": title,
            "date": date_str,
            "time": time_str,
            "duration_minutes": duration,
            "description": query
        }
    
    def _extract_notion_page(self, query: str) -> Dict[str, Any]:
        """Extrait les informations d'une page Notion"""
        # Extraction du titre
        title_match = re.search(r'page\s+(?:notion\s+)?(?:pour\s+)?([^\.]+)', query, re.IGNORECASE)
        if not title_match:
            title_match = re.search(r'crée\s+(?:une\s+)?([^\s]+(?:\s+\w+){0,3})', query, re.IGNORECASE)
        
        title = title_match.group(1).strip() if title_match else "Nouvelle page"
        
        # Extraction du contenu
        content_match = re.search(r'(?:contenu|avec|pour)\s+["\']?([^"\'\.]+)["\']?', query, re.IGNORECASE)
        content = content_match.group(1).strip() if content_match else ""
        
        return {
            "action": "create_page",
            "app": "notion",
            "title": title,
            "content": content or query
        }
    
    def _extract_notion_task(self, query: str) -> Dict[str, Any]:
        """Extrait les informations d'une tâche Notion"""
        # Extraction du titre
        title_match = re.search(r'(?:tâche|tache|todo|task)[\s:]+([^\.]+)', query, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else query
        
        # Extraction de la date d'échéance
        date_str, _ = self._extract_datetime(query)
        
        # Extraction de la priorité
        priority = "medium"
        if any(word in query.lower() for word in ["urgent", "important", "haute", "high"]):
            priority = "high"
        elif any(word in query.lower() for word in ["basse", "low"]):
            priority = "low"
        
        return {
            "action": "create_task",
            "app": "notion",
            "title": title,
            "due_date": date_str,
            "priority": priority,
            "description": query
        }
    
    def _extract_datetime(self, query: str) -> tuple[str, str]:
        """Extrait la date et l'heure d'une requête"""
        # Jours de la semaine
        today = datetime.now()
        
        days_map = {
            "lundi": 0, "mardi": 1, "mercredi": 2, "jeudi": 3,
            "vendredi": 4, "samedi": 5, "dimanche": 6
        }
        
        # Détection jour de la semaine
        for day_name, day_num in days_map.items():
            if day_name in query.lower():
                current_day = today.weekday()
                days_ahead = (day_num - current_day) % 7
                if days_ahead == 0:
                    days_ahead = 7  # Semaine prochaine
                target_date = today + timedelta(days=days_ahead)
                date_str = target_date.strftime("%Y-%m-%d")
                break
        else:
            # Mots clés temporels
            if "demain" in query.lower():
                target_date = today + timedelta(days=1)
                date_str = target_date.strftime("%Y-%m-%d")
            elif "après-demain" in query.lower() or "apres-demain" in query.lower():
                target_date = today + timedelta(days=2)
                date_str = target_date.strftime("%Y-%m-%d")
            else:
                # Date par défaut: demain
                target_date = today + timedelta(days=1)
                date_str = target_date.strftime("%Y-%m-%d")
        
        # Extraction de l'heure
        time_match = re.search(r'(\d{1,2})[h:](\d{2})?', query, re.IGNORECASE)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            time_str = f"{hour:02d}:{minute:02d}"
        else:
            time_str = "10:00"  # Heure par défaut
        
        return date_str, time_str
    
    async def _openai_parse(self, query: str) -> Dict[str, Any]:
        """
        Parse avec OpenAI GPT (mode production)
        """
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(api_key=self.openai_api_key)
            
            system_prompt = """Tu es un assistant qui convertit des requêtes en langage naturel en JSON structuré.
            
Les actions possibles sont:
- create_event (Google Calendar): nécessite title, date (YYYY-MM-DD), time (HH:MM), duration_minutes (optionnel)
- create_page (Notion): nécessite title, content (optionnel)
- create_task (Notion): nécessite title, due_date (optionnel), priority (low/medium/high)

Réponds UNIQUEMENT avec un JSON valide au format:
{
  "tasks": [
    {
      "action": "create_event",
      "app": "google_calendar",
      "title": "...",
      "date": "2025-01-20",
      "time": "10:00",
      "duration_minutes": 60
    }
  ]
}
"""
            
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            
            # Nettoyer le JSON si nécessaire
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"OpenAI parsing error: {e}")
            # Fallback vers le mock
            return self._mock_parse(query)


# Instance globale
llm_parser = None


def get_llm_parser(demo_mode: bool = None) -> LLMParser:
    """Récupère ou crée l'instance du parser LLM"""
    global llm_parser
    
    if demo_mode is None:
        demo_mode = os.getenv("DEMO_MODE", "True").lower() == "true"
    
    if llm_parser is None:
        llm_parser = LLMParser(demo_mode=demo_mode)
    
    return llm_parser
