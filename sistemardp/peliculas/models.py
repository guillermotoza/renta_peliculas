from django.db import models
import os
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

def upload_to(instance, filename):
    return os.path.join('peliculas', datetime.now().strftime('%Y/%m/%d'), filename)

# Create your models here.
class CategoriaPel(models.Model):
    nombreCatPel = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria de Pelicula"
        verbose_name_plural = "Categorias de Peliculas"
    
    def __str__(self):
        return self.nombreCatPel


class pelicula(models.Model):
    titulo = models.CharField(max_length=25, help_text="nombre de la pelicula")
    imagen = models.ImageField(upload_to=upload_to, null=True, blank=True, help_text='Imagen del producto frontal')
    precio = models.DecimalField(max_digits=5, decimal_places=2, help_text='Precio de la pelicula')
    descuento = models.IntegerField(default=0, help_text='Descuento en porcentaje')
    publicacion = models.DateField(help_text="año en que se publico la pelicula")
    calificacion = models.IntegerField(help_text="calificacion de la pelicula")
    categorias = models.ForeignKey(CategoriaPel, on_delete=models.CASCADE, null=False,blank=False, help_text="categorias de la pelicula")
    stock = models.PositiveIntegerField(help_text="cantidad disponible en stock")
    descripcion = models.TextField(max_length=200, help_text="descripcion de la pelicula")
    director = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def precio_final(self):
        # Calcula el precio final aplicando el descuento solo si existe un descuento
        if self.descuento > 0:
            return self.precio - (self.precio * self.descuento / 100)
        return self.precio #no remplazar el precio sin descuento

    class Meta:
        verbose_name = "Pelicula"
        verbose_name_plural = "Peliculas"

    def __str__(self):
        return self.titulo
    
