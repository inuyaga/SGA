# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib import admin

# Register your models here.
from apps.admon_empresa.models import Empresa, Sucursal, Zona


class EmpresaInstanceInline(admin.TabularInline):
    model = Sucursal


class AdminSuc(admin.ModelAdmin):
    inlines = [EmpresaInstanceInline]


admin.site.register(Empresa, AdminSuc)
admin.site.register(Sucursal)
# admin.site.register(Zona)
