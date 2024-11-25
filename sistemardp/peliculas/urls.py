from django.urls import path
from peliculas import views


urlpatterns = [
    path('', views.busqueda_peliculas,name="busqueda_peliculas"),
    path('resultados_pelicula/',views.resultados,name="resultados_peliculas"),
]