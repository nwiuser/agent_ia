# 🚀 Guide de Déploiement

Ce guide explique comment déployer l'Assistant Étudiant IA en production.

## 📋 Table des Matières

1. [Préparation](#préparation)
2. [Déploiement Local](#déploiement-local)
3. [Déploiement Cloud](#déploiement-cloud)
4. [Configuration Production](#configuration-production)
5. [Sécurité](#sécurité)
6. [Monitoring](#monitoring)

## 🎯 Préparation

### Checklist Avant Déploiement

- [ ] Configurer les clés API (Google, Notion, OpenAI)
- [ ] Tester en mode production localement
- [ ] Définir les variables d'environnement
- [ ] Configurer HTTPS/SSL
- [ ] Préparer la base de données (si nécessaire)
- [ ] Configurer les logs
- [ ] Tester les endpoints API

### Variables d'Environnement Production

```env
# Mode
DEMO_MODE=False

# OpenAI
OPENAI_API_KEY=sk-...

# Google Calendar
GOOGLE_CALENDAR_CREDENTIALS_FILE=/app/secrets/credentials.json
GOOGLE_CALENDAR_TOKEN_FILE=/app/secrets/token.json

# Notion
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=...

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Logs
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log
```

## 💻 Déploiement Local

### Option 1: Python Direct

```bash
# Installation
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Éditer .env avec vos clés

# Lancement Backend
gunicorn main:app --workers 4 --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker

# Lancement UI (nouveau terminal)
streamlit run ui/app.py --server.port 8501
```

### Option 2: Docker

Voir section Docker ci-dessous.

## ☁️ Déploiement Cloud

### Heroku

```bash
# Installation Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Créer app
heroku create assistant-etudiant-ai

# Variables d'environnement
heroku config:set DEMO_MODE=False
heroku config:set OPENAI_API_KEY=your_key

# Déployer
git push heroku main
```

### Railway

1. Connectez votre repo GitHub
2. Configurez les variables d'environnement
3. Deploy automatique

### Render

1. Connectez votre repo
2. Configurez le service web
3. Ajoutez les variables d'environnement
4. Deploy

### Azure App Service

```bash
# Login
az login

# Créer resource group
az group create --name assistant-ai-rg --location westeurope

# Créer app service plan
az appservice plan create --name assistant-ai-plan --resource-group assistant-ai-rg --sku B1

# Créer web app
az webapp create --resource-group assistant-ai-rg --plan assistant-ai-plan --name assistant-etudiant-ai --runtime "PYTHON:3.9"

# Deploy
az webapp up --name assistant-etudiant-ai
```

## 🐳 Docker

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code
COPY . .

# Créer répertoires
RUN mkdir -p /app/logs /app/secrets

# Exposer port
EXPOSE 8000

# Lancement
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEMO_MODE=False
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - NOTION_API_KEY=${NOTION_API_KEY}
    volumes:
      - ./secrets:/app/secrets
      - ./logs:/app/logs
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
    depends_on:
      - backend
    restart: unless-stopped
```

### Lancement Docker

```bash
# Build
docker-compose build

# Lancement
docker-compose up -d

# Logs
docker-compose logs -f

# Arrêt
docker-compose down
```

## 🔒 Sécurité

### HTTPS/SSL

Pour la production, utilisez HTTPS :

```bash
# Avec Nginx
# /etc/nginx/sites-available/assistant-ai

server {
    listen 80;
    server_name votre-domaine.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name votre-domaine.com;

    ssl_certificate /etc/letsencrypt/live/votre-domaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votre-domaine.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Authentification

Ajoutez l'authentification si nécessaire :

```python
# Dans main.py
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/run")
async def run_query(
    query: UserQuery,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Vérifier le token
    if not verify_token(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Suite du code...
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/run")
@limiter.limit("10/minute")
async def run_query(request: Request, query: UserQuery):
    # Code...
```

## 📊 Monitoring

### Logs

Configurez les logs pour la production :

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'app.log',
    maxBytes=10000000,
    backupCount=5
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[handler]
)
```

### Monitoring avec Sentry

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0
)
```

### Health Checks

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "llm": check_llm_service(),
            "google": check_google_api(),
            "notion": check_notion_api()
        }
    }
```

## 🔧 Optimisations Production

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def parse_query_cached(query: str):
    # Parsing...
    pass
```

### Workers Multiples

```bash
# Gunicorn avec plusieurs workers
gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120
```

### Base de Données

Pour stocker l'historique :

```python
# Ajoutez une DB (PostgreSQL, MongoDB)
from sqlalchemy import create_engine

engine = create_engine(os.getenv("DATABASE_URL"))
```

## 📈 Scaling

### Horizontal Scaling

- Utilisez un load balancer
- Déployez plusieurs instances
- Utilisez Redis pour le cache partagé

### Vertical Scaling

- Augmentez les resources (CPU/RAM)
- Optimisez les workers
- Utilisez des instances plus puissantes

## ✅ Checklist Post-Déploiement

- [ ] Vérifier que l'API répond
- [ ] Tester tous les endpoints
- [ ] Vérifier les logs
- [ ] Tester l'interface UI
- [ ] Vérifier les intégrations (Google, Notion)
- [ ] Configurer les alertes
- [ ] Documenter l'URL de production
- [ ] Tester la charge

## 🆘 Troubleshooting

### Backend ne démarre pas
```bash
# Vérifier les logs
tail -f app.log

# Vérifier les ports
netstat -an | grep 8000

# Vérifier les variables d'env
printenv | grep DEMO_MODE
```

### Erreurs API
```bash
# Tester avec curl
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

---

**Bon déploiement ! 🚀**
