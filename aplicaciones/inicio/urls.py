from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import InicioSga, err_permisos
app_name = "inicio"
urlpatterns = [
    path('', InicioSga.as_view(), name='index'),
    path('permisos/', err_permisos, name='need_permisos'),
]