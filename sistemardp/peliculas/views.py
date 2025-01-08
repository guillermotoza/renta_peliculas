from django.shortcuts import render, redirect, get_object_or_404
from peliculas.models import Pelicula, CategoriaPel
from django.contrib.auth import get_user_model
from pedidos.models import Pedido
from django.contrib import messages
from datetime import datetime
from carro.carro import Carro
from django.views import View
from django.http import JsonResponse
from django.core import serializers

User = get_user_model()

class TiendaView(View):
    def get(self, request):
        peliculas = Pelicula.objects.all()
        if request.headers.get('Accept') == 'application/json':
            peliculas_json = serializers.serialize('json', peliculas)
            return JsonResponse(peliculas_json, safe=False)    

        
        return render(request, "resultados_busqueda_peliculas.html", {"peliculas": peliculas})

class PeliculasJsonView(View):
    def get(self, request):
        peliculas = Pelicula.objects.all()
        peliculas_json = serializers.serialize('json', peliculas)
        return JsonResponse(peliculas_json, safe=False)

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

    if request.headers.get('Accept') == 'application/json':
        # Serializar resultados en JSON
        peliculas_json = serializers.serialize('json', pelicula_buscar)
        return JsonResponse({'peliculas': peliculas_json}, safe=False)

    return render(request, "resultados_busqueda_peliculas.html", {"peliculas": pelicula_buscar})

def pelicula_detalles(request, pelicula_id):
    filtro_pelicula = Pelicula.objects.get(id=pelicula_id)
    return render(request, "detalles_pelicula.html", {"pelicula": filtro_pelicula})

def busqueda_peliculas(request):
    carro = Carro(request)
    top_10_peliculas = Pelicula.objects.order_by('-ventas_totales')[:10]
    todas_peliculas = Pelicula.objects.all()
    categoria_accion = CategoriaPel.objects.get(nombreCatPel='accion')
    categoria_infantil = CategoriaPel.objects.get(nombreCatPel='Infantil')
    peliculas_accion = Pelicula.objects.filter(categorias=categoria_accion)
    peliculas_infantiles = Pelicula.objects.filter(categorias=categoria_infantil)
    context = {
        'top_10_peliculas': top_10_peliculas,
        'todas_peliculas': todas_peliculas,
        'peliculas_accion': peliculas_accion,
        'peliculas_infantiles': peliculas_infantiles,
    }
    return render(request, "busqueda_peliculas.html", context)



