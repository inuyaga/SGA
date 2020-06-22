from aplicaciones.pedidos.models import Area
from aplicaciones.web.models import Evento, Detalle_Compra_Web
from django.db.models import Sum, F, FloatField
def load_menus(request):
    area = Area.objects.all()
    area_init = Area.objects.all()[:7]
    area_continue = Area.objects.all()[7:]
    items = {
        'area':area, 
        'area_init':area_init, 
        'area_continue':area_continue, 
    }
    return items

def shopin_car(request):
    items={}
    if request.user.is_authenticated:        
        producto_pre_compra = Detalle_Compra_Web.objects.filter(dcw_creado_por=request.user, dcw_status=False)
        conteo_pre_compra=Detalle_Compra_Web.objects.filter(dcw_creado_por=request.user, dcw_status=False).count()
        suma_pre_compra=Detalle_Compra_Web.objects.filter(dcw_creado_por=request.user, dcw_status=False).aggregate(suma_total=Sum(F('dcw_precio') * F('dcw_cantidad'), output_field=FloatField()))['suma_total'] or 0.00
        items={
            'conteo_pre_compra':conteo_pre_compra,
            'suma_pre_compra':round(suma_pre_compra, 2),
            'producto_pre_compra':producto_pre_compra,
        }
    return items