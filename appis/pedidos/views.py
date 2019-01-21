# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def compra_tienda(request):
    return render(request, 'pedidos/compra_tiendas.html', {})
