from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'direccion', 'detalles_membresia', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('nombre', 'correo')
