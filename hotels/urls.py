from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.hotel_page, name='hotel_home_page'),

]