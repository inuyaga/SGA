from ajax_select import register, LookupChannel
from aplicaciones.empresa.models import Cliente

@register('ClientesVentasExpo')
class TagsLookup(LookupChannel):

    model = Cliente

    def get_query(self, q, request):
        return self.model.objects.filter(cli_clave__icontains=q).order_by('cli_clave')[:50]

    def format_item_display(self, item):
        filtering='<div class="alert alert-primary" role="alert">{}</div>'.format(item.cli_clave)
        return filtering

