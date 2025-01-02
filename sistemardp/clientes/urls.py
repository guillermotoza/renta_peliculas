from django.urls import path
from . import views
from .views import Vregistro
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('clientes/', views.cargar_clientes, name='cargar_clientes'),  
    path('usuario', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path("", Vregistro.as_view(), name="autentificar"),
    path("cerrar_sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("iniciar_sesion/", views.iniciar_sesion, name="iniciar_sesion"),
   
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset_form.html',
        email_template_name='auth/password_reset_email.html',
        success_url='done/'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),
]


