from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView
from aplicaciones.empresa.models import Cliente
from aplicaciones.expo.models import AsignacionMarca, VentaExpo, Detalle_venta, TIPO_VENTA
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

class SelectCienteView(TemplateView):
    template_name = "expo/select_cliente.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Buscar=self.request.GET.get('Buscar')
        if Buscar != None:
            context['cliente_list']=Cliente.objects.filter(Q(cli_clave=Buscar) | Q(cli_nombre__icontains=Buscar))
        return context

class VentaView(TemplateView):
    template_name = "expo/ventalist.html"
    tipo_venta=0
    no_venta=0

    def dispatch(self, *args, **kwargs):      
        cliente=self.request.GET.get('cleint')   
        tipo_vent=self.request.GET.get('tip')

        if self.request.GET.get('end') != None:
            VentaExpo.objects.filter(Venta_ID=self.request.GET.get('venta')).update(venta_e_status=True)
            url=reverse('expo:selec_cliente')
            return redirect(url)
        
        if self.request.GET.get('venta') == None:
            obj=VentaExpo(
            venta_e_cliente_id=cliente,
            venta_e_creado=self.request.user,
            venta_e_tipo=tipo_vent,
            )
            obj.save()
            url=reverse('expo:venta')
            url = "{}?cleint={}&tip={}&venta={}".format(url, cliente, tipo_vent, obj.Venta_ID)
            return redirect(url)
        return super(VentaView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        venta=self.request.GET.get('venta')
        tip=self.request.GET.get('tip')
        try:
            asignacion=AsignacionMarca.objects.get(am_user=self.request.user)
            filtro=asignacion.am_marca.values_list('marca_id_marca')
        except ObjectDoesNotExist:
            filtro=[]
            messages.warning(self.request, 'Es necesario que se le asigne una marca al usuario "'+ str(self.request.user) + '" posteriormente actualice la pagina')
        
        context['productos_list']=Producto.objects.filter(producto_marca__in=filtro, tipo_producto=tip)
        sum_detalle=Detalle_venta.objects.filter(detalle_venta=venta).aggregate(total=Sum(F('detalle_cantidad')*F('detalle_precio'), output_field=FloatField()))['total']
        context['total_venta']=round(sum_detalle, 3) if sum_detalle != None else sum_detalle
          
        return context
    def post(self, request, *args, **kwargs):
        cliente=self.request.POST.get('cleint')   
        tipo_vent=self.request.POST.get('tip')

        venta=self.request.POST.get('no_venta')
        cantidad=self.request.POST.get('cantidad')
        producto=self.request.POST.get('producto')

        # PROCESO DE VENTA
        obj_producto=Producto.objects.get(producto_codigo=producto)

        obj_detalle_venta=Detalle_venta(
            detalle_venta_id = venta,
            detalle_producto_id = obj_producto,
            detalle_cantidad = cantidad,
            detalle_precio = obj_producto.producto_precio,
        )
        obj_detalle_venta.save()
        url=reverse('expo:venta')
        url = "{}?cleint={}&tip={}&venta={}".format(url, cliente, tipo_vent, venta) 
        messages.success(self.request, 'Agregado Correctamente.')
        return redirect(url)


class VentaList(ListView):
    template_name = "expo/ventas.html"
    model=VentaExpo
    paginate_by = 200 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        urls_formateada = self.request.GET.copy()
        if 'page' in urls_formateada:
            del urls_formateada['page']
        context['urls_formateada'] = urls_formateada
        
        context['Clientes'] = VentaExpo.objects.values('venta_e_cliente__cli_clave').annotate(dcount=Count('venta_e_cliente__cli_clave')).order_by('venta_e_cliente__cli_clave')
        context['tipo_venta'] = TIPO_VENTA
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        venta_e_fecha_pedido_init=self.request.GET.get('venta_e_fecha_pedido_init')
        venta_e_fecha_pedido_end=self.request.GET.get('venta_e_fecha_pedido_end')
        venta_e_cliente=self.request.GET.get('venta_e_cliente')
        venta_e_status=self.request.GET.get('venta_e_status')
        venta_e_tipo=self.request.GET.get('venta_e_tipo')

        if venta_e_fecha_pedido_init != None and venta_e_fecha_pedido_init != "":
            if venta_e_fecha_pedido_end != None and venta_e_fecha_pedido_end != "":
                queryset = queryset.filter(venta_e_fecha_pedido__range=(venta_e_fecha_pedido_init, venta_e_fecha_pedido_end))
        
        if venta_e_cliente != None and venta_e_cliente != "":
            queryset = queryset.filter(venta_e_cliente__cli_clave=venta_e_cliente)
        if venta_e_status != None and venta_e_status != "":
            queryset = queryset.filter(venta_e_status=venta_e_status)
        if venta_e_tipo != None and venta_e_tipo != "":
            queryset = queryset.filter(venta_e_tipo=venta_e_tipo)

        return queryset


class VentaDelete(DeleteView):
    model = VentaExpo
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('expo:venta_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

    @method_decorator(permission_required('expo.delete_ventaexpo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class VentaExpoUpdate(UpdateView):
    model = VentaExpo 
    template_name = "expo/formulario.html"
    form_class = VentaExpoForm
    success_url = reverse_lazy('expo:venta_list')

    @method_decorator(permission_required('expo.change_ventaexpo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class DetalleVentaList(ListView):
    template_name = "expo/detalleventas.html"
    model=Detalle_venta
    paginate_by = 200 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        urls_formateada = self.request.GET.copy()
        if 'page' in urls_formateada:
            del urls_formateada['page']
        context['urls_formateada'] = urls_formateada
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        venta_id=self.request.GET.get('vent')
        queryset = queryset.filter(detalle_venta=venta_id)
        return queryset


class DetalleVentaDelete(DeleteView):
    model = Detalle_venta
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('expo:detalle_vent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context
    def get_success_url(self):
        vent = self.request.GET.get('vent')
        url = self.success_url
        url = url + "?vent="+vent
        return url

            

    @method_decorator(permission_required('expo.delete_detalle_venta',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class ProductoListProveedor(ListView):
    model = Producto
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
        producto_categoria=self.request.GET.getlist('producto_categoria')
        tipo_producto=self.request.GET.getlist('tipo_producto')
        checkbox_visible=self.request.GET.getlist('checkbox_visible')
        Buscar=self.request.GET.get('Buscar')
        try:
            asignacion=AsignacionMarca.objects.get(am_user=self.request.user)
            filtro=asignacion.am_marca.values_list('marca_id_marca')
            queryset = queryset.filter(producto_marca__in=filtro)
            if len(tipo_producto) != 0:
                queryset=queryset.filter(tipo_producto__in=tipo_producto)
            if len(producto_categoria) != 0:
                queryset=queryset.filter(producto_categoria__in=producto_categoria)
            if len(checkbox_visible) != 0:
                queryset=queryset.filter(producto_visible__in=checkbox_visible)
            if Buscar != None:
                queryset=queryset.filter(Q(producto_codigo=Buscar) | Q(producto_nombre__icontains=Buscar))
        except ObjectDoesNotExist:
            queryset=queryset.none()
            messages.warning(self.request, 'Es necesario que se le asigne una marca al usuario "'+ str(self.request.user) + '" posteriormente actualice la pagina')
        return queryset

    @method_decorator(permission_required('expo.puede_ver_producto_expo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductoExpoEdit(UpdateView):
    model = Producto
    form_class = EditProductoExpoForm
    template_name = "expo/form_producto.html" 
    success_url = reverse_lazy('expo:producto_list_proveedor')

    @method_decorator(permission_required('expo.puede_editar_producto_expo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

        