# 📘 Guide Complet d'Intégration Notion

## 🎯 Vue d'ensemble

Ce guide vous explique comment configurer Notion avec votre assistant IA pour créer automatiquement des pages et des tâches.

---

## 🚀 Option 1 : Mode Démo (Recommandé pour commencer)

### ✅ Avantages
- ✨ Aucune configuration nécessaire
- 🎮 Testez immédiatement le système
- 📋 Simule toutes les fonctionnalités Notion

### 📝 Configuration

Votre fichier `.env` doit contenir :
```env
DEMO_MODE=True
```

### 🧪 Test rapide

```bash
# Activer l'environnement virtuel
..\venv\Scripts\Activate.ps1

# Lancer le test
python test_notion.py
```

### 💬 Exemples de requêtes en mode démo

```
"Crée une page Notion pour réviser les maths"
"Ajoute une tâche urgente pour le projet de physique"
"Planifie une tâche avec priorité haute pour vendredi"
```

---

## 🔧 Option 2 : Mode Production (API Réelle)

### Étape 1️⃣ : Créer une intégration Notion

1. **Aller sur Notion Developers**
   - URL : https://www.notion.so/my-integrations
   - Connectez-vous à votre compte Notion

2. **Créer une nouvelle intégration**
   - Cliquez sur **"+ New integration"**
   - Donnez un nom : `Assistant Étudiant IA`
   - Sélectionnez votre workspace
   - Capabilities recommandées :
     - ✅ Read content
     - ✅ Update content
     - ✅ Insert content

3. **Copier le token**
   - Après création, copiez le **"Internal Integration Token"**
   - Format : `secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - ⚠️ **Gardez ce token secret !**

---

### Étape 2️⃣ : Créer une base de données Notion

#### A. Créer la base de données

1. Dans Notion, créez une **nouvelle page**
2. Tapez `/table` et sélectionnez **"Table - Full page"**
3. Nommez la page : `Tâches Assistant IA`

#### B. Configurer les colonnes

Votre table doit avoir ces colonnes :

| Nom de la colonne | Type | Valeurs possibles |
|-------------------|------|-------------------|
| **Name** | Title | (texte libre) |
| **Status** | Status | "Not started", "In progress", "Done" |
| **Priority** | Status | "Low", "Medium", "High" |
| **Due Date** | Date | (date) |

**Comment ajouter une colonne :**
1. Cliquez sur le **`+`** à droite de la dernière colonne
2. Choisissez le type (Select, Date, etc.)
3. Nommez la colonne exactement comme indiqué ci-dessus
4. Pour les colonnes "Select", ajoutez les valeurs possibles

#### C. Configuration des options Select

**Pour la colonne "Status" (type Status, pas Select) :**
1. Cliquez sur le **`+`** pour ajouter une colonne
2. Sélectionnez le type **"Status"**
3. Nommez-la `Status`
4. Les valeurs par défaut sont :
   - 📝 Not started (gris)
   - 🔄 In progress (bleu)
   - ✅ Done (vert)

**Pour la colonne "Priority" (type Status, pas Select) :**
1. Cliquez sur le **`+`** pour ajouter une colonne
2. Sélectionnez le type **"Status"**
3. Nommez-la `Priority`
4. Modifiez les valeurs pour avoir :
   - 🟢 Low (vert)
   - 🟡 Medium (jaune)
   - 🔴 High (rouge)

---

### Étape 3️⃣ : Partager avec l'intégration

1. Dans votre page de base de données, cliquez sur **`⋯`** (trois points) en haut à droite
2. Sélectionnez **"Add connections"** ou **"Connexions"**
3. Cherchez votre intégration : `Assistant Étudiant IA`
4. Cliquez dessus pour la connecter
5. ✅ Votre intégration a maintenant accès à cette base de données

---

### Étape 4️⃣ : Récupérer l'ID de la base de données

#### Méthode 1 : Via l'URL

1. Ouvrez votre base de données dans Notion
2. Regardez l'URL dans votre navigateur :
   ```
   https://www.notion.so/votre-workspace/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=...
   ```
3. L'ID est la partie de **32 caractères** entre le nom du workspace et `?v=`
4. Exemple : `a1b2c3d4e5f6789012345678901234ab`

#### Méthode 2 : Copier le lien

1. Cliquez sur **`⋯`** (trois points) en haut de la page
2. Sélectionnez **"Copy link"** ou **"Copier le lien"**
3. Le lien ressemble à :
   ```
   https://www.notion.so/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=...
   ```
4. L'ID est la partie de 32 caractères

---

### Étape 5️⃣ : Configurer les variables d'environnement

1. **Créer le fichier `.env`** (s'il n'existe pas déjà)
   ```bash
   cp .env.example .env
   ```

2. **Éditer le fichier `.env`** et modifier ces lignes :

```env
# Passer en mode production
DEMO_MODE=False

