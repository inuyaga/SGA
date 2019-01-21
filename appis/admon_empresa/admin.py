# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib import admin

# Register your models here.
from appis.admon_empresa.models import Empresa, Sucursal, Zona, Departamento


class EmpresaInstanceInline(admin.TabularInline):
    model = Sucursal

class DepartamentoInstanceInline(admin.TabularInline):
    model = Departamento


class AdminSuc(admin.ModelAdmin):
    inlines = [EmpresaInstanceInline]


class Suc(admin.ModelAdmin):
    raw_id_fields = ('sucursal_id_zona',)
    inlines = [DepartamentoInstanceInline]
    list_display=('sucursal_nombre','sucursal_id_zona','sucursal_empresa_id',)

class DepoConfig(admin.ModelAdmin):
    list_display=('departamento_nombre', 'departamento_limite_gasto', 'departamento_id_sucursal', 'nombre_empresa',)
    list_filter=('departamento_id_sucursal',)


admin.site.register(Empresa, AdminSuc)
admin.site.register(Sucursal, Suc)
admin.site.register(Zona)
admin.site.register(Departamento, DepoConfig)
