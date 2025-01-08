from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby, name='lobby'),  # Vista principal de la aplicación de lobby
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('peliculas/', views.listar_peliculas, name='listar_peliculas'),
    path('peliculas/agregar/', views.agregar_pelicula, name='agregar_pelicula'),
    path('peliculas/eliminar/<int:pelicula_id>/', views.eliminar_pelicula, name='eliminar_pelicula'),
    path('peliculas/<int:pelicula_id>/editar/', views.editar_pelicula, name='editar_pelicula'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('contactanos/',views.contactar,name="contactanos"),
    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
]