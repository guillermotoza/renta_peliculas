from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cliente, Pelicula
from django.shortcuts import render
from django.contrib.auth import logout
from carro.carro import Carro
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

def lobby(request):
    carro=Carro(request)
    return render(request, 'lobby.html')

#validacion manual del formulario contacto
def contactar (request):
    if request.method=="POST":
        subject="reclamacion: "+" "+request.POST["asunto"]
        message="el problema del cliente es: "+""+request.POST["mensaje"]+" el correo del cliente, para contactarlo es: "+request.POST["email"]
        email_from=settings.EMAIL_HOST_USER
        recipient_list=["moisesr_1000@hotmail.com"]
        
        if subject and message and email_from:
            send_mail(subject, message, email_from, recipient_list)
            return render(request,"gracias.html")
        else:
            messages.error(request, "No has introducido nada")
            return render(request, "contacto.html")


            
    return render(request, "contacto.html")

# Vistas para clientes
def listar_clientes(request):
    clientes = Cliente.objects.all()
    clientes_data = [{
        'id': cliente.id,
        'nombre': cliente.nombre,
        'correo': cliente.correo,
        'direccion': cliente.direccion,
        'membresia': cliente.detalles_membresia
    } for cliente in clientes]
    
    return JsonResponse({'clientes': clientes_data})

def agregar_cliente(request):
    if request.method == 'POST' and request.is_ajax():
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')
        membresia = request.POST.get('membresia')
        
        if not nombre or not correo or not direccion or not membresia:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)
        
        cliente = Cliente.objects.create(
            nombre=nombre,
            correo=correo,
            direccion=direccion,
            detalles_membresia=membresia
        )
        
        return JsonResponse({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'correo': cliente.correo,
            'direccion': cliente.direccion,
            'membresia': cliente.detalles_membresia
        })
    return JsonResponse({'error': 'Solicitud no válida'}, status=400)

def editar_cliente(request, cliente_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.nombre = request.POST.get('nombre', cliente.nombre)
            cliente.correo = request.POST.get('correo', cliente.correo)
            cliente.direccion = request.POST.get('direccion', cliente.direccion)
            cliente.detalles_membresia = request.POST.get('membresia', cliente.detalles_membresia)
            cliente.save()

            return JsonResponse({
                'id': cliente.id,
                'nombre': cliente.nombre,
                'correo': cliente.correo,
                'direccion': cliente.direccion,
                'membresia': cliente.detalles_membresia
            })
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    return JsonResponse({'error': 'Solicitud no válida'}, status=400)

def eliminar_cliente(request, cliente_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.delete()
            return JsonResponse({'success': True})
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    return JsonResponse({'error': 'Solicitud no válida'}, status=400)

# Vistas para películas
def listar_peliculas(request):
    peliculas = Pelicula.objects.all()
    peliculas_data = [{
        'id': pelicula.id,
        'titulo': pelicula.titulo,
        'descripcion': pelicula.descripcion,
        'fecha_lanzamiento': pelicula.fecha_lanzamiento,
        'disponible': pelicula.disponible
    } for pelicula in peliculas]
    
    return JsonResponse({'peliculas': peliculas_data})

def agregar_pelicula(request):
    if request.method == 'POST' and request.is_ajax():
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha_lanzamiento = request.POST.get('fecha_lanzamiento')
        disponible = request.POST.get('disponible') == 'true'
        
        if not titulo or not descripcion or not fecha_lanzamiento:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)
        
        pelicula = Pelicula.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha_lanzamiento=fecha_lanzamiento,
            disponible=disponible
        )
        
        return JsonResponse({
            'id': pelicula.id,
            'titulo': pelicula.titulo,
            'descripcion': pelicula.descripcion,
            'fecha_lanzamiento': pelicula.fecha_lanzamiento,
            'disponible': pelicula.disponible
        })
    return JsonResponse({'error': 'Solicitud no válida'}, status=400)

def editar_pelicula(request, pelicula_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            pelicula = Pelicula.objects.get(id=pelicula_id)
            pelicula.titulo = request.POST.get('titulo', pelicula.titulo)
            pelicula.descripcion = request.POST.get('descripcion', pelicula.descripcion)
            pelicula.fecha_lanzamiento = request.POST.get('fecha_lanzamiento', pelicula.fecha_lanzamiento)
            pelicula.disponible = request.POST.get('disponible') == 'true'
            pelicula.save()

            return JsonResponse({
                'id': pelicula.id,
                'titulo': pelicula.titulo,
                'descripcion': pelicula.descripcion,
                'fecha_lanzamiento': pelicula.fecha_lanzamiento,
                'disponible': pelicula.disponible
            })
        except Pelicula.DoesNotExist:
            return JsonResponse({'error': 'Película no encontrada'}, status=404)
    return JsonResponse({'error': 'Solicitud no válida'}, status=400)

def eliminar_pelicula(request, pelicula_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            pelicula = Pelicula.objects.get(id=pelicula_id)
            pelicula.delete()
            return JsonResponse({'success': True})
        except Pelicula.DoesNotExist:
            return JsonResponse({'error': 'Película no encontrada'}, status=404)
    return JsonResponse({'error': 'Solicitud no válida'}, status=400)


def custom_logout_view(request):
    logout(request)
    return redirect('iniciar_sesion')

def politica_privacidad(request):
    return render(request, 'politica_privacidad.html')

