from django.urls import path
from peliculas import views


urlpatterns = [
    path('', views.busqueda_peliculas,name="busqueda_peliculas"),
    path('resultados_pelicula/',views.resultados_peliculas,name="resultados_peliculas"),
    path('pelicula/<int:pelicula_id>/',views.pelicula_detalles, name="pelicula_id"),
    path('mostrar_peliculas/',views.pelicula_detalles,name="mostrar"),
]