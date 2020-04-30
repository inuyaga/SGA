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