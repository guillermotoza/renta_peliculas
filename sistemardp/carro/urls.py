from django.urls import path
"from .views import agregar_pelicula, eliminar_pelicula, limpiar_carro, restar_pelicula"
from carro.views import (
    AgregarPeliculaView,
    EliminarPeliculaView,
    RestarPeliculaView,
    LimpiarCarroView,
)


app_name = 'carro'  # nombre de la app para poder diferenciar al llamar el nombre de la url

urlpatterns = [
    # Rutas para las acciones del carrito
    path('agregar/<int:pelicula_id>/', AgregarPeliculaView.as_view(), name="carro_agregar"),
    path('eliminar/<int:pelicula_id>/', EliminarPeliculaView.as_view(), name="carro_eliminar"),
    path('restar/<int:pelicula_id>/', RestarPeliculaView.as_view(), name="carro_restar"),
    path('limpiar/', LimpiarCarroView.as_view(), name="carro_limpiar"),
]

"""
urlpatterns = [
    path("agregar/<int:pelicula_id>/", agregar_pelicula.as_view(), name="agregar"),
    path("eliminar/<int:pelicula_id>/",eliminar_pelicula.as_view(), name="eliminar"),
    path("restar/<int:pelicula_id>/",restar_pelicula.as_view(), name="restar"),
    path("limpiar/",limpiar_carro.as_view(), name="vaciar"),
]
    """