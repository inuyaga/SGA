from django.contrib import admin
from aplicaciones.empresa.models import Empresa, Sucursal, Zona, Departamento, Pertenece_empresa
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class EmpresaInstanceInline(admin.TabularInline):
    model = Sucursal


class DepartamentoInstanceInline(admin.TabularInline):
    model = Departamento


class AdminSuc(admin.ModelAdmin):
    inlines = [EmpresaInstanceInline]


class Suc(admin.ModelAdmin):
    raw_id_fields = ('sucursal_id_zona',)
    inlines = [DepartamentoInstanceInline]
    list_display = ('sucursal_nombre', 'sucursal_id_zona',
                    'sucursal_empresa_id',)


class DepoConfig(admin.ModelAdmin):
    list_display = ('departamento_nombre',
                    'departamento_id_sucursal', 'nombre_empresa',)
    list_filter = ('departamento_id_sucursal',)


class ConfigEmpresa(admin.StackedInline):
    model = Pertenece_empresa
    can_delete = False
    verbose_name_plural = 'Pertenece a'
    raw_id_fields = ['pertenece_empresa', ]

# Define a new User admin


class UserAdminConfig(BaseUserAdmin):
    inlines = (ConfigEmpresa,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(Empresa, AdminSuc)
admin.site.register(Sucursal, Suc)
admin.site.register(Zona)
admin.site.register(Departamento, DepoConfig)
admin.site.register(User, UserAdminConfig)