from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    correo = models.EmailField()
    direccion = models.CharField(max_length=255)
    detalles_membresia = models.CharField(max_length=100) 
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

