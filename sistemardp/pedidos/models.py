from tabnanny import verbose
from django.db import models
from django.contrib.auth import get_user_model
from peliculas.models import Pelicula, CategoriaPel
from django.db.models import F, Sum, FloatField

User = get_user_model()

class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    # Campos para almacenar los totales y descuentos
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total antes del descuento
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total del descuento
    total_con_descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total con descuento

    def __str__(self):
        return f"Pedido #{self.id}"

    @property
    def calcular_total(self):
        # Calcula el total en base a las l�neas de pedido
        return self.lineapedido_set.aggregate(
            total=Sum(F("pelicula__precio") * F("dias"), output_field=FloatField())
        )["total"] or 0

    class Meta:
        db_table = 'pedidos'
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['id']

class LineaPedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="lineapedido_set")
    dias = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.dias} dias rentados para {self.pelicula.titulo}'

    class Meta:
        db_table = 'lineapedidos'
        verbose_name = 'lineapedido'
        verbose_name_plural = 'lineaspedidos'
        ordering = ['id']
