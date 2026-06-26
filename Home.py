import streamlit as st

# Configuration de la page d'accueil
st.set_page_config(
    page_title="Competitor Analysis",
    page_icon="📊",
    layout="wide"
)

# Titre principal et vue d'ensemble (Overview)
st.title("Competitor Analysis")
st.header("Overview")
st.write("This is a rapid prototype of a Competitor Analysis application.")
st.write("Based on a search query, the app provides an Analysis of mobile apps in the targeted market for competitive insights.")

# Organisation en deux colonnes (Key Features & Improvements) comme sur le PDF
col1, col2 = st.columns(2)

with col1:
    st.subheader("Key Features")
    st.markdown("""
    - Search for Apps
    - Listing results
    - Filtering results
    - Sorting results
    - Data visualizations for Competitor analysis
    - Conducting Sentiment Analysis on Applications' reviews
    """)

with col2:
    st.subheader("Improvements")
    st.markdown("""
    - Enhance data visualizations
    - Load more data
    - Revise features based on feedback
    """)