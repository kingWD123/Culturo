import json
import os
import random
import requests
import re  # Assurez-vous que cette importation est bien présente
import ast
from urllib.parse import urlencode
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Import Google Generative AI
import google.generativeai as genai
from django.conf import settings

# Configuration de l'API Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Fonction pour récupérer des images d'Unsplash
def get_unsplash_image(query):
    try:
        unsplash_access_key = settings.UNSPLASH_ACCESS_KEY
        url = f"https://api.unsplash.com/search/photos?query={query}&client_id={unsplash_access_key}&per_page=1"
        response = requests.get(url)
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]['urls']['regular']
    except Exception as e:
        print(f"Erreur Unsplash: {e}")
    return "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=1000&auto=format&fit=crop"

# Fonction pour construire l'URL Qloo
def build_qloo_url(entity_type="urn:entity:place", extra_params=None):
    """Génère une URL Qloo pour les recommandations de restaurants."""
    base_url = "https://hackathon.api.qloo.com/v2/insights/"
    params = {
        "filter.type": entity_type
    }
    
    if extra_params:
        for key, value in extra_params.items():
            if isinstance(value, list):
                # Pour les listes de tags, Qloo attend une chaîne de caractères séparée par des virgules
                params[key] = ",".join(value)
            else:
                params[key] = value
    
    return base_url + "?" + urlencode(params)

# Vue principale pour les recommandations de restaurants
def restaurant_recommandations(request):
    return render(request, 'restaurant/restaurant_recommandations.html')

