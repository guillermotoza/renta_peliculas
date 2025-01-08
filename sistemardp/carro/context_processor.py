from decimal import Decimal
from membership.models import UserMembership

from decimal import Decimal
from membership.models import UserMembership

def calcular_descuento_membresia(request):
    descuento_total = Decimal('0.00')
    if request.user.is_authenticated:
        user_membership = UserMembership.objects.get(user=request.user)
        membership_type = user_membership.membership.membership_type

        # Definir el descuento según el tipo de membresía
        if membership_type == 'Silver':
            discount = Decimal('0.05')
        elif membership_type == 'Gold':
            discount = Decimal('0.10')
        else:
            discount = Decimal('0.00')

        carro = request.session.get("carro", {})
        for key, value in carro.items():
            precio = Decimal(value["precio"])
            precio_final = precio * (1 - discount)
            descuento_total += (precio - precio_final) * value["dias"]

    return descuento_total

def importe_total_carro(request):
    total = Decimal('0.00')
    if request.user.is_authenticated:
        carro = request.session.get("carro", {})
        for key, value in carro.items():
            precio_final = Decimal(value.get("precio_final", value["precio"]))
            total += precio_final * value["dias"]

    descuento_membresia = calcular_descuento_membresia(request)
    total -= descuento_membresia

    return {"importe_total_carro": total}