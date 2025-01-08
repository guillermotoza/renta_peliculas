from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from carro.carro import Carro
from django.views import View
from peliculas.models import Pelicula
from membership.models import UserMembership
from decimal import Decimal

"Clase base para manejar las acciones del carrito."
class BaseCarroView(View): 

    def get_carro(self, request):
        return Carro(request)

    def get_pelicula(self, pelicula_id):
        return get_object_or_404(Pelicula, id=pelicula_id)

def obtener_descuento_membresia(request):
    if request.user.is_authenticated:
        try:
            user_membership = UserMembership.objects.get(user=request.user)
            membership_type = user_membership.membership.membership_type

            if membership_type == 'Silver':
                return Decimal('0.05')
            elif membership_type == 'Gold':
                return Decimal('0.10')
        except UserMembership.DoesNotExist:
            pass
    return Decimal('0.00')


class AgregarPeliculaView(BaseCarroView):
    def post(self, request, pelicula_id):
        # Obtén el carrito y la película
        carro = self.get_carro(request)
        pelicula = self.get_pelicula(pelicula_id)
        
        # Máximo de días permitidos para rentar
        dias_maximos = 15
        dias_rentados_en_carro = carro.obtener_cantidad(pelicula)
        
        # Calcula el descuento de la membresía del usuario
        descuento_membresia = obtener_descuento_membresia(request)
        
        if dias_rentados_en_carro < dias_maximos:
            # Agrega la película al carrito con el descuento correspondiente
            carro.agregar(pelicula=pelicula, descuento_membresia=descuento_membresia)
            
            # Respuestas en caso de éxito
            messages.success(request, f'Película "{pelicula.titulo}" agregada al carrito.')
            response = {
                "success": True,
                "message": f'Película "{pelicula.titulo}" agregada al carrito.',
                "descuento": float(descuento_membresia),  # Envíalo en la respuesta si es necesario
            }
        else:
            # Respuestas en caso de error
            messages.error(request, "Lo sentimos, el máximo de días permitidos son 15.")
            response = {
                "success": False,
                "message": "Lo sentimos, el máximo de días permitidos son 15.",
            }
        
        # Si la petición es AJAX, responde con JSON
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(response)
        
        # Si no es AJAX, redirige a la tienda
        return redirect("tienda")


class EliminarPeliculaView(BaseCarroView):
    def post(self, request, pelicula_id):
        carro = self.get_carro(request)
        pelicula = self.get_pelicula(pelicula_id)
        carro.eliminar(pelicula)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":  # Manejo para peticiones AJAX
            return JsonResponse({"success": True, "message": f'La película "{pelicula.titulo}" ha sido eliminada del carrito.'})
        return redirect("tienda")


class RestarPeliculaView(BaseCarroView):
    def post(self, request, pelicula_id):
        carro = self.get_carro(request)
        pelicula = self.get_pelicula(pelicula_id)
        carro.restar_pelicula(pelicula)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":  # Manejo para peticiones AJAX
            return JsonResponse({"success": True, "message": f'Se ha reducido un día de la película "{pelicula.titulo}" en el carrito.'})
        return redirect("tienda")


class LimpiarCarroView(BaseCarroView):
    def post(self, request):
        carro = self.get_carro(request)
        carro.vaciar_carro()

        messages.success(request, "El carrito ha sido vaciado correctamente.")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":  # Manejo para peticiones AJAX
            return JsonResponse({"success": True, "message": "El carrito ha sido vaciado correctamente."})
        return redirect("tienda")
