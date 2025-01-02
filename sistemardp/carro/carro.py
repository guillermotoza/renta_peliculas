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
        self.guardar_carro()

    def guardar_carro(self):
        self.session.modified = True

    def eliminar(self, pelicula):
        pelicula_id = str(pelicula.id)
        if pelicula_id in self.carro:
            del self.carro[pelicula_id]
            self.guardar_carro()

    def restar_pelicula(self, pelicula):
        pelicula_id = str(pelicula.id)
        if pelicula_id in self.carro:
            self.carro[pelicula_id]["cantidad"] -= 1
            if self.carro[pelicula_id]["cantidad"] <= 0:
                self.eliminar(pelicula)
            self.guardar_carro()

    def vaciar_carro(self):
        self.session["carro"] = {}
        self.guardar_carro()

    def obtener_cantidad(self, pelicula):
        pelicula_id = str(pelicula.id)
        if pelicula_id in self.carro:
            return self.carro[pelicula_id]["cantidad"]
        return 0