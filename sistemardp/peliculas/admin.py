from django.contrib import admin

from peliculas.models import pelicula, CategoriaPel
# Register your models here.

class gestion_peliculas(admin.ModelAdmin):
    list_display=("titulo","director")
    search_fields=("titulo","director")

class categoria_admin(admin.ModelAdmin):
    readonly_fields=('created','updated')

admin.site.register(pelicula,gestion_peliculas)
admin.site.register(CategoriaPel)