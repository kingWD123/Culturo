import json
import os
import random
import requests
import re
import ast
from urllib.parse import urlencode
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Import Google Generative AI
import google.generativeai as genai

# Configuration de l'API Gemini
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY', 'your-api-key'))
model = genai.GenerativeModel('gemini-pro')

# Fonction pour récupérer des images d'Unsplash
def get_unsplash_image(query):
    try:
        unsplash_access_key = os.environ.get('UNSPLASH_ACCESS_KEY', 'your-unsplash-key')
        url = f"https://api.unsplash.com/search/photos?query={query}&client_id={unsplash_access_key}&per_page=1"
        response = requests.get(url)
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]['urls']['regular']
    except Exception as e:
        print(f"Erreur Unsplash: {e}")
    return "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=1000&auto=format&fit=crop"

# Fonction pour construire l'URL Qloo
def build_qloo_url(entity_type, entity_id=None, limit=10):
    qloo_api_key = os.environ.get('QLOO_API_KEY', 'your-qloo-key')
    base_url = "https://api.qloo.com/v1/recommendations"
    
    if entity_id:
        url = f"{base_url}/{entity_type}/{entity_id}?limit={limit}&apikey={qloo_api_key}"
    else:
        url = f"{base_url}/{entity_type}?limit={limit}&apikey={qloo_api_key}"
    
    return url

# Vue principale pour les recommandations de restaurants
def restaurant_recommandations(request):
    return render(request, 'restaurant/restaurant_recommandations.html')

