from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .forms import PizzaForm, RegistroFormulario
from .models import cartao


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

def registrar_usuario(request):
    if request.method == 'POST':
        form =RegistroFormulario(request.POST)
        if form.is_valid():
            form.save()  # Guarda en la base de datos si es ModelForm
            return redirect('gracias')
    else:
        form = RegistroFormulario()
    return render(request,"Crear_Cuenta.html",{'form': form})





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