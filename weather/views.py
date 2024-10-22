from django.shortcuts import render
import requests
from django.http import JsonResponse
from datetime import datetime

def weather_form(request):
    return render(request, 'weather/weather_form.html')


import requests

def get_city_or_town_coordinates(city_name, country='España'):
    try:
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': f'{city_name}, {country}',
            'format': 'json'
        }
        headers = {
            'User-Agent': 'djangoDeploy/1.0 (icarpiodeveloper@gmail.com)'  # Cambia esto por tu información
        }

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        if data:
            for location in data:
                if location.get('addresstype') in ['city', 'town', 'suburb','village','quarter']:
                    latitude = location['lat']
                    longitude = location['lon']
                    display_name = location['display_name']
                    return latitude, longitude,display_name

        return None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None, None
    
def get_weather_data(request):
    city_name = request.GET.get('city')
    lat, lon, dis= get_city_or_town_coordinates(city_name)

    if lat is not None and lon is not None and dis is not None:
        try:
            weather_response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&timezone=Europe/Madrid&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation_probability')
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            
             # Generar lista de datos meteorológicos para mostrar en la tabla
            weather_list = [
                {
                    'time': datetime.fromisoformat(time).strftime('%d-%m-%H:%M'),
                    'temp': temp,
                    'humidity': humidity,
                    'wind': wind,
                    'rain':rain
                }
                for time, temp, humidity, wind, rain in zip(
                    weather_data['hourly']['time'], 
                    weather_data['hourly']['temperature_2m'],
                    weather_data['hourly']['relative_humidity_2m'],
                    weather_data['hourly']['wind_speed_10m'],
                    weather_data['hourly']['precipitation_probability']
                )
            ]
        

            return render(request, 'weather/weather_form.html', {
                'weather_data': {
                    'city': city_name,
                    'coordinates': {'latitude': lat, 'longitude': lon},
                    'weather': weather_data,
                    'weather_list': weather_list             
                }
            })
        
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos del clima: {e}")
            return JsonResponse({'error': 'No se pudo obtener datos del clima'}, status=500)
    else:
        return JsonResponse({'error': 'Ciudad o pueblo no encontrado'}, status=404)

