from django.contrib import admin
from django.urls import path
from django.urls import path
from . import views

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

    path('contacto/',contacto_view, name='contacto'),
    path('contacto/',go_contacto, name='contacto'),


    #Esto es para la carta
    path('carta/',go_carta, name='carta'),
    path('formulario_carta/nuevo/<int:id>',go_formulario_carta, name='formulario_carta'),
    path('formulario_carta/borrar/<int:id>',eliminar_carta, name='eliminar_carta'),
    path('mesas/', views.mostrar_mesas, name='mostrar_mesas'),
    path('asignar/<int:mesa_id>/', views.asignar_mesa, name='asignar_mesa'),

    #Carrito
    path('carrito/add/<int:id>',add_carrito, name='add_carrito'),
    path('ver_carrito/',go_carrito, name='ver_carrito'),
    path('carrito/sumar/<int:id>/', sumar_carrito, name='sumar_carrito'),
    path('carrito/restar/<int:id>/', restar_carrito, name='restar_carrito'),
    path('completar_compra/', comprar, name='comprar'),
    path('carrito/quitar/<int:id>/', quitar_de_carrito, name='quitar_de_carrito'),
]