from decimal import Decimal

def importe_total_carro(request):
    # Verifica si 'carro' existe en la sesión, si no, usa un diccionario vacío
    carro = request.session.get('carro', {})
    total = sum(item['price'] * item['quantity'] for item in carro.values())
    return {'importe_total_carro': total}

#def importe_total_carro(request):
#    total=0
 #   if request.user.is_authenticated: # hasta que existan una autentificacion de 
  #      carro = request.session.get("carro", {})
   #     for key, value in request.session["carro"].items():
    #        if Decimal(value["descuento"]) > 0:
     #           total+=(Decimal(value["precio_final"]))
      #      else:
       #         total+=(Decimal(value["precio"]))
    #return {"importe_total_carro":total}    
