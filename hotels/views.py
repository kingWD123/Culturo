from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import requests
import google.generativeai as genai
from urllib.parse import urlencode

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

def hotel_page(request):
    return render(request, 'hotels/hotel.html')

def hotel_map(request):
    return render(request, 'hotels/hotel_map.html')

def get_unsplash_image(query):
    """Get image from Unsplash API"""
    try:
        url = "https://api.unsplash.com/search/photos"
        params = {
            'query': query,
            'per_page': 1,
            'client_id': settings.UNSPLASH_ACCESS_KEY
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['urls']['small']
    except Exception as e:
        print(f"Error fetching Unsplash image: {e}")
    return None

def build_qloo_url(base_url, **params):
    """Build Qloo API URL with parameters"""
    query_params = {}
    for key, value in params.items():
        if value is not None:
            if key == 'location_query':
                query_params['filter.location.query'] = value
            elif key == 'entity_type':
                query_params['filter.type'] = value
            elif key == 'signal_entities':
                query_params['signal.interests.entities'] = value
            else:
                query_params[key] = value
    
    return f"{base_url}?{urlencode(query_params)}"

@csrf_exempt
@login_required
def hotel_chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            history = data.get('history', [])
            
            # Build conversation history for Gemini
            conversation_history = []
            for msg in history:
                role = "user" if msg['role'] == 'user' else "model"
                conversation_history.append({
                    "role": role,
                    "parts": [msg['content']]
                })
            
            # Check if this is an initial request for popular hotels
            is_initial_request = (len(history) == 1 and 
                                'popular hotel recommendations worldwide' in history[0].get('content', '').lower())
            
            if is_initial_request:
                # For initial request, provide popular hotels directly
                bot_message = "Here are some popular hotel destinations worldwide! I can help you find more specific recommendations based on your preferences. Where would you like to stay?"
                
                # Generate mock popular hotels from different cities
                popular_hotels = [
                    {
                        'name': 'The Ritz Paris',
                        'location': 'Paris, France',
                        'rating': '4.8',
                        'price_range': '$$$$',
                        'description': 'Legendary luxury hotel in the heart of Paris',
                        'amenities': ['spa', 'restaurant', 'bar', 'concierge'],
                        'coordinates': {'lat': 48.8566, 'lng': 2.3522},
                        'img': get_unsplash_image("luxury hotel Paris")
                    },
                    {
                        'name': 'Marina Bay Sands',
                        'location': 'Singapore',
                        'rating': '4.7',
                        'price_range': '$$$$',
                        'description': 'Iconic hotel with infinity pool and stunning views',
                        'amenities': ['pool', 'casino', 'shopping', 'restaurants'],
                        'coordinates': {'lat': 1.2834, 'lng': 103.8607},
                        'img': get_unsplash_image("Marina Bay Sands Singapore")
                    },
                    {
                        'name': 'The Plaza Hotel',
                        'location': 'New York, USA',
                        'rating': '4.6',
                        'price_range': '$$$$',
                        'description': 'Historic luxury hotel overlooking Central Park',
                        'amenities': ['spa', 'restaurant', 'fitness center', 'business center'],
                        'coordinates': {'lat': 40.7648, 'lng': -73.9808},
                        'img': get_unsplash_image("Plaza Hotel New York")
                    }
                ]
                
                return JsonResponse({
                    'message': bot_message,
                    'hotels': popular_hotels,
                    'qloo_url': None,
                    'done': False
                })
            
            # Check for direct location queries (like "paris")
            user_message = history[-1].get('content', '').lower().strip()
            
            # Common city names for direct detection
            cities = ['paris', 'london', 'tokyo', 'new york', 'rome', 'barcelona', 'berlin', 'amsterdam', 'madrid', 'vienna']
            
            detected_city = None
            for city in cities:
                if city in user_message:
                    detected_city = city
                    break
            
            if detected_city:
                # Direct city query - use Qloo API
                bot_message = f"Great choice! Here are some excellent hotels in {detected_city.title()}:"
                
                # Build Qloo URL
                qloo_url = build_qloo_url(
                    "https://hackathon.api.qloo.com/v2/insights/",
                    entity_type="urn:entity:place",
                    signal_entities="DC37BBAC-E7C4-48F3-BEED-1BE35786B3A5",
                    location_query=detected_city
                )
                
                hotels = []
                
                # Call Qloo API
                headers = {
                    'X-API-KEY': settings.CLOOAI_API_KEY,
                    'Content-Type': 'application/json'
                }
                
                try:
                    qloo_response = requests.get(qloo_url, headers=headers, timeout=10)
                    print(f"Qloo API Status: {qloo_response.status_code}")
                    
                    if qloo_response.status_code == 200:
                        qloo_data = qloo_response.json()
                        print(f"Qloo response structure: {list(qloo_data.keys())}")
                        
                        # Process hotels from Qloo API (similar to restaurants)
                        for entity in qloo_data.get("results", {}).get("entities", []):
                            hotel = {}
                            hotel["name"] = entity.get("name", "Hotel Name Not Available")
                            properties = entity.get("properties", {})
                            
                            # Location
                            hotel["location"] = properties.get("address", f"{detected_city.title()}, Location not specified")
                            
                            # Rating
                            hotel["rating"] = properties.get("business_rating", 4.0)
                            
                            # Price range
                            price_level = properties.get("price_level", 2)
                            hotel["price_range"] = '$' * min(price_level, 4)
                            
                            # Description
                            hotel["description"] = f"Excellent accommodation in {detected_city.title()}"
                            
                            # Amenities
                            amenities = []
                            if 'keywords' in properties:
                                hotel_amenities = ['spa', 'pool', 'gym', 'restaurant', 'bar', 'wifi', 'parking', 'concierge']
                                for keyword in properties['keywords']:
                                    if keyword['name'].lower() in hotel_amenities:
                                        amenities.append(keyword['name'].lower())
                            
                            if not amenities:
                                amenities = ['wifi', 'restaurant', 'concierge']
                            
                            hotel["amenities"] = amenities
                            
                            # Coordinates
                            location_coords = {
                                'paris': (48.8566, 2.3522),
                                'london': (51.5074, -0.1278),
                                'tokyo': (35.6762, 139.6503),
                                'new york': (40.7128, -74.0060),
                                'rome': (41.9028, 12.4964),
                                'barcelona': (41.3851, 2.1734),
                                'berlin': (52.5200, 13.4050),
                                'amsterdam': (52.3676, 4.9041),
                                'madrid': (40.4168, -3.7038),
                                'vienna': (48.2082, 16.3738)
                            }
                            
                            base_coords = location_coords.get(detected_city, (48.8566, 2.3522))
                            import random
                            hotel["coordinates"] = {
                                'lat': base_coords[0] + random.uniform(-0.05, 0.05),
                                'lng': base_coords[1] + random.uniform(-0.05, 0.05)
                            }
                            
                            # Image
                            search_query = f"{hotel['name']} hotel {detected_city}"
                            hotel["img"] = get_unsplash_image(search_query.strip())
                            
                            hotels.append(hotel)
                    
                    else:
                        print(f"Qloo API Error: {qloo_response.status_code}")
                        # Generate mock data if API fails
                        hotels = generate_mock_hotels(3, detected_city)
                        
                except requests.exceptions.Timeout:
                    print("Timeout lors de l'appel à l'API Qloo")
                    hotels = generate_mock_hotels(3, detected_city)
                except requests.exceptions.RequestException as e:
                    print(f"Erreur réseau Qloo: {e}")
                    hotels = generate_mock_hotels(3, detected_city)
                
                # If no hotels from API, generate mock data
                if not hotels:
                    hotels = generate_mock_hotels(3, detected_city)
                
                return JsonResponse({
                    'message': bot_message,
                    'hotels': hotels,
                    'qloo_url': qloo_url,
                    'done': True
                })
            
            # For other queries, use Gemini
            system_prompt = """You are a helpful hotel recommendation assistant. Your goal is to understand the user's hotel preferences and provide personalized recommendations.
Be conversational and helpful. Ask one question at a time to avoid overwhelming the user.
Avoid long answers.
Give short responses with less thant 20 words\n
Ask questions about:
- Destination/location
- Budget range
- Hotel type (luxury, business, boutique, budget, etc.)
- Amenities preferences (spa, pool, gym, restaurant, etc.)
- Travel dates or season
- Purpose of travel (business, leisure, romantic, family, etc.)

When you have enough information, provide a JSON response with hotel search parameters:
```json
{
    "location": "destination name",
    "hotel_type": "luxury/business/boutique/budget",
    "amenities": ["spa", "pool", "gym"],
    "budget_range": "low/medium/high",
    "travel_purpose": "business/leisure/romantic/family"
}
```


"""

            # Create the model
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Generate response
            chat = model.start_chat(history=conversation_history[:-1])
            response = chat.send_message(conversation_history[-1]["parts"][0])
            bot_message = response.text
            
            # Try to extract JSON parameters for Qloo API
            hotels = []
            qloo_url = None
            qloo_params = None
            
            try:
                # Look for JSON in the response
                import re
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', bot_message, re.DOTALL)
                if json_match:
                    qloo_params = json.loads(json_match.group(1))
                    location = qloo_params.get('location', '')
                    
                    if location:
                        # Build Qloo URL for hotels
                        qloo_url = build_qloo_url(
                            "https://hackathon.api.qloo.com/v2/insights/",
                            entity_type="urn:entity:place",
                            signal_entities="DC37BBAC-E7C4-48F3-BEED-1BE35786B3A5",
                            location_query=location
                        )
                        
                        # Call Qloo API
                        headers = {
                            'X-API-KEY': settings.CLOOAI_API_KEY,
                            'Content-Type': 'application/json'
                        }
                        
                        try:
                            qloo_response = requests.get(qloo_url, headers=headers, timeout=10)
                            print(f"Status code Qloo: {qloo_response.status_code}")
                            
                            if qloo_response.status_code == 200:
                                qloo_data = qloo_response.json()
                                
                                # Process hotels from Qloo API
                                for entity in qloo_data.get("results", {}).get("entities", []):
                                    hotel = {}
                                    hotel["name"] = entity.get("name")
                                    properties = entity.get("properties", {})
                                    
                                    # Location
                                    hotel["location"] = properties.get("address", "Address not available")
                                    
                                    # Rating
                                    hotel["rating"] = properties.get("business_rating", 4.0)
                                    
                                    # Price range
                                    price_level = properties.get("price_level", 2)
                                    hotel["price_range"] = '$' * min(price_level, 4)
                                    
                                    # Description
                                    location_query = qloo_params.get("location", "worldwide")
                                    hotel["description"] = f"Excellent accommodation in {location_query}."
                                    
                                    # Amenities
                                    amenities = []
                                    if 'keywords' in properties and len(properties['keywords']) > 0:
                                        hotel_amenities = ['spa', 'pool', 'gym', 'restaurant', 'bar', 'wifi', 'parking', 'concierge']
                                        
                                        for keyword in properties['keywords']:
                                            if keyword['name'].lower() in hotel_amenities:
                                                amenities.append(keyword['name'].lower())
                                        
                                        if not amenities and len(properties['keywords']) > 0:
                                            amenities = [properties['keywords'][0]['name'].lower()]
                                    
                                    if not amenities:
                                        amenities = ['wifi', 'restaurant']
                                    
                                    hotel["amenities"] = amenities
                                    
                                    # Coordinates
                                    location_coords = {
                                        'paris': (48.8566, 2.3522),
                                        'london': (51.5074, -0.1278),
                                        'tokyo': (35.6762, 139.6503),
                                        'new york': (40.7128, -74.0060),
                                        'rome': (41.9028, 12.4964),
                                        'barcelona': (41.3851, 2.1734),
                                        'worldwide': (48.8566, 2.3522)
                                    }
                                    
                                    location_key = location_query.lower()
                                    base_coords = location_coords.get(location_key, (48.8566, 2.3522))
                                    import random
                                    hotel["coordinates"] = {
                                        'lat': base_coords[0] + random.uniform(-0.05, 0.05),
                                        'lng': base_coords[1] + random.uniform(-0.05, 0.05)
                                    }

                                    # Image
                                    search_query = f"{hotel['name']} hotel"
                                    hotel["img"] = get_unsplash_image(search_query.strip())
                                    
                                    hotels.append(hotel)
                            
                            else:
                                print(f"Qloo API Error: {qloo_response.status_code}")
                                # Generate mock data
                                location_query = qloo_params.get("location", "worldwide")
                                hotels = generate_mock_hotels(3, location_query)
                                
                        except requests.exceptions.Timeout:
                            print("Timeout lors de l'appel à l'API Qloo")
                            location_query = qloo_params.get("location", "worldwide")
                            hotels = generate_mock_hotels(3, location_query)
                        except requests.exceptions.RequestException as e:
                            print(f"Erreur réseau Qloo: {e}")
                            location_query = qloo_params.get("location", "worldwide")
                            hotels = generate_mock_hotels(3, location_query)
                            
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Erreur lors du parsing JSON: {e}")
                # Pas de JSON trouvé, c'est normal pour les premières interactions

            # Determine if conversation is done
            done = qloo_params is not None and len(hotels) > 0

            print(f"Returning response with {len(hotels)} hotels")
            return JsonResponse({
                "message": bot_message,
                "qloo_url": qloo_url,
                "done": done,
                "hotels": hotels
            })
            
        except Exception as e:
            print(f"=== ERROR IN HOTEL CHATBOT API ===")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
            return JsonResponse({
                "message": "Sorry, an error occurred. Please try again.",
                "error": str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Function to generate mock hotel data
def generate_mock_hotels(count=3, location_query="worldwide"):
    hotel_types = ['Grand Hotel', 'Business Inn', 'Boutique Hotel', 'Luxury Resort', 'City Hotel', 'Palace Hotel']
    
    # If a specific location is requested, use it
    if location_query and location_query.lower() != "worldwide":
        locations = [location_query.title()]
    else:
        locations = ['Paris', 'Tokyo', 'New York', 'London', 'Rome', 'Barcelona', 'Berlin', 'Amsterdam', 'Sydney', 'Toronto']
    
    price_ranges = ['$', '$$', '$$$', '$$$$']
    amenities_list = [
        ['spa', 'pool', 'restaurant'],
        ['gym', 'wifi', 'parking'],
        ['concierge', 'bar', 'room service'],
        ['business center', 'conference rooms', 'wifi'],
        ['spa', 'restaurant', 'concierge'],
        ['pool', 'bar', 'parking']
    ]
    
    # Coordinates for major cities
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
    
    hotels = []
    import random
    for i in range(count):
        hotel_type = random.choice(hotel_types)
        location = random.choice(locations)
        base_coords = city_coords.get(location, (48.8566, 2.3522))
        
        # Add random variations to coordinates
        lat_variation = random.uniform(-0.05, 0.05)
        lng_variation = random.uniform(-0.05, 0.05)
        
        hotel = {
            'name': f"{hotel_type} {location}",
            'location': f"{location} City Center",
            'rating': round(random.uniform(3.5, 5.0), 1),
            'price_range': random.choice(price_ranges),
            'description': f"Excellent accommodation in {location}.",
            'amenities': random.choice(amenities_list),
            'coordinates': {
                'lat': base_coords[0] + lat_variation,
                'lng': base_coords[1] + lng_variation
            },
            'img': get_unsplash_image(f"{hotel_type} {location} hotel")
        }
        hotels.append(hotel)
    
    return hotels


def hotel_detail(request, hotel_name):
    """Vue pour afficher les détails d'un hôtel et permettre la réservation"""
    # Décodage du nom de l'hôtel (remplace les tirets par des espaces)
    hotel_name_decoded = hotel_name.replace('-', ' ').title()
    
    # Génération de données fictives pour l'hôtel (dans une vraie app, on récupérerait depuis la DB)
    import random
    
    # Données de base de l'hôtel
    hotel_data = {
        'name': hotel_name_decoded,
        'location': random.choice(['Paris, France', 'London, UK', 'Tokyo, Japan', 'New York, USA', 'Rome, Italy']),
        'rating': round(random.uniform(4.0, 5.0), 1),
        'price_per_night': random.randint(80, 500),
        'description': f"Experience luxury and comfort at {hotel_name_decoded}. Our hotel offers exceptional service and world-class amenities in the heart of the city.",
        'amenities': random.sample(['WiFi', 'Pool', 'Spa', 'Gym', 'Restaurant', 'Bar', 'Room Service', 'Concierge', 'Parking', 'Business Center'], 6),
        'address': f"{random.randint(1, 999)} {random.choice(['Main St', 'Central Ave', 'Grand Blvd', 'Royal Rd', 'Palace St'])}, City Center",
        'phone': f"+{random.randint(1, 99)} {random.randint(1, 9)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}",
        'email': f"reservations@{hotel_name_decoded.lower().replace(' ', '')}.com",
        'check_in': "15:00",
        'check_out': "11:00",
        'room_types': [
            {
                'name': 'Standard Room',
                'price': random.randint(80, 150),
                'description': 'Comfortable room with modern amenities',
                'capacity': '2 guests',
                'size': '25 m²'
            },
            {
                'name': 'Deluxe Room',
                'price': random.randint(150, 250),
                'description': 'Spacious room with city view',
                'capacity': '2-3 guests',
                'size': '35 m²'
            },
            {
                'name': 'Suite',
                'price': random.randint(250, 500),
                'description': 'Luxury suite with separate living area',
                'capacity': '4 guests',
                'size': '50 m²'
            }
        ]
    }
    
    # Récupération d'images depuis Unsplash
    images = []
    try:
        search_query = f"{hotel_name_decoded} hotel luxury"
        url = f"https://api.unsplash.com/search/photos?query={search_query}&client_id={settings.UNSPLASH_ACCESS_KEY}&per_page=20&orientation=landscape"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            images = [img['urls']['regular'] for img in data.get('results', [])]
    except Exception as e:
        print(f"Erreur Unsplash: {e}")
    
    # Images par défaut si Unsplash ne fonctionne pas
    if not images:
        images = [
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
            "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800"
        ]
    
    context = {
        'hotel': hotel_data,
        'images': images,
        'hotel_name': hotel_name_decoded
    }
    
    return render(request, 'hotels/hotel_detail.html', context)
