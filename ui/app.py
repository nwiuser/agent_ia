"""
Interface utilisateur Streamlit - Assistant Étudiant IA
"""
import streamlit as st
import requests
import json
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Assistant Étudiant IA",
    page_icon="🎓",
    layout="wide"
)

# URL de l'API FastAPI
API_URL = "http://localhost:8000"

# Titre de l'application
st.title("🎓 Assistant Étudiant Automatisé")
st.markdown("""
Transformez vos instructions en langage naturel en actions concrètes !

**Exemples de requêtes :**
- "Ajoute un examen de maths mardi à 10h et crée une page Notion pour réviser"
- "Crée un événement pour mon cours de physique demain à 14h30"
- "Ajoute une tâche pour rendre le projet vendredi avec haute priorité"
- "Planifie une réunion de groupe jeudi à 16h et note les points à discuter dans Notion"
""")

st.divider()

# Colonne principale
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Votre requête")
    
    # Zone de texte pour la requête
    user_query = st.text_area(
        "Que voulez-vous faire ?",
        placeholder="Ex: Ajoute un examen de maths mardi à 10h et crée une page Notion pour réviser",
        height=120,
        key="query_input"
    )
    
    # Boutons d'action
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        execute_btn = st.button("🚀 Exécuter", type="primary", use_container_width=True)
    
    with col_btn2:
        parse_only_btn = st.button("🔍 Parser uniquement", use_container_width=True)
    
    with col_btn3:
        clear_btn = st.button("🗑️ Effacer", use_container_width=True)
    
    if clear_btn:
        st.rerun()

with col2:
    st.subheader("ℹ️ Informations")
    st.info("""
    **Actions disponibles :**
    
    📅 **Google Calendar**
    - Créer des événements
    - Planifier des examens
    - Ajouter des cours
    
    📝 **Notion**
    - Créer des pages
    - Ajouter des tâches
    - Organiser les révisions
    """)

st.divider()

# Fonction pour appeler l'API
def call_api(endpoint: str, query: str):
    """Appelle l'API FastAPI"""
    try:
        response = requests.post(
            f"{API_URL}/{endpoint}",
            json={"query": query},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Impossible de se connecter à l'API. Assurez-vous que le backend est lancé (python main.py)")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Timeout - La requête a pris trop de temps")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erreur API: {str(e)}")
        return None

# Exécution complète
if execute_btn and user_query:
    with st.spinner("🔄 Traitement en cours..."):
        result = call_api("run", user_query)
        
        if result:
            # Afficher le temps d'exécution
            st.success(f"✅ Requête traitée en {result['execution_time']:.2f}s")
            
            # Créer des onglets pour les résultats
            tab1, tab2, tab3 = st.tabs(["📊 Résultats", "🔧 JSON Parsé", "📄 Réponse complète"])
            
            with tab1:
                st.subheader("Résultats des actions")
                
                for i, action_result in enumerate(result['results'], 1):
                    # Déterminer la couleur selon le statut
                    if action_result['status'] == 'success':
                        status_color = "🟢"
                    elif action_result['status'] == 'mock':
                        status_color = "🟡"
                    else:
                        status_color = "🔴"
                    
                    with st.expander(f"{status_color} Action {i}: {action_result['action']} sur {action_result['app']}", expanded=True):
                        st.write(f"**Message:** {action_result['message']}")
                        
                        if action_result.get('details'):
                            st.write("**Détails:**")
                            st.json(action_result['details'])
            
            with tab2:
                st.subheader("JSON généré par le LLM")
                st.json(result['parsed_tasks'])
            
            with tab3:
                st.subheader("Réponse complète de l'API")
                st.json(result)

# Parser uniquement
if parse_only_btn and user_query:
    with st.spinner("🔄 Parsing en cours..."):
        result = call_api("parse", user_query)
        
        if result:
            st.success("✅ Parsing réussi")
            
            col_parse1, col_parse2 = st.columns(2)
            
            with col_parse1:
                st.subheader("🔧 JSON Parsé")
                st.json(result['parsed_tasks'])
            
            with col_parse2:
                st.subheader("📝 Requête originale")
                st.info(result['query'])

# Message si aucune requête
if (execute_btn or parse_only_btn) and not user_query:
    st.warning("⚠️ Veuillez entrer une requête")

# Sidebar avec des exemples
with st.sidebar:
    st.header("💡 Exemples de requêtes")
    
    example_queries = [
        "Ajoute un examen de maths mardi à 10h et crée une page Notion pour réviser",
        "Crée un événement pour mon cours de physique demain à 14h30 durant 2 heures",
        "Planifie une réunion de groupe jeudi à 16h",
        "Ajoute une tâche pour rendre le projet vendredi avec haute priorité",
        "Crée une page Notion pour mes notes de cours",
        "Ajoute un événement examen final lundi prochain à 9h"
    ]
    
    for i, example in enumerate(example_queries, 1):
        if st.button(f"Exemple {i}", key=f"example_{i}", use_container_width=True):
            st.session_state.query_input = example
            st.rerun()
    
    st.divider()
    
    st.header("⚙️ Configuration")
    
    # Vérifier l'état de l'API
    try:
        health = requests.get(f"{API_URL}/health", timeout=2)
        if health.status_code == 200:
            st.success("✅ API connectée")
        else:
            st.error("❌ API non disponible")
    except:
        st.error("❌ API non disponible")
    
    st.info("""
    **Pour lancer le backend:**
    ```bash
    python main.py
    ```
    
    **Pour lancer l'interface:**
    ```bash
    streamlit run ui/app.py
    ```
    """)
    
    st.divider()
    
    st.caption("🎓 Assistant Étudiant IA v1.0")
    st.caption("Projet de démonstration - 4 jours")
