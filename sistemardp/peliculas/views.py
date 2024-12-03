from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse 
from peliculas.models import pelicula, CategoriaPel
from django.contrib import messages
from datetime import date, datetime


# Create your views here.

def busqueda_peliculas(request):
    return render(request, "busqueda_peliculas.html")


def resultados_peliculas(request):
    if request.GET.get("pelicula") and request.GET.get("fecha_inicio") and request.GET.get("fecha_devolver"):
        pelicula_nombre = request.GET.get("pelicula")
        fecha_inicio_str = request.GET.get("fecha_inicio")
        fecha_devolver_str = request.GET.get("fecha_devolver")

        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None
        fecha_devolver = datetime.strptime(fecha_devolver_str, '%Y-%m-%d').date() if fecha_devolver_str else None

        if len(pelicula_nombre) > 25 :
            messages.error(request, 'texto de busqueda demasiado largo')
            return redirect('busqueda_peliculas')
        
        elif pelicula_nombre == "venom" :
            messages.error(request, 'que fea pelicula, elije otra')
            return redirect('busqueda_peliculas')

        elif fecha_inicio >= fecha_devolver:
            messages.error(request,"la fecha de devolucion no puede ser antes de la fecha de inicio de renta")
            return redirect('busqueda_peliculas')

        elif fecha_inicio < date.today():
            messages.error(request, "la fecha de inicio de renta no puede ser anterior al dia actual")

        else:
            pelicula_buscar = pelicula.objects.filter(titulo__icontains=pelicula_nombre)
            return render(request, "resultados_busqueda_peliculas.html",{"peliculas":pelicula_buscar })

    else:
        messages.error(request, "No has introducido nada")
        return redirect('busqueda_peliculas')  # Redirige a la p�gina de b�squeda