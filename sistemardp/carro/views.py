from itertools import product
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from carro.carro import Carro
from django.views import View
from peliculas.models import Pelicula


# Create your views here.


class agregar_pelicula(View):
    def post(self, request, pelicula_id):
        carro = Carro(request)
        pelicula = get_object_or_404(Pelicula, id=pelicula_id)

        dias_maximos = 15
        dias_rentados_en_carro = carro.obtener_cantidad(pelicula)

        if dias_rentados_en_carro < dias_maximos:
            carro.agregar(pelicula=pelicula)
            messages.success(request, f'Película "{pelicula.titulo}" agregada al carrito')
        else:
            messages.error(request, "Lo sentimos, el máximo de días permitidos son 15.")

        peliculas = Pelicula.objects.all()  # Actualiza tu contexto si es necesario
        return render(request, "resultados_busqueda_peliculas.html", {"peliculas": peliculas})


class eliminar_pelicula(View):
    def post(self, request, pelicula_id):
        carro = Carro(request)
        pelicula = get_object_or_404(Pelicula, id=pelicula_id)
        carro.eliminar(pelicula)
        messages.success(request, f'La película "{pelicula.titulo}" ha sido eliminada del carrito.') 

        # Volver a renderizar la misma página con datos actualizados
        return render(request, "resultados_busqueda_peliculas.html", {})

class restar_pelicula(View):
    def post(self, request, pelicula_id):
        carro = Carro(request)
        pelicula = get_object_or_404(Pelicula, id=pelicula_id)
        carro.restar_pelicula(pelicula)
        messages.success(request, f'Se ha reducido un día de la película "{pelicula.titulo}" en el carrito.')

        return render(request, "resultados_busqueda_peliculas.html", {})

class limpiar_carro(View):
    def post(self, request):
        carro = Carro(request)
        carro.vaciar_carro()
        messages.success(request, "El carrito ha sido vaciado correctamente.")

        return render(request, "resultados_busqueda_peliculas.html", {})


