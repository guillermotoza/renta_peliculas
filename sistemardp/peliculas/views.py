from django.shortcuts import render, redirect
from django.http import JsonResponse 
from peliculas.models import Pelicula
from django.contrib import messages
from datetime import datetime
from carro.carro import Carro


def busqueda_peliculas(request):
    carro = Carro(request)
    return render(request, "busqueda_peliculas.html")


def resultados_peliculas(request):
    carro = Carro(request)
    if request.GET.get("pelicula"):
        pelicula_nombre = request.GET.get("pelicula")
        fecha_inicio_str = request.GET.get("fecha_inicio")
        fecha_devolver_str = request.GET.get("fecha_devolver")

        # Convertir las fechas si existen
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None
        fecha_devolver = datetime.strptime(fecha_devolver_str, '%Y-%m-%d').date() if fecha_devolver_str else None

        # Validaciones
        if len(pelicula_nombre) > 25:
            messages.error(request, 'Texto de búsqueda demasiado largo')
            return redirect('busqueda_peliculas')

        elif pelicula_nombre == "venom":
            messages.error(request, '¡Que fea película, elige otra!')
            return redirect('busqueda_peliculas')

        if fecha_inicio and fecha_devolver and fecha_inicio > fecha_devolver:
            messages.error(request, 'La fecha de inicio no puede ser mayor a la de devolución.')
            return redirect('busqueda_peliculas')

        # Llamar a la función para mostrar las películas
        return mostrar_peliculas(request, pelicula_nombre)

    else:
        messages.error(request, "No has introducido nada")
        return redirect('busqueda_peliculas')


def mostrar_peliculas(request, pelicula_nombre):
    # Filtrar las películas por el nombre
    pelicula_buscar = Pelicula.objects.filter(titulo__icontains=pelicula_nombre)
    return render(request, "resultados_busqueda_peliculas.html", {"peliculas": pelicula_buscar})


def pelicula_detalles(request, pelicula_id):
    filtro_pelicula = Pelicula.objects.get(id=pelicula_id)
    return render(request, "detalles_pelicula.html", {"pelicula": filtro_pelicula})
