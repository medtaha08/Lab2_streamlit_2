import streamlit as st
from utils import get_apps_data

st.set_page_config(page_title="Results Table", layout="wide")

st.title("🔍 Competitor App Search")
st.write("Enter a keyword to discover competitors and extract their Play Store records.")

# Saisie utilisateur dynamique (ex: mental health, fitness, edtech...)
query = st.text_input("Enter your search term:", placeholder="e.g., mental health AI")

if st.button("Search Competitors"):
    if query:
        with st.spinner("Scraping Play Store data... Please wait..."):
            df_results = get_apps_data(query)
            
            if not df_results.empty:
                # Sauvegarde globale dans la session
                st.session_state['search_results'] = df_results
                st.session_state['query_term'] = query
                
                st.success(f"Successfully retrieved {len(df_results)} unique applications!")
                
                # Affichage de la table de données configurable
                st.dataframe(df_results, use_container_width=True)
            else:
                st.warning("No applications found for this query.")
    else:
        st.error("Please enter a valid keyword.")

# Si les données existent déjà dans la session, on les affiche par défaut
elif 'search_results' in st.session_state:
    st.info(f"Showing previous results for: **{st.session_state['query_term']}**")
    st.dataframe(st.session_state['search_results'], use_container_width=True)