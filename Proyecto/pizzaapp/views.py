import uuid
from datetime import datetime, timezone
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect

from .forms import *
from .forms import PizzaForm, RegistroFormulario
from .models import cartao, LineaPedido, Pedido, EstadoPedido, EstadoPedidoCamarero
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
from .models import Pedido, LineaPedido
import random
import string
from django.db.models import Sum




def solo_admin(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'admin')(view_func)

def solo_camarero_admin(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'camarero' and 'admin')(view_func)

def solo_camarero(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'camarero')(view_func)

def solo_cliente(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'cliente')(view_func)

def solo_camarero_cocinero(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'camarero' or 'cocinero')(view_func)

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


def go_carta(request, mesa_id):
    lista_carta = cartao.objects.all()
    request.session['mesa_id'] = int(mesa_id)
    return render(request, 'carta.html', {'carta': lista_carta, 'mesa_id': mesa_id})


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

@solo_camarero_admin
def historial_mesa(request, mesa_id):
    pedidos = Pedido.objects.filter(mesa_id=mesa_id).order_by('-fecha')
    return render(request, 'historial_mesa.html', {'pedidos': pedidos, 'mesa_id': mesa_id})


def historial_pedidos(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)

    # Obtener todos los pedidos relacionados con esta mesa
    pedidos = Pedido.objects.filter(mesa_id=mesa.id).order_by('-id')

    # Para cada pedido, obtener sus líneas de pedido
    historial = []
    for pedido in pedidos:
        lineas = LineaPedido.objects.filter(pedido=pedido)
        historial.append({
            'pedido': pedido,
            'lineas': lineas,
            'total': lineas.aggregate(total=Sum('producto__precio'))['total']
        })

    context = {
        'mesa': mesa,
        'historial': historial
    }

    return render(request, 'pizzaapp/historial_pedidos.html', context)



def add_carrito(request, producto_id):
    mesa_id = request.session.get('mesa_id')
    if not mesa_id:
        return redirect('mesas')

    producto = cartao.objects.get(id=producto_id)
    carrito = request.session.get('carrito', {})

    mesa_key = f"mesa_{mesa_id}"
    if mesa_key not in carrito:
        carrito[mesa_key] = {}

    if str(producto_id) in carrito[mesa_key]:
        carrito[mesa_key][str(producto_id)]['cantidad'] += 1
    else:
        carrito[mesa_key][str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': 1
        }

    request.session['carrito'] = carrito
    return redirect('carta', mesa_id=mesa_id)



def ver_carrito(request):
    mesa_id = request.session.get('mesa_id')
    if not mesa_id:
        return redirect('mesas')

    carrito = request.session.get('carrito', {}).get(f"mesa_{mesa_id}", {})
    return render(request, 'carrito.html', {'carrito': carrito, 'mesa_id': mesa_id})

def carrito_general(request):
    productos = cartao.objects.all()
    context = {
        'productos': productos,
        'carrito_tipo': 'general'
    }
    return render(request, 'pizzaapp/carrito_general.html', context)

def carrito_por_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)

    productos = cartao.objects.all()
    context = {
        'productos': productos,
        'mesa': mesa,
        'carrito_tipo': 'mesa'
    }
    return render(request, 'pizzaapp/carrito_por_mesa.html', context)


def go_carrito(request):
    carrito = {}
    total = 0.0

    carrito_session = request.session.get('carrito', {})

    for k, v in carrito_session.items():
        try:
            producto = cartao.objects.get(id=int(k))
            carrito[producto] = v
            total += producto.precio * v
        except cartao.DoesNotExist:
            continue

    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': total,

    })






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


def crear_pedido(request, mesa_id):
    mesa_key = f"mesa_{mesa_id}"
    carrito_general = request.session.get('carrito', {})
    carrito_session = carrito_general.get(mesa_key, {})

    if not carrito_session:
        return redirect('mostrar_mesas')  # o alguna página de error/mensaje

    total = 0
    pedido = Pedido.objects.create(
        usuario=request.user,  # Si estás usando autenticación
        codigo=str(uuid.uuid4())[:8],
        precio_total=0,  # Se actualizará después
        mesa=Mesa.objects.get(id=mesa_id),
        fecha=timezone.now()
    )

    for k, v in carrito_session.items():
        producto = cartao.objects.get(id=k)
        cantidad = v['cantidad']
        subtotal = producto.precio * cantidad

        LineaPedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio=subtotal
        )

        total += subtotal

    # Actualizamos el total del pedido
    pedido.precio_total = total
    pedido.save()

    # Cambiar estado de la mesa
    pedido.mesa.estado = 'OCUPADO'
    pedido.mesa.save()

    # Limpiar carrito de la sesión para esa mesa
    del carrito_general[mesa_key]
    request.session['carrito'] = carrito_general
    request.session.modified = True

    return redirect('ver_mesas')


@solo_cliente
def pedidos_antiguos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'pedidos_antiguos.html', {'pedidos': pedidos})



@solo_admin
def pedidos_todos(request):
    pedidos = Pedido.objects.all().order_by('-fecha')
    return render(request, 'pedidos_todos.html', {'pedidos': pedidos})


@solo_camarero_cocinero
def pedidos_todos(request):
    pedidos = Pedido.objects.all().order_by('-fecha')
    return render(request, 'pedidos_todos.html', {'pedidos': pedidos})



def cambiar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if pedido.estado == EstadoPedido.PREPARANDO:
        pedido.estado = EstadoPedido.TERMINADO
    else:
        pedido.estado = EstadoPedido.PREPARANDO
    pedido.save()
    return redirect('pedidos_todos')

def cambiar_estado_pedido_camarero(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if pedido.estado_camarero == EstadoPedidoCamarero.EN_PROCESO:
        pedido.estado_camarero = EstadoPedidoCamarero.FINALIZADO
    else:
        pedido.estado_camarero = EstadoPedidoCamarero.FINALIZADO
    pedido.save()
    return redirect('pedidos_todos')    