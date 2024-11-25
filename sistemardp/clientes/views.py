from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Cliente
from django.utils.dateparse import parse_datetime
import json

# Alta de Cliente (POST /clientes)
@csrf_exempt
@require_http_methods(["POST"])
def crear_cliente(request):
    try:
        data = json.loads(request.body)
        cliente = Cliente.objects.create(
            nombre=data['nombre'],
            correo=data['correo'],
            direccion=data['direccion'],
            detalles_membresia=data.get('detalles_membresia', ''),
        )
        return JsonResponse({'id': cliente.id, 'nombre': cliente.nombre}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Baja de Cliente (DELETE /clientes/<id>)
@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        cliente.fecha_baja = parse_datetime('now')  # Marca la fecha de baja
        cliente.save()
        return JsonResponse({'message': 'Cliente eliminado correctamente'}, status=200)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

# Cambios de Cliente (PUT /clientes/<id>)
@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_cliente(request, cliente_id):
    try:
        data = json.loads(request.body)
        cliente = Cliente.objects.get(id=cliente_id)
        
        # Actualizamos solo los campos que se reciben
        cliente.nombre = data.get('nombre', cliente.nombre)
        cliente.correo = data.get('correo', cliente.correo)
        cliente.direccion = data.get('direccion', cliente.direccion)
        cliente.detalles_membresia = data.get('detalles_membresia', cliente.detalles_membresia)
        
        cliente.save()
        return JsonResponse({'id': cliente.id, 'nombre': cliente.nombre}, status=200)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

