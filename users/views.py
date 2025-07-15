from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
import json
import random
from datetime import datetime, timedelta

import google.generativeai as genai
from django.conf import settings
from urllib.parse import urlencode
import requests

genai.configure(api_key=settings.GEMINI_API_KEY)

from .models import (
    CulturalProfile, Destination, CulturalHighlight, 
    Itinerary, ItineraryDay, ItineraryItem,
    Artiste, Oeuvre, Evenement, Playlist, ConseilCulturel
)

def home(request):
    """Culturo homepage"""
    return render(request, 'users/home.html')

def CinemaRecommandations(request):
    """Page of cinema recommendations"""
    return render(request, 'users/cinema_recommandations.html')

def ArtistsRecommandations(request):
    """Page of artists recommendations"""
    return render(request, 'users/artists_recommandations.html')

def EventsRecommandations(request):
    """Page of events recommendations"""

# Fonction pour rechercher des films/genres et obtenir leurs IDs Qloo
def search_qloo_entities(query, entity_type="film"):
    """Recherche des entités (films, genres, réalisateurs) via l'API Qloo et retourne leurs IDs"""
    try:
        qloo_api_key = getattr(settings, 'QLOO_API_KEY', '')
        qloo_base_url = getattr(settings, 'QLOO_BASE_URL', '')
        
        if not qloo_api_key or qloo_api_key in ['YOUR_QLOO_API_KEY_HERE', 'YOUR_QLOO_API_KEY']:
            print(f"[WARNING] Clé API Qloo non configurée, mode démo pour: {query}")
            return None
        
        headers = {
            "Authorization": qloo_api_key,
            "Content-Type": "application/json"
        }
        
        params = {
            "query": query,
            "type": entity_type
        }
        
        print(f"[DEBUG] Recherche Qloo: {query} (type: {entity_type})")
        response = requests.get(f"{qloo_base_url}/v2/search", headers=headers, params=params, timeout=10)
        
        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                entity_id = results[0]["id"]
                print(f"[SUCCESS] ID trouvé pour '{query}': {entity_id}")
                return entity_id
            else:
                print(f"[WARNING] Aucun résultat trouvé pour: {query}")
                return None
        else:
            print(f"[ERROR] Erreur API Qloo: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Erreur lors de la recherche Qloo: {e}")
        return None

# Fonction utilitaire pour transformer les préférences utilisateur en paramètres Qloo

def build_qloo_api_params(user_data, limit=5):
    """Construit les paramètres GET pour l'API Qloo à partir des préférences utilisateur"""
    genre = user_data.get("genre", "").lower()
    pays = user_data.get("pays", "")
    age = user_data.get("age", "")
    langue = user_data.get("langue", "")
    annee_min = user_data.get("annee_min", 2019)
    annee_max = user_data.get("annee_max", 2024)
    rating_min = user_data.get("rating_min", 3.0)
    
    # Mapping genre -> tag Qloo (à compléter selon besoins)
    genre_tag_map = {
        "action": "urn:tag:genre:media:action",
        "anime": "urn:tag:genre:media:anime",
        "animes": "urn:tag:genre:media:anime",
        "drame": "urn:tag:genre:media:drama",
        "comédie": "urn:tag:genre:media:comedy",
        "comedy": "urn:tag:genre:media:comedy",
        "romance": "urn:tag:genre:media:romance",
        "thriller": "urn:tag:genre:media:thriller",
        "science-fiction": "urn:tag:genre:media:science_fiction",
        "horreur": "urn:tag:genre:media:horror",
        "animation": "urn:tag:genre:media:animation",
        # ... autres genres ...
    }
    tag = genre_tag_map.get(genre, "urn:tag:genre:media:action")
    
    # Formatage du paramètre tags
    tags = [{"tag": tag, "weight": 20}]
    
    params = {
        "filter.type": "urn:entity:movie",
        "signal.interests.tags": json.dumps(tags, ensure_ascii=False),
        "limit": limit,
        "feature.explainability": "true"
    }
    if pays:
        params["filter.location.query"] = pays
    if age:
        params["signal.demographics.age"] = age
    if annee_min:
        params["filter.release_year.min"] = annee_min
    if annee_max:
        params["filter.release_year.max"] = annee_max
    if rating_min:
        params["filter.rating.min"] = rating_min
    if langue:
        params["filter.language"] = langue
    return params

# Nouvelle version de la fonction pour obtenir des recommandations via l'API Qloo

def get_qloo_recommendations_from_user_data(user_data, limit=5):
    """Obtient des recommandations de films via l'API Qloo en utilisant les préférences utilisateur"""
    try:
        qloo_api_key = getattr(settings, 'QLOO_API_KEY', '')
        qloo_base_url = getattr(settings, 'QLOO_BASE_URL', 'https://hackathon.api.qloo.com')
        if not qloo_api_key or qloo_api_key in ['YOUR_QLOO_API_KEY_HERE', 'YOUR_QLOO_API_KEY']:
            print("[WARNING] Clé API Qloo non configurée, mode démo")
            return None
        headers = {
            "Authorization": qloo_api_key,
            "Content-Type": "application/json"
        }
        params = build_qloo_api_params(user_data, limit=limit)
        print(f"[DEBUG] Appel Qloo API avec params: {params}")
        response = requests.get(f"{qloo_base_url}/v2/insights", headers=headers, params=params, timeout=10)
        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Response: {response.text[:200]}...")
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get("recs", [])
            print(f"[SUCCESS] {len(recommendations)} recommandations obtenues (nouveau format)")
            return recommendations
        else:
            print(f"[ERROR] Erreur API Qloo: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Erreur lors de l'obtention des recommandations (nouveau format): {e}")
        return None

