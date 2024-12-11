from django.urls import path
from .views import agregar_pelicula, eliminar_pelicula, limpiar_carro, restar_pelicula


app_name = 'carro'  # nombre de la app para poder diferenciar al llamar el nombre de la url

urlpatterns = [
    path("agregar/<int:pelicula_id>/", agregar_pelicula.as_view(), name="agregar"),
    path("eliminar/<int:pelicula_id>/",eliminar_pelicula.as_view(), name="eliminar"),
    path("restar/<int:pelicula_id>/",restar_pelicula.as_view(), name="restar"),
    path("limpiar/",limpiar_carro.as_view(), name="vaciar"),
]