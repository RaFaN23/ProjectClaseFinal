from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.db import models

# LOGIN Y REGISTRO
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, rol, password=None):
        if not email:
            raise ValueError('El usuario debe tener un email')

        email = self.normalize_email(email)
        usuario = self.model(email=email, nombre=nombre, rol=rol)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nombre, rol='admin', password=None):
        usuario = self.create_user(email, nombre, rol, password)
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)
        return usuario


class Usuario(AbstractUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Administrador'),
        ('cocinero', 'Cocinero'),
        ('camarero', 'Camarero'),
        ('cliente', 'Cliente')
    )

    email = models.EmailField(max_length=250, unique=True)
    nombre = models.CharField(max_length=250)
    apellidos = models.CharField(max_length=250)
    rol = models.CharField(max_length=25, choices=ROLES, default='cliente')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'rol']

    def __str__(self):
        return self.email + " - " + self.nombre + " - " + self.rol


# Contactos
class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


# Mesas
class EstadoMesa(models.TextChoices):
    OCUPADO = 'OCUPADO', 'Ocupado'
    LIBRE = 'LIBRE', 'Libre'
    RESERVADO = 'RESERVADO', 'Reservado'

class Mesa(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    estado = models.CharField(
        max_length=10,
        choices=EstadoMesa.choices,
        default=EstadoMesa.LIBRE
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mesa {self.numero} - {self.estado}"


# Carta
class cartao(models.Model):
    nombre = models.CharField(max_length=210, null=False)
    ingredientes = models.TextField(max_length=250)
    precio = models.IntegerField(null=False)
    imagen = models.CharField(max_length=400, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


# Pedidos
class Pedido(models.Model):
    codigo = models.CharField(max_length=50)
    fecha = models.DateTimeField()
    usuario = models.ForeignKey('Usuario', on_delete=models.DO_NOTHING, related_name='pedidos')
    precio_total = models.FloatField(default=0)
    mesa = models.ForeignKey('Mesa', on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.codigo


class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(cartao, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField()
    precio = models.FloatField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.precio}"
