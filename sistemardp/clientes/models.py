from django.db import models

class Cliente(models.Model):
    
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    direccion = models.TextField()
    detalles_membresia = models.CharField(max_length=100)

   
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
