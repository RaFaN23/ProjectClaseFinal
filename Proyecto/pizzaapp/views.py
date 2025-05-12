from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import FormularioContacto
# Create your views here.


def go_home(request):
    return render(request, 'home.html')

def go_crearCuenta(request):
    return render(request, 'Crear_Cuenta.html')
def go_registro(request):
    return render(request, 'registro_tarjeta.html')

def go_pedido(request):
    return render(request, 'hacer_pedido.html')
def go_crearCuenta(request):
    return render(request, 'Crear_Cuenta.html')

def go_iniciarSesion(request):
    return render(request, 'InicioSesion.html')

def contacto_view(request):
    if request.method == 'POST':
        form = form
def go_carrito(request):
    return render(request, 'carrito.html')
