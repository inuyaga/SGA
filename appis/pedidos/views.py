# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from appis.pedidos.models import Producto

from django.shortcuts import render

# Create your views here.

def compra_tienda(request):
    productos = Producto.objects.all()
    contex = {'productos': productos}
    return render(request, 'pedidos/compra_tiendas.html', contex)
