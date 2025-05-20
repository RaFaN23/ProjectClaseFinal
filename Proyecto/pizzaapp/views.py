import uuid
from datetime import datetime, timezone
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect

from .forms import *
from .forms import PizzaForm, RegistroFormulario
from .models import cartao, LineaPedido, Pedido
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mesa
from django.shortcuts import render
from .models import Usuario
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .models import Mesa, EstadoMesa
from django.shortcuts import get_object_or_404, redirect



def solo_admin(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'admin')(view_func)

def solo_camarero_admin(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'camarero' or 'admin')(view_func)

def solo_camarero(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'camarero')(view_func)

def solo_cliente(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'cliente')(view_func)


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
    logout(request)
    return redirect('InicioSesion')


def go_carta(request):
    lista_carta = cartao.objects.all()
    return render(request, 'carta.html', {'carta': lista_carta})


def go_formulario_carta(request, id):
    plato = cartao.objects.filter(id=id)

    if len(plato) == 0:
        nuevo_plato = cartao()
    else:
        nuevo_plato = plato[0]

    if request.method == 'POST':

        nuevo_plato.nombre = request.POST['nombre']
        nuevo_plato.ingredientes = request.POST['ingredientes']
        nuevo_plato.precio = request.POST['precio']
        nuevo_plato.imagen = request.POST['imagen']

        nuevo_plato.save()
        return redirect('carta')

    else:
        return render(request, 'formularioCarta.html', {'plato': nuevo_plato})


def eliminar_carta(request, id):
    plato_eliminar = cartao.objects.filter(id=id)
    if len(plato_eliminar) != 0:
        plato_eliminar[0].delete()
        return redirect('carta')


def mostrar_mesas(request):
    mesas = Mesa.objects.all().order_by('numero')
    return render(request, 'Mesas.html', {'mesas': mesas})


@solo_camarero_admin
def asignar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)

    if mesa.estado == EstadoMesa.LIBRE:
        mesa.estado = EstadoMesa.OCUPADO
    elif mesa.estado == EstadoMesa.OCUPADO:
        mesa.estado = EstadoMesa.LIBRE

    mesa.save()
    return redirect('mostrar_mesas')



def add_carrito(request,id):
    carrito = request.session.get('carrito', {})
    producto_en_carrito = carrito.get(str(id),0)

    if producto_en_carrito == 0:

        carrito[str(id)] = 1

    else:
       carrito[str(id)] += 1

    request.session['carrito'] = carrito

    return redirect('carta')






def go_carrito(request):
    carrito = {}
    total = 0.0
    carrito_session = request.session.get('carrito', {})
    #recuperar productos
    for k, v in carrito_session.items():
        producto = cartao.objects.get(id=k)
        carrito[producto] = v
        total += producto.precio * v

    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})





def restar_carrito(request, id):
    carrito = request.session.get('carrito', {})
    producto_id = str(id)

    if producto_id in carrito:
        if carrito[producto_id] > 1:
            carrito[producto_id] -= 1
        else:
            del carrito[producto_id]

    request.session['carrito'] = carrito
    return redirect('ver_carrito')


def sumar_carrito(request, id):
    carrito = request.session.get('carrito', {})
    producto_id = str(id)

    carrito[producto_id] = carrito.get(producto_id, 0) + 1

    request.session['carrito'] = carrito
    return redirect('ver_carrito')


def quitar_de_carrito(request, id):
    carrito = request.session.get('carrito', {})
    producto_id = str(id)

    del carrito[producto_id]

    request.session['carrito'] = carrito
    return redirect('ver_carrito')


def comprar(request):
    nuevo_pedido = cartao()
    nuevo_pedido.codigo = 'CP0001'
    nuevo_pedido.fecha = datetime.now()
    nuevo_pedido.hermano = request.user

    carrito_session = request.session.get('carrito', {})

    for k, v in carrito_session.items():
        linea_pedido = LineaPedido()
        producto = cartao.objects.get(id=k)
        linea_pedido.producto = producto
        linea_pedido.precio = producto.precio
        linea_pedido.cantidad = v
        linea_pedido.pedido = nuevo_pedido
        linea_pedido.save()

    nuevo_pedido.save()


def limpiar(request):
    if 'carrito' in request.session:
        del request.session['carrito']
    request.session.modified = True
    return redirect('ver_carrito')
@solo_admin
@solo_admin
def lista_empleados(request):
    empleados = Usuario.objects.all()  # o filtra solo clientes: .filter(rol='cliente')
    return render(request, 'Gestion_empleados.html', {'empleados': empleados})


@solo_admin
def editar_empleado(request, pk):
    empleado = get_object_or_404(Usuario, pk=pk)
    form = EmpleadoForm(request.POST or None, instance=empleado)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('Usuarios')
    return render(request, 'editar_empleado.html', {'form': form})


@solo_admin
def borrar_empleado(request, pk):
    empleado = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('Usuarios')
    return render(request, 'confirmar_borrado.html', {'empleado': empleado})




def ver_pedidos_antiguos(request):
    return render(request,'pedidos_antiguos.html')







def crear_pedido(request):
    carrito = request.session.get('carrito', {})
    usuario = request.user

    if not carrito or not usuario.is_authenticated:
        return redirect('home')

    total = 0

    pedido = Pedido.objects.create(
        codigo=str(uuid.uuid4())[:8],
        fecha=timezone.now(),
        usuario=usuario,
        precio_total=0
    )

    for producto_id_str, cantidad in carrito.items():
        try:
            producto_id = int(producto_id_str)
            producto = cartao.objects.get(id=producto_id)
        except (ValueError, cartao.DoesNotExist):
            continue

        subtotal = cantidad * producto.precio
        total += subtotal

        LineaPedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio=producto.precio
        )


    pedido.precio_total = total
    pedido.save()


    if 'carrito' in request.session:
        del request.session['carrito']

    return redirect('home')



@solo_cliente
def pedidos_antiguos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'pedidos_antiguos.html', {'pedidos': pedidos})