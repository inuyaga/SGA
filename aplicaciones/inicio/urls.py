from django.contrib import admin
from django.urls import path
from aplicaciones.inicio.views import InicioSga, err_permisos, ChatView
app_name = "inicio"
urlpatterns = [
    path('', InicioSga.as_view(), name='index'), 
    path('chat_msn', ChatView.as_view(), name='chat'),
    path('permisos/', err_permisos, name='need_permisos'),
]