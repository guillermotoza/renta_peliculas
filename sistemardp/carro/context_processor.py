from decimal import Decimal

def importe_total_carro(request):
    total=0
    if request.user.is_authenticated: # hasta que existan una autentificacion de 
        carro = request.session.get("carro", {})
        for key, value in request.session["carro"].items():
            if Decimal(value["descuento"]) > 0:
                total+=(Decimal(value["precio_final"]))
            else:
                total+=(Decimal(value["precio"]))
    return {"importe_total_carro":total}