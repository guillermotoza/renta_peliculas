from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    direccion = models.TextField()
    detalles_membresia = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)
    historial_rentas = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
