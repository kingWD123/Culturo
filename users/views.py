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

@csrf_exempt
def cinema_chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        history = data.get("history", [])

        system_prompt = (
            "Tu es un assistant qui aide l’utilisateur à obtenir des recommandations de films et séries via ClooAI. "
            "Pose une question à la fois pour recueillir : le genre préféré, la langue, la plateforme de streaming, l’âge, le pays. "
            "Quand tu as toutes les informations, affiche un résumé en JSON structuré comme ceci : "
            '{"genre": "...", "langue": "...", "plateforme": "...", "age": "...", "pays": "..."}. '
            "Ne propose le résumé JSON qu’à la toute fin."
        )

        messages = [{"role": "user", "parts": [system_prompt]}]
        for m in history:
            messages.append({"role": m["role"], "parts": [m["content"]]})

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(messages)
        bot_message = response.text

        user_data = None
        qloo_url = None
        try:
            start = bot_message.index("{")
            end = bot_message.rindex("}") + 1
            user_data = json.loads(bot_message[start:end])
            # Mapping simple : ici on suppose que user_data['entity_id'] existe, sinon à adapter
            entity_ids = user_data.get("entity_id") or []
            if isinstance(entity_ids, str):
                entity_ids = [entity_ids]
            extra_params = {}
            if 'langue' in user_data:
                extra_params['filter.language'] = user_data['langue']
            if 'pays' in user_data:
                extra_params['filter.country'] = user_data['pays']
            qloo_url = build_qloo_url(
                entity_type="urn:entity:movie",
                entity_ids=entity_ids,
                extra_params=extra_params
            )
            print("[Qloo URL]", qloo_url)
        except Exception:
            pass

        return JsonResponse({
            "message": bot_message,
            "user_data": user_data,
            "qloo_url": qloo_url,
            "done": user_data is not None
        })

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

# Fonction pour générer une URL Qloo/ClooAI GET

def build_qloo_url(
    entity_type="urn:entity:movie",
    entity_ids=None,
    extra_params=None
):
    base_url = "https://hackathon.api.qloo.com/v2/insights/"
    params = {
        "filter.type": entity_type
    }
    if entity_ids:
        if isinstance(entity_ids, list):
            params["signal.interests.entities"] = ",".join(entity_ids)
        else:
            params["signal.interests.entities"] = entity_ids
    if extra_params:
        params.update(extra_params)
    return base_url + "?" + urlencode(params)
