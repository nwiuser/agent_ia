# 🚀 Guide de Démarrage Rapide

Un guide pour lancer l'Assistant Étudiant IA en 5 minutes !

## ⚡ Installation Express

### Méthode 1: Scripts Automatiques (Windows)

```bash
# 1. Double-cliquez sur start.bat
# OU en ligne de commande:
start.bat
```

Le script va :
- ✅ Créer l'environnement virtuel
- ✅ Installer les dépendances
- ✅ Créer le fichier .env
- ✅ Lancer le backend

### Méthode 2: Installation Manuelle

```bash
# 1. Créer environnement virtuel
python -m venv venv

# 2. Activer l'environnement
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Configurer .env
copy .env.example .env

# 5. Lancer le backend
python main.py
```

## 🎯 Premier Test

### 1. Vérifier que l'API fonctionne

Ouvrir `http://localhost:8000` dans un navigateur

Vous devriez voir :
```json
{
  "message": "Assistant Étudiant IA - API v1.0",
  "status": "running"
}
```

### 2. Tester avec une requête simple

**Option A: Interface Streamlit (Recommandé)**

```bash
# Nouveau terminal
streamlit run ui/app.py
```

Puis ouvrir `http://localhost:8501`

**Option B: Script de démo**

```bash
python demo.py
```

**Option C: Requête directe**

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Ajoute un examen de maths mardi à 10h\"}"
```

## 📝 Exemples de Requêtes

Testez ces exemples :

```
Ajoute un examen de maths mardi à 10h
```

```
Crée une page Notion pour réviser l'histoire
```

```
Ajoute un examen de maths mardi à 10h et crée une page Notion pour réviser
```

```
Ajoute une tâche urgente pour rendre le projet vendredi
```

## 🎨 Interface Utilisateur

L'interface Streamlit offre :

- 📝 Zone de saisie pour les requêtes
- 🚀 Bouton d'exécution
- 📊 Affichage des résultats
- 🔧 Vue du JSON parsé
- 💡 Exemples pré-définis

### Captures d'écran du workflow

1. **Entrer une requête** → Tapez votre instruction
2. **Cliquer sur Exécuter** → L'agent traite la requête
3. **Voir les résultats** → Actions exécutées affichées

## 🔧 Modes de Fonctionnement

### Mode Démo (Par défaut)

- ✅ Aucune configuration API nécessaire
- ✅ Utilise des mocks
- ✅ Parfait pour tester
- ✅ Réponses instantanées

**Fichier .env:**
```env
DEMO_MODE=True
```

### Mode Production

- 🔑 Nécessite clés API
- 🌐 Intégrations réelles
- 📅 Vraies créations dans Google Calendar
- 📝 Vraies pages dans Notion

**Fichier .env:**
```env
DEMO_MODE=False
OPENAI_API_KEY=sk-...
GOOGLE_CALENDAR_CREDENTIALS_FILE=credentials.json
NOTION_API_KEY=secret_...
```

## 📚 Documentation Complète

- `README.md` - Documentation principale
- `EXAMPLES.md` - Exemples de requêtes
- `DEPLOYMENT.md` - Guide de déploiement
- `http://localhost:8000/docs` - API interactive

## 🆘 Problèmes Courants

### "Port already in use"

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### "Module not found"

```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### "API not responding"

```bash
# Vérifier que le backend est lancé
# Vérifier les logs dans le terminal
# Redémarrer le backend
```

### ".env file not found"

```bash
# Créer depuis l'exemple
copy .env.example .env
```

## ✅ Checklist de Démarrage

- [ ] Python 3.9+ installé
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées
- [ ] Fichier .env configuré
- [ ] Backend lancé (port 8000)
- [ ] Test API réussi
- [ ] Interface Streamlit lancée (port 8501)
- [ ] Première requête testée

## 🎯 Prochaines Étapes

Une fois le test réussi :

1. **Explorer les exemples** → `EXAMPLES.md`
2. **Configurer les APIs** → Mode production
3. **Personnaliser** → Modifier les actions
4. **Déployer** → `DEPLOYMENT.md`

## 💡 Conseils Pro

### Développement

```bash
# Rechargement automatique du backend
uvicorn main:app --reload

# Logs détaillés
python main.py --log-level DEBUG
```

### Tests

```bash
# Lancer les tests
pytest tests/

# Script de démo
python demo.py
```

### Productivité

- Utilisez les exemples pré-définis dans Streamlit
- Créez vos propres raccourcis de requêtes
- Combinez plusieurs actions en une seule requête

## 📞 Support

En cas de problème :

1. Vérifier les logs du terminal
2. Consulter `README.md`
3. Tester en mode démo
4. Vérifier les ports (8000, 8501)

## 🎉 Résultat Attendu

Après avoir suivi ce guide, vous devriez avoir :

- ✅ Backend API fonctionnel
- ✅ Interface Streamlit accessible
- ✅ Première requête exécutée avec succès
- ✅ Résultats affichés

---

**Temps estimé : 5-10 minutes**

**Difficulté : ⭐ Débutant**

**Bon développement ! 🚀**
