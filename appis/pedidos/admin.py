# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib import admin
from appis.pedidos.models import Producto, Area, Marca, Pedido, Detalle_pedido
from appis.admon_empresa.models import Departamento
# Register your models here.
#class Detalle_pedidoInstanceInLine(admin.TabularInline):
#    model = Detalle_pedido


#EJEMPLO COMO SE OBTIENN LOS ELEMENTOS DE UN POST Y POSTERIORMENTE GUARDAR
#def save_model(self, request, obj, form, change):
#    qr=Producto.objects.get(producto_codigo=request.POST.get('detalle_pedido_set-0-detallepedido_producto_id'))
#    print(obj.__dict__)
#    super(PedidoConfig, self).save_model(request, obj, form, change)

class detallePedido(admin.ModelAdmin):
    list_display=('detallepedido_pedido_id', 'detallepedido_producto_id', 'detallepedido_cantidad','detallepedido_precio',)
    readonly_fields=('detallepedido_precio',)
    list_filter=('detallepedido_pedido_id',)
    def save_model(self, request, obj, form, change):
        qr=Producto.objects.get(producto_codigo=request.POST.get('detallepedido_producto_id'))
        obj.detallepedido_precio=qr.producto_precio
        super(detallePedido, self).save_model(request, obj, form, change)

class PedidoConfig(admin.ModelAdmin):
    list_display=('pedido_id_pedido', 'pedido_fecha_pedido', 'pedido_status', 'pedido_id_depo', 'limite_gastos', 'total', 'nombre_sucursal', 'empresa',)
    exclude=("pedido_status",)
    readonly_fields=('pedido_status',)
    raw_id_fields=('pedido_id_depo',)
    list_filter=('pedido_status',)
    #inlines = [Detalle_pedidoInstanceInLine]
    list_editable = ('pedido_status',)




    #def getnombredepo(self, object):
    #    n = object.pedido_id_depo
    #    query=Departamento.objects.get(departamento_id_depo=n)
    #    return query.departamento_nombre


admin.site.register(Producto)
admin.site.register(Area)
admin.site.register(Marca)
admin.site.register(Pedido, PedidoConfig)
admin.site.register(Detalle_pedido, detallePedido)
