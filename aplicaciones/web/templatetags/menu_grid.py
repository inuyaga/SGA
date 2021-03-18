from django import template
from aplicaciones.pedidos.models import Area, Subcategoria, Linea, Producto

register = template.Library() 

@register.filter
def get_subcategoria(key):
    query = Subcategoria.objects.filter(sc_area=key)
    return query

@register.filter
def get_linea(key):
    query = Linea.objects.filter(l_subcat=key)
    return query

@register.filter
def get_producto(IDMarca):
    query = Producto.objects.filter(producto_marca=IDMarca).exclude(producto_marca=40).exclude(producto_importancia = 0).order_by('producto_importancia','producto_marca')[:25]
    return query
