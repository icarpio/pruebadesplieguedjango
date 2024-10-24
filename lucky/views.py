from django.http import HttpResponseServerError
from django.shortcuts import render
import random

def index_lucky(request):
    try:
        return render(request, 'lucky/index_lucky.html')
    except Exception as e:
        return HttpResponseServerError(f"Error: {e}")

# Definimos las opciones de serie una sola vez
serie_options = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5
}


def form_view(request):
    return render(request, 'lucky/form.html', {'options': serie_options})

def generate_numbers(request):
    selection = request.GET.get('selection') # form.html -> <select name="selection" id="selection">

    if selection in serie_options:
        series = []
        try:
            for _ in range(serie_options[selection]):
                serie = sorted(random.sample(range(1, 51), 6))  # Asegúrate de incluir el 50
                series.append(serie)
            return render(request, 'lucky/result.html', {'series': series})
        except Exception as e:
            return HttpResponseServerError(f"Error: {e}")
    else:
        return HttpResponseServerError("Selección no válida.")
    
def form_view_stars(request):
    return render(request, 'lucky/form_stars.html', {'options': serie_options})

def generate_numbers_and_stars(request):
    selection = request.GET.get('selection') # form_stars.html -> <select name="selection" id="selection">

    if selection in serie_options:
        series = []
        try:
            for _ in range(serie_options[selection]):
                numbers = sorted(random.sample(range(1, 51), 5))  # 5 números del 1 al 50
                stars = sorted(random.sample(range(1, 13), 2))  # 2 estrellas del 1 al 11
                series.append({'numbers': numbers, 'stars': stars})
            return render(request, 'lucky/result_stars.html', {'series': series})
        except Exception as e:
            return HttpResponseServerError(f"Error: {e}")
    else:
        return HttpResponseServerError("Selección no válida.")