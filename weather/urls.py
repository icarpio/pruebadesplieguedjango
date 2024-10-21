from django.urls import path
from .views import weather_form, get_weather_data

urlpatterns = [
    path('', weather_form, name='weather_form'),
    path('get_weather/', get_weather_data, name='get_weather'),
]