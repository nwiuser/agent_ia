import os
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class LLMParser:
    """Parse les requêtes utilisateur et les convertit en actions structurées"""
    
    def __init__(self):
        self.meta_api_key = os.getenv("META_API_KEY")
        self.meta_model = os.getenv("META_MODEL", "meta-llama/llama-3.1-8b-instruct")
        
        if not self.meta_api_key:
            raise ValueError("META_API_KEY not found in environment variables")
    
    async def parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse une requête utilisateur avec Meta LLaMA et retourne un JSON structuré
        
        Args:
            query: La requête en langage naturel
            
        Returns:
            Dict contenant les tasks à exécuter
        """
        return await self._meta_parse(query)
    
    async def _meta_parse(self, query: str) -> Dict[str, Any]:
        """
        Parse avec Meta LLaMA via OpenRouter (API REST)
        """
        try:
            import requests
            
            # API REST OpenRouter
            url = "https://openrouter.ai/api/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.meta_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Assistant Agent IA"
            }
            
            system_prompt = """Tu es un assistant qui convertit des requêtes en langage naturel en JSON structuré.
            
Les actions possibles sont:
- create_event (Notion): nécessite title, date (YYYY-MM-DD), time (HH:MM), duration_minutes (optionnel)
- create_page (Notion): nécessite title, content (optionnel)
- create_task (Notion): nécessite title, due_date (optionnel), priority (low/medium/high)

Réponds UNIQUEMENT avec un JSON valide au format:
{
  "tasks": [
    {
      "action": "create_event",
      "app": "notion",
      "title": "...",
      "date": "2025-11-28",
      "time": "10:00",
      "duration_minutes": 60
    }
  ]
}

IMPORTANT: Réponds UNIQUEMENT avec le JSON, sans texte avant ou après."""
            
            payload = {
                "model": self.meta_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                "temperature": 0.3
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            logger.info(f"✅ Meta LLaMA response received")
            logger.info(f"Raw response: {content[:200]}...")
            
            # Nettoyer le JSON si nécessaire
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            
            content = content.strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Meta LLaMA parsing error: {e}")
            raise Exception(f"Failed to parse query with Meta LLaMA: {str(e)}")


# Instance globale
llm_parser = None


def get_llm_parser() -> LLMParser:
    """Récupère ou crée l'instance du parser LLM Meta"""
    global llm_parser
    
    if llm_parser is None:
        llm_parser = LLMParser()
    
    return llm_parser
