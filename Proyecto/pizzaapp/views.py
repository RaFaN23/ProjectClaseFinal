from django.shortcuts import render

# Create your views here.


def go_home(request):
    return render(request, 'home.html')
    
def go_registro(request):
    return render(request, 'registro_tarjeta.html')

def go_pedido(request):
    return render(request, 'hacer_pedido.html')
def go_crearCuenta(request):
    return render(request, 'Crear_Cuenta.html')

def go_iniciarSesion(request):
    return render(request, 'InicioSesion.html')