# Notion API
NOTION_API_KEY=secret_votre_token_ici_xxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# OpenAI (optionnel mais recommandé)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google Calendar (optionnel)
GOOGLE_CALENDAR_CREDENTIALS_FILE=config/credentials.json
GOOGLE_CALENDAR_TOKEN_FILE=config/token.json
```

3. **Remplacez** :
   - `secret_votre_token_ici_xxx` → Votre token d'intégration Notion
   - `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` → L'ID de votre base de données

---

### Étape 6️⃣ : Vérifier l'installation

```bash
# Vérifier que notion-client est installé
pip list | Select-String "notion"

# Si non installé, installez-le
pip install notion-client==2.2.1
```

---

### Étape 7️⃣ : Tester l'intégration

```bash
# Activer l'environnement virtuel
..\venv\Scripts\Activate.ps1

# Tester Notion
python test_notion.py
```

**Résultat attendu :**
```
============================================================
🧪 TEST INTÉGRATION NOTION
============================================================
Mode: PRODUCTION

📝 Test 1: Création d'une page Notion
------------------------------------------------------------
Status: success
Message: Page 'Plan de révision Mathématiques' créée avec succès
URL: https://www.notion.so/xxxxx

✅ Test 2: Création d'une tâche prioritaire
------------------------------------------------------------
Status: success
Message: Tâche 'Rendre le projet de physique' créée avec succès
URL: https://www.notion.so/xxxxx

✨ Tests terminés!
```

---

## 📚 Fonctionnalités disponibles

### 1. Créer une page Notion

**Paramètres :**
- `title` : Titre de la page (obligatoire)
- `content` : Contenu de la page (optionnel)
- `database_id` : ID de la base (optionnel si configuré dans .env)

**Exemples de requêtes naturelles :**
```
"Crée une page Notion pour mon plan de révision"
"Ajoute une page dans Notion avec mes notes de cours"
"Fais une page Notion pour le projet final de Python"
```

### 2. Créer une tâche Notion

**Paramètres :**
- `title` : Titre de la tâche (obligatoire)
- `due_date` : Date d'échéance au format YYYY-MM-DD (optionnel)
- `priority` : "low", "medium", ou "high" (défaut: "medium")
- `description` : Description de la tâche (optionnel)

**Exemples de requêtes naturelles :**
```
"Ajoute une tâche urgente pour le projet de physique"
"Crée une tâche avec priorité haute pour vendredi"
"Planifie une tâche de révision pour demain"
"Ajoute une tâche pour rendre le devoir le 30 novembre"
```

---

## 🎮 Utiliser le système complet

### Lancer l'API Backend

```bash
cd agent_ia
python main.py
```

L'API démarre sur : http://localhost:8000

### Lancer l'interface Streamlit (dans un nouveau terminal)

```bash
cd agent_ia
streamlit run ui/app.py
```

L'interface s'ouvre sur : http://localhost:8501

### Exemples de requêtes complètes

```
"Ajoute un examen de maths mardi à 10h et crée une page Notion pour réviser"

"Crée une tâche urgente pour rendre le projet vendredi et ajoute l'événement au calendrier"

