
from django.urls import path
from .views import generate_numbers, index_lucky,form_view,generate_numbers_and_stars,form_view_stars

urlpatterns = [
    path('', index_lucky, name='index_lucky'), 
    path('form/', form_view, name='form_view'),
    path('generate/', generate_numbers, name='generate_numbers'),
    path('form_view_stars/', form_view_stars, name='form_view_stars'),
    path('generate_numbers_and_stars/', generate_numbers_and_stars, name='generate_numbers_and_stars'),
    #path('generate_num_stars/', generate_num_stars, name='generate_num_stars')
    #path('nombre de la ruta/', nombre_de_la_funcion_del_views, name='nombre por el se accede a través de 'url')
]