from django.urls import path
from pedidos import views


urlpatterns = [
    path('', views.procesar_pedido,name="pedidos"),
    path('generar_pdf_pedido/<int:pedido_id>/', views.generar_pdf_pedido, name='generar_pdf_pedido'),
    path('generar_excel_pedido/<int:pedido_id>/',views.generar_excel_pedido,name='generar_excel_pedido'),
]