"Planifie une réunion demain à 14h et note les points à discuter dans Notion"
```

---

## 🔍 Structure de la base de données recommandée

Voici un exemple de structure avancée (optionnelle) :

| Colonne | Type | Description |
|---------|------|-------------|
| Name | Title | Nom de la tâche/page |
| Status | Select | À faire, En cours, Terminé |
| Priority | Select | Basse, Moyenne, Haute |
| Due Date | Date | Date d'échéance |
| Category | Select | Cours, Projet, Examen, Révision |
| Tags | Multi-select | Math, Physique, Info, etc. |
| Notes | Text | Notes supplémentaires |
| Created | Created time | Date de création automatique |

---

## 🐛 Dépannage

### Erreur : "Database ID not configured"

**Solution :**
- Vérifiez que `NOTION_DATABASE_ID` est bien défini dans `.env`
- Vérifiez que l'ID fait exactement 32 caractères (sans espaces)

### Erreur : "API key not found"

**Solution :**
- Vérifiez que `NOTION_API_KEY` est bien défini dans `.env`
- Vérifiez que le token commence par `secret_`
- Rechargez le fichier `.env` en redémarrant l'application

### Erreur : "Unauthorized" ou "Forbidden"

**Solution :**
- Vérifiez que vous avez partagé la base de données avec votre intégration
- Dans Notion : Page → `⋯` → Add connections → Sélectionnez votre intégration

### Erreur : "Property not found"

**Solution :**
- Vérifiez que les colonnes sont nommées exactement : `Name`, `Status`, `Priority`, `Due Date`
- Les noms sont sensibles à la casse et aux espaces

### Le système reste en mode DEMO

**Solution :**
- Vérifiez que `DEMO_MODE=False` dans `.env` (pas `True`)
- Redémarrez l'application après modification du `.env`

---

## 📖 Documentation officielle

- **Notion API** : https://developers.notion.com/
- **Python SDK** : https://github.com/ramnes/notion-sdk-py
- **Guide Notion** : https://developers.notion.com/docs/getting-started

---

## ✨ Conseils et bonnes pratiques

### 🎯 Organisation

1. **Créez plusieurs bases de données** selon vos besoins :
   - Une pour les tâches académiques
   - Une pour les projets personnels
   - Une pour les notes de cours

2. **Utilisez des templates** Notion pour standardiser vos pages

3. **Activez les rappels** sur les dates d'échéance importantes

### 🔐 Sécurité

- ⚠️ Ne partagez **JAMAIS** votre `NOTION_API_KEY`
- 🔒 Ajoutez `.env` dans `.gitignore`
- 🛡️ Utilisez des variables d'environnement en production

### 🚀 Performance

- Utilisez le mode démo pour les tests rapides
- Activez le mode production seulement quand nécessaire
- Limitez le nombre d'appels API simultanés

---

## 📝 Exemples de cas d'usage

### Cas 1 : Étudiant en préparation d'examen

```
"Crée une tâche pour réviser les chapitres 1-5 pour lundi avec priorité haute"
"Ajoute l'examen final de maths le 15 décembre à 9h au calendrier et crée une page de révision dans Notion"
```

### Cas 2 : Gestion de projet

```
"Planifie une réunion d'équipe jeudi à 16h et crée une page Notion pour l'ordre du jour"
"Ajoute une tâche pour finir le rapport avant vendredi"
```

### Cas 3 : Organisation hebdomadaire

```
"Crée une page Notion pour ma planification de la semaine"
"Ajoute toutes mes séances de TP au calendrier et liste les tâches dans Notion"
```

---

## 🎓 Conclusion

Vous êtes maintenant prêt à utiliser Notion avec votre assistant IA ! 

**Prochaines étapes :**

1. ✅ Testez en mode démo
2. ✅ Configurez l'API Notion pour le mode production
3. ✅ Personnalisez votre base de données
4. ✅ Explorez les autres intégrations (Google Calendar)

**Besoin d'aide ?** Consultez les logs dans la console pour plus de détails sur les erreurs.

---

**Bon travail ! 🚀**
