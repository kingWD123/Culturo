from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('cinema-recommandations/', views.CinemaRecommandations, name='cinema_recommandations'),
    path('cinema_chatbot_api/', views.cinema_chatbot_api, name='cinema_chatbot_api'),
] 