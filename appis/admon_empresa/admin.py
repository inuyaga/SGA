# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib import admin

# Register your models here.
from appis.admon_empresa.models import Empresa, Sucursal, Zona


class EmpresaInstanceInline(admin.TabularInline):
    model = Sucursal


class AdminSuc(admin.ModelAdmin):
    inlines = [EmpresaInstanceInline]


class Suc(admin.ModelAdmin):
    raw_id_fields = ('id_zona',)


admin.site.register(Empresa, AdminSuc)
admin.site.register(Sucursal, Suc)
admin.site.register(Zona)
