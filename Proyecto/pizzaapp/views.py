from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .forms import PizzaForm
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


def go_carrito(request):
    return render(request, 'carrito.html')

def go_contacto(request):
    return render(request, 'contacto.html')
def contacto_view(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda en la base de datos si es ModelForm
            return redirect('gracias')
    else:
        form = PizzaForm()

    return render(request, 'contacto.html', {'form': form})