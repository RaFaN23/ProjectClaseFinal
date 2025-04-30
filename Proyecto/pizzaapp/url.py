from django.contrib import admin
from django.urls import path

from pizzaapp.views import *

#URL , METODO , NOMBRE
urlpatterns = [
    path('',go_home,name='home_vacio'),
    path('home/',go_home,name='home'),
    path('registro_tarjerta/',go_registro,name='registro'),
    #path('Crear_Cuenta/',go_crearCuenta,name='Crear_Cuenta'),
    path('carrito/',go_carrito, name='carrito'),
]