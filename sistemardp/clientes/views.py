from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cliente
from .forms import ClienteForm
from django.views.decorators.csrf import csrf_exempt

# listar clientes y enviar datos
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

# VAgregar clientes a traves de ajax

@csrf_exempt
def agregar_cliente(request):
    if request.method == 'POST' and request.is_ajax():
        print(request.POST)  # Verifica los datos recibidos
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')
        membresia = request.POST.get('membresia')
        
        if not nombre or not correo or not direccion or not membresia:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)
        
        try:
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
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Solicitud no válida'}, status=400)

# editar clientes con ajax
@csrf_exempt
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

@csrf_exempt
def eliminar_cliente(request, cliente_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.delete()
            return JsonResponse({'success': True})
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    return JsonResponse({'error': 'Solicitud no válida'}, status=400)

@csrf_exempt
def cargar_clientes(request):
    clientes = Cliente.objects.filter(detalles_membresia='premium')  
    clientes_data = list(clientes.values('id', 'nombre', 'correo', 'direccion', 'detalles_membresia'))
    return JsonResponse({'clientes': clientes_data})