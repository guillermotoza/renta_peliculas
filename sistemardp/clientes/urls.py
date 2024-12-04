from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.cargar_clientes, name='cargar_clientes'),  
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
]


