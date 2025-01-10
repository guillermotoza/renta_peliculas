from decimal import Decimal
from membership.models import UserMembership

def importe_total_carro(request):
    total = Decimal('0.00')
    if request.user.is_authenticated:  # hasta que existan una autentificacion 
        carro = request.session.get("carro", {})
        for key, value in carro.items():
            # Usa el precio final calculado en models, si está disponible, si no, usa el precio normal
            total += Decimal(value.get("precio_final", value["precio"]))
    return {"importe_total_carro": total}

def calcular_descuento_global(request):
    # Context processor para calcular el descuento de membresía y el precio total del carrito con descuento.
    descuento = Decimal('0.00')  # Descuento por defecto para los que tienen membresia free
    total_carro_con_descuento = Decimal('0.00')  # Total inicial del carro con descuento
    total_carro = importe_total_carro(request)["importe_total_carro"]
    ahorro = Decimal('0.00')  # Inicializar ahorro

    # Solo para usuarios autenticados
    if request.user.is_authenticated:
        try:
            # Obtener la membresía del usuario
            user_membership = UserMembership.objects.get(user=request.user)
            membership_type = user_membership.membership.membership_type

            # Definir el porcentaje de descuento según el tipo de membresía
            if membership_type == 'Silver':
                descuento = Decimal('0.05')  # 5% de descuento
            elif membership_type == 'Gold':
                descuento = Decimal('0.10')  # 10% de descuento

            # Calcular el total con descuento
            total_carro_con_descuento = total_carro * (1 - descuento)
            ahorro = total_carro - total_carro_con_descuento
        except UserMembership.DoesNotExist:
            pass  # El usuario no tiene membresía; se usa el descuento por defecto

    # Retornar valores al contexto
    return {
        "total_carro_con_descuento": total_carro_con_descuento,
        "descuento": descuento,
        "ahorro": ahorro,       
    }