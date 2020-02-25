from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView
from aplicaciones.empresa.models import Cliente
from aplicaciones.expo.models import AsignacionMarca, VentaExpo, Detalle_venta, TIPO_VENTA, AsignacionVendedor_a_Supervisor
from aplicaciones.pedidos.models import Producto
from django.db.models import Q, Sum, F, FloatField, Count
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects

from aplicaciones.expo.forms import VentaExpoForm, EditProductoExpoForm
# Create your views here.

# import para generar xls
from openpyxl.styles import Font, Fill, Alignment
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from decimal import Decimal
class SelectCienteView(TemplateView):
    template_name = "expo/select_cliente.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Buscar = self.request.GET.get('Buscar')
        if Buscar != None:
            context['cliente_list'] = Cliente.objects.filter(
                Q(cli_clave=Buscar) | Q(cli_nombre__icontains=Buscar))
        return context


class VentaView(TemplateView):
    template_name = "expo/ventalist.html"
    tipo_venta = 0
    no_venta = 0

    def dispatch(self, *args, **kwargs):
        cliente = self.request.GET.get('cleint')
        tipo_vent = self.request.GET.get('tip')

        if self.request.GET.get('end') != None:
            VentaExpo.objects.filter(Venta_ID=self.request.GET.get(
                'venta')).update(venta_e_status=True)
            url = reverse('expo:selec_cliente')
            return redirect(url)

        if self.request.GET.get('venta') == None:
            obj = VentaExpo(
                venta_e_cliente_id=cliente,
                venta_e_creado=self.request.user,
                venta_e_tipo=tipo_vent,
            )
            obj.save()
            url = reverse('expo:venta')
            url = "{}?cleint={}&tip={}&venta={}".format(
                url, cliente, tipo_vent, obj.Venta_ID)
            return redirect(url)
        return super(VentaView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta = self.request.GET.get('venta')
        tip = self.request.GET.get('tip')
        try:
            asignacion = AsignacionMarca.objects.get(am_user=self.request.user)
            filtro = asignacion.am_marca.values_list('marca_id_marca')
        except ObjectDoesNotExist:
            filtro = []
            messages.warning(self.request, 'Es necesario que se le asigne una marca al usuario "' +
                             str(self.request.user) + '" posteriormente actualice la pagina')

        context['productos_list'] = Producto.objects.filter(producto_marca__in=filtro, tipo_producto=tip).order_by('producto_descripcion')
        sum_detalle = Detalle_venta.objects.filter(detalle_venta=venta).aggregate(total=Sum(F('detalle_cantidad')*F('detalle_precio'), output_field=FloatField()))['total']
        context['total_venta'] = round(sum_detalle, 3) if sum_detalle != None else sum_detalle

        return context

    def post(self, request, *args, **kwargs):
        from django.http import JsonResponse
        cliente = self.request.POST.get('cleint')
        tipo_vent = self.request.POST.get('tip')

        venta = self.request.POST.get('no_venta')
        cantidad = self.request.POST.get('cantidad')
        producto = self.request.POST.get('producto')

        # PROCESO DE VENTA
        obj_producto = Producto.objects.get(producto_codigo=producto)

        obj_detalle_venta = Detalle_venta(
            detalle_venta_id=venta,
            detalle_producto_id=obj_producto,
            detalle_cantidad=cantidad,
            detalle_precio=obj_producto.producto_precio,
        )
        obj_detalle_venta.save()

        sum_detalle = Detalle_venta.objects.filter(detalle_venta=venta).aggregate(total=Sum(F('detalle_cantidad')*F('detalle_precio'), output_field=FloatField()))['total']
        total_venta = round(sum_detalle, 3) if sum_detalle != None else sum_detalle
        data = {
            'producto': producto,
            'total_venta': total_venta,
        }
        return JsonResponse(data)
        


class VentaList(ListView):
    template_name = "expo/ventas.html"
    model = VentaExpo
    paginate_by = 200

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sum_detalle=0;
        urls_formateada = self.request.GET.copy()
        if 'page' in urls_formateada:
            del urls_formateada['page']
        context['urls_formateada'] = urls_formateada
        context['Clientes'] = VentaExpo.objects.values('venta_e_cliente__cli_clave').annotate(dcount=Count('venta_e_cliente__cli_clave')).order_by('venta_e_cliente__cli_clave')
        context['tipo_venta'] = TIPO_VENTA

        
        

        return context

    def get_queryset(self):
        from django.contrib.humanize.templatetags.humanize import intcomma
        queryset = super().get_queryset()
        sum_detalle=0
        if self.request.user.is_superuser == False:
            try:
                supervisor = AsignacionVendedor_a_Supervisor.objects.get(
                    avs_Supervisor=self.request.user)
                vendedores = supervisor.avs_vendedors.values_list('id')
                queryset = queryset.filter(
                    venta_e_creado__in=vendedores).order_by('venta_e_fecha_pedido')
            except ObjectDoesNotExist:
                queryset = queryset.none()
                messages.warning(self.request, 'Es necesario que se le asigne vendedores al usuario "' + str(
                    self.request.user) + '" posteriormente actualice la pagina')

        venta_e_fecha_pedido_init = self.request.GET.get('venta_e_fecha_pedido_init')
        venta_e_fecha_pedido_end = self.request.GET.get('venta_e_fecha_pedido_end')
        venta_e_cliente = self.request.GET.get('venta_e_cliente')
        venta_e_status = self.request.GET.get('venta_e_status')
        venta_e_tipo = self.request.GET.get('venta_e_tipo')
        Buscar = self.request.GET.get('Buscar')

        if venta_e_fecha_pedido_init != None and venta_e_fecha_pedido_init != "":
            if venta_e_fecha_pedido_end != None and venta_e_fecha_pedido_end != "":
                queryset = queryset.filter(venta_e_fecha_pedido__range=( venta_e_fecha_pedido_init, venta_e_fecha_pedido_end))
        if venta_e_cliente != None and venta_e_cliente != "":
            queryset = queryset.filter(venta_e_cliente__cli_clave=venta_e_cliente)
        if venta_e_status != None and venta_e_status != "":
            queryset = queryset.filter(venta_e_status=venta_e_status)
        if venta_e_tipo != None and venta_e_tipo != "":
            queryset = queryset.filter(venta_e_tipo=venta_e_tipo)
        if Buscar != None and Buscar != "":
            queryset = queryset.filter(Venta_ID=Buscar)

        
        for item in queryset:
            sum_detalle = sum_detalle + item.total_venta()
        
        suma= round(sum_detalle, 3) if sum_detalle != None else sum_detalle
        messages.info(self.request, "Total ventas ${}".format(intcomma(suma)))

        

        return queryset


class dowload_ventas_expo(TemplateView):
    def get(self, request, *args, **kwargs):
        wb = Workbook()
        ws = wb.active
        queryset = VentaExpo.objects.all()

        if request.user.is_superuser == False:
            try:
                supervisor = AsignacionVendedor_a_Supervisor.objects.get(
                    avs_Supervisor=request.user)
                vendedores = supervisor.avs_vendedors.values_list('id')
                queryset = queryset.filter(
                    venta_e_creado__in=vendedores).order_by('venta_e_fecha_pedido')
            except ObjectDoesNotExist:
                queryset = queryset.none()
        venta_e_fecha_pedido_init = request.GET.get(
            'venta_e_fecha_pedido_init')
        venta_e_fecha_pedido_end = request.GET.get('venta_e_fecha_pedido_end')
        venta_e_cliente = request.GET.get('venta_e_cliente')
        venta_e_status = request.GET.get('venta_e_status')
        venta_e_tipo = request.GET.get('venta_e_tipo')

        if venta_e_fecha_pedido_init != None and venta_e_fecha_pedido_init != "":
            if venta_e_fecha_pedido_end != None and venta_e_fecha_pedido_end != "":
                queryset = queryset.filter(venta_e_fecha_pedido__range=(
                    venta_e_fecha_pedido_init, venta_e_fecha_pedido_end))

        if venta_e_cliente != None and venta_e_cliente != "":
            queryset = queryset.filter(
                venta_e_cliente__cli_clave=venta_e_cliente)
        if venta_e_status != None and venta_e_status != "":
            queryset = queryset.filter(venta_e_status=venta_e_status)
        if venta_e_tipo != None and venta_e_tipo != "":
            queryset = queryset.filter(venta_e_tipo=venta_e_tipo)

        ws['A1'] = 'Ventas Expo'
        st = ws['A1']
        st.font = Font(size=14, b=True, color="004ee0")
        st.alignment = Alignment(horizontal='center')
        ws.merge_cells('A1:G1')
        ws.sheet_properties.tabColor = "1072BA"

        ws['A2'] = '##'
        ws['B2'] = 'Fecha'
        ws['C2'] = 'Actualizado'
        ws['D2'] = 'Cliente'
        ws['E2'] = 'Creador'
        ws['F2'] = 'Tipo'
        ws['G2'] = 'Total'
        cont = 3

        for item in queryset:
            ws.cell(row=cont, column=1).value = item.Venta_ID
            ws.cell(row=cont, column=2).value = item.venta_e_fecha_pedido
            ws.cell(row=cont, column=3).value = item.venta_e_actualizado
            ws.cell(row=cont, column=4).value = item.venta_e_cliente.cli_clave
            ws.cell(row=cont, column=5).value = str(item.venta_e_creado)
            ws.cell(row=cont, column=6).value = item.get_venta_e_tipo_display()
            ws.cell(row=cont, column=7).value = item.total_venta()
            ws.cell(row=cont, column=7).number_format = '#,##0'
            cont += 1

        ws["F"+str(cont)] = "TOTAL"
        ws["G"+str(cont)] = "=SUM(G3:G"+str(cont-1)+")"
        ws["G"+str(cont)].number_format = '#,##0'

        dims = {}
        for row in ws.rows:
            for cell in row:
                if cell.value:
                    if cell.row != 1:
                        dims[cell.column] = max(
                            (dims.get(cell.column, 0), len(str(cell.value))))

        for col, value in dims.items():
            ws.column_dimensions[get_column_letter(col)].width = value+1

        nombre_archivo = 'VENTAS_EXPO.xls'
        response = HttpResponse(content_type="application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response


class VentaDelete(DeleteView):
    model = VentaExpo
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('expo:venta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([
                                                                        self.object])
        context['deletable_objects'] = deletable_objects
        context['model_count'] = dict(model_count).items()
        context['protected'] = protected
        return context

    @method_decorator(permission_required('expo.delete_ventaexpo', reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class VentaExpoUpdate(UpdateView):
    model = VentaExpo
    template_name = "expo/formulario.html"
    form_class = VentaExpoForm
    success_url = reverse_lazy('expo:venta_list')

    @method_decorator(permission_required('expo.change_ventaexpo', reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class DetalleVentaList(ListView):
    template_name = "expo/detalleventas.html"
    model = Detalle_venta
    paginate_by = 200

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        urls_formateada = self.request.GET.copy()
        producto = self.request.GET.get('find_prod')
        if 'page' in urls_formateada:
            del urls_formateada['page']
    
        context['productos_list'] = Producto.objects.filter(producto_codigo=producto)
        
        
        context['urls_formateada'] = urls_formateada
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        venta_id = self.kwargs['pk']
        queryset = queryset.filter(detalle_venta=venta_id)
        return queryset

    
    def post(self, request, *args, **kwargs):

        venta = self.request.POST.get('no_venta')
        cantidad = self.request.POST.get('cantidad')
        producto = self.request.POST.get('producto')

        # PROCESO DE VENTA
        producto_obj=Producto.objects.get(producto_codigo=producto)
        venta_expo_obj = VentaExpo.objects.get(Venta_ID=venta)

        detalle_venta=Detalle_venta(
            detalle_venta = venta_expo_obj,
            detalle_producto_id = producto_obj,
            detalle_cantidad = cantidad,
            detalle_precio = producto_obj.producto_precio,
            )
        print(producto_obj.producto_precio)
        detalle_venta.save()
        url = reverse_lazy('expo:detalle_vent', kwargs = {'pk':venta})
        return redirect(url)



class DetalleVentaDelete(DeleteView):
    model = Detalle_venta
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('expo:detalle_vent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([
                                                                        self.object])
        context['deletable_objects'] = deletable_objects
        context['model_count'] = dict(model_count).items()
        context['protected'] = protected
        return context

    def get_success_url(self):
        vent = self.request.GET.get('vent')
        url = reverse_lazy('expo:detalle_vent', kwargs = {'pk':vent})
        return url



    @method_decorator(permission_required('expo.delete_detalle_venta', reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductoListProveedor(ListView):
    model = Producto
    ordering = ['producto_descripcion']
    template_name = "pedidos/producto/list_producto.html"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        urls_formateada = self.request.GET.copy()
        if 'page' in urls_formateada:
            del urls_formateada['page']
        context['urls_formateada'] = urls_formateada
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        producto_categoria = self.request.GET.getlist('producto_categoria')
        tipo_producto = self.request.GET.getlist('tipo_producto')
        checkbox_visible = self.request.GET.getlist('checkbox_visible')
        Buscar = self.request.GET.get('Buscar')
        try:
            asignacion = AsignacionMarca.objects.get(am_user=self.request.user)
            filtro = asignacion.am_marca.values_list('marca_id_marca')
            queryset = queryset.filter(producto_marca__in=filtro)
            if len(tipo_producto) != 0:
                queryset = queryset.filter(tipo_producto__in=tipo_producto)
            if len(producto_categoria) != 0:
                queryset = queryset.filter(
                    producto_categoria__in=producto_categoria)
            if len(checkbox_visible) != 0:
                queryset = queryset.filter(
                    producto_visible__in=checkbox_visible)
            if Buscar != None:
                queryset = queryset.filter(Q(producto_codigo=Buscar) | Q(
                    producto_nombre__icontains=Buscar))
        except ObjectDoesNotExist:
            queryset = queryset.none()
            messages.warning(self.request, 'Es necesario que se le asigne una marca al usuario "' + \
                             str(self.request.user) + '" posteriormente actualice la pagina')
        return queryset

    @method_decorator(permission_required('expo.puede_ver_producto_expo', reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductoExpoEdit(UpdateView):
    model = Producto
    form_class = EditProductoExpoForm
    template_name = "expo/form_producto.html"
    success_url = reverse_lazy('expo:producto_list_proveedor')

    @method_decorator(permission_required('expo.puede_editar_producto_expo', reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)




class dowload_venta_expo_ID(TemplateView):
    def get(self, request, *args, **kwargs):
        wb = Workbook()
        ws = wb.active
        VentaID = request.GET.get('vent')
        queryset = Detalle_venta.objects.filter(detalle_venta=VentaID)
        

        ws['A1'] = 'Detalle de venta N° {}'.format(VentaID)
        st = ws['A1']
        st.font = Font(size=14, b=True, color="004ee0")
        st.alignment = Alignment(horizontal='center')
        ws.merge_cells('A1:E1')
        ws.sheet_properties.tabColor = "1072BA"

        ws['A2'] = 'Producto'
        ws['B2'] = 'Descripción'
        ws['C2'] = 'Cantidad'
        ws['D2'] = 'Precio'
        ws['E2'] = 'Subtotal'
        cont = 3

        for item in queryset:
            ws.cell(row=cont, column=1).value = item.detalle_producto_id.producto_codigo
            ws.cell(row=cont, column=2).value = item.detalle_producto_id.producto_descripcion
            ws.cell(row=cont, column=3).value = item.detalle_cantidad
            ws.cell(row=cont, column=4).value = item.detalle_precio
            ws.cell(row=cont, column=5).value = item.subtotal()
            ws.cell(row=cont, column=5).number_format = '#,##0'
            cont += 1

        ws["D"+str(cont)] = "TOTAL"
        ws["E{}".format(cont)] = "=SUM(E3:E{})".format(cont-1)
        ws["E"+str(cont)].number_format = '#,##0'

        dims = {}
        for row in ws.rows:
            for cell in row:
                if cell.value:
                    if cell.row != 1:
                        dims[cell.column] = max(
                            (dims.get(cell.column, 0), len(str(cell.value))))

        for col, value in dims.items():
            ws.column_dimensions[get_column_letter(col)].width = value+1

        nombre_archivo = 'venta_no_{}.xls'.format(VentaID)
        response = HttpResponse(content_type="application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response