from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
from django.conf import settings
import requests
from urllib.parse import urlencode
import re

genai.configure(api_key=settings.GEMINI_API_KEY)

def build_qloo_url(entity_type="urn:entity:destination", extra_params=None):
    """Génère une URL Qloo pour les recommandations de destinations."""
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

def destination_recommandations(request):
    """Page of destination recommendations with a map"""
    return render(request, 'destination/destination_recommandations.html')

@csrf_exempt
def destination_chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        history = data.get("history", [])

        system_prompt = (
            "Tu es un assistant spécialisé dans les recommandations de destinations. "
            "Pose des questions pour comprendre :\n"
            "- Le pays ou la région souhaitée (ex : France)\n"
            "- Les centres d'intérêt (plage, montagne, culture, etc.)\n"
            "- Le niveau de popularité ou d'animation recherché (ex : lieux populaires, lieux actifs)\n"
            "- Les choses à éviter (ex : pas de lieux détente)\n"
            "Quand tu as assez d'informations, génère le JSON Qloo à la fin de ta réponse, entre balises ```json et ```, sans jamais l'afficher à l'utilisateur dans la partie visible/conversationnelle. Ce JSON est uniquement destiné à l'API.\n"
            '{\n'
            '  "filter.type": "urn:entity:destination",\n'
            '  "filter.geocode.country_code": "FR",\n'
            '  "filter.popularity.min": 0.6,\n'
            '  "signal.interests.tags": ["plage"],\n'
            '  "filter.exclude.tags": ["détente"]\n'
            '}\n'
            "N'invente pas de tags ou de paramètres si l'utilisateur ne les a pas donnés.\n"
            "L'utilisateur n'est pas obligé de répondre à toutes les questions.\n"
            "Pose les question les unes après les autres, pour ne pas submerger l'utilisateur.\n"
            "N'évoque jamais les paramètres Qloo dans tes réponses.\n"
            "Adapte tes questions pour obtenir ces informations de façon naturelle."
        )

        messages = [{"role": "user", "parts": [system_prompt]}]
        for m in history:
            messages.append({"role": m["role"], "parts": [m["content"]]})

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(messages)
        bot_message = response.text

        destinations = []
        qloo_params = None
        
        try:
            # Cherche le JSON entre balises ```json ... ```
            match = re.search(r'```json\s*([\s\S]+?)\s*```', bot_message)
            if match:
                qloo_params = json.loads(match.group(1))
            else:
                # Fallback: essaie de parser le premier JSON trouvé
                start = bot_message.index("{")
                end = bot_message.rindex("}") + 1
                qloo_params = json.loads(bot_message[start:end])
            
            qloo_url = build_qloo_url(extra_params=qloo_params)
            print("qloo_url: ", qloo_url)
            
            qloo_headers = {
                "x-api-key": settings.CLOOAI_API_KEY,
                "Accept": "application/json"
            }
            qloo_response = requests.get(qloo_url, headers=qloo_headers)

            if qloo_response.status_code == 200:
                qloo_data = qloo_response.json()
                print("qloo_data: ", qloo_data)
                for entity in qloo_data.get("results", {}).get("entities", []):
                    properties = entity.get("properties", {})
                    dest = {
                        "name": entity.get("name"),
                        "location": properties.get("location_name"),
                        "latitude": properties.get("latitude"),
                        "longitude": properties.get("longitude"),
                        "img": properties.get("image", {}).get("url"),
                        "desc": properties.get("description")
                    }
                    if dest["latitude"] and dest["longitude"]:
                        destinations.append(dest)
            else:
                print(f"Qloo API Error: {qloo_response.status_code} - {qloo_response.text}")

        except (ValueError, KeyError, json.JSONDecodeError) as e:
            print(f"Error processing chatbot response or Qloo API: {e}")
            pass

        return JsonResponse({
            "message": bot_message,
            "destinations": destinations
        })

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