# API du chatbot pour les restaurants
@csrf_exempt
def restaurant_chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            chat_history = data.get('history', [])
            
            # Formatage de l'historique pour Gemini
            gemini_history = []
            for msg in chat_history:
                role = 'user' if msg['role'] == 'user' else 'model'
                gemini_history.append({"role": role, "parts": [msg['content']]})
            
            # Si c'est le premier message ou si l'historique est vide
            if not gemini_history:
                gemini_history = [{"role": "user", "parts": ["Donne-moi des recommandations de restaurants populaires en France."]}]
            
            # Ajout d'un contexte système pour guider le modèle
            system_prompt = """
            Tu es un assistant spécialisé dans les recommandations de restaurants. 
            Ton objectif est d'aider l'utilisateur à trouver des restaurants qui correspondent à ses préférences.
            
            Pose des questions pour comprendre :
            - La région ou ville en France où l'utilisateur souhaite manger
            - Le type de cuisine recherché (ex : italienne, française, japonaise)
            - Le budget (ex : économique, moyen, luxe)
            - L'ambiance recherchée (ex : romantique, familial, branché)
            
            Quand tu as assez d'informations, génère le JSON Qloo à la fin de ta réponse, entre balises ```json et ``` 
            Le JSON doit être STRICTEMENT valide, conforme à la norme JSON : toutes les clés et valeurs doivent être entourées de guillemets doubles, aucune virgule en trop, aucune syntaxe Python, pas de commentaires.
            
            Exemple strictement valide :
            ```json
            {
              "filter.type": "urn:entity:place",
              "filter.location.query": "Paris",
              "signal.interests.tags": ["restaurant", "italian"]
            }
            ```
            
            N'invente pas de tags ou de paramètres si l'utilisateur ne les a pas donnés.
            L'utilisateur n'est pas obligé de répondre à toutes les questions.
            Pose les questions les unes après les autres, pour ne pas submerger l'utilisateur.
            N'évoque jamais les paramètres Qloo dans tes réponses.
            Adapte tes questions pour obtenir ces informations de façon naturelle.
            IMPORTANT: Assure-toi d'inclure la région ou ville mentionnée par l'utilisateur dans le paramètre 'filter.location.query' du JSON.
            """
            
            # Ajout du prompt système au début de l'historique
            gemini_history.insert(0, {"role": "model", "parts": [system_prompt]})
            
            # Appel à l'API Gemini
            response = model.generate_content(gemini_history)
            response_text = response.text
            
            # Extraction du JSON avec les paramètres Qloo
            qloo_params = None
            try:
                # Cherche le DERNIER bloc ```json ... ```
                matches = list(re.finditer(r'```json\s*([\s\S]+?)\s*```', response_text))
                json_str = None
                if matches:
                    json_str = matches[-1].group(1)
                else:
                    # Fallback: essaie d'extraire le dernier objet JSON de la réponse
                    try:
                        start = response_text.rindex("{")
                        # Remonte pour trouver le début du dernier objet JSON
                        while start > 0 and response_text[start-1] != '\n':
                            start -= 1
                        end = response_text.rindex("}") + 1
                        json_str = response_text[start:end]
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
                    
                # Si aucun paramètre n'a été trouvé, utiliser des valeurs par défaut
                if not qloo_params:
                    qloo_params = {
                        "filter.type": "urn:entity:place",
                        "filter.location.query": "France",
                        "signal.interests.tags": ["restaurant"]
                    }
            except Exception as e:
                print(f"Erreur lors de l'extraction du JSON: {e}")
                qloo_params = {
                    "filter.type": "urn:entity:place",
                    "filter.location.query": "France",
                    "signal.interests.tags": ["restaurant"]
                }
            
            # Appel à l'API Qloo pour obtenir des recommandations de restaurants
            restaurants_data = []
            try:
                # Construction de l'URL de l'API Qloo avec les paramètres extraits
                base_url = "https://hackathon.api.qloo.com/v2/insights/"
                params = {}
                
                # Ajout des paramètres extraits du JSON
                for key, value in qloo_params.items():
                    if isinstance(value, list):
                        # Pour les listes de tags, Qloo attend une chaîne de caractères séparée par des virgules
                        params[key] = ",".join(value)
                    else:
                        params[key] = value
                
                # S'assurer que le type est toujours défini
                if "filter.type" not in params:
                    params["filter.type"] = "urn:entity:place"
                
                # Construire l'URL finale
                qloo_url = base_url + "?" + urlencode(params)
                
                # Ajout des headers nécessaires
                qloo_headers = {
                    "x-api-key": os.environ.get('CLOOAI_API_KEY', 'your-qloo-key'),
                    "Accept": "application/json"
                }
                
                # Appel à l'API Qloo
                qloo_response = requests.get(qloo_url, headers=qloo_headers)
                qloo_data = qloo_response.json()
                
                # Traitement des données de l'API Qloo
                if 'results' in qloo_data and 'entities' in qloo_data['results'] and len(qloo_data['results']['entities']) > 0:
                    for place in qloo_data['results']['entities'][:8]:  # Augmenter à 8 restaurants pour plus de variété
                        # Extraction des données pertinentes
                        name = place.get('name', 'Restaurant sans nom')
                        
                        # Extraction de la cuisine à partir des mots-clés
                        cuisine = 'Non spécifiée'
                        if 'properties' in place and 'keywords' in place['properties'] and len(place['properties']['keywords']) > 0:
                            # Parcourir les mots-clés pour trouver un type de cuisine
                            cuisine_keywords = ['italian', 'french', 'japanese', 'chinese', 'indian', 'mexican', 'thai', 'spanish', 'greek', 'american', 'vietnamese', 'korean', 'lebanese', 'turkish']
                            
                            for keyword in place['properties']['keywords']:
                                if keyword['name'].lower() in cuisine_keywords:
                                    cuisine = keyword['name'].capitalize()
                                    break
                            
                            # Si aucun mot-clé de cuisine n'a été trouvé, utiliser le premier mot-clé
                            if cuisine == 'Non spécifiée' and len(place['properties']['keywords']) > 0:
                                cuisine = place['properties']['keywords'][0]['name'].capitalize()
                        
                        # Extraction de l'adresse
                        address = 'Adresse non disponible'
                        if 'properties' in place and 'address' in place['properties']:
                            address = place['properties']['address']
                        
                        # Extraction du prix
                        price_level = '€€'
                        if 'properties' in place and 'price_level' in place['properties']:
                            level = place['properties']['price_level']
                            price_level = '€' * min(level, 4)  # Limiter à 4 €
                        
                        # Extraction de la note
                        rating = 4.0
                        if 'properties' in place and 'business_rating' in place['properties']:
                            rating = place['properties']['business_rating']
                        
                        # Extraction de la localisation pour la description
                        location = "France"
                        if 'filter.location.query' in qloo_params:
                            location = qloo_params['filter.location.query']
                        elif 'properties' in place and 'geocode' in place['properties'] and 'admin1_region' in place['properties']['geocode']:
                            location = place['properties']['geocode']['admin1_region']
                        
                        # Génération d'une description plus détaillée
                        description = f"Un excellent restaurant {cuisine.lower()} situé à {location}."
                        
                        # Ajout de détails supplémentaires à la description si disponibles
                        if 'properties' in place and 'keywords' in place['properties'] and len(place['properties']['keywords']) > 2:
                            specialties = [kw['name'] for kw in place['properties']['keywords'][1:4]]
                            description += f" Spécialités: {', '.join(specialties)}."
                        
                        # Extraction des coordonnées (à implémenter si disponible dans l'API)
                        latitude = None
                        longitude = None
                        
                        # Si pas de coordonnées, utiliser des valeurs par défaut basées sur la localisation
                        if latitude is None or longitude is None:
                            # Dictionnaire des coordonnées par pays/région
                            location_coords = {
                                'france': (48.8566, 2.3522),
                                'paris': (48.8566, 2.3522),
                                'lyon': (45.7578, 4.8320),
                                'marseille': (43.2965, 5.3698),
                                'bordeaux': (44.8378, -0.5792),
                                'italy': (41.9028, 12.4964),
                                'italie': (41.9028, 12.4964),
                                'rome': (41.9028, 12.4964),
                                'milan': (45.4642, 9.1900),
                                'spain': (40.4168, -3.7038),
                                'espagne': (40.4168, -3.7038),
                                'madrid': (40.4168, -3.7038),
                                'barcelona': (41.3851, 2.1734),
                                'germany': (52.5200, 13.4050),
                                'allemagne': (52.5200, 13.4050),
                                'berlin': (52.5200, 13.4050),
                                'munich': (48.1351, 11.5820),
                                'uk': (51.5074, -0.1278),
                                'united kingdom': (51.5074, -0.1278),
                                'royaume-uni': (51.5074, -0.1278),
                                'london': (51.5074, -0.1278),
                                'londres': (51.5074, -0.1278)
                            }
                            
                            # Recherche des coordonnées par localisation
                            location_key = location.lower()
                            base_coords = location_coords.get(location_key, (48.8566, 2.3522))  # Paris par défaut
                            
                            # Ajouter une variation plus importante aux coordonnées pour éviter la superposition
                            latitude = base_coords[0] + random.uniform(-0.05, 0.05)
                            longitude = base_coords[1] + random.uniform(-0.05, 0.05)
                        
                        # Récupération de l'image
                        img_url = get_unsplash_image(f"{name} {cuisine} restaurant")
                        if 'properties' in place and 'images' in place['properties'] and len(place['properties']['images']) > 0:
                            # Utiliser l'image de l'API si disponible
                            img_url = place['properties']['images'][0]['url'].strip()
                        
                        # Construction de l'objet restaurant
                        restaurant = {
                            'name': name,
                            'cuisine': cuisine,
                            'location': address,
                            'price_range': price_level,
                            'rating': rating,
                            'description': description,
                            'latitude': latitude,
                            'longitude': longitude,
                            'img': img_url
                        }
                        
                        restaurants_data.append(restaurant)
            except Exception as e:
                print(f"Erreur lors de l'appel à l'API Qloo: {e}")
            
            # Si aucun restaurant n'a été trouvé via l'API Qloo, générer des données fictives
            if not restaurants_data:
                restaurants_data = generate_mock_restaurants(3)
            
            # Filtrer le JSON technique de la réponse pour l'affichage
            import re
            display_response = re.sub(r'```json[\s\S]*?```', '', response_text).strip()
            
            return JsonResponse({
                'message': display_response,
                'restaurants': restaurants_data
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

# Fonction pour générer des données fictives de restaurants
def generate_mock_restaurants(count=3):
    cuisines = ['Française', 'Italienne', 'Japonaise', 'Mexicaine', 'Indienne', 'Thaïlandaise']
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
        base_coords = city_coords.get(location, (48.8566, 2.3522))  # Paris par défaut
        
        # Ajouter une petite variation aux coordonnées
        lat_variation = random.uniform(-0.02, 0.02)
        lng_variation = random.uniform(-0.02, 0.02)
        
        restaurant = {
            'name': f"Restaurant {chr(65+i)}",
            'cuisine': cuisine,
            'location': location,
            'price_range': random.choice(price_ranges),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'description': f"Un excellent restaurant {cuisine.lower()} situé à {location}.",
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
    cuisines = ['Française', 'Italienne', 'Japonaise', 'Mexicaine', 'Indienne', 'Thaïlandaise']
    locations = ['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Lille', 'Strasbourg']
    
    restaurant = {
        'name': restaurant_name,
        'cuisine': random.choice(cuisines),
        'location': random.choice(locations),
        'price_range': random.choice(['€', '€€', '€€€', '€€€€']),
        'rating': round(random.uniform(3.5, 5.0), 1),
        'description': f"Un excellent restaurant situé à {random.choice(locations)}. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        'img': get_unsplash_image(f"{restaurant_name} restaurant"),
        'address': f"{random.randint(1, 100)} rue de {random.choice(['Paris', 'Lyon', 'Bordeaux', 'Lille'])}, {random.randint(10000, 99999)} France",
        'phone': f"+33 {random.randint(1, 9)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}",
        'website': f"https://www.{restaurant_name.lower().replace(' ', '')}.fr",
        'hours': {
            'Lundi': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Mardi': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Mercredi': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Jeudi': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Vendredi': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Samedi': f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00",
            'Dimanche': 'Fermé' if random.choice([True, False]) else f"{random.randint(11, 12)}:00 - {random.randint(21, 23)}:00"
        }
    }
    
    return render(request, 'restaurant/restaurant_detail.html', {'restaurant': restaurant})