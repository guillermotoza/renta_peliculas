from email import header
from statistics import LinearRegression
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
import os
from decimal import Decimal
from membership.models import UserMembership
#context procesor
from carro.context_processor import calcular_descuento_global, importe_total_carro

#reportlab para generar PDF
import openpyxl.workbook
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

@login_required(login_url="/usuario/iniciar_sesion/")
def procesar_pedido(request):  
   # Context processors  
   total_carro = importe_total_carro(request)["importe_total_carro"]  
   descuento = calcular_descuento_global(request)["descuento"]  
   total_carro_con_descuento = calcular_descuento_global(request)["total_carro_con_descuento"]  

   # Copiar el carrito antes de vaciarlo  
   carro = Carro(request)  
   carro_items = list(carro.carro.items())  # Copiar los items del carrito  

   # Crear el pedido  
   pedido = Pedido.objects.create(user=request.user)  
   lineas_pedido = []  

   for key, value in carro_items:  
       lineas_pedido.append(LineaPedido(  
           pelicula_id=key,  
           dias=value["dias"],  
           user=request.user,  
           pedido=pedido,  
       ))  

   LineaPedido.objects.bulk_create(lineas_pedido)  

   # Enviar email  
   enviar_mail(  
       pedido=pedido,  
       lineas_pedido=lineas_pedido,  
       nombreusuario=request.user.username,  
       emailusuario=request.user.email,  
       total_carro=total_carro,  
       descuento=descuento,  
       total_carro_con_descuento=total_carro_con_descuento,  
   )  

   # Generar reportes antes de vaciar el carrito  
   pdf_response = generar_pdf_pedido(request, pedido_id=pedido.id)  
   excel_response = generar_excel_pedido(request, pedido_id=pedido.id)  

   # Renderizar la página de confirmación del pedido  
   response = render(request, "confirmar_pedido.html", {  
       "pedido": pedido,  
       "lineas_pedido": lineas_pedido,  
       "pdf_response": pdf_response,  
       "total_pedido": total_carro_con_descuento,  
   })  

   # Vaciar el carrito después de renderizar la página  
   carro.vaciar_carro()  

   return response

    

#funcion para enviar email
def enviar_mail(**kwargs):
    if Carro:
        asunto="PEDIDO REALIZADO, GRACIAS"
        mensaje=render_to_string("email/pedido.html",{
            "pedido":kwargs.get("pedido"),
            "lineas_pedido":kwargs.get("lineas_pedido"),
            "nombreusuario":kwargs.get("nombreusuario"),
            "email":kwargs.get("emailusuario"),
            "importe_total_carro":kwargs.get("total_carro"),
            "descuento":kwargs.get("descuento"),
            "total_carro_con_descuento":kwargs.get("total_carro_con_descuento")
        })
        
        mensaje_texto=strip_tags(mensaje)
        from_email='moises.ramirezr@fgr.org.mx'
        to=kwargs.get("emailusuario")
        
        send_mail(asunto,mensaje_texto,from_email,[to],html_message=mensaje)

#funcion para generar pdf
def generar_pdf_pedido(request, pedido_id):

    total_carro = importe_total_carro(request)["importe_total_carro"]
    descuento = calcular_descuento_global(request)["descuento"]
    total_carro_con_descuento = calcular_descuento_global(request)["total_carro_con_descuento"]

    pedido = Pedido.objects.get(id=pedido_id, user=request.user)
    lineas_pedidos = LineaPedido.objects.filter(pedido=pedido)
    nombreusuario = request.user.username

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=pedido_{pedido.id}.pdf' #nombre del archivo

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet() #estilo de la hoja
    elements = []

    elements.append(Paragraph(f'Detalles del Pedido #{pedido.id}', styles['Title'])) #titulo del pdf
    elements.append(Paragraph(f'Usuario: {nombreusuario}', styles['Normal']))

    data = [
        ['Pelicula', 'Dias', 'Precio','sub-total']
    ]

    total= 0
    for linea in lineas_pedidos:
        if linea.pelicula.descuento > 0:
            precio_final = linea.pelicula.precio_final
        else:
            precio_final = linea.pelicula.precio
        sub_total = linea.dias * precio_final
        total += sub_total
        

        data.append([
            linea.pelicula.titulo, 
            linea.dias, 
            f"${precio_final:.2f}", 
            f"${sub_total:.2f}"
            ])
        if descuento > 0:
            data.append(['', '', 'Total', f"${total_carro_con_descuento:.2f}"])
        else:
            data.append(['', '', 'Total', f"${total_carro:.2f}"]) #total del pedido

         # Configura la tabla y el estilo
        table = Table(data)
        table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

     # Genera el contenido del PDF
    doc.build(elements)

    # Guarda el PDF en el buffer y lo envía en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

#funcion para generar excel
def generar_excel_pedido(request, pedido_id):
    #variables del context_processor
    total_carro = importe_total_carro(request)["importe_total_carro"]
    descuento = calcular_descuento_global(request)["descuento"]
    total_carro_con_descuento = calcular_descuento_global(request)["total_carro_con_descuento"]

    pedido = Pedido.objects.get(id=pedido_id, user=request.user)
    lineas_pedido = LineaPedido.objects.filter(pedido=pedido)
    nombreusuario = request.user.username

    wb = openpyxl.Workbook() #crea un libro de trabajo
    sheet = wb.active   #hoja activa
    sheet.title = f'Pedido {pedido.id}' #titulo de la hoja

    headers = ['Pelicula', 'Dias', 'Precio', 'Sub-total'] #nombres de las columnas
    sheet.append(headers)

    #estilos de los encabezados
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    #insertar datos
    total = 0
    for linea in lineas_pedido:
        if linea.pelicula.descuento > 0:
            precio_final = linea.pelicula.precio_final
        else:
            precio_final = linea.pelicula.precio
        sub_total = linea.dias * precio_final
        total += sub_total

        #agregando datos a la hoja
        sheet.append([
            linea.pelicula.titulo,
            linea.dias,
            f"${precio_final:.2f}",
            f"${sub_total:.2f}"
        ])
    # Agregar el total
    if descuento > 0:
        sheet.append(["", "", "", "TOTAL", f"${total_carro_con_descuento:.2f}"])
    else:
        sheet.append(["", "", "", "TOTAL", f"${total_carro:.2f}"])

    # Ajustar el ancho de columnas
    for column_cells in sheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    # Preparar la respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="pedido_{pedido_id}.xlsx"'

    # Guardar el archivo en el objeto response
    wb.save(response)

    return response