# API du chatbot pour les restaurants
@csrf_exempt
def restaurant_chatbot_api(request):
    try:
        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
            
            history = data.get("history", [])

            system_prompt = (
                "You are an assistant specialized in restaurant recommendations. "
                "Ask questions to understand:\n"
                "- The region or city in France where the user wants to eat\n"
                "- The type of cuisine sought (e.g., Italian, French, Japanese)\n"
                "- The budget (e.g., economical, medium, luxury)\n"
                "- The desired atmosphere (e.g., romantic, family-friendly, trendy)\n"
                "When you have enough information, generate the Qloo JSON at the end of your response, between ```json and ``` tags "
                "The JSON must be STRICTLY valid, compliant with JSON standard: all keys and values must be surrounded by double quotes, no extra commas, no Python syntax, no comments. "
                "Strictly valid example:\n"
                '{\n'
                '  "filter.type": "urn:entity:place",\n'
                '  "filter.location.query": "Paris",\n'
                '  "signal.interests.tags": ["restaurant", "italian"]\n'
                '}\n'
                "Don't invent tags or parameters if the user hasn't provided them.\n"
                "The user is not required to answer all questions.\n"
                "Ask questions one by one, so as not to overwhelm the user.\n"
                "Never mention Qloo parameters in your responses.\n"
                "Adapt your questions to obtain this information naturally."
            )

            try:
                messages = [{"role": "user", "parts": [system_prompt]}]
                for m in history:
                    messages.append({"role": m["role"], "parts": [m["content"]]})

                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(messages)
                bot_message = response.text
                
            except Exception as e:
                print(f"Gemini API Error: {type(e).__name__}: {e}")
                return JsonResponse({
                    "message": "Sorry, an error occurred. Please try again.",
                    "restaurants": []
                })

            restaurants = []
            qloo_params = None
            
            try:
                # Cherche le DERNIER bloc ```json ... ```
                matches = list(re.finditer(r'```json\s*([\s\S]+?)\s*```', bot_message))
                json_str = None
                # Cherche le dernier bloc ```json ... ```
                json_start = response_text.rfind("```json")
                if json_start != -1:
                    # Trouve le début du contenu JSON après ```json
                    content_start = response_text.find("\n", json_start)
                    if content_start != -1:
                        # Trouve la fin du bloc ```
                        content_end = response_text.find("```", content_start)
                        if content_end != -1:
                            # Extrait le contenu JSON
                            json_str = response_text[content_start+1:content_end].strip()
                
                # Si aucun bloc JSON n'a été trouvé, essaie d'extraire un objet JSON
                if not json_str:
                    try:
                        start = bot_message.rindex("{")
                        # Remonte pour trouver le début du dernier objet JSON
                        while start > 0 and bot_message[start-1] != '\n':
                            start -= 1
                        end = bot_message.rindex("}") + 1
                        json_str = bot_message[start:end]
                    except Exception:
                        json_str = None

                print("JSON extrait du chatbot :")
                print(json_str)

                if json_str:
                    # Nettoyage basique : remplace les guillemets simples par des doubles si besoin
                    if json_str.count('"') < 2 and json_str.count("'") > 1:
                        json_str = json_str.replace("'", '"')
                    json_str = json_str.strip()
                    try:
                        qloo_params = json.loads(json_str)
                    except json.JSONDecodeError:
                        try:
                            qloo_params = ast.literal_eval(json_str)
                        except Exception as e:
                            print(f"Impossible de parser le JSON Gemini: {e}")
                            qloo_params = None
                else:
                    print("Aucun JSON détecté dans la réponse du chatbot.")

                if not qloo_params:
                    return JsonResponse({
                        "message": bot_message,  # On renvoie la réponse conversationnelle du bot
                        "restaurants": [],
                        "debug_json": json_str
                    })

                qloo_url = build_qloo_url(extra_params=qloo_params)
                
                qloo_headers = {
                    "x-api-key": settings.CLOOAI_API_KEY,
                    "Accept": "application/json"
                }
                qloo_response = requests.get(qloo_url, headers=qloo_headers)

                if qloo_response.status_code == 200:
                    qloo_data = qloo_response.json()
                    restaurants = []
                    for entity in qloo_data.get("results", {}).get("entities", []):
                        restaurant = {}
                        restaurant["name"] = entity.get("name")
                        properties = entity.get("properties", {})
                        
                        # Extraction de la cuisine à partir des mots-clés
                        cuisine = 'Not specified'
                        if 'keywords' in properties and len(properties['keywords']) > 0:
                            # Parcourir les mots-clés pour trouver un type de cuisine
                            cuisine_keywords = ['italian', 'french', 'japanese', 'chinese', 'indian', 'mexican', 'thai', 'spanish', 'greek', 'american', 'vietnamese', 'korean', 'lebanese', 'turkish']
                            
                            for keyword in properties['keywords']:
                                if keyword['name'].lower() in cuisine_keywords:
                                    cuisine = keyword['name'].capitalize()
                                    break
                            
                            # Si aucun mot-clé de cuisine n'a été trouvé, utiliser le premier mot-clé
                            if cuisine == 'Not specified' and len(properties['keywords']) > 0:
                                cuisine = properties['keywords'][0]['name'].capitalize()
                        
                        restaurant["cuisine"] = cuisine
                        
                        # Extraction de l'adresse
                        restaurant["location"] = properties.get("address", "Address not available")
                        
                        # Extraction du prix
                        price_level = properties.get("price_level", 2)
                        restaurant["price_range"] = '€' * min(price_level, 4)
                        
                        # Extraction de la note
                        restaurant["rating"] = properties.get("business_rating", 4.0)
                        
                        # Génération d'une description
                        location_query = qloo_params.get("filter.location.query", "France")
                        restaurant["description"] = f"An excellent {cuisine.lower()} restaurant located in {location_query}."
                        
                        # Coordonnées par défaut (à améliorer avec de vraies coordonnées)
                        location_coords = {
                            'paris': (48.8566, 2.3522),
                            'lyon': (45.7578, 4.8320),
                            'marseille': (43.2965, 5.3698),
                            'bordeaux': (44.8378, -0.5792),
                            'lille': (50.6292, 3.0573),
                            'france': (48.8566, 2.3522)
                        }
                        
                        location_key = location_query.lower()
                        base_coords = location_coords.get(location_key, (48.8566, 2.3522))
                        restaurant["latitude"] = base_coords[0] + random.uniform(-0.05, 0.05)
                        restaurant["longitude"] = base_coords[1] + random.uniform(-0.05, 0.05)

                        # Enrichir avec une image Unsplash
                        search_query = f"{restaurant['name']} {cuisine} restaurant"
                        restaurant["img"] = get_unsplash_image(search_query.strip())
                        
                        restaurants.append(restaurant)
                    
                else:
                    print(f"Qloo API Error: {qloo_response.status_code} - {qloo_response.text}")
                    # Générer des données fictives en cas d'erreur
                    restaurants = generate_mock_restaurants(3)

            except (ValueError, KeyError, json.JSONDecodeError) as e:
                print(f"Error processing chatbot response or Qloo API: {e}")
                # Générer des données fictives en cas d'erreur
                restaurants = generate_mock_restaurants(3)

            return JsonResponse({
                "message": bot_message,
                "restaurants": restaurants
            })

        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    except Exception as e:
        print(f"Unexpected error in restaurant_chatbot_api: {type(e).__name__}: {e}")
        return JsonResponse({
            "message": "Sorry, an error occurred. Please try again.",
            "restaurants": []
        }, status=500)

