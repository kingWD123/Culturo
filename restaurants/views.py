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
from django.contrib.auth.decorators import login_required

# Import Google Generative AI
import google.generativeai as genai

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

# Vue principale pour les restaurant
def restaurant_page(request):
    return render(request, 'restaurant/restaurant.html')

def restaurant_recommandations(request):
    return render(request, 'restaurant/restaurant_recommandations.html')


# API du chatbot pour les restaurants
@csrf_exempt
@login_required
def restaurant_chatbot_api(request):
    try:
        print(f"=== DEBUG CHATBOT API ===")
        print(f"Method: {request.method}")
        
        if request.method == "POST":
            print("Parsing request body...")
            data = json.loads(request.body)
            history = data.get("history", [])
            message = data.get("message", "")
            
            print(f"User message: {message}")
            print(f"History length: {len(history)}")

            # Prompt système adapté pour les restaurants
            system_prompt = (
                "You are an assistant specialized in restaurant recommendations via ClooAI. "
                "Ask adaptive questions to gather available information. "
                "The user is not required to provide all information.\n\n"
                "Questions to ask (one by one, according to responses):\n"
                "1. What type of cuisine do you prefer? (Italian, French, Japanese, etc.) (optional)\n"
                "2. In which city/country are you located? (optional)\n"
                "3. What is your budget range? (€, €€, €€€, €€€€) (optional)\n"
                "4. What atmosphere do you prefer? (casual, fine dining, romantic, etc.) (optional)\n"
                "5. Any dietary restrictions? (vegetarian, vegan, gluten-free, etc.) (optional)\n"
                "6. What minimum rating do you want? (optional)\n\n"
                "When you have enough information (at least 2-3 criteria), display a JSON summary with only the provided information:\n"
                '{\n'
                '  "filter.type": "urn:entity:place",\n'
                '  "signal.interests.tags": ["restaurant"],\n'
                '  "filter.location.query": "Paris", // only if provided\n'
                '  "filter.price_level.min": 1, // only if provided (1-4)\n'
                '  "filter.price_level.max": 3, // only if provided (1-4)\n'
                '  "filter.rating.min": 4.0, // only if provided\n'
                '  "signal.interests.cuisine": ["italian", "french"], // only if provided\n'
                '  "signal.interests.atmosphere": ["casual", "romantic"] // only if provided\n'
                '}\n\n'
                "Only propose the JSON summary when you have at least some useful information. "
                "Make a small summary of the information provided by the user at the end of their last message. "
                "Adapt your questions according to previous responses. "
                "Adapt to the user's language, and keep in mind that the user is here to discover restaurants"
            )

            # Construire les messages pour Gemini
            messages = [{"role": "user", "parts": [system_prompt]}]
            for m in history:
                messages.append({"role": m["role"], "parts": [m["content"]]})
            
            # Ajouter le message actuel
            messages.append({"role": "user", "parts": [message]})

            print("Calling Gemini API...")
            try:
                # Appel à Gemini avec gestion d'erreur améliorée
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(messages)
                bot_message = response.text
                
                print(f"Gemini response: {bot_message[:100]}...")
            except Exception as gemini_error:
                print(f"Gemini API Error: {type(gemini_error).__name__}: {gemini_error}")
                return JsonResponse({
                    "message": "Sorry, I'm having trouble connecting to the AI service. Please try again in a moment.",
                    "error": f"Gemini API error: {str(gemini_error)}"
                }, status=500)

            # Extraction du JSON de la réponse
            qloo_params = None
            restaurants = []
            qloo_url = None
            
            try:
                # Chercher le JSON dans la réponse
                start = bot_message.find("{")
                end = bot_message.rfind("}") + 1
                if start != -1 and end > start:
                    json_str = bot_message[start:end]
                    qloo_params = json.loads(json_str)
                    
                    # Construire l'URL Qloo
                    qloo_url = build_qloo_url(extra_params=qloo_params)
                    print(f"=== DEBUG QLOO RESTAURANTS ===")
                    print(f"URL Qloo générée: {qloo_url}")
                    print(f"Paramètres Qloo: {qloo_params}")
                    
                    # Appel à l'API Qloo
                    qloo_headers = {
                        "x-api-key": settings.CLOOAI_API_KEY,
                        "Accept": "application/json"
                    }
                    
                    try:
                        qloo_response = requests.get(qloo_url, headers=qloo_headers, timeout=10)
                        print(f"Status code Qloo: {qloo_response.status_code}")
                        
                        if qloo_response.status_code == 200:
                            qloo_data = qloo_response.json()
                            
                            # Traitement des restaurants
                            for entity in qloo_data.get("results", {}).get("entities", []):
                                restaurant = {}
                                restaurant["name"] = entity.get("name")
                                properties = entity.get("properties", {})
                                
                                # Extraction de la cuisine
                                cuisine = 'Not specified'
                                if 'keywords' in properties and len(properties['keywords']) > 0:
                                    cuisine_keywords = ['italian', 'french', 'japanese', 'chinese', 'indian', 'mexican', 'thai', 'spanish', 'greek', 'american', 'vietnamese', 'korean', 'lebanese', 'turkish']
                                    
                                    for keyword in properties['keywords']:
                                        if keyword['name'].lower() in cuisine_keywords:
                                            cuisine = keyword['name'].capitalize()
                                            break
                                    
                                    if cuisine == 'Not specified' and len(properties['keywords']) > 0:
                                        cuisine = properties['keywords'][0]['name'].capitalize()
                                
                                restaurant["cuisine"] = cuisine
                                restaurant["location"] = properties.get("address", "Address not available")
                                
                                # Prix
                                price_level = properties.get("price_level", 2)
                                restaurant["price_range"] = '€' * min(price_level, 4)
                                
                                # Note
                                restaurant["rating"] = properties.get("business_rating", 4.0)
                                
                                # Description
                                location_query = qloo_params.get("filter.location.query", "France")
                                restaurant["description"] = f"An excellent {cuisine.lower()} restaurant located in {location_query}."
                                
                                # Coordonnées
                                location_coords = {
                                    'paris': (48.8566, 2.3522),
                                    'lyon': (45.7578, 4.8320),
                                    'marseille': (43.2965, 5.3698),
                                    'tokyo': (35.6762, 139.6503),
                                    'new york': (40.7128, -74.0060),
                                    'london': (51.5074, -0.1278),
                                    'rome': (41.9028, 12.4964),
                                    'barcelona': (41.3851, 2.1734),
                                    'worldwide': (48.8566, 2.3522)
                                }
                                
                                location_key = location_query.lower()
                                base_coords = location_coords.get(location_key, (48.8566, 2.3522))
                                restaurant["latitude"] = base_coords[0] + random.uniform(-0.05, 0.05)
                                restaurant["longitude"] = base_coords[1] + random.uniform(-0.05, 0.05)

                                # Image
                                search_query = f"{restaurant['name']} {cuisine} restaurant"
                                restaurant["img"] = get_unsplash_image(search_query.strip())
                                
                                restaurants.append(restaurant)
                        
                        else:
                            print(f"Qloo API Error: {qloo_response.status_code}")
                            # Générer des données fictives
                            location_query = qloo_params.get("filter.location.query", "worldwide")
                            restaurants = generate_mock_restaurants(3, location_query)
                            
                    except requests.exceptions.Timeout:
                        print("Timeout lors de l'appel à l'API Qloo")
                        location_query = qloo_params.get("filter.location.query", "worldwide")
                        restaurants = generate_mock_restaurants(3, location_query)
                    except requests.exceptions.RequestException as e:
                        print(f"Erreur réseau Qloo: {e}")
                        location_query = qloo_params.get("filter.location.query", "worldwide")
                        restaurants = generate_mock_restaurants(3, location_query)
                        
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Erreur lors du parsing JSON: {e}")
                # Pas de JSON trouvé, c'est normal pour les premières interactions

            # Déterminer si on a terminé la collecte d'informations
            done = qloo_params is not None and len(restaurants) > 0

            print(f"Returning response with {len(restaurants)} restaurants")
            return JsonResponse({
                "message": bot_message,
                "qloo_url": qloo_url,
                "done": done,
                "restaurants": restaurants
            })

        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    except Exception as e:
        print(f"=== ERROR IN CHATBOT API ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        
        return JsonResponse({
            "message": "Sorry, an error occurred. Please try again.",
            "error": str(e)
        }, status=500)

# Fonction pour générer des données fictives de restaurants
def generate_mock_restaurants(count=3, location_query="worldwide"):
    cuisines = ['French', 'Italian', 'Japanese', 'Mexican', 'Indian', 'Thai', 'Chinese', 'American', 'Mediterranean', 'Korean']
    
    # Si une localisation spécifique est demandée, l'utiliser
    if location_query and location_query.lower() != "worldwide":
        locations = [location_query.title()]
    else:
        locations = ['Paris', 'Tokyo', 'New York', 'London', 'Rome', 'Barcelona', 'Berlin', 'Amsterdam', 'Sydney', 'Toronto']
    
    price_ranges = ['€', '€€', '€€€', '€€€€']
    
    # Coordonnées approximatives des villes du monde
    city_coords = {
        'Paris': (48.8566, 2.3522),
        'Tokyo': (35.6762, 139.6503),
        'New York': (40.7128, -74.0060),
        'London': (51.5074, -0.1278),
        'Rome': (41.9028, 12.4964),
        'Barcelona': (41.3851, 2.1734),
        'Berlin': (52.5200, 13.4050),
        'Amsterdam': (52.3676, 4.9041),
        'Sydney': (-33.8688, 151.2093),
        'Toronto': (43.6532, -79.3832)
    }
    
    restaurants = []
    for i in range(count):
        cuisine = random.choice(cuisines)
        location = random.choice(locations)
        base_coords = city_coords.get(location, (48.8566, 2.3522))
        
        # Ajouter des variations aléatoires aux coordonnées
        lat_variation = random.uniform(-0.05, 0.05)
        lng_variation = random.uniform(-0.05, 0.05)
        
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