# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib import admin
from appis.pago_proveedor.models import Complemento, Contrato, Factura, Pago, Proveedor
from xml.dom.minidom import parse
# CLASES PARA EDICION CONTINUAS


# class FacturaInlines(admin.TabularInline):
#     model = Factura
#     extra = 0
class ContratosInlines(admin.StackedInline):
    model = Contrato
    extra = 1
    readonly_fields = ('contrato_autorizado', 'contrato_status',)
##########################################################################################

# CONFIGURACIONES PARA LA VISTA DEL PANEL ADMINISTRADOR


class ProveedorConfig(admin.ModelAdmin):
    list_display = ('proveedor_nombre', 'proveedor_email',)
    inlines = [ContratosInlines]


class ContratoConfig(admin.ModelAdmin):
    list_display = ('contrato_id', 'contrato_proveedor_id',
                    'contrato_fecha_inicio', 'contrato_fecha_termino', 'contrato_dias_pago',
                    'contrato_monto', 'contrato_autorizado', 'contrato_status')

    readonly_fields = ('contrato_autorizado', 'contrato_status',)

    # def save_related(self, request, form, formsets, change):
    #     form.save_m2m()
    #     contador = 1
    #     for formset in formsets:
    #         self.save_formset(request, form, formset, change=change)
    #         contador = contador + 1
    #         print(formset.factura_set-3-factura_xml)

    #         super(ContratoConfig, self).save_model(
    #             request, form.instance, form, change)


class FacturaConfig(admin.ModelAdmin):

    readonly_fields = ('factura_monto_total', 'factura_iva_trasladado',
                       'factura_iva_retenido', 'factura_isr_retenido',)
    raw_id_fields = ['factura_contrato_id']

    def save_model(self, request, obj, form, change):

            # OBTENEMOS EL XML DEL POST Y LO PARSEAMOS
        xmlDoc = parse(obj.factura_xml)

        # OBTENEMOS LA RAIZ PRINCIPAL DEL CFDI Y LO ASIGNAMOS A LA VARIABLE
        raiz = xmlDoc.getElementsByTagName("cfdi:Comprobante")[0]

        # OBTENEMOS LA INFORMACION EN EL NODO PRINCIPAL
        TOTAL = raiz.attributes["Total"].value

        # OBTENEMOS TODOS LOS ARRAY DEL NODO PRINCIPAL
        nodos_total = raiz.childNodes

        # NOS UBICAMOS EN EL NODO DE INPUESTOS EN EL INDICE 3
        impuestos = nodos_total[3].childNodes

        # OBTENEMOS LAS RETENCIONES EN EL NODO DEL INDICE 0
        retenciones = impuestos[0].childNodes
        isr_retenido = retenciones[0].attributes["Importe"].value
        iva_retenido = retenciones[1].attributes["Importe"].value

        # OBTENEMOS TODOS LOS ELEMENTOS DE TRASLADOS
        traslados = impuestos[1].childNodes
        iva_trasladado = traslados[0].attributes["Importe"].value

        print(obj.factura_tipo)

        if obj.factura_tipo == 1:  # ES PERSONA FISICA
            obj.factura_monto_total = TOTAL
            obj.factura_iva_trasladado = iva_trasladado

        else:  # PERSONA MORAL
            obj.factura_monto_total = TOTAL
            obj.factura_iva_trasladado = iva_trasladado
            obj.factura_iva_retenido = iva_retenido
            obj.factura_isr_retenido = isr_retenido

        super(FacturaConfig, self).save_model(request, obj, form, change)


#####################################################################################################


# Register your models here.
admin.site.register(Proveedor, ProveedorConfig)
admin.site.register(Contrato, ContratoConfig)
admin.site.register(Factura, FacturaConfig)
admin.site.register(Pago)
admin.site.register(Complemento)
