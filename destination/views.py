from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
import ast
import requests
from django.contrib.auth.decorators import login_required
from django.conf import settings
import google.generativeai as genai
from urllib.parse import urlencode

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

def get_unsplash_image(query):
    """Get an image from Unsplash API"""
    access_key = getattr(settings, 'UNSPLASH_ACCESS_KEY', None)
    if not access_key:
        return "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
    
    try:
        url = f"https://api.unsplash.com/search/photos?query={query}&client_id={access_key}&per_page=1&orientation=landscape"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get('results'):
            return data['results'][0]['urls']['regular']
    except Exception as e:
        print(f"Unsplash error: {e}")
    
    return "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"

def build_qloo_url(entity_type="urn:entity:destination", entity_ids=None, extra_params=None):
    """Generates a Qloo URL for destination recommendations."""
    base_url = "https://hackathon.api.qloo.com/v2/insights/"
    
    params = {
        "filter.type": entity_type,
    }
    
    if entity_ids:
        params["signal.interests.entities"] = json.dumps(entity_ids)
    
    if extra_params:
        for key, value in extra_params.items():
            if isinstance(value, list):
                # For tag lists, convert to JSON string
                params[key] = json.dumps(value)
            else:
                params[key] = value
    
    return base_url + "?" + urlencode(params)

def destination_recommandations(request):
    """Page of destination recommendations with a map"""
    return render(request, 'destination/destination_recommandations.html')

