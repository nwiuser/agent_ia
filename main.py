"""
FastAPI Backend - API principale de l'assistant étudiant
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import time
from datetime import datetime

from models import UserQuery, AgentResponse, ActionResult
from llm import get_llm_parser
from action_runner import get_action_runner

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

# Créer l'application FastAPI
app = FastAPI(
    title="Assistant Étudiant IA",
    description="API pour gérer automatiquement Google Calendar et Notion via langage naturel",
    version="1.0.0"
)

# Configuration CORS pour permettre l'accès depuis l'interface web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Route de base pour vérifier que l'API fonctionne"""
    return {
        "message": "Assistant Étudiant IA - API v1.0",
        "status": "running",
        "endpoints": {
            "run": "/run - Exécuter une requête en langage naturel",
            "health": "/health - Vérifier l'état de l'API",
            "docs": "/docs - Documentation interactive"
        }
    }


@app.get("/health")
async def health_check():
    """Vérifie l'état de santé de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "llm": "operational",
            "action_runner": "operational"
        }
    }


@app.post("/run", response_model=AgentResponse)
async def run_query(query: UserQuery):
    """
    Endpoint principal - Exécute une requête en langage naturel
    
    Args:
        query: UserQuery contenant la requête utilisateur
        
    Returns:
        AgentResponse avec le JSON parsé et les résultats d'exécution
    """
    start_time = time.time()
    
    logger.info(f"Received query: {query.query}")
    
    try:
        # Étape 1: Parser la requête avec le LLM
        llm_parser = get_llm_parser()
        parsed_tasks = await llm_parser.parse_query(query.query)
        
        logger.info(f"Parsed tasks: {parsed_tasks}")
        
        # Étape 2: Exécuter les actions
        action_runner = get_action_runner()
        results = await action_runner.execute_tasks(parsed_tasks)
        
        # Calculer le temps d'exécution
        execution_time = time.time() - start_time
        
        logger.info(f"Execution completed in {execution_time:.2f}s")
        
        # Construire la réponse
        response = AgentResponse(
            query=query.query,
            parsed_tasks=parsed_tasks,
            results=results,
            execution_time=execution_time
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement de la requête: {str(e)}"
        )


@app.post("/parse", response_model=dict)
async def parse_only(query: UserQuery):
    """
    Endpoint pour parser uniquement (sans exécution)
    Utile pour tester le parsing du LLM
    
    Args:
        query: UserQuery contenant la requête utilisateur
        
    Returns:
        JSON parsé
    """
    try:
        llm_parser = get_llm_parser()
        parsed_tasks = await llm_parser.parse_query(query.query)
        
        return {
            "query": query.query,
            "parsed_tasks": parsed_tasks,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error parsing query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du parsing: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    # Démarrer le serveur
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
