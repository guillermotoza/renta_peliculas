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
    pdf_response = generar_pdf_pedido(request, pedido_id=pedido.id) #deberia descargar el pdf en automatico en la pagina

    messages.success(request, "El pedido se ha creado correctamente")
    return render(request, "confirmar_pedido.html", {
        "pedido": pedido,
        "lineas_pedido": lineas_pedido,
        "pdf_response": pdf_response,
        "total_pedido":total_pedido
    })
    

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
        from_email='moises.ramirezr@fgr.org.mx'
        to=kwargs.get("emailusuario")
        
        send_mail(asunto,mensaje_texto,from_email,[to],html_message=mensaje)

#funcion para generar pdf
def generar_pdf_pedido(request, pedido_id):
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

        data.append(['', '', 'Total', f"${total:.2f}"]) #total del pedido

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
    sheet.append(["", "", "", "TOTAL", f"${total:.2f}"])

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
