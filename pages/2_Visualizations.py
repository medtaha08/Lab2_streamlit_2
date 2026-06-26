import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Data Visualizations", layout="wide")

st.title("📊 Competitor Data Insights")

if 'search_results' not in st.session_state:
    st.warning("⚠️ No data available. Please perform a search first on the 'Results Table' page.")
else:
    df = st.session_state['search_results']
    
    # ─── SIDEBAR FILTER ───
    st.sidebar.header("Filter Options")
    all_app_ids = ["All Applications"] + list(df['appId'].unique())
    selected_app = st.sidebar.selectbox("Filter charts by Application ID:", all_app_ids)
    
    # Application du filtre si choisi
    if selected_app != "All Applications":
        filtered_df = df[df['appId'] == selected_app]
    else:
        filtered_df = df

    if filtered_df.empty:
        st.error("No data matches the selected filter.")
    else:
        # Layout en grilles / colonnes
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⭐ App Ratings Distribution")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            # Graphique des notes (distribution des scores)
            sns.histplot(data=filtered_df, x="score", bins=10, kde=True, color="skyblue", ax=ax1)
            ax1.set_xlabel("Rating Score")
            st.pyplot(fig1)
            
        with col2:
            st.subheader("💰 Pricing Model: Paid vs Free")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            # Compte des apps gratuites vs payantes
            free_counts = filtered_df['free'].value_counts()
            labels = ['Free' if index else 'Paid' for index in free_counts.index]
            ax2.pie(free_counts, labels=labels, autopct='%1.1f%%', colors=['#4CAF50', '#FF5722'], startangle=90)
            st.pyplot(fig2)

        st.divider()
        
        # Top applications par volume d'installation
        st.subheader("📥 Top Applications by Downloads")
        top_apps = filtered_df.sort_values(by="real_installs", ascending=False).head(10)
        
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        sns.barplot(data=top_apps, x="real_installs", y="title", palette="viridis", ax=ax3)
        ax3.set_xlabel("Minimum Installs")
        ax3.set_ylabel("")
        st.pyplot(fig3)