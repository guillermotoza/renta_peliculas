from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/<int:cliente_id>/baja/', views.eliminar_cliente, name='eliminar_cliente'),
]
