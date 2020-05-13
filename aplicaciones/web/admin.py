from django.contrib import admin

from aplicaciones.web.models import *

class ConfigCorreos(admin.ModelAdmin):
    list_display = ('corr_nombre', 
                    'corr_email',
                    'corr_telefono',
                    'corr_asunto',
                    'corr_mensaje',
                    'corr_depo',
                    'corr_crado',)
    list_filter = ['corr_depo', 'corr_crado']
class ConfigRegistro(admin.ModelAdmin):
    list_display = ('re_nombre', 
                    're_apellidos',
                    're_correo',
                    're_telefono',
                    're_evento',
                    're_creado',
                    )
    list_filter = ['re_evento', 're_creado']


class ConfigPostulate(admin.ModelAdmin):
    list_display = ('pos_vacante', 
                    'pos_nombre',
                    'pos_correo',
                    'pos_telefono',
                    'pos_cv',
                    'pos_creacion',
                    )
    list_filter = ['pos_vacante', 'pos_creacion']


class ConfigCompraWeb(admin.ModelAdmin):
    list_display = ('cw_id', 
                    'cw_fecha',
                    'cliente_str',
                    'cw_status',
                    'domicilio',
                    'cw_numero_venta',
                    'cw_numero_factura',
                    'cw_tipo_pago',
                    )
    list_filter = ['cw_fecha', 'cw_status']
    search_fields = ['cw_id', 'cw_cliente__rfc']
    readonly_fields = ('domicilio', 'cw_tipo_pago', 'cw_status', 'cliente_str')
    exclude = ('cw_domicilio','cw_cliente')
# Register your models here.
admin.site.register(Departamento)
admin.site.register(CorreoCco, ConfigCorreos)
admin.site.register(Evento)
admin.site.register(RegistroExpo, ConfigRegistro)
admin.site.register(Marca)
admin.site.register(Catalagos)
admin.site.register(Promocion)

admin.site.register(Vacante)
admin.site.register(Postulacion, ConfigPostulate)
admin.site.register(CompraWeb, ConfigCompraWeb)