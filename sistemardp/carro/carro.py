from django.shortcuts import redirect
from peliculas.models import Pelicula
from decimal import Decimal, ROUND_HALF_UP


class Carro:
    def __init__(self, request):
        self.session = request.session
        carro = self.session.get("carro")
        if not carro:
            carro = self.session["carro"] = {}
        self.carro = carro

    def agregar(self, pelicula):
<<<<<<< Updated upstream
        pelicula_id = str(pelicula.id)
        if pelicula_id not in self.carro:
            self.carro[pelicula_id] = {
                "pelicula_id": pelicula.id,
                "titulo": pelicula.titulo,
                "precio": str(pelicula.precio_final),
                "cantidad": 1,
                "imagen": pelicula.imagen.url if pelicula.imagen else None,
            }
        else:
            self.carro[pelicula_id]["cantidad"] += 1
=======
        if(str(pelicula.id) not in self.carro.keys()):
            self.carro[pelicula.id]={
                "pelicula_id":pelicula.id,
                "titulo":pelicula.titulo,
                "precio":str(pelicula.precio),
                "dias":1, #dias de renta de la pelicula
                "imagen":pelicula.imagen.url,
                "descuento":pelicula.descuento,
                "precio_final":str(pelicula.precio - (pelicula.precio * pelicula.descuento / 100)),
                "stock":pelicula.stock,
                }
        else:
            for key, value in self.carro.items():
                if key == str(pelicula.id):
                    value["dias"] = value["dias"]+1
                    # Precio unitario actualizado con descuento aplicado
                    precio_con_descuento = pelicula.precio - (pelicula.precio * pelicula.descuento / 100)
                    # Actualiza el precio total sumando el precio con descuento
                    value["precio"] = str(Decimal(value["precio"]) + precio_con_descuento)
                    # Actualiza el precio final total (aunque este valor puede depender de cómo se quiera mostrar en la vista)
                    value["precio_final"] = str(Decimal(value["precio_final"]) + precio_con_descuento)
                    #value["precio"] = round(float(value["precio"])+ float(pelicula.precio_final),2)
                break

>>>>>>> Stashed changes
        self.guardar_carro()

    def guardar_carro(self):
        self.session.modified = True

    def eliminar(self, pelicula):
        pelicula_id = str(pelicula.id)
        if pelicula_id in self.carro:
            del self.carro[pelicula_id]
            self.guardar_carro()

<<<<<<< Updated upstream
    def restar_pelicula(self, pelicula):
        pelicula_id = str(pelicula.id)
        if pelicula_id in self.carro:
            self.carro[pelicula_id]["cantidad"] -= 1
            if self.carro[pelicula_id]["cantidad"] <= 0:
                self.eliminar(pelicula)
            self.guardar_carro()
=======
    def restar_pelicula(self,pelicula):
        for key, value in self.carro.items():
            if key == str(pelicula.id):
                value["dias"]=value["dias"]-1
                # Calcular el precio considerando si hay descuento o no
                if float(value["descuento"]) > 0:
                # Si hay descuento, recalculamos el precio con descuento
                    precio_con_descuento = pelicula.precio - (pelicula.precio * pelicula.descuento / 100)
                    value["precio"] = str(float(value["precio"]) - precio_con_descuento)
                else:
                    # Si no hay descuento, restamos el precio unitario directamente
                    value["precio"] = str(float(value["precio"]) - pelicula.precio)
                if value["dias"] < 1:
                    self.eliminar(pelicula)
>>>>>>> Stashed changes

    def vaciar_carro(self):
        self.session["carro"] = {}
        self.guardar_carro()

    def obtener_cantidad(self, pelicula):
        pelicula_id = str(pelicula.id)
        if pelicula_id in self.carro:
            return self.carro[pelicula_id]["cantidad"]
        return 0