# Fonction pour générer des données fictives de restaurants
def generate_mock_restaurants(count=3):
    cuisines = ['French', 'Italian', 'Japanese', 'Mexican', 'Indian', 'Thai']
    locations = ['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Lille', 'Strasbourg']
    price_ranges = ['€', '€€', '€€€', '€€€€']
    
    # Coordonnées approximatives des villes françaises
    city_coords = {
        'Paris': (48.8566, 2.3522),
        'Lyon': (45.7578, 4.8320),
        'Marseille': (43.2965, 5.3698),
        'Bordeaux': (44.8378, -0.5792),
        'Lille': (50.6292, 3.0573),
        'Strasbourg': (48.5734, 7.7521)
    }
    
    restaurants = []
    for i in range(count):
        cuisine = random.choice(cuisines)
        location = random.choice(locations)
        base_coords = city_coords.get(location, (48.8566, 2.3522))
        
        restaurant = {
            'name': f"Restaurant {chr(65+i)}",
            'cuisine': cuisine,
            'location': location,
            'price_range': random.choice(price_ranges),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'description': f"An excellent {cuisine.lower()} restaurant located in {location}.",
            'latitude': base_coords[0] + lat_variation,
            'longitude': base_coords[1] + lng_variation,
            'img': get_unsplash_image(f"{cuisine} food restaurant")
        }
        restaurants.append(restaurant)
    
    return restaurants

# Vue pour les détails d'un restaurant
def restaurant_detail(request, restaurant_name):
    # Dans une version réelle, on récupérerait les données depuis la base de données
    # Pour l'instant, on génère des données fictives
    
    # Décodage du nom du restaurant
    restaurant_name = restaurant_name.replace('-', ' ').title()
    
    # Génération d'un restaurant fictif
    cuisines = ['French', 'Italian', 'Japanese', 'Mexican', 'Indian', 'Thai']
    locations = ['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Lille', 'Strasbourg']
    
    restaurant = {
        'name': restaurant_name,
        'cuisine': random.choice(cuisines),
        'location': random.choice(locations),
        'price_range': random.choice(['€', '€€', '€€€', '€€€€']),
        'rating': round(random.uniform(3.5, 5.0), 1),
        'description': f"An excellent restaurant located in {random.choice(locations)}. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        'img': get_unsplash_image(f"{restaurant_name} restaurant"),
        'address': f"{random.randint(1, 100)} rue de {random.choice(['Paris', 'Lyon', 'Bordeaux', 'Lille'])}, {random.randint(10000, 99999)} France",
        'phone': f"+33 {random.randint(1, 9)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}",
        'website': f"https://www.{restaurant_name.lower().replace(' ', '')}.fr",
        'hours': {
            'Monday': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Tuesday': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Wednesday': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Thursday': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Friday': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Saturday': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Sunday': 'Closed' if random.choice([True, False]) else f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00"
        }
    }
    
    return render(request, 'restaurant/restaurant_detail.html', {'restaurant': restaurant})

# Additional mock data for testing
def get_mock_restaurant_data():
    cuisines = ['French', 'Italian', 'Japanese', 'Mexican', 'Indian', 'Thai']
    return cuisines