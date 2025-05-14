from django.contrib import admin
from django.urls import path

from pizzaapp.views import *

#URL , METODO , NOMBRE
urlpatterns = [
    path('',go_home,name='home_vacio'),
    path('home/',go_home,name='home'),
    #LOGIN Y REGISTRO
    path('registro_tarjeta/',go_registro,name='registro'),
    path('Crear_Cuenta/',registrar_usuario,name='Crear_Cuenta'),
    path('InicioSesion/', login_usuario,name='InicioSesion'),

    path('InicioSesion/', logout_usuario, name='cerrarsesion'),

    path('hacer_pedido/',go_pedido,name='Hacer_Pedido'),
    #path('Crear_Cuenta/',go_crearCuenta,name='Crear_Cuenta'),
    path('carrito/',go_carrito, name='carrito'),
    path('contacto/',contacto_view, name='contacto'),
]