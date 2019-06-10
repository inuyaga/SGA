from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from aplicaciones.pago_proveedor.models import Proveedor
from aplicaciones.pedidos.models import Pedido

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

    contex = {
    'usuario': request.user,
    'pedido': Pedido.objects.filter(pedido_fecha_pedido__range=(start_date,end_date)).count(),
    }
    return render(request, 'index/principal.html', contex)

@login_required(login_url='/login/')
def err_permisos(request):
    contex = {
    'productos': 'productos',
    'usuario': request.user,
    }
    return render(request, 'index/error_permisos.html', contex)