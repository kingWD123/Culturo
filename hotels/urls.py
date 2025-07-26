from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.hotel_page, name='hotel_home_page'),
    path('map/', views.hotel_map, name='hotel_map'),
    path('api/chatbot/', views.hotel_chatbot_api, name='hotel_chatbot_api'),
]