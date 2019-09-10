from django import template
from aplicaciones.pedidos.models import Tipo_Pedido
from aplicaciones.pedidos.models import Detalle_pedido

register = template.Library()
 
@register.filter
def get_item(dictionary, key):
    return dict(dictionary).get(key)

@register.filter
def get_tipoPedido(key):
    t_p=Tipo_Pedido.objects.get(tp=key)
    return t_p.tp_nombre

@register.filter
def get_count_tipo_pedido(key, user_id):
    detalle_tipo_pedido_conteo=Detalle_pedido.objects.filter(detallepedido_tipo_pedido=key, detallepedido_creado_por=user_id, detallepedido_status=False).count()
    return detalle_tipo_pedido_conteo

@register.filter
def get_color_class_badge(num_status):
    color=''
    if num_status == 1:
        color = 'secondary'
    if num_status == 2:
        color = 'success'
    if num_status == 3:
        color = 'danger'
    if num_status == 4:
        color = 'info'
    if num_status == 5:
        color = 'warning'
    if num_status == 6:
        color = 'primary'
    if num_status == 7:
        color = 'dark'
    return color

@register.filter
def get_nombre_mes(num_mes):
    mes=''
    if num_mes == 1:
        mes = 'Enero'
    if num_mes == 2:
        mes = 'Febrero'
    if num_mes == 3:
        mes = 'Marzo'
    if num_mes == 4:
        mes = 'Abril'
    if num_mes == 5:
        mes = 'Mayo'
    if num_mes == 6:
        mes = 'Junio'
    if num_mes == 7:
        mes = 'Julio'
    if num_mes == 8:
        mes = 'Agosto'
    if num_mes == 9:
        mes = 'Septiembre'
    if num_mes == 10:
        mes = 'Octubre'
    if num_mes == 11:
        mes = 'Noviembre'
    if num_mes == 12:
        mes = 'Diciembre'
    return mes
    