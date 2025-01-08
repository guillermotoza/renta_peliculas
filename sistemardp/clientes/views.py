from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Cliente
from .forms import ClienteForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy

# Listar clientes y enviar datos
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

# Agregar clientes a través de AJAX
@csrf_exempt
def agregar_cliente(request):
    if request.method == 'POST' and request.is_ajax():
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

# Editar clientes con AJAX
@csrf_exempt
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')  # Redirige a la vista de lista de clientes después de guardar
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})

@csrf_exempt
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/listar_clientes.html', {'clientes': clientes})

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

# Registro y autenticación
class Vregistro(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "clientes/registro.html", {"form": form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('busqueda_peliculas')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, "clientes/registro.html", {"form": form})

def cerrar_sesion(request):
    logout(request) 
    return redirect('busqueda_peliculas')

def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contraseña_usuario = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contraseña_usuario)
            if usuario is not None:
                login(request, usuario)
                return redirect('busqueda_peliculas')
            else:
                messages.error(request, "* Usuario no válido")
        else:
            messages.error(request, "* Información incorrecta")

    form = AuthenticationForm()
    return render(request, "clientes/login.html", {"form": form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'