# Fonction pour obtenir des films populaires par genre (pour le mode démo)
def get_popular_movies_by_genre(genre):
    """Retourne des films populaires par genre pour le mode démo"""
    genre_movies = {
        "drame": ["Parasite", "Joker", "La La Land"],
        "comédie": ["The Grand Budapest Hotel", "Deadpool", "Superbad"],
        "action": ["Mad Max: Fury Road", "John Wick", "Mission: Impossible - Fallout"],
        "thriller": ["Inception", "The Dark Knight", "Gone Girl"],
        "romance": ["La La Land", "Before Sunrise", "Eternal Sunshine of the Spotless Mind"],
        "science-fiction": ["Inception", "Interstellar", "Blade Runner 2049"],
        "horreur": ["Get Out", "Hereditary", "A Quiet Place"],
        "documentaire": ["Planet Earth", "Cosmos", "13th"],
        "animation": ["Spider-Man: Into the Spider-Verse", "Coco", "Zootopia"],
        "art-house": ["Moonlight", "The Shape of Water", "Parasite"],
        "anime": ["Spirited Away", "Attack on Titan", "Demon Slayer"],
        "animes": ["Spirited Away", "Attack on Titan", "Demon Slayer"],
        "dessin animé": ["Spider-Man: Into the Spider-Verse", "Coco", "Zootopia"],
        "dessin animés": ["Spider-Man: Into the Spider-Verse", "Coco", "Zootopia"]
    }
    
    genre_lower = genre.lower().strip()
    for key in genre_movies:
        if key in genre_lower or genre_lower in key:
            return genre_movies[key]
    
    return ["Inception", "The Dark Knight", "Parasite"]

# Fonction pour générer des recommandations de démo
def generate_demo_recommendations(user_data):
    """Génère des recommandations de démo basées sur les préférences utilisateur"""
    genre = user_data.get("genre", "").lower()
    langue = user_data.get("langue", "").lower()
    
    # Obtenir des films populaires pour le genre
    popular_movies = get_popular_movies_by_genre(genre)
    
    # Créer des recommandations de démo basées sur les films populaires
    demo_recommendations = []
    for i, movie in enumerate(popular_movies[:5]):
        # Générer des données réalistes pour chaque film
        demo_recommendations.append({
            "id": f"demo_film_{i+1}",
            "name": movie,
            "type": "film",
            "score": round(0.9 - (i * 0.05), 2),  # Score décroissant
            "year": 2010 + i,  # Année fictive
            "language": "Japanese" if genre in ["anime", "animes"] else "English",
            "image_url": f"https://images.unsplash.com/photo-{1489599832527 + i}?w=200&h=300&fit=crop"
        })
    
    return {
        "success": True,
        "data": {
            "recommendations": demo_recommendations,
            "total_results": len(demo_recommendations),
            "user_preferences": user_data,
            "source": "demo_mode"
        },
        "status_code": 200
    }
    
    # Filtrer par langue si spécifiée
    recommendations = demo_recommendations.get(genre, demo_recommendations["drame"])
    if langue and langue != "toutes" and langue != "tous":
        # Pour les animes, accepter japonais ET français (doublage)
        if genre in ["anime", "animes"]:
            if langue in ["francais", "français", "french"]:
                # Garder tous les animes (ils sont souvent doublés en français)
                pass
            elif langue in ["japonais", "japanese"]:
                recommendations = [r for r in recommendations if "japanese" in r["language"].lower()]
            else:
                recommendations = [r for r in recommendations if langue in r["language"].lower()]
        else:
            recommendations = [r for r in recommendations if langue in r["language"].lower()]
    
    return {
        "success": True,
        "data": {
            "recommendations": recommendations[:5],
            "total_results": len(recommendations),
            "user_preferences": user_data,
            "source": "demo_mode"
        },
        "status_code": 200
    }

# Fonction pour traiter les recommandations Qloo et les formater pour l'affichage
def process_qloo_recommendations(qloo_recs, user_data):
    """Traite les recommandations Qloo et les formate pour l'affichage"""
    if not qloo_recs:
        return None
    
    formatted_recommendations = []
    for i, rec in enumerate(qloo_recs):
        formatted_rec = {
            "id": rec.get("id", f"qloo_film_{i+1}"),
            "title": rec.get("name", "Film inconnu"),
            "score": rec.get("score", 0.0),
            "type": rec.get("type", "film"),
            "year": 2020 + i,  # Année fictive
            "language": "Japanese" if user_data.get("genre", "").lower() in ["anime", "animes"] else "English",
            "image_url": f"https://images.unsplash.com/photo-{1489599832527 + i}?w=200&h=300&fit=crop"
        }
        formatted_recommendations.append(formatted_rec)
    
    return {
        "success": True,
        "data": {
            "recommendations": formatted_recommendations,
            "total_results": len(formatted_recommendations),
            "user_preferences": user_data,
            "source": "qloo_api"
        },
        "status_code": 200
    }

