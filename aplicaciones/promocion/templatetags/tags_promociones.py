from django.template import Library

register = Library()

def generarPuntos(puntos, multiplicador):
    return str(puntos * multiplicador)

register.filter("PuntoG",generarPuntos)