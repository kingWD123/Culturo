from django.urls import path
from . import views

app_name = 'destination'

urlpatterns = [
    path('', views.destination_recommandations, name='destination_recommandations'),
    path('api/', views.destination_chatbot_api, name='destination_chatbot_api'),
    path('detail/<str:name>/', views.destination_detail, name='destination_detail'),
] 