@csrf_exempt
def cinema_chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        history = data.get("history", [])

        system_prompt = (
            "Tu es un assistant qui aide l'utilisateur à obtenir des recommandations de films et séries via Qloo API. "
            "Pose une question à la fois pour recueillir : le genre préféré, la langue, la plateforme de streaming, l'âge, le pays. "
            "Quand tu as toutes les informations, affiche un résumé en JSON structuré comme ceci : "
            '{"genre": "...", "langue": "...", "plateforme": "...", "age": "...", "pays": "..."}. '
            "Ne propose le résumé JSON qu'à la toute fin."
        )

        messages = [{"role": "user", "parts": [system_prompt]}]
        for m in history:
            messages.append({"role": m["role"], "parts": [m["content"]]})

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(messages)
        bot_message = response.text

        user_data = None
        qloo_url = None
        qloo_response = None
        try:
            # Amélioration du parsing JSON
            if "{" in bot_message and "}" in bot_message:
                start = bot_message.index("{")
                end = bot_message.rindex("}") + 1
                json_str = bot_message[start:end]
                
                try:
                    user_data = json.loads(json_str)
                    print(f"[SUCCESS] JSON parsé avec succès: {user_data}")
                except json.JSONDecodeError as json_error:
                    print(f"[ERROR] Erreur parsing JSON: {json_error}")
                    print(f"[DEBUG] JSON string: {json_str}")
                    user_data = None
            else:
                print(f"[WARNING] Aucun JSON trouvé dans la réponse: {bot_message}")
                user_data = None
            
            # Continuer seulement si on a des données utilisateur
            if user_data:
                print(f"[INFO] Obtention de recommandations Qloo avec user_data: {user_data}")
                qloo_recommendations = get_qloo_recommendations_from_user_data(user_data, limit=5)
                
                if qloo_recommendations:
                    print("[SUCCESS] Recommandations Qloo obtenues avec succès (nouveau format)")
                    qloo_response = process_qloo_recommendations(qloo_recommendations, user_data)
                else:
                    print("[WARNING] Échec de l'obtention des recommandations Qloo, passage en mode démo")
                    qloo_response = generate_demo_recommendations(user_data)
                
                # Sauvegarder les recommandations dans la session
                if qloo_response.get("success") and qloo_response.get("data", {}).get("recommendations"):
                    save_recommendations_to_session(request, qloo_response["data"]["recommendations"])
                    print("[INFO] Recommandations sauvegardées dans la session")
                
                print("[User Data]", user_data)
                print("[Qloo Response Status]", qloo_response.get("success", False))
                print("[Qloo Response Source]", qloo_response.get("data", {}).get("source", "unknown"))
            else:
                print("[WARNING] Pas de données utilisateur, pas d'appel API Qloo")
                
        except Exception as e:
            print(f"[ERROR] Erreur générale: {e}")
            import traceback
            traceback.print_exc()

        return JsonResponse({
            "message": bot_message,
            "user_data": user_data,
            "qloo_url": qloo_url,
            "qloo_response": qloo_response,
            "done": user_data is not None
        })

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)



def recommendations_page(request):
    """Page dédiée aux recommandations de films avec images"""
    # Récupérer les dernières recommandations depuis la session ou générer des exemples
    recommendations = request.session.get('last_recommendations', [])
    
    if not recommendations:
        # Générer des recommandations d'exemple
        recommendations = [
            {
                "title": "Spirited Away",
                "year": 2001,
                "rating": 8.6,
                "language": "Japanese",
                "image_url": "https://images.unsplash.com/photo-1489599832527-3f53c85c63eb?w=200&h=300&fit=crop",
                "genre": "anime",
                "description": "Un chef-d'œuvre de l'animation japonaise"
            },
            {
                "title": "Attack on Titan",
                "year": 2013,
                "rating": 9.0,
                "language": "Japanese", 
                "image_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=200&h=300&fit=crop",
                "genre": "anime",
                "description": "Une série d'animation épique"
            },
            {
                "title": "Demon Slayer",
                "year": 2019,
                "rating": 8.7,
                "language": "Japanese",
                "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=300&fit=crop",
                "genre": "anime",
                "description": "Animation spectaculaire et histoire captivante"
            }
        ]
    
    context = {
        'recommendations': recommendations,
        'total_results': len(recommendations)
    }
    
    return render(request, 'users/recommendations.html', context)

def save_recommendations_to_session(request, recommendations):
    """Sauvegarde les recommandations dans la session pour les afficher plus tard"""
    request.session['last_recommendations'] = recommendations
    return True
