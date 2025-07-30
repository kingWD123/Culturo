from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    
    # Authentification
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Cinema
    path('cinema-recommandations/', views.CinemaRecommandations, name='cinema_recommandations'),
    path('cinema_chatbot_api/', views.cinema_chatbot_api, name='cinema_chatbot_api'),
    path('api/get_movies_from_qloo/', views.get_movies_from_qloo, name='get_movies_from_qloo'),
    path('movie_detail/', views.movie_detail, name='movie_detail'),
]