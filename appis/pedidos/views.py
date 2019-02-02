# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from appis.pedidos.models import Producto

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# pylint:disable=E1101

@login_required(login_url='/admin/')
def compra_tienda(request):
    productos = Producto.objects.all()
    contex = {'productos': productos}
    return render(request, 'pedidos/compra_tiendas.html', contex)


def busquedafiltro(request):
    productos = Producto.objects.filter(
        producto_descripcion__icontains=request.GET['buqueda'])
    contex = {'productos': productos}
    return render(request, 'pedidos/compra_tiendas.html', contex)
