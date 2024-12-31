from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
#reportlab para generar PDF
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.pdfgen import canvas
#openpyxl para generar EXCEL
from openpyxl.styles import Font, Alignment
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font,PatternFill,Side
#VISTAS
from .models import Pedido, LineaPedido
from carro.carro import Carro
from pedidos.models import LineaPedido, Pedido

# Create your views here.

@login_required(login_url="/usuario/iniciar_sesion/")
def procesar_pedido(request):
    pedido = Pedido.objects.create(user=request.user)
    carro = Carro(request)
    lineas_pedido = []
    total_pedido = sum(linea.total_pedido for linea in lineas_pedido)

    for key, value in carro.carro.items():
        lineas_pedido.append(LineaPedido(
            pelicula_id=key,
            dias=value["dias"],
            user=request.user,
            pedido=pedido,
            ))

    LineaPedido.objects.bulk_create(lineas_pedido)

    
    enviar_mail(
        pedido=pedido,
        lineas_pedido=lineas_pedido,
        nombreusuario=request.user.username,
        emailusuario=request.user.email
    )

   

    messages.success(request, "El pedido se ha creado correctamente")
    

#funcion para enviar email
def enviar_mail(**kwargs):
    if Carro:
        asunto="PEDIDO REALIZADO, GRACIAS"
        mensaje=render_to_string("email/pedido.html",{
            "pedido":kwargs.get("pedido"),
            "lineas_pedido":kwargs.get("lineas_pedido"),
            "nombreusuario":kwargs.get("nombreusuario"),
            "email":kwargs.get("emailusuario")
        })
        
        mensaje_texto=strip_tags(mensaje)
        from_email="moises.ramirezr@fgr.org.mx"
        to=kwargs.get("emailusuario")
        
        send_mail(asunto,mensaje_texto,from_email,[to],html_message=mensaje)  