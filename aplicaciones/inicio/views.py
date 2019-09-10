from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from aplicaciones.pago_proveedor.models import Proveedor
from aplicaciones.pedidos.models import Pedido, Detalle_pedido
from django.db.models import Sum, Q, F, Max

# Create your views here.
@login_required(login_url='/login/')
def inicio(request):
    from datetime import datetime, date
    import calendar
    today = datetime.now()
    # CONSULTAMOS CUAL ES EL ULTIMO DIA DEL MES ACTUAL
    last_day=calendar.monthrange(today.year, today.month)[1]
    # INICIALIZAMOS LA FECHA INICIAL
    start_date = datetime(today.year, today.month, 1) 
    # INICIALIZAMOS LA FECHA FINAL
    end_date = datetime(today.year, today.month, last_day)
 
    

    pedidos_list=Detalle_pedido.objects.filter(detallepedido_pedido_id__pedido_fecha_pedido__range=(start_date,end_date)).exclude(Q(detallepedido_pedido_id__pedido_status=3)|Q(detallepedido_pedido_id__pedido_status=1)).aggregate(total=Sum(F('detallepedido_cantidad')*F('detallepedido_precio')))

    query_group=Detalle_pedido.objects.filter(detallepedido_pedido_id__pedido_fecha_pedido__range=(start_date,end_date)).exclude(Q(detallepedido_pedido_id__pedido_status=3)|Q(detallepedido_pedido_id__pedido_status=1)).values('detallepedido_pedido_id__pedido_id_depo__departamento_id_sucursal__sucursal_nombre').order_by('detallepedido_pedido_id__pedido_id_depo__departamento_id_sucursal').annotate(suma=Sum(F('detallepedido_cantidad')*F('detallepedido_precio')))
    ped_pendientes=Pedido.objects.filter(pedido_fecha_pedido__range=(start_date,end_date), pedido_status=1).count()

    # QUERY FILTRADO Y AGRUPADO PARA SABER DETALLE DE GASTO POR MES EN EL AÑO ACTUAL
    query_gasto_mensual=Detalle_pedido.objects.values('detallepedido_pedido_id__pedido_fecha_pedido__month').filter(detallepedido_pedido_id__pedido_fecha_pedido__range=(datetime(today.year, 1, 1),datetime(today.year, 12, 31))).exclude(Q(detallepedido_pedido_id__pedido_status=3)|Q(detallepedido_pedido_id__pedido_status=1)).annotate(total=Sum(F('detallepedido_cantidad')*F('detallepedido_precio'))).order_by('detallepedido_pedido_id__pedido_fecha_pedido__month')
    maximo=0
    maximo_gasto={}
    for item in query_group:
        if item['suma'] > maximo:
            maximo=item['suma']
            maximo_gasto={'sucursal':item['detallepedido_pedido_id__pedido_id_depo__departamento_id_sucursal__sucursal_nombre'], 'gasto':item['suma']}
    
    contex = { 
    'usuario': request.user, 
    'total_mes': pedidos_list['total'],
    'ped_pendientes': ped_pendientes,
    'total_gatos_suc2': query_group, 
    'maximo_gasto': maximo_gasto,
    'pedido': Pedido.objects.filter(pedido_fecha_pedido__range=(start_date,end_date), pedido_status=2).count(),
    'pedidos_anual': query_gasto_mensual,
    }
    return render(request, 'index/principal.html', contex)

@login_required(login_url='/login/')
def err_permisos(request):
    contex = {
    'productos': 'productos',
    'usuario': request.user,
    }
    return render(request, 'index/error_permisos.html', contex)