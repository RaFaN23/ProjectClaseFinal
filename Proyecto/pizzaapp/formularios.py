from django.db import models



class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    mensaje = models.CharField()
    def __str__(self):
        return self.nombre
