# 🔄 Migration vers Notion

## Changements effectués

Le projet a été migré de **Google Calendar + Google Tasks** vers **Notion uniquement**.

### ✅ Avantages de la migration

- **Une seule plateforme** : Tout est centralisé dans Notion
- **Pas de configuration OAuth complexe** : Juste une clé API Notion
- **Meilleure intégration** : Pages, tâches et événements au même endroit
- **Plus simple** : Une seule base de données à configurer

### 🗂️ Changements dans le code

#### Fichiers modifiés :
- **`action_runner.py`** : Supprimé Google Calendar et Google Tasks, tout utilise Notion
- **`llm.py`** : Les événements sont maintenant créés comme des tâches Notion avec emoji 📅
- **`.env`** : Supprimé les variables Google Calendar

#### Fichiers non utilisés (peuvent être supprimés) :
- `actions/google_calendar.py`
- `actions/google_tasks.py`

### 📋 Fonctionnalités

Toutes les actions utilisent maintenant **Notion** :

#### 1. Créer un événement
```
"Ajoute un examen de maths mardi à 10h"
```
→ Crée une tâche dans Notion avec :
- Titre : `📅 examen de maths`
- Date d'échéance : `2025-11-27`
- Description : `Événement le 2025-11-27 à 10:00`

#### 2. Créer une tâche
```
"Ajoute une tâche urgente pour le projet"
```
→ Crée une tâche avec priorité haute

#### 3. Créer une page
```
"Crée une page Notion pour mes révisions"
```
→ Crée une page Notion

### 🎯 Configuration Notion

Votre base de données Notion doit avoir ces colonnes :

| Colonne | Type | Description |
|---------|------|-------------|
| **Name** | Title | Titre de la tâche/événement |
| **Status** | Status | `Not started`, `In progress`, `Done` |
| **Priority** | Status | `Low`, `Medium`, `High` |
| **Due Date** | Date | Date d'échéance |

### 🚀 Utilisation

```bash
# Redémarrer le backend
python main.py

# Dans Streamlit
"Ajoute une réunion jeudi à 16h"
"Crée une tâche pour réviser vendredi"
"Fais une page Notion pour mon projet"
```

### 📝 Exemples de requêtes

**Événements → Tâches Notion avec 📅 :**
- "Planifie un examen lundi à 9h"
- "Ajoute un cours de physique mercredi à 14h"
- "Crée une réunion demain à 16h30"

**Tâches normales :**
- "Ajoute une tâche urgente pour le devoir"
- "Crée une tâche pour lire le chapitre 3"

**Pages :**
- "Crée une page pour mes notes de cours"
- "Fais une page Notion pour le projet final"

### ✨ Résultat

Tous les événements et tâches apparaissent dans la même base Notion, ce qui facilite :
- La gestion centralisée
- La vue d'ensemble de toutes vos activités
- Le suivi de vos événements et tâches au même endroit

---

**Note** : Les événements sont maintenant des tâches Notion avec un emoji 📅 pour les distinguer des tâches normales.
