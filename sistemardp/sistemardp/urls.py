"""
URL configuration for sistemardp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('lobby.urls')), 
    path('usuario/', include('clientes.urls')), 
    path('rentar/',include('peliculas.urls')),
    path('carro/',include('carro.urls')),
    path('membership/', include('membership.urls')),
    path('pedidos/',include('pedidos.urls')),
    path('clientes/', include('clientes.urls')),
    path('bloqueado/', views.bloqueado, name='bloqueado'), # URL para mostrar mensaje de bloqueo

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