@csrf_exempt
@login_required
def destination_chatbot_api(request):
    try:
        print(f"Request method: {request.method}")
        print(f"Request body: {request.body}")
        
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                print(f"Parsed data: {data}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
            
            history = data.get("history", [])
            print(f"History: {history}")

            system_prompt = (
                "You are an assistant specialized in destination recommendations. "
                "Your MAIN GOAL is to provide destination recommendations as quickly as possible. "
                "After the user provides ANY information about their preferences (even just a city name or interest), "
                "you MUST immediately generate recommendations by including the Qloo JSON at the end of your response. "
                "Guidelines:\n"
                "- If user mentions a city (like Paris), recommend similar destinations\n"
                "- If user mentions interests (nightlife, culture, etc.), use those as tags\n"
                "- If user mentions popularity preference, adjust the popularity filter\n"
                "- Default country: France (FR) if not specified\n"
                "- Default popularity: 0.6 for popular places, 0.3 for less known places\n"
                "CRITICAL: You MUST ALWAYS end your response with a JSON block between ```json and ``` tags. "
                "The JSON must be STRICTLY valid JSON format with double quotes only. "
                "Example for nightlife destinations in France:\n"
                '```json\n'
                '{\n'
                '  "filter.type": "urn:entity:destination",\n'
                '  "filter.geocode.country_code": "FR",\n'
                '  "filter.popularity.min": 0.6,\n'
                '  "signal.interests.tags": ["nightlife"]\n'
                '}\n'
                '```\n'
                "Example for destinations similar to Paris:\n"
                '```json\n'
                '{\n'
                '  "filter.type": "urn:entity:destination",\n'
                '  "filter.geocode.country_code": "FR",\n'
                '  "filter.popularity.min": 0.7,\n'
                '  "signal.interests.tags": ["culture", "nightlife"]\n'
                '}\n'
                '```\n'
                "NEVER end a conversation without providing the JSON block for recommendations. "
                "Be conversational but ALWAYS conclude with recommendations."
            )

            try:
                print("Configuring Gemini...")
                print(f"Gemini API Key configured: {bool(settings.GEMINI_API_KEY)}")
                
                messages = [{"role": "user", "parts": [system_prompt]}]
                for m in history:
                    messages.append({"role": m["role"], "parts": [m["content"]]})
                
                print(f"Messages to send to Gemini: {messages}")
                
                model = genai.GenerativeModel("gemini-2.0-flash")
                print("Model created, generating content...")
                
                response = model.generate_content(messages)
                print(f"Gemini response received: {response}")
                
                bot_message = response.text
                print(f"Bot message: {bot_message}")
                
            except Exception as e:
                print(f"Gemini API Error details: {type(e).__name__}: {e}")
                import traceback
                print(f"Full traceback: {traceback.format_exc()}")
                return JsonResponse({
                    "message": f"Gemini technical error: {str(e)}",
                    "destinations": []
                })

            destinations = []
            qloo_params = None
            
            try:
                # Look for the LAST ```json ... ``` block
                matches = list(re.finditer(r'```json\s*([\s\S]+?)\s*```', bot_message))
                json_str = None
                if matches:
                    json_str = matches[-1].group(1)
                else:
                    # Fallback: try to extract the last JSON object from the response
                    try:
                        start = bot_message.rindex("{")
                        # Go back to find the beginning of the last JSON object
                        while start > 0 and bot_message[start-1] != '\n':
                            start -= 1
                        end = bot_message.rindex("}") + 1
                        json_str = bot_message[start:end]
                    except Exception:
                        json_str = None

                print("JSON extracted from chatbot:")
                print(json_str)

                if json_str:
                    # Basic cleanup: replace single quotes with double quotes if needed
                    if json_str.count('"') < 2 and json_str.count("'") > 1:
                        json_str = json_str.replace("'", '"')
                    json_str = json_str.strip()
                    try:
                        qloo_params = json.loads(json_str)
                    except json.JSONDecodeError:
                        try:
                            qloo_params = ast.literal_eval(json_str)
                        except Exception as e:
                            print(f"Unable to parse Gemini JSON: {e}")
                            qloo_params = None
                else:
                    print("No JSON detected in chatbot response.")

                if not qloo_params:
                    return JsonResponse({
                        "message": bot_message,  # Return the conversational bot response
                        "destinations": [],
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
                    destinations = []
                    for entity in qloo_data.get("results", {}).get("entities", []):
                        destination = {}
                        destination["name"] = entity.get("name")
                        properties = entity.get("properties", {})
                        geocode = properties.get("geocode", {})
                        location = entity.get("location", {})

                        destination["location1"] = geocode.get("admin1_region")
                        destination["location2"] = geocode.get("admin2_region")
                        destination["latitude"] = location.get("lat")
                        destination["longitude"] = location.get("lon")
                        destination["geohash"] = location.get("geohash")
                        destination["popularity"] = entity.get("popularity")

                        # Enrich with Unsplash image
                        search_query = f"{destination['name']} {destination.get('location1', '')}"
                        destination["img"] = get_unsplash_image(search_query.strip())
                        
                        destinations.append(destination)
                    
       
                else:
                    print(f"Qloo API Error: {qloo_response.status_code} - {qloo_response.text}")

            except (ValueError, KeyError, json.JSONDecodeError) as e:
                print(f"Error processing chatbot response or Qloo API: {e}")
                pass

            return JsonResponse({
                "message": bot_message,
                "destinations": destinations
            })

        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    except Exception as e:
        print(f"Unexpected error in destination_chatbot_api: {type(e).__name__}: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return JsonResponse({
            "error": "An unexpected error occurred",
            "message": f"Detailed error: {str(e)}",
            "destinations": []
        }, status=500)

def destination_detail(request, name):
    access_key = getattr(settings, 'UNSPLASH_ACCESS_KEY', None)
    images = []
    destination_info = None
    
    # Get images from Unsplash
    if access_key:
        url = f"https://api.unsplash.com/search/photos?query={name}&client_id={access_key}&per_page=30&orientation=landscape"
        try:
            resp = requests.get(url, timeout=5)
            data = resp.json()
            images = [img['urls']['regular'] for img in data.get('results', [])]
        except Exception as e:
            print(f"Unsplash error: {e}")
    
    # Get destination information from Qloo API
    try:
        qloo_params = {
            "filter.type": "urn:entity:destination",
            "filter.name": name
        }
        qloo_url = build_qloo_url(extra_params=qloo_params)
        qloo_headers = {
            "x-api-key": settings.CLOOAI_API_KEY,
            "Accept": "application/json"
        }
        qloo_response = requests.get(qloo_url, headers=qloo_headers)
        
        if qloo_response.status_code == 200:
            qloo_data = qloo_response.json()
            entities = qloo_data.get("results", {}).get("entities", [])
            if entities:
                entity = entities[0]  # Take the first match
                properties = entity.get("properties", {})
                geocode = properties.get("geocode", {})
                location = entity.get("location", {})
                
                destination_info = {
                    "name": entity.get("name"),
                    "location1": geocode.get("admin1_region"),
                    "location2": geocode.get("admin2_region"),
                    "country": geocode.get("country_code"),
                    "latitude": location.get("lat"),
                    "longitude": location.get("lon"),
                    "popularity": entity.get("popularity"),
                    "tags": properties.get("tags", [])
                }
                
                # Generate description using Gemini
                try:
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    prompt = f"""
                    Write a compelling and informative description for the destination "{name}" located in {destination_info.get('location1', '')}, {destination_info.get('country', '')}.
                    
                    Include information about:
                    - What makes this destination special and unique
                    - Main attractions and activities
                    - Cultural highlights
                    - Best time to visit
                    - Local cuisine or specialties
                    
                    Keep it engaging, informative, and around 200-300 words. Write in French.
                    """
                    
                    response = model.generate_content(prompt)
                    destination_info["description"] = response.text
                except Exception as e:
                    print(f"Gemini error for description: {e}")
                    destination_info["description"] = f"Découvrez {name}, une destination fascinante qui vous attend avec ses merveilles uniques et son charme authentique."
        
    except Exception as e:
        print(f"Qloo API error: {e}")
    
    # If no destination info found, create a basic one
    if not destination_info:
        destination_info = {
            "name": name,
            "description": f"Découvrez {name}, une destination fascinante qui vous attend avec ses merveilles uniques et son charme authentique."
        }
    
    return render(request, "destination/destination_detail.html", {
        "name": name, 
        "images": images,
        "destination_info": destination_info
    })

