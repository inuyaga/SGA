from django.contrib import admin
from aplicaciones.pedidos.models import *
# Register your models here.
class LineaInstanceInline(admin.TabularInline):
    model = Linea
class SubcategoriaConfig(admin.ModelAdmin):
    inlines = [LineaInstanceInline]

class SubcategoriaInstanceInline(admin.TabularInline):
    model = Subcategoria
class AreaConfig(admin.ModelAdmin):
    inlines = [SubcategoriaInstanceInline]


class ProductoConfig(admin.ModelAdmin):
    filter_horizontal = ('producto_productos',) 

class GaleriaConfig(admin.ModelAdmin):
    list_display = ('ga_alt','show_img') 




admin.site.register(Area, AreaConfig)
admin.site.register(Subcategoria, SubcategoriaConfig)
admin.site.register(Galeria, GaleriaConfig)
