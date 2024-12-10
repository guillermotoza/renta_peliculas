from tabnanny import verbose
from django.db import models

from django.contrib.auth import get_user_model

from peliculas.models import pelicula, CategoriaPel

from django.db.models import F, Sum, FloatField

# Create your models here.

User=get_user_model()

class Pedido(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    @property
    def total(self):
        return self.lineapedido_set.aggregate(
            total=Sum(F("precio")*F("dias"), output_field=FloatField())
            )["total"]

    class Meta:
        db_table='pedidos'
        verbose_name='pedido'
        verbose_name_plural='pedidos'
        ordering=['id']

class LineaPedido(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    pelicula=models.ForeignKey(pelicula, on_delete=models.CASCADE)
    pedido=models.ForeignKey(Pedido, on_delete=models.CASCADE)
    dias=models.IntegerField(default=1)
    create_at=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.dias} dias rentados para {self.pelicula.titulo}'

    class Meta:
        db_table='lineapedidos'
        verbose_name='lineapedido'
        verbose_name_plural='lineaspedidos'
        ordering=['id']