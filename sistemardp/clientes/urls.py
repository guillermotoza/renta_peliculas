from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.cargar_clientes, name='cargar_clientes'),  # Cargar clientes en formato JSON
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/<int:id>/editar/', views.editar_cliente, name='editar_cliente'),
]
