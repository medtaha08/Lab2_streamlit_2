import pandas as pd
from google_play_scraper import search, app, reviews, Sort

LANG = "en"
COUNTRY = "us"

def get_apps_data(search_query, n_apps=20):
    """
    Page 1 & 2 : Recherche des applications basée sur le mot-clé de l'utilisateur.
    Retourne un DataFrame Pandas contenant les détails essentiels.
    """
    try:
        # Recherche initiale (comme ton Lab 1)
        results = search(
            search_query,
            lang=LANG,
            country=COUNTRY,
            n_hits=n_apps
        )
        
        if not results:
            return pd.DataFrame()
            
        apps_list = []
        
        # Extraction des détails pour chaque application trouvée
        for r in results:
            app_id = r["appId"]
            try:
                details = app(app_id, lang=LANG, country=COUNTRY)
                
                # On filtre et structure les champs utiles demandés par le Lab 2
                apps_list.append({
                    "appId": details.get("appId"),
                    "title": details.get("title"),
                    "developer": details.get("developer"),
                    "genre": details.get("genre"),
                    "score": details.get("score"),          # Note globale (1-5)
                    "ratings": details.get("ratings"),      # Nombre d'avis total
                    "installs": details.get("installs"),    # Format texte (ex: '10M+')
                    "real_installs": details.get("minInstalls"), # Nombre exact pour graphiques
                    "free": details.get("free"),            # True / False
                    "price": details.get("price"),
                    "description": details.get("description") # Pour le Word Cloud
                })
            except Exception:
                continue # Si une app bloque, on passe à la suivante
                
        return pd.DataFrame(apps_list)
        
    except Exception as e:
        print(f"Error searching apps: {e}")
        return pd.DataFrame()

def get_app_reviews(app_id, n_reviews=50):
    """
    Page 3 : Récupère les commentaires d'une application pour l'analyse de sentiment.
    """
    try:
        result, _ = reviews(
            app_id,
            lang=LANG,
            country=COUNTRY,
            sort=Sort.MOST_RELEVANT,
            count=n_reviews
        )
        
        if not result:
            return pd.DataFrame()
            
        cleaned_reviews = []
        for r in result:
            cleaned_reviews.append({
                "userName": r.get("userName"),
                "content": r.get("content"), # Le texte à analyser par l'IA
                "score": r.get("score")      # Étoiles de l'utilisateur
            })
            
        return pd.DataFrame(cleaned_reviews)
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return pd.DataFrame()