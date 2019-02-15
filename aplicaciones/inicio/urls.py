from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import inicio, err_permisos
app_name = "inicio"
urlpatterns = [
    path('', inicio, name='index'),
    path('permisos/', err_permisos, name='need_permisos'),
]