from django.shortcuts import render
import requests
from django.http import JsonResponse

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
                if location.get('addresstype') in ['city', 'town', 'suburb']:
                    latitude = location['lat']
                    longitude = location['lon']
                    return latitude, longitude

        return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None, None
    
def get_weather_data(request):
    city_name = request.GET.get('city')
    lat, lon = get_city_or_town_coordinates(city_name)

    if lat is not None and lon is not None:
        try:
            weather_response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&timezone=Europe/Madrid&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m')
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            print(weather_data)

            return render(request, 'weather/weather_form.html', {
                'weather_data': {
                    'city': city_name,
                    'coordinates': {'latitude': lat, 'longitude': lon},
                    'weather': weather_data
                }
            })
        
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos del clima: {e}")
            return JsonResponse({'error': 'No se pudo obtener datos del clima'}, status=500)
    else:
        return JsonResponse({'error': 'Ciudad o pueblo no encontrado'}, status=404)

