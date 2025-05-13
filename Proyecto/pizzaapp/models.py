from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.db import models
# Create your models here.














































#LOGIN Y REGISTRO
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, rol, password=None):
        if not email:
            raise ValueError('El usuario debe tener un email')

        email = self.normalize_email(email)
        usuario = self.model(email=email, nombre=nombre,rol=rol)
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


    email = models.EmailField(max_length=500, unique=True)
    nombre = models.CharField(max_length=250)
    apellidos = models.CharField(max_length=250)
    rol = models.CharField(max_length=25, choices=ROLES, default='cliente')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['nombre', 'rol']

    def __str__(self):
        return self.email + "-" + self.nombre + "-" + self.rol

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
