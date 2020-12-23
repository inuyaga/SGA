"""SGA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView, LogoutView
from ajax_select import urls as ajax_select_urls

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin



admin.site.index_title = 'SGA Administración'



urlpatterns = [
    path('', include('aplicaciones.web.urls'), name='web'),
    path('adminsga/', admin.site.urls),
    path('api_mobile/', include('aplicaciones.api_mobile.urls'), name='api'),
    path('gastos/', include('aplicaciones.gasto.urls'), name='gasto'),
    path('ods/', include('aplicaciones.ods.urls'), name='ods'),
    path('empresa/', include('aplicaciones.empresa.urls'), name='empresa'),
    path('proveedor/', include('aplicaciones.pago_proveedor.urls'), name='proveedor'),
    path('activos/', include('aplicaciones.activos.urls'), name='activos'),
    path('fuds/', include('aplicaciones.fuds.urls'), name='fuds'),
    path('pedidos/', include('aplicaciones.pedidos.urls'), name='pedidos'),
    path('login/',LoginView.as_view(template_name='index/inicio.html'), name='inicio'),
    path('salir/', LogoutView.as_view(template_name='index/salir.html'), name="salir"),
    path('sga', include('aplicaciones.inicio.urls'), name='principal'),
    re_path(r'^ajax_select/', include(ajax_select_urls)),
    path('Expos/', include('aplicaciones.expo.urls'), name='expo'),
    path('compras/', include('aplicaciones.compra.urls'), name='compras'),
    path('descargas/', include('aplicaciones.descargas.urls'), name='descargas'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
