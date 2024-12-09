from itertools import product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from carro.carro import Carro
from django.views import View
from peliculas.models import pelicula
from sistemardp import carro, peliculas

# Create your views here.


class agregar_pelicula(View):
    def post(self, request, pelicula_id):
        carro=Carro(request)
        pelicula=get_object_or_404(peliculas,id=pelicula_id)

        dias_maximos = 15 # el maximo que una persona puede alquilar una pelicula
        dias_rentados_en_carro = carro.obtener_cantidad(pelicula) 

        if dias_rentados_en_carro < dias_maximos:
            carro.agregar(pelicula=pelicula)
            messages.success(request, f'Pelicula {pelicula.titulo} agregado al carrito')
        else:
            messages.error(request, f'lo sentimos, el maximo de dias son 15')

        return redirect("busqueda_peliculas")

class eliminar_pelicula(View):
    def post(self, request, pelicula_id):
        carro=Carro(request)
        pelicula=peliculas.objects.get(id=pelicula_id)
        carro.eliminar(pelicula)
        return redirect("busqueda_peliculas")

class restar_pelicula(View):
    def post(self, request, pelicula_id):
        carro=Carro(request)
        pelicula=peliculas.objects.get(id=pelicula_id)
        carro.restar_pelicula(pelicula)
        return redirect("busqueda_peliculas")

class limpiar_carro(View):
    def post(self,request):
        carro=Carro(request)
        carro.vaciar_carro()
        return redirect("busqueda_peliculas")


