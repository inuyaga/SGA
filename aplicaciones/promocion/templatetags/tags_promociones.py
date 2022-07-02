import random
from django.template import Library

register = Library()

def generarPuntos(a, puntos):
    multiplicador=0
    if a == '255':
        multiplicador= 15 *puntos
    if a == '855':
        multiplicador= 15 * puntos
    if a == '261':
        multiplicador= 9 * puntos
    if a == '440':
        multiplicador= 15 * puntos
    if a == '022':
        multiplicador= 9 * puntos
    if a == '009':
        multiplicador= 9 * puntos
    if a == '623':
        multiplicador= 6 *puntos
    if a == '111':
        multiplicador= 3 * puntos
    if a == '801':
        multiplicador= 3 * puntos
    return str(multiplicador)

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)

@register.simple_tag
def proveedorLetra(a):
    proveedor="ninguno"
    if a == '255':
        proveedor="NORMA"
    if a == '855':
        proveedor="RODIN"
    if a == '261':
        proveedor="ESCRIMEX"
    if a == '440':
        proveedor="ARIMANY"
    if a == '022':
        proveedor="HENKEL"
    if a == '009':
        proveedor="PELIKAN"
    if a == '623':
        proveedor="JUMBO"
    if a == '111':
        proveedor="KOLA LOKA"
    if a == '801':
        proveedor="ESTILO"
    return str(proveedor)
    
register.filter("PuntoG",generarPuntos)