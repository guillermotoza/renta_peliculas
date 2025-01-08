from django.urls import path
from peliculas import views
from peliculas.views import TiendaView, PeliculasJsonView


urlpatterns = [
    path('', views.busqueda_peliculas,name="busqueda_peliculas"),
    path('resultados_busqueda/',views.resultados_peliculas,name="resultados_busqueda"),
    path('pelicula/<int:pelicula_id>/',views.pelicula_detalles, name="pelicula_detalles"),
    path('mostrar_peliculas/',views.pelicula_detalles,name="mostrar"),
    path('tienda/', TiendaView.as_view(), name='tienda'),
    path('p/', PeliculasJsonView.as_view(), name='peliculas_json'),
]