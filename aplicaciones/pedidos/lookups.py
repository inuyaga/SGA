from ajax_select import register, LookupChannel
from aplicaciones.pedidos.models import Producto

@register('productos_tags')
class TagsLookup(LookupChannel):

    model = Producto

    def get_query(self, q, request):
        return self.model.objects.filter(producto_visible=True,producto_codigo__icontains=q).order_by('producto_codigo')[:50]

    def format_item_display(self, item):
        filtering='<span class="tag">{}</span> <p>{}</p> <img src="/media/{}" alt="Producto img" height="42" width="42">'.format(item.producto_codigo,item.producto_nombre, item.producto_imagen)
        return filtering

@register('productos_tags_kits')
class TagsLookupKits(LookupChannel):

    model = Producto

    def get_query(self, q, request):
        return self.model.objects.filter(producto_es_kit=True,producto_codigo__icontains=q).order_by('producto_codigo')[:50]

    def format_item_display(self, item):
        filtering='<span class="tag">{}</span> <p>{}</p> <img src="/media/{}" alt="Producto img" height="42" width="42">'.format(item.producto_codigo,item.producto_nombre, item.producto_imagen)
        return filtering