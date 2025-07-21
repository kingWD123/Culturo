from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def destination_recommandations(request):
    """Page of destination recommendations with a map"""
    return render(request, 'destination/destination_recommandations.html')

@csrf_exempt
def destination_chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        history = data.get("history", [])

        system_prompt = (
            "Tu es un assistant spécialisé dans les recommandations de destinations de voyage. "
            "Pose des questions pour comprendre les préférences de l'utilisateur, telles que le type de voyage (aventure, détente, culturel), le budget, la période de l'année, et les centres d'intérêt (plage, montagne, ville, etc.). "
            "Quand tu as assez d'informations, fournis une liste de destinations recommandées avec leurs coordonnées (latitude, longitude) et une brève description, au format JSON. "
            "Par exemple:\n"
            '{\n'
            '  "destinations": [\n'
            '    {\n'
            '      "nom": "Paris, France",\n'
            '      "latitude": 48.8566,\n'
            '      "longitude": 2.3522,\n'
            '      "description": "La ville de l\'amour, avec ses musées emblématiques et sa gastronomie."\n'
            '    }\n'
            '  ]\n'
            '}'
        )

        messages = [{"role": "user", "parts": [system_prompt]}]
        for m in history:
            messages.append({"role": m["role"], "parts": [m["content"]]})

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(messages)
        bot_message = response.text

        destinations = None
        try:
            start = bot_message.index("{")
            end = bot_message.rindex("}") + 1
            data = json.loads(bot_message[start:end])
            destinations = data.get("destinations")
        except (ValueError, KeyError):
            pass

        return JsonResponse({
            "message": bot_message,
            "destinations": destinations
        })

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

