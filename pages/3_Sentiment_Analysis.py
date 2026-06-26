import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_app_reviews
from transformers import pipeline

st.set_page_config(page_title="Sentiment Analysis", layout="wide")

st.title("🤖 ML-Based User Review Sentiment Analysis")

# On vérifie si la recherche de l'étape 2 a été effectuée
if 'search_results' not in st.session_state:
    st.warning("⚠️ Please search for applications first in the 'Results Table' page.")
else:
    df_apps = st.session_state['search_results']
    
    # Permettre à l'étudiant de choisir l'app à analyser
    app_choice = st.selectbox(
        "Select an application to analyze its user reviews:", 
        options=df_apps['appId'].tolist(),
        format_func=lambda x: df_apps[df_apps['appId'] == x]['title'].values[0]
    )
    
    if st.button("Run Sentiment Analysis Pipeline"):
        with st.spinner("Downloading/Loading HuggingFace Model & Fetching reviews..."):
            
            # 1. Chargement du pipeline d'analyse de sentiment (modèle de text classification)
            # Utilise un modèle standard léger et performant en anglais
            sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
            
            # 2. Récupération des avis via utils.py (Logique héritée du Lab 1)
            df_reviews = get_app_reviews(app_choice, n_reviews=30)
            
            if not df_reviews.empty and 'content' in df_reviews.columns:
                
                sentiments = []
                # 3. Calcul des Sentiments pour chaque commentaire
                for text in df_reviews['content'].tolist():
                    # Sécurité si le commentaire est trop long ou vide
                    if str(text).strip():
                        truncated_text = str(text)[:512] 
                        res = sentiment_pipeline(truncated_text)[0]
                        sentiments.append(res['label'])
                    else:
                        sentiments.append("NEUTRAL")
                
                df_reviews['sentiment'] = sentiments
                
                # Visualisation globale des scores de sentiment de l'application choisie
                st.success("Analysis Complete!")
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.subheader("Overall App Sentiment Breakdown")
                    sentiment_counts = df_reviews['sentiment'].value_counts()
                    fig, ax = plt.subplots()
                    sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'][:len(sentiment_counts)], ax=ax)
                    plt.xticks(rotation=0)
                    st.pyplot(fig)
                    
                with col2:
                    st.subheader("Sample of Analyzed Reviews")
                    st.dataframe(df_reviews[['userName', 'content', 'sentiment']], use_container_width=True)
            else:
                st.error("Could not fetch reviews for this specific app or no reviews are available.")