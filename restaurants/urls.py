from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.restaurant_page, name='home_restaurant_page'),
    path('map', views.restaurant_recommandations, name='restaurant_recommandations'),
    path('api/chatbot/', views.restaurant_chatbot_api, name='restaurant_chatbot_api'),
    path('detail/<str:restaurant_name>/', views.restaurant_detail, name='restaurant_detail'),
]