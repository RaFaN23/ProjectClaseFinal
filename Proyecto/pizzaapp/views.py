from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .forms import *
from .forms import PizzaForm, RegistroFormulario
from .models import cartao


# Create your views here.


from django.shortcuts import render
from django.http import HttpResponse

def go_home(request):
    response = render(request, 'home.html')
    response['Cache-Control'] = 'no-store'
    return response



def go_crearCuenta(request):
    return render(request, 'Crear_Cuenta.html')


def go_registro(request):
    return render(request, 'registro_tarjeta.html')


def go_pedido(request):
    return render(request, 'hacer_pedido.html')


def go_crearCuenta(request):
    return render(request, 'Crear_Cuenta.html')


def go_iniciarSesion(request):
    form = LoginFormulario()
    return render(request, 'InicioSesion.html', {'form': form})


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


def registrar_usuario(request):
    form = RegistroFormulario()
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            usuario_nuevo = form.save(commit=False)  # Guarda en la base de datos si es ModelForm
            usuario_nuevo.set_password(form.cleaned_data['password'])
            usuario_nuevo.save()
            return redirect('InicioSesion')
    else:
        form = RegistroFormulario()
    return render(request, "Crear_Cuenta.html", {'form': form})


def login_usuario(request):
    if request.method == 'POST':
        form = LoginFormulario(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            usuario = authenticate(request, email=email, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('home')
    else:
        form = LoginFormulario()

    return render(request, 'InicioSesion.html', {'form': form})


def logout_usuario(request):
    logout_usuario()
    return redirect('InicioSesion')



def go_carta(request):
    lista_carta = cartao.objects.all()
    return render(request, 'carta.html', {'carta': lista_carta})

def go_formulario_carta(request,id):

    plato = cartao.objects.filter(id=id)

    if len(plato) == 0:
        nuevo_plato = cartao()
    else:
        nuevo_plato=plato[0]

    if request.method == 'POST':

        nuevo_plato.nombre = request.POST['nombre']
        nuevo_plato.ingredientes = request.POST['ingredientes']
        nuevo_plato.precio = request.POST['precio']
        nuevo_plato.imagen = request.POST['imagen']

        nuevo_plato.save()
        return redirect('carta')

    else:
        return render(request, 'formularioCarta.html',{'plato': nuevo_plato})



def eliminar_carta(request,id):
    plato_eliminar = cartao.objects.filter(id=id)
    if len(plato_eliminar) != 0:
        plato_eliminar[0].delete()
        return redirect('carta')
