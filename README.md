# 🎓 Assistant Étudiant Automatisé

Un système d'agent IA qui transforme des instructions en langage naturel en actions concrètes sur Notion.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)

## 🎯 Objectif

Permettre à un étudiant de taper une instruction simple comme :
> "Ajoute un examen de maths mardi à 10h et crée une page Notion pour réviser"

Et l'agent IA :
1. 🧠 Analyse la requête via un LLM
2. 📋 Transforme la requête en JSON structuré
3. ⚡ Exécute automatiquement les actions dans Notion :
   - Créer un événement (tâche avec date/heure)
   - Créer une page de notes
   - Créer une tâche
4. ✅ Retourne le résultat

## 📦 Structure du Projet

```
tp_agent_ai/
├── main.py                 # API FastAPI principale
├── llm.py                  # Module de parsing LLM
├── action_runner.py        # Exécuteur d'actions
├── models.py              # Modèles Pydantic
├── actions/
│   ├── __init__.py
│   └── notion.py          # Gestion Notion (pages, tâches, événements)
├── ui/
│   └── app.py             # Interface Streamlit
├── requirements.txt       # Dépendances Python
├── .env.example          # Template des variables d'environnement
├── MIGRATION_NOTION.md   # Guide de migration
├── GUIDE_NOTION.md       # Guide d'intégration Notion
├── .gitignore
└── README.md
```

## 🚀 Installation

### 1. Cloner et configurer l'environnement

```bash
cd tp_agent_ai

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet :

```bash
cp .env.example .env
```

Éditez le fichier `.env` :

```env
# Mode démo (True = utilise des mocks, False = utilise les vraies APIs)
DEMO_MODE=True

# OpenAI API (optionnel en mode démo)
OPENAI_API_KEY=your_openai_api_key_here

# Notion API (obligatoire en mode production)
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_notion_database_id_here
```

## 🔑 Configuration de Notion (Optionnel - Mode Production)

### Notion API

1. Aller sur [Notion Developers](https://www.notion.so/my-integrations)
2. Créer une nouvelle intégration
3. Copier le token d'intégration
4. Créer une base de données Notion et partager avec votre intégration
5. Copier l'ID de la base de données

### OpenAI API

1. Aller sur [OpenAI Platform](https://platform.openai.com/)
2. Créer une clé API
3. Ajouter la clé dans le fichier `.env`

## 🎮 Utilisation

### Mode Démo (Recommandé pour tester)

Le mode démo utilise des mocks et ne nécessite aucune configuration d'API.

### 1. Lancer le backend FastAPI

```bash
python main.py
```

L'API sera accessible sur `http://localhost:8000`

Documentation interactive : `http://localhost:8000/docs`

### 2. Lancer l'interface Streamlit

Dans un **nouveau terminal** :

```bash
streamlit run ui/app.py
```

L'interface sera accessible sur `http://localhost:8501`

## 💡 Exemples de Requêtes

Voici quelques exemples à tester :

1. **Créer un événement simple :**
   ```
   Ajoute un examen de maths mardi à 10h
   ```

2. **Créer un événement + page Notion :**
   ```
   Ajoute un examen de maths mardi à 10h et crée une page Notion pour réviser
   ```

3. **Créer une tâche avec priorité :**
   ```
   Ajoute une tâche urgente pour rendre le projet vendredi
   ```

4. **Planifier un cours :**
   ```
   Crée un événement pour mon cours de physique demain à 14h30 durant 2 heures
   ```

5. **Organiser une réunion :**
   ```
   Planifie une réunion de groupe jeudi à 16h et note les points à discuter dans Notion
   ```

## 📋 Format JSON Attendu

Le LLM transforme les requêtes en JSON structuré :

```json
{
  "tasks": [
    {
      "action": "create_event",
      "app": "google_calendar",
      "title": "Examen de maths",
      "date": "2025-01-20",
      "time": "10:00",
      "duration_minutes": 60
    },
    {
      "action": "create_page",
      "app": "notion",
      "title": "Révision Maths",
      "content": "Chapitre 5"
    }
  ]
}
```

## 🔧 API Endpoints

### `POST /run`
Exécute une requête complète (parsing + exécution)

**Request:**
```json
{
  "query": "Ajoute un examen de maths mardi à 10h"
}
```

**Response:**
```json
{
  "query": "Ajoute un examen de maths mardi à 10h",
  "parsed_tasks": { "tasks": [...] },
  "results": [...],
  "execution_time": 0.45
}
```

### `POST /parse`
Parse uniquement la requête sans exécution

### `GET /health`
Vérifie l'état de l'API

### `GET /docs`
Documentation interactive Swagger

## 🏗️ Architecture

```
┌─────────────────┐
│   Interface     │
│   Streamlit     │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   API FastAPI   │
│   (main.py)     │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌────────────┐
│  LLM  │ │   Action   │
│Parser │ │   Runner   │
└───────┘ └─────┬──────┘
                │
                ▼
          ┌─────────┐
          │ Notion  │
          │   API   │
          └─────────┘
    (Pages, Tâches, Événements)
```

## 🧪 Tests Rapides

### Test API avec curl

```bash
# Test de santé
curl http://localhost:8000/health

# Test de requête
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"query": "Ajoute un examen demain à 10h"}'
```

### Test API avec Python

```python
import requests

response = requests.post(
    "http://localhost:8000/run",
    json={"query": "Ajoute un examen de maths mardi à 10h"}
)

print(response.json())
```

## 📝 Logs

Les logs sont affichés dans la console et incluent :
- Requêtes reçues
- Actions parsées
- Exécution des actions
- Erreurs éventuelles

## 🐛 Dépannage

### Erreur "API non disponible"
- Vérifiez que le backend est lancé : `python main.py`
- Vérifiez que le port 8000 est libre

### Erreur de parsing
- En mode démo, le parsing utilise des mots-clés simples
- Pour un parsing plus précis, configurez OpenAI API

### Erreur d'installation
```bash
# Mettre à jour pip
pip install --upgrade pip

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

## 🎯 Fonctionnalités

✅ Parsing de langage naturel (mode mock + OpenAI)  
✅ Création d'événements dans Notion (avec date/heure)  
✅ Création de pages Notion  
✅ Création de tâches Notion avec priorités  
✅ Interface web intuitive  
✅ API REST documentée  
✅ Mode démo sans configuration  
✅ Logs détaillés  
✅ Gestion d'erreurs robuste  
✅ **Tout centralisé dans Notion** - Plus de configuration OAuth complexe !

## 🚀 Prochaines Étapes

- [ ] Intégration avec Notion Calendar (API officielle)
- [ ] Gestion des récurrences d'événements
- [ ] Export des résultats en PDF
- [ ] Interface mobile
- [ ] Support multi-utilisateurs
- [ ] Historique des requêtes
- [ ] Notifications push

## 📄 Licence

Ce projet est un projet de démonstration éducatif.

## 👨‍💻 Auteur

Projet créé pour une démonstration de 4 jours - Assistant IA pour étudiants

## 🙏 Remerciements

- FastAPI pour le framework web
- Streamlit pour l'interface utilisateur
- OpenAI pour les capacités LLM
- Notion pour son API puissante et simple

---

**Bon développement ! 🚀**
