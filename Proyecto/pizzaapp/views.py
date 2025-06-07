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
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from .models import Mesa, EstadoMesa
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import redirect, render
from .models import Pedido, LineaPedido
import random
import string


def solo_admin(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'admin')(view_func)


def solo_camarero_admin(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol in ('camarero', 'admin'))(view_func)


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



# views.py
def add_carrito(request, id):
    carrito = request.session.get('carrito', {})

    if str(id) in carrito:
        carrito[str(id)] += 1  # sumar cantidad
    else:
        carrito[str(id)] = 1   # agregar producto con cantidad 1

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


def restar_editar(request, id):
    linea_pedido = get_object_or_404(LineaPedido, id=id)
    pedido_id = linea_pedido.pedido.id

    if linea_pedido.cantidad > 1:
        linea_pedido.cantidad -= 1
        linea_pedido.save()
    else:
        linea_pedido.delete()

    return redirect('editar_pedido', pk=pedido_id)


def sumar_carrito(request, id):
   carrito = request.session.get('carrito', {})
   producto_id = str(id)


   carrito[producto_id] = carrito.get(producto_id, 0) + 1


   request.session['carrito'] = carrito
   return redirect('ver_carrito')


def sumar_editar(request, id):
    linea_pedido = get_object_or_404(LineaPedido, id=id)
    pedido_id = linea_pedido.pedido.id

    linea_pedido.cantidad += 1
    linea_pedido.save()

    return redirect('editar_pedido', pk=pedido_id)


def quitar_de_carrito(request, id):
   carrito = request.session.get('carrito', {})
   producto_id = str(id)


   del carrito[producto_id]


   request.session['carrito'] = carrito
   return redirect('ver_carrito')


def quitar_editar(request, id):
    linea_pedido = get_object_or_404(LineaPedido, id=id)
    pedido_id = linea_pedido.pedido.id

    linea_pedido.delete()

    return redirect('editar_pedido', pk=pedido_id)


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
    empleados = Usuario.objects.all()
    return render(request, 'Gestion_empleados.html', {'empleados': empleados})


@solo_admin
def editar_empleado(request, pk):
    empleado = get_object_or_404(Usuario, pk=pk)
    form = EmpleadoForm(request.POST or None, instance=empleado)

    if request.method == 'POST' and form.is_valid():
        empleado = form.save(commit=False)
        nueva_contraseña = form.cleaned_data.get('password')
        if nueva_contraseña:
            empleado.set_password(nueva_contraseña)
        empleado.save()
        return redirect('Usuarios')

    return render(request, 'editar_empleado.html', {'form': form})


@solo_admin
def borrar_empleado(request, pk):
    empleado = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('Usuarios')
    return render(request, 'confirmar_borrado.html', {'empleado': empleado})


def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'Gestion_pedidos.html', {'pedidos': pedidos})


def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    lineas = LineaPedido.objects.filter(pedido=pedido).select_related('producto')

    total = 0
    for linea in lineas:
        linea.subtotal = linea.cantidad * linea.precio
        total += linea.subtotal

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')
    else:
        form = PedidoForm(instance=pedido)

    context = {
        'pedido': pedido,
        'form': form,
        'lineas': lineas,
        'total': total,
    }
    return render(request, 'editar_pedido.html', context)


def borrar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('lista_pedidos')
    return render(request, 'confirmar_borrado_pedido.html', {'pedido': pedido})


def ver_pedidos_antiguos(request):
    return render(request, 'pedidos_antiguos.html')


def crear_pedido(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('ver_carrito')

    total = 0
    pedido = Pedido.objects.create(
        codigo=''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
        fecha=timezone.now(),
        usuario=request.user,
        precio_total=0  # lo actualizamos luego
    )

    for producto_id, cantidad in carrito.items():
        producto = cartao.objects.get(id=int(producto_id))
        LineaPedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio=producto.precio
        )
        total += producto.precio * cantidad

    pedido.precio_total = total
    pedido.save()

    del request.session['carrito']
    return redirect('pedidos_antiguos')



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





def crear_o_editar_resena(request, resena_id=None):
    if resena_id:
        resena_obj = get_object_or_404(resena, id=resena_id, usuario=request.user)
    else:
        resena_obj = None

    if request.method == 'POST':
        form = form_resena(request.POST, instance=resena_obj)
        if form.is_valid():
            nueva_resena = form.save(commit=False)
            nueva_resena.usuario = request.user
            nueva_resena.save()
            return redirect('lista_resenas')  # <- Redirige a la vista que renderiza resena.html
    else:
        form = form_resena(instance=resena_obj)

    contexto = {
        'form': form,
        'es_edicion': resena_obj is not None
    }
    return render(request, 'formulario_resena.html', contexto)

def eliminar_resena(request, resena_id):
    resena_eliminar = resena.objects.filter(id=resena_id, usuario=request.user)
    if len(resena_eliminar) != 0:
        resena_eliminar[0].delete()
    return redirect('lista_resenas')

def go_resena(request):
    resenas = resena.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'resena.html', {'resenas': resenas})