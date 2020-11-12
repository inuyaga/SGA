from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView

class InicioView(TemplateView):
    template_name = "gasto/inicio.html"
    

class CrearTipoGasto(CreateView):
    template_name = "gasto/crear.html"