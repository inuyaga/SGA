from django import template
from aplicaciones.pedidos.models import Area, Subcategoria, Linea
register = template.Library() 

@register.filter
def get_subcategoria(key):
    query = Subcategoria.objects.filter(sc_area=key)
    return query

@register.filter
def get_linea(key):
    query = Linea.objects.filter(l_subcat=key)
    return query
