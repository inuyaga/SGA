from django.shortcuts import render
from aplicaciones.empresa.models import Empresa
from django.contrib.auth.decorators import login_required
from aplicaciones.pago_proveedor.models import Proveedor
from aplicaciones.pedidos.models import Pedido, Detalle_pedido
from django.db.models import Sum, Q, F, Max
from aplicaciones.ods.models import Refaccion
from datetime import datetime, date
import calendar
from django.contrib import messages

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class InicioSga(LoginRequiredMixin, TemplateView):
    template_name = 'index/principal.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    def get_context_data(self, **kwargs):
        context = super(InicioSga, self).get_context_data(**kwargs)
        # DEFINIMOS VARIABLES DE CONSULTA GET
        init_pedido=self.request.GET.get('init_pedido')
        fin_pedido=self.request.GET.get('fin_pedido')
        pedido_empresa=self.request.GET.get('pedido_empresa')

        init_ods=self.request.GET.get('init_ods')
        fin_ods=self.request.GET.get('fin_ods')
        empresa_ods=self.request.GET.get('empresa_ods')

        ########################################################################

        today = datetime.now()
        # CONSULTAMOS CUAL ES EL ULTIMO DIA DEL MES ACTUAL
        last_day=calendar.monthrange(today.year, today.month)[1]
        # INICIALIZAMOS LA FECHA INICIAL
        start_date = datetime(today.year, today.month, 1) 
        # INICIALIZAMOS LA FECHA FINAL
        end_date = datetime(today.year, today.month, last_day)

        pedidos_list=Detalle_pedido.objects.filter(detallepedido_pedido_id__pedido_fecha_pedido__range=(start_date,end_date)).exclude(Q(detallepedido_pedido_id__pedido_status=3)|Q(detallepedido_pedido_id__pedido_status=1)).aggregate(total=Sum(F('detallepedido_cantidad')*F('detallepedido_precio')))


        if init_pedido == None or fin_pedido == None or pedido_empresa == None:
            query_group=Detalle_pedido.objects.filter(detallepedido_pedido_id__pedido_fecha_pedido__range=(start_date,end_date)).exclude(Q(detallepedido_pedido_id__pedido_status=3)|Q(detallepedido_pedido_id__pedido_status=1)).values('detallepedido_pedido_id__pedido_id_depo__departamento_id_sucursal__sucursal_nombre').order_by('detallepedido_pedido_id__pedido_id_depo__departamento_id_sucursal').annotate(suma=Sum(F('detallepedido_cantidad')*F('detallepedido_precio')))
            if pedido_empresa == None and (init_pedido != None and fin_pedido != None):
                messages.info(self.request, 'Elija una empresa')
        else:
            query_group=Detalle_pedido.objects.filter(detallepedido_pedido_id__pedido_id_depo__departamento_id_sucursal__sucursal_empresa_id=pedido_empresa,detallepedido_pedido_id__pedido_fecha_pedido__range=(init_pedido,fin_pedido)).exclude(Q(detallepedido_pedido_id__pedido_status=3)|Q(detallepedido_pedido_id__pedido_status=1)).values('detallepedido_pedido_id__pedido_id_depo__departamento_id_sucursal__sucursal_nombre').order_by('detallepedido_pedido_id__pedido_id_depo__departamento_id_sucursal').annotate(suma=Sum(F('detallepedido_cantidad')*F('detallepedido_precio')))
            context['init_pedido']=datetime.strptime(init_pedido, '%Y-%m-%d')
            context['fin_pedido']=datetime.strptime(fin_pedido, '%Y-%m-%d')
        
        ped_pendientes=Pedido.objects.filter(pedido_fecha_pedido__range=(start_date,end_date), pedido_status=1).count()

        # QUERY FILTRADO Y AGRUPADO PARA SABER DETALLE DE GASTO POR MES EN EL AÑO ACTUAL
        query_gasto_mensual=Detalle_pedido.objects.values('detallepedido_pedido_id__pedido_fecha_pedido__month').filter(detallepedido_pedido_id__pedido_fecha_pedido__range=(datetime(today.year, 1, 1),datetime(today.year, 12, 31))).exclude(Q(detallepedido_pedido_id__pedido_status=3)|Q(detallepedido_pedido_id__pedido_status=1)).annotate(total=Sum(F('detallepedido_cantidad')*F('detallepedido_precio'))).order_by('detallepedido_pedido_id__pedido_fecha_pedido__month')
        maximo=0
        maximo_gasto={}
        for item in query_group:
            if item['suma'] > maximo:
                maximo=item['suma']
                maximo_gasto={'sucursal':item['detallepedido_pedido_id__pedido_id_depo__departamento_id_sucursal__sucursal_nombre'], 'gasto':item['suma']}
        

        # QUERY PARA INFORMACION DE GASTOS DE REFACCIONES DE ORDENES DE SERVICIOS
        if init_ods == None or fin_ods == None or empresa_ods == None:
            gasto_refaccion_query_group=Refaccion.objects.filter(ref_add_fecha__range=(start_date,end_date)).values('ref_departamento__departamento_id_sucursal__sucursal_nombre').order_by('ref_departamento__departamento_id_sucursal').annotate(suma=Sum(F('ref_precio')*F('ref_cantidad')))
            if empresa_ods == None and (init_ods != None and fin_ods != None):
                messages.info(self.request, 'Elija una empresa')
        else:
            gasto_refaccion_query_group=Refaccion.objects.filter(ref_departamento__departamento_id_sucursal__sucursal_empresa_id=empresa_ods, ref_add_fecha__range=(init_ods,fin_ods)).values('ref_departamento__departamento_id_sucursal__sucursal_nombre').order_by('ref_departamento__departamento_id_sucursal').annotate(suma=Sum(F('ref_precio')*F('ref_cantidad')))
            context['init_ods']=datetime.strptime(init_ods, '%Y-%m-%d')
            context['fin_ods']=datetime.strptime(fin_ods, '%Y-%m-%d')
            


        context['list_empresas']=Empresa.objects.all()
        context['usuario']=self.request.user
        context['query_gasto_ods']=gasto_refaccion_query_group
        context['total_mes']=pedidos_list['total']
        context['ped_pendientes']=ped_pendientes
        context['total_gatos_suc2']=query_group
        context['maximo_gasto']=maximo_gasto
        context['pedido']=Pedido.objects.filter(pedido_fecha_pedido__range=(start_date,end_date), pedido_status=2).count()
        context['pedidos_anual']=query_gasto_mensual
        return context



@login_required(login_url='/login/')
def err_permisos(request):
    contex = {
    'productos': 'productos',
    'usuario': request.user,
    }
    return render(request, 'index/error_permisos.html', contex)