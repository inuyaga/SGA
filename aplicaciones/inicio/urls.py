from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import InicioSga, err_permisos, v2
app_name = "inicio"
urlpatterns = [
    path('', InicioSga.as_view(), name='index'),
    path('v2/', v2.as_view(), name='version2'),
    path('permisos/', err_permisos, name='need_permisos'),
]