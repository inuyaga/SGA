from django.contrib import admin
from aplicaciones.expo.models import AsignacionMarca, AsignacionVendedor_a_Supervisor
# Register your models here.
class AsignacionMarcaConfigAdmin(admin.ModelAdmin):
    list_display = [
        'am_user',
        'marcas',
    ] 
    search_fields = [
        'am_user__username'
    ]

class AsignacionVendedor_a_SupervisorConfigAdmin(admin.ModelAdmin):
    list_display = [
        'avs_Supervisor',
        'vendedores',
    ]
    search_fields = [
        'avs_Supervisor__username'
    ]
admin.site.register(AsignacionMarca, AsignacionMarcaConfigAdmin)
admin.site.register(AsignacionVendedor_a_Supervisor, AsignacionVendedor_a_SupervisorConfigAdmin)