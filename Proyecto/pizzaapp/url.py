from django.contrib import admin
from django.urls import path
from . import views
from pizzaapp.views import *

urlpatterns = [


    # HOME
    path('', go_home, name='home_vacio'),
    path('home/', go_home, name='home'),


    # LOGIN Y REGISTRO
    path('registro_tarjeta/', go_registro, name='registro'),
    path('Crear_Cuenta/', registrar_usuario, name='Crear_Cuenta'),
    path('InicioSesion/', login_usuario, name='InicioSesion'),
    path('cerrarSesion/', logout_usuario, name='cerrarSesion'),

    # GESTIÓN DE EMPLEADOS
    path('Gestion_Users/', lista_empleados, name='Usuarios'),
    path('empleado/editar/<int:pk>/', editar_empleado, name='editar_empleado'),
    path('empleado/borrar/<int:pk>/', borrar_empleado, name='borrar_empleado'),

    # PEDIDOS
    path('hacer_pedido/', go_pedido, name='Hacer_Pedido'),

    # CONTACTO
    path('contacto/', contacto_view, name='contacto'),

    # CARTA
    path('carta/', go_carta, name='carta'),
    path('formulario_carta/nuevo/<int:id>', go_formulario_carta, name='formulario_carta'),
    path('formulario_carta/borrar/<int:id>', eliminar_carta, name='eliminar_carta'),

    # MESAS
    path('mesas/', mostrar_mesas, name='mostrar_mesas'),
    path('asignar/<int:mesa_id>/', asignar_mesa, name='asignar_mesa'),
    path('carta/<int:mesa_id>/', go_carta, name='carta'),
    path('historial_mesa/<int:mesa_id>/', historial_mesa, name='historial_mesa'),


    # CARRITO
    path('carrito/', go_carrito, name='carrito'),
    # urls.py
    path('carrito/<int:mesa_id>/', go_carrito, name='ver_carrito'),
    path('add_carrito/<int:producto_id>/', add_carrito, name='add_carrito'),
    path('carrito/sumar/<int:id>/', sumar_carrito, name='sumar_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('crear_pedido/<int:mesa_id>/', crear_pedido, name='crear_pedido'),
    path('carrito/restar/<int:id>/', restar_carrito, name='restar_carrito'),
    path('carrito/quitar/<int:id>/', quitar_de_carrito, name='quitar_de_carrito'),
    path('carrito/limpiar/', limpiar, name='limpiar'),
    path('completar_compra/', comprar, name='comprar'),

    #pedidos antiguos

    path('peidos_antiguos/', pedidos_antiguos, name='pedidos_antiguos'),

    path('crear_pedido/', crear_pedido, name='crear_pedido'),

    path('pedidos_todos/', pedidos_todos, name='pedidos_todos'),

    path('pedido/<int:pedido_id>/cambiar_estadoCocinero/', cambiar_estado_pedido, name='cambiar_estado_pedido'),

    path('pedido/<int:pedido_id>/cambiar_estadoCamarero/', cambiar_estado_pedido_camarero, name='cambiar_estado_pedido_camarero'),

]
