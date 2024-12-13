from django.shortcuts import redirect
from peliculas.models import Pelicula
from decimal import Decimal, ROUND_HALF_UP


class Carro:
    def __init__(self,request):
        self.request=request
        self.session=request.session
        carro=self.session.get("carro")
        if not carro:
            carro=self.session["carro"]={}

        self.carro=carro

    def agregar(self, pelicula):
        if(str(pelicula.id) not in self.carro.keys()):
            self.carro[pelicula.id]={
                "pelicula_id":pelicula.id,
                "titulo":pelicula.titulo,
                "precio":float(pelicula.precio),
                "dias":1, #dias de renta de la pelicula
                "imagen":pelicula.imagen.url,
                "descuento":float(pelicula.descuento),
                "precio_final":float(pelicula.precio_final),
                "stock":pelicula.stock,
                }
        else:
            for key, value in self.carro.items():
                if key == str(pelicula.id):
                    value["dias"] = value["dias"]+1
                    value["precio"] = round(float(value["precio"])+ float(pelicula.precio_final),2)
                break

        self.guardar_carro()

    def guardar_carro(self):
        self.session["carro"]=self.carro
        self.session.modified=True

    def eliminar(self, pelicula):
        pelicula_id =str(pelicula.id)
        if pelicula_id in self.carro:
            del self.carro[pelicula_id]
            self.guardar_carro()

    def restar_pelicula(self,pelicula):
        for key, value in self.carro.items():
            if key == str(pelicula.id):
                value["dias"]=value["dias"]-1
                value["precio"]= round(float(value["precio"]) - float(pelicula.precio_final),2)
            if value["dias"] < 1:
                self.eliminar(pelicula)

            break
        self.guardar_carro()

    def obtener_cantidad(self, pelicula):
        pelicula_id = str(pelicula.id)
        if pelicula_id in self.carro:
            return self.carro[pelicula_id]['dias']
        return 0

    def vaciar_carro(self):
        self.session["carro"]={}
        self.session.modified=True