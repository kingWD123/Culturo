from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
import random
from datetime import datetime, timedelta
import google.generativeai as genai
from django.conf import settings
from urllib.parse import urlencode
import requests
import time

genai.configure(api_key=settings.GEMINI_API_KEY)


def home(request):
    """Culturo homepage"""
    return render(request, 'users/home.html')

def CinemaRecommandations(request):
    """Page of cinema recommendations"""
    print("DEBUG: Début de la vue CinemaRecommandations")
    
    # Critères par défaut adaptés à l'API Qloo
    params = {
        "filter.type": "urn:entity:movie",
        "feature.explainability": "true",
        "filter.genres": "slice of life",
        "filter.release_country": "Japan"
    }
    
    from urllib.parse import urlencode
    base_url = "https://hackathon.api.qloo.com/v2/insights/"
    qloo_url = base_url + "?" + urlencode(params)
    
    import requests
    headers = {
        "x-api-key": settings.CLOOAI_API_KEY,
        "Accept": "application/json"
    }
    
    recommendations = []
    movie_details = {}
    
    try:
        print(f"DEBUG: Appel API vers {qloo_url}")
        response = requests.get(qloo_url, headers=headers)
        print(f"DEBUG: Réponse API - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"DEBUG: Données brutes de l'API: {data}")
            
            # Vérifier si nous avons des résultats
            if not data.get("results", {}).get("entities"):
                print("DEBUG: Aucun résultat trouvé dans la réponse de l'API")
            
            for element in data.get("results", {}).get("entities", []):
                film = {
                    "name": element.get("name"),
                    "entity_id": element.get("entity_id"),
                    "properties": element.get("properties", {}),
                    "tags": element.get("tags", []),
                    "external": element.get("external", {}),
                    # Ajout d'une image par défaut pour le débogage
                    "image_url": element.get("image_url", "https://via.placeholder.com/300x450?text=No+Image")
                }
                recommendations.append(film)
                if film["entity_id"]:
                    movie_details[film["entity_id"]] = film
        else:
            print(f"DEBUG: Erreur API - Status: {response.status_code}")
            print(f"DEBUG: Réponse API: {response.text}")
    except Exception as e:
        print(f"DEBUG: Exception lors de l'appel API: {str(e)}")
    
    print(f"DEBUG: Nombre de recommandations: {len(recommendations)}")
    print(f"DEBUG: Détails des films: {movie_details}")
    
    # Stocke tous les détails en session
    request.session['movie_details'] = movie_details
    
    # Ajout de données de test si aucune recommandation n'est trouvée
    if not recommendations:
        print("\n" + "="*80)
        print("DEBUG: Aucune recommandation trouvée, utilisation des données de test")
        print("="*80)
        
        # Log détaillé des en-têtes de la requête
        print("\nEn-têtes de la requête:")
        for header, value in request.META.items():
            if header.startswith('HTTP_') or header in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                print(f"{header}: {value}")
                
        # Log de la session
        print("\nContenu de la session:", dict(request.session))
        
        # Log des paramètres GET
        print("\nParamètres GET:", dict(request.GET))
        
        # Log des paramètres POST
        print("\nParamètres POST:", dict(request.POST))
        recommendations = [
            {
                "name": "Film de test 1",
                "entity_id": "test1",
                "properties": {"release_year": "2023"},
                # Formatage pour correspondre à ce qu'attend le JavaScript
                "image": {
                    "url": "https://via.placeholder.com/300x450?text=Film+1"
                },
                "release_year": "2023"  # Ajouté pour la compatibilité
            },
            {
                "name": "Film de test 2",
                "entity_id": "test2",
                "properties": {"release_year": "2022"},
                # Formatage pour correspondre à ce qu'attend le JavaScript
                "image": {
                    "url": "https://via.placeholder.com/300x450?text=Film+2"
                },
                "release_year": "2022"  # Ajouté pour la compatibilité
            }
        ]
    
    context = {
        "recommendations": recommendations,
        "debug_info": {
            "api_url": qloo_url,
            "recommendations_count": len(recommendations),
            "has_movie_details": bool(movie_details)
        }
    }
    
    print(f"DEBUG: Contexte envoyé au template: {context}")
    return render(request, 'users/cinema_recommandations.html', context)


def get_movie_urns_from_titles(titles):
    """Recherche les URNs ClooAI pour une liste de titres de films."""
    urns = []
    not_found = []
    for title in titles:
        try:
            url = f"https://hackathon.api.qloo.com/v2/entities/search?query={title}&type=movie"
            headers = {
                "x-api-key": settings.GEMINI_API_KEY, 
                "Accept": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # Prendre le premier résultat si disponible
                if data.get("entities"):
                    urn = data["entities"][0]["urn"]
                    urns.append(urn)
                else:
                    not_found.append(title)
            else:
                not_found.append(title)
            time.sleep(0.2)  # Petite pause pour éviter le rate limit
        except Exception as e:
            print(f"Erreur lors de la recherche d'URN pour {title}: {e}")
            not_found.append(title)
    return urns, not_found

@csrf_exempt
def cinema_chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        history = data.get("history", [])

        system_prompt = (
            "Tu es un assistant spécialisé dans les recommandations de films via ClooAI. "
            "Ton objectif est de comprendre les préférences du visiteur pour lui proposer des films adaptés. "
            "Pose des questions naturelles et adapte-toi à la langue de l'utilisateur.\n\n"
            "Questions à poser (une par une, selon les réponses) :\n"
            "1. Quels sont tes films préférés ? (pour comprendre ses goûts)\n"
            "2. Quels genres de films apprécies-tu ?\n"
            "3. Préfères-tu des films récents ou des classiques ?\n"
            "4. Quelle note minimale souhaites-tu pour les films recommandés ?\n"
            "5. Y a-t-il une langue de préférence ?\n"
            "6. As-tu une préférence pour une période particulière ?\n\n"
            "Ne propose les recommandations que quand tu as au moins 3-4 critères pertinents. "
            "Pour chaque question, adapte ta réponse selon les réponses précédentes. "
            "Si l'utilisateur ne répond pas à une question, passe à la suivante. "
            "Quand tu as assez d'informations, affiche un résumé en JSON avec seulement les informations fournies :\n"
            '{\n'
            '  "films_aimes": ["titre1", "titre2"], // films mentionnés ou préférés\n'
            '  "genres": ["action", "drame"], // genres mentionnés\n'
            '  "annee_min": 2000, // année minimum si mentionnée\n'
            '  "annee_max": 2024, // année maximum si mentionnée\n'
            '  "note_min": 3.5, // note minimale si mentionnée\n'
            '  "langue": "français" // langue de préférence si mentionnée\n'
            '}\n\n'
            "Ne propose le résumé JSON que quand tu as au moins quelques informations utiles. "
            "Fais un petit resume des informations fournis par le user a la fin de son dernier message"
            "Adapte tes questions selon les réponses précédentes."
            "Adapte toi à la langue de l'utilisateur, et garde à l'esprit que l'utilisateur est là pour découvrir"
        )

        messages = [{"role": "user", "parts": [system_prompt]}]
        for m in history:
            messages.append({"role": m["role"], "parts": [m["content"]]})

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(messages)
        bot_message = response.text

        user_data = None
        qloo_url = None
        urn_not_found = []
        recommendations = None
        try:
            start = bot_message.index("{")
            end = bot_message.rindex("}") + 1
            user_data = json.loads(bot_message[start:end])
            # Préparer les paramètres pour l'URL ClooAI (seulement les infos fournies)
            extra_params = {}
            
            # Films aimés (entités d'intérêt)
            entity_ids = user_data.get("films_aimes", [])
            if entity_ids:
                entity_ids, urn_not_found = get_movie_urns_from_titles(entity_ids)
            
            # Genres avec poids (seulement si fournis)
            genres = user_data.get("genres", [])
            if genres:
                genre_tags = []
                for genre in genres:
                    # Mapping des genres vers les URNs ClooAI
                    genre_mapping = {
                        "action": "urn:tag:genre:media:action",
                        "thriller": "urn:tag:genre:media:thriller",
                        "comedie": "urn:tag:genre:media:comedy",
                        "drame": "urn:tag:genre:media:drama",
                        "science_fiction": "urn:tag:genre:media:sci_fi",
                        "horreur": "urn:tag:genre:media:horror",
                        "romance": "urn:tag:genre:media:romance",
                        "aventure": "urn:tag:genre:media:adventure",
                        "animation": "urn:tag:genre:media:animation",
                        "documentaire": "urn:tag:genre:media:documentary"
                    }
                    if genre.lower() in genre_mapping:
                        genre_tags.append({"tag": genre_mapping[genre.lower()], "weight": 20})
                
                if genre_tags:
                    extra_params['signal.interests.tags'] = json.dumps(genre_tags)
            
            # Localisation géographique (seulement si fournie)
            if user_data.get("localisation"):
                extra_params['filter.location.query'] = user_data["localisation"]
            
            # Démographie - âge (mapping vers valeurs acceptées par ClooAI)
            if user_data.get("age"):
                age_value = user_data["age"].lower().replace(" ", "").replace("_", "")
                age_map = {
                    "18to35": "35_and_younger",
                    "18to25": "24_and_younger",
                    "25to29": "25_to_29",
                    "30to34": "30_to_34",
                    "35to44": "35_to_44",
                    "36to55": "36_to_55",
                    "45to54": "45_to_54",
                    "55andolder": "55_and_older",
                    "35andyounger": "35_and_younger",
                    "24andyounger": "24_and_younger"
                }
                mapped_age = None
                for key, val in age_map.items():
                    if key in age_value: 
                        mapped_age = val
                        break
                if mapped_age:
                    extra_params['signal.demographics.age'] = mapped_age
            
            # Démographie - genre (seulement si fourni)
            if user_data.get("genre"):
                extra_params['signal.demographics.gender'] = user_data["genre"]
            
            # Filtrage temporel (seulement si fourni)
            if user_data.get("annee_min"):
                extra_params['filter.release_year.min'] = user_data["annee_min"]
            if user_data.get("annee_max"):
                extra_params['filter.release_year.max'] = user_data["annee_max"]
            
            # Note minimale (seulement si fournie)
            if user_data.get("note_min"):
                extra_params['filter.rating.min'] = user_data["note_min"]
            
            # Langue (seulement si fournie)
            if user_data.get("langue"):
                extra_params['filter.language'] = user_data["langue"]

            if extra_params:
                extra_params['feature.explainability'] = True
            
            # Générer l'URL seulement si on a au moins quelques paramètres
            if entity_ids or extra_params:
                if 'feature.explainability' in extra_params:
                    extra_params['feature.explainability'] = True
                qloo_url = build_qloo_url(
                    entity_type="urn:entity:movie",
                    entity_ids=entity_ids,
                    extra_params=extra_params
                )
                print("[Qloo URL]", qloo_url)
                # Appeler l'API Qloo/ClooAI pour obtenir les recommandations
                try:
                    qloo_headers = {
                        "x-api-key": settings.CLOOAI_API_KEY,
                        "Accept": "application/json"
                    }
                    qloo_response = requests.get(qloo_url, headers=qloo_headers)

                    if qloo_response.status_code == 200:
                        qloo_data = qloo_response.json()
                        # Extraire les titres recommandés (adapter selon la structure de la réponse)
                        titles = []
                        # Initialiser le dictionnaire des détails des films dans la session s'il n'existe pas
                        if 'movie_details' not in request.session:
                            request.session['movie_details'] = {}
                            
                        for element in qloo_data["results"]["entities"]:
                            entity_id = element.get("entity_id")
                            film = {
                                "name": element.get("name"),
                                "entity_id": entity_id,
                                "properties": element.get("properties", {}),
                                "tags": element.get("tags", []),
                                "external": element.get("external", {}),
                                "release_year": element.get("properties", {}).get("release_year"),
                                "description": element.get("properties", {}).get("description"),
                                "image": element.get("properties", {}).get("image", {}).get("url"),
                                "genres": [tag.get("name") for tag in element.get("tags", [])],
                                "release_country": element.get("properties", {}).get("release_country"),
                                "imdb_id": None,
                                "imdb_user_rating": None,
                                "imdb_user_rating_count": None
                            }
                            
                            # Ajouter les informations IMDB si disponibles
                            imdb = element.get("external", {}).get("imdb", [])
                            if imdb and isinstance(imdb, list) and len(imdb) > 0:
                                imdb_info = imdb[0]
                                film["imdb_id"] = imdb_info.get("id")
                                film["imdb_user_rating"] = imdb_info.get("user_rating")
                                film["imdb_user_rating_count"] = imdb_info.get("user_rating_count")
                            
                            # Stocker les détails complets du film dans la session
                            if entity_id:
                                request.session['movie_details'][entity_id] = film
                                # S'assurer que la session est sauvegardée
                                request.session.modified = True
                            
                            # Ajouter à la liste des recommandations
                            titles.append(film)
                        
                        recommendations = titles
                    else:
                        recommendations = [f"Erreur API Qloo: {qloo_response.status_code}"]
                except Exception as api_exc:
                    recommendations = [f"Erreur lors de l'appel API Qloo: {api_exc}"]
            else:
                print("Pas assez d'informations pour générer une URL de recommandation")
                
        except Exception as e:
            print(f"Erreur lors du parsing JSON: {e}")
            pass

        # Message d'avertissement si certains titres n'ont pas d'URN
        warning = None  
        if urn_not_found:
            warning = f"Aucun identifiant ClooAI trouvé pour : {', '.join(urn_not_found)}. Les recommandations seront moins précises."

        # Si recommandations prêtes, stocke-les dans la session
        if recommendations and (user_data is not None and (entity_ids or extra_params)):
            request.session['cinema_recommendations'] = recommendations
            request.session['cinema_qloo_url'] = qloo_url
            
            # S'assurer que les détails des films sont bien stockés dans la session
            if 'movie_details' not in request.session:
                request.session['movie_details'] = {}
                
            # Mise à jour des détails des films dans la session
            for film in recommendations:
                if 'entity_id' in film and film['entity_id']:
                    request.session['movie_details'][film['entity_id']] = film
                    
            # Marquer la session comme modifiée pour s'assurer qu'elle est sauvegardée
            request.session.modified = True

        return JsonResponse({
            "message": bot_message,
            # "user_data": user_data,
            "qloo_url": qloo_url,
            "done": user_data is not None and (entity_ids or extra_params),
            "warning": warning,
            "recommendations": recommendations
        })

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def get_movies_from_qloo(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
    try:
        data = json.loads(request.body)
        qloo_url = data.get("qloo_url")
        if not qloo_url:
            return JsonResponse({"error": "Aucune URL fournie"}, status=400)
        # Utiliser la clé API fournie par l'utilisateur
        api_key = "ELT40OrStBysskCLRvuxrB9-h6ZakP_jZ2O0j9TMHZI"
        headers = {
            "x-api-key": api_key,
            "Accept": "application/json"
        }
        response = requests.get(qloo_url, headers=headers)
        if response.status_code != 200:
            return JsonResponse({"error": f"Erreur API externe: {response.status_code}"}, status=502)
        data = response.json()
        # Extraire les films (nom, image, date de sortie)
        movies = []
        entities = data.get("results", {}).get("entities", [])
        for entity in entities:
            movie_data = {
                "name": entity.get("name"),
                "entity_id": entity.get("entity_id"),
            }
            # Ajoute toutes les propriétés brutes
            movie_data.update(entity.get("properties", {}))
            # Ajoute aussi tags, external, etc. si présents
            if "tags" in entity:
                movie_data["tags"] = entity["tags"]
            if "external" in entity:
                movie_data["external"] = entity["external"]
            movies.append(movie_data)
        return JsonResponse({"movies": movies})
    except Exception as e:
        return JsonResponse({"error": f"Erreur serveur: {str(e)}"}, status=500)

def movie_detail(request):
    entity_id = request.GET.get('id')
    # 1. Cherche d'abord dans la session
    movie_details = request.session.get('movie_details', {})
    if entity_id in movie_details:
        return render(request, 'users/movie_detail.html', {'movie': movie_details[entity_id]})
    # 2. Cas spécial the-godfather
    if entity_id == 'the-godfather':
        godfather_data = {
            'name': 'The Godfather',
            'description': "A chronic war between New York’s five mafia families — and the rising power of the Corleones — transforms Michael Corleone from reluctant family outsider into ruthless mob boss. What begins as a hopeful offer instead spins into a violent empire that reshapes the American crime landscape forever.",
            'akas': [
                {'value': 'Kumbari', 'languages': ['sq']},
                {'value': 'Կնքահայրը', 'languages': ['hy']},
                {'value': 'Xaç Atası', 'languages': ['az']},
                {'value': '教父Ⅰ / 教父1', 'languages': ['zh']},
                {'value': 'The Godfather Part I', 'languages': ['da']},
                {'value': 'ნათლიმამა', 'languages': ['ka']},
                {'value': 'پدرخوانده', 'languages': ['fa']},
                {'value': 'Il Padrino', 'languages': ['it']},
                {'value': 'ゴッドファーザー', 'languages': ['ja']},
                {'value': 'De Peetvader', 'languages': ['nl']},
                {'value': 'Gudfaren', 'languages': ['no']},
                {'value': 'Ojciec chrzestny', 'languages': ['pl']},
                {'value': 'O Padrinho', 'languages': ['pt']},
                {'value': 'Крёстный отец / Крестный отец', 'languages': ['ru']},
                {'value': 'Кум', 'languages': ['sr']},
                {'value': '教父', 'languages': ['tw']},
                {'value': 'Baba', 'languages': ['tr']},
                {'value': 'Krusttēvs', 'languages': ['lv']},
            ],
            'external': {
                'imdb': [{'id': 'tt0068646'}],
                'wikidata': [{'id': 'Q47703'}],
                'letterboxd': [{'id': 'the-godfather'}],
                'apple_tv': [{'id': 'umc.cmc.3ew9fykdnpfaq9t2jq5da011c'}],
            },
            'tags': [
                {'name': 'Drama'},
                {'name': 'Crime'},
            ],
            'release_country': ['United States'],
            'production_companies': ['Paramount Pictures', 'Alfran Productions'],
            'content_rating': 'R (Violence, language, some sexuality/nudity)',
            'duration': 175,
            'image_url': 'https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_ver1.jpg',
        }
        return render(request, 'users/movie_detail.html', {'movie': godfather_data})
    if not entity_id:
        return render(request, 'users/movie_detail.html', {'movie': {}, 'error': "Aucun identifiant de film fourni."})
    api_key = "ELT40OrStBysskCLRvuxrB9-h6ZakP_jZ2O0j9TMHZI"
    url = f"https://hackathon.api.qloo.com/v2/entities/{entity_id}"
    headers = {
        "x-api-key": api_key,
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return render(request, 'users/movie_detail.html', {
                'movie': {},
                'error': f"Erreur API externe: {response.status_code}"
            })
        data = response.json()
        entity = data.get('entity', {})
        return render(request, 'users/movie_detail.html', {'movie': entity})
    except Exception as e:
        return render(request, 'users/movie_detail.html', {
            'movie': {},
            'error': f"Erreur serveur: {str(e)}"
        })

# Fonction améliorée pour générer une URL Qloo/ClooAI GET
def build_qloo_url(
    entity_type="urn:entity:movie",
    entity_ids=None,
    extra_params=None
):
    """
    Génère une URL ClooAI avec tous les paramètres de recommandation de films
    
    Args:
        entity_type: Type d'entité (urn:entity:movie par défaut)
        entity_ids: Liste des films aimés (URNs)
        extra_params: Paramètres supplémentaires (genres, localisation, démographie, etc.)
    """
    base_url = "https://hackathon.api.qloo.com/v2/insights/"
    params = {
        "filter.type": entity_type
    }
    
    # Ajouter les entités d'intérêt (films aimés)
    if entity_ids:
        if isinstance(entity_ids, list):
            # Convertir les titres de films en URNs si nécessaire
            urn_entities = []
            for entity in entity_ids:
                if entity.startswith("urn:entity:movie:"):
                    urn_entities.append(entity)
                else:
                    # Convertir le titre en URN (format simplifié)
                    urn_entity = f"urn:entity:movie:{entity.lower().replace(' ', '_').replace('-', '_')}"
                    urn_entities.append(urn_entity)
            params["signal.interests.entities"] = ",".join(urn_entities)
        else:
            params["signal.interests.entities"] = entity_ids
    
    # Ajouter tous les paramètres supplémentaires
    if extra_params:
        for key, value in extra_params.items():
            if key == 'feature.explainability' and isinstance(value, bool):
                # Encoder en 'true' ou 'false' (string, lowercase)
                params[key] = 'true' if value else 'false'
            elif isinstance(value, (list, dict)):
                # Pour les listes et dictionnaires, utiliser JSON
                params[key] = json.dumps(value)
            else:
                params[key] = value
    
    return base_url + "?" + urlencode(params)

def cinema_recommendations_result(request):
    """Affiche la page de résultats détaillés des recommandations cinéma"""
    recommendations = request.session.get('cinema_recommendations', [])
    qloo_url = request.session.get('cinema_qloo_url', None)
    return render(request, 'users/cinema_recommendations_result.html', {
        'recommendations': recommendations,
        'qloo_url': qloo_url
    })
