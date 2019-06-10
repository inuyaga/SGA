from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, View
from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects
from aplicaciones.pedidos.models import Area, Marca, Producto, Detalle_pedido, Pedido, Configuracion_pedido
from aplicaciones.pedidos.froms import AreaForm, MarcaForm, ProductoForm, PedidoForm, ProductoKitForm, ConfigForm
from aplicaciones.empresa.models import Pertenece_empresa
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import ProtectedError

from django.http import JsonResponse

from aplicaciones.empresa.models import Departamento 
# Create your views here.
# pylint: disable=no-member
# pylint: disable = E1101

# VISTAS GENERICAS DE LA AREA
# ---------------------------------------------------------------------------------------------------------
class AreaCreate(CreateView):
    model = Area
    form_class = AreaForm
    template_name = "pedidos/area/area_create.html"
    success_url = reverse_lazy('pedidos:listar_area')

    def get_context_data(self, **kwargs):
        context = super(AreaCreate, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Crear'
        context['usuario'] = self.request.user
        return context

    @method_decorator(permission_required('pedidos.add_area',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(AreaCreate, self).dispatch(*args, **kwargs)
class AreaList(ListView):
    paginate_by = 20
    model = Area
    template_name='pedidos/area/area_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['usuario'] = self.request.user
        return context
    @method_decorator(permission_required('pedidos.view_area',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(AreaList, self).dispatch(*args, **kwargs)

class AreaUpdate(UpdateView): 
    model = Area
    form_class = AreaForm
    template_name = "pedidos/area/area_create.html"
    success_url = reverse_lazy('pedidos:listar_area')

    def get_context_data(self, **kwargs):
        context = super(AreaUpdate, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Actualizar'
        context['usuario'] = self.request.user
        return context

    @method_decorator(permission_required('pedidos.change_area',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(AreaUpdate, self).dispatch(*args, **kwargs)

class AreaDelete(DeleteView):
    model = Area
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('pedidos:listar_area')

    def get_context_data(self, **kwargs):
        context = super(AreaDelete, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Actualizar'
        context['usuario'] = self.request.user

        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

    @method_decorator(permission_required('pedidos.delete_area',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(AreaDelete, self).dispatch(*args, **kwargs)

# ---------------------------------------------------------------------------------------------------------

# VISTAS GENERICAS DE LA MARCAS
# ---------------------------------------------------------------------------------------------------------
class MarcaCreate(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = "pedidos/marca/marca_create.html"
    success_url = reverse_lazy('pedidos:listar_marca')

    def get_context_data(self, **kwargs):
        context = super(MarcaCreate, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Crear'
        context['usuario'] = self.request.user
        return context

    @method_decorator(permission_required('pedidos.add_marca',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(MarcaCreate, self).dispatch(*args, **kwargs)


class MarcaList(ListView):
    paginate_by = 20
    model = Marca
    template_name='pedidos/marca/marca_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['usuario'] = self.request.user
        return context
    @method_decorator(permission_required('pedidos.view_area',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(MarcaList, self).dispatch(*args, **kwargs)

class MarcaUpdate(UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = "pedidos/marca/marca_create.html"
    success_url = reverse_lazy('pedidos:listar_marca')

    def get_context_data(self, **kwargs):
        context = super(MarcaUpdate, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Actualizar'
        context['usuario'] = self.request.user
        return context

    @method_decorator(permission_required('pedidos.change_marca',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(MarcaUpdate, self).dispatch(*args, **kwargs)

class MarcaDelete(DeleteView):
    model = Marca
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('pedidos:listar_marca')

    def get_context_data(self, **kwargs):
        context = super(MarcaDelete, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Eliminar'
        context['usuario'] = self.request.user

        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

    @method_decorator(permission_required('pedidos.delete_area',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(MarcaDelete, self).dispatch(*args, **kwargs)
# ---------------------------------------------------------------------------------------------------------


# VISTAS GENERICAS DE LA PRODUCTOS
# ---------------------------------------------------------------------------------------------------------
class ProductoCreate(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "pedidos/producto/producto_create.html"
    success_url = reverse_lazy('pedidos:listar_producto')

    def get_context_data(self, **kwargs):
        context = super(ProductoCreate, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Crear'
        context['usuario'] = self.request.user
        return context

    @method_decorator(permission_required('pedidos.add_producto',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ProductoCreate, self).dispatch(*args, **kwargs)

class ProductokitCreate(CreateView):
    model = Producto
    form_class = ProductoKitForm
    template_name = "pedidos/producto/producto_create.html"
    success_url = reverse_lazy('pedidos:listar_producto')

    def get_context_data(self, **kwargs):
        context = super(ProductokitCreate, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Crear'
        context['usuario'] = self.request.user
        return context

    @method_decorator(permission_required('pedidos.add_producto',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ProductokitCreate, self).dispatch(*args, **kwargs)

class ProductoList(ListView):
    paginate_by = 20
    model = Producto
    template_name='pedidos/producto/list_producto.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['usuario'] = self.request.user
        return context

    @method_decorator(permission_required('pedidos.view_producto',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ProductoList, self).dispatch(*args, **kwargs)


class ProductoUpdate(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "pedidos/producto/producto_create.html"
    success_url = reverse_lazy('pedidos:listar_producto')

    def get_context_data(self, **kwargs):
        context = super(ProductoUpdate, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Actualizar'
        context['usuario'] = self.request.user
        return context

    @method_decorator(permission_required('pedidos.change_producto',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ProductoUpdate, self).dispatch(*args, **kwargs)

class ProductoKitUpdate(UpdateView):
    model = Producto
    form_class = ProductoKitForm
    template_name = "pedidos/producto/producto_create.html"
    success_url = reverse_lazy('pedidos:listar_producto')

    def get_context_data(self, **kwargs):
        context = super(ProductoKitUpdate, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Actualizar'
        context['usuario'] = self.request.user
        return context

    @method_decorator(permission_required('pedidos.change_producto',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ProductoKitUpdate, self).dispatch(*args, **kwargs)

class ProductoDelete(DeleteView): 
    model = Producto
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('pedidos:listar_producto')

    def get_context_data(self, **kwargs):
        context = super(ProductoDelete, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Eliminar'
        context['usuario'] = self.request.user

        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            contex = {
        'mns_producto': 'Este producto esta relacionado con una compra'
                        }
        return render(request, 'pagoproveedor/protecteError.html', contex)

    @method_decorator(permission_required('pedidos.delete_producto',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ProductoDelete, self).dispatch(*args, **kwargs)



class ProductoCompraList(ListView):
    paginate_by = 20
    model = Producto
    template_name='pedidos/compra_tiendas.html' 

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['usuario'] = self.request.user
        context['conteo'] = Detalle_pedido.objects.filter(detallepedido_creado_por=self.request.user, detallepedido_status=False).count()
        context['msn_empresa'] = None
        try:
            empresa_pertenece = Pertenece_empresa.objects.get(pertenece_id_usuario=self.request.user)
        except ObjectDoesNotExist as error:
            context['msn_empresa'] = 'Para poder hacer pedidos es nesesario que pertenesca a una empresa, ¡comuniquese con el administrador del sistema!'

        return context
    def get_queryset(self):
        from datetime import datetime, date
        import calendar
        queryset = super(ProductoCompraList, self).get_queryset()
        try:
            departamento=Pertenece_empresa.objects.get(pertenece_id_usuario=self.request.user)
            # ESTABLECEMOS LA FECHA ACTUAL
            today = datetime.now()
            # CONSULTAMOS CUAL ES EL ULTIMO DIA DEL MES ACTUAL
            last_day=calendar.monthrange(today.year, today.month)[1]
            # INICIALIZAMOS LA FECHA INICIAL
            start_date = datetime(today.year, today.month, 1)
            # INICIALIZAMOS LA FECHA FINAL
            end_date = datetime(today.year, today.month, last_day)

            tipo_pedido=self.kwargs.get('tipo')
            queryset = queryset.filter(producto_es_kit=False, producto_categoria=tipo_pedido)

            if tipo_pedido == 1:
                conteo_pedido=Pedido.objects.filter(pedido_tipo=tipo_pedido, pedido_id_depo=departamento.pertenece_empresa, pedido_fecha_pedido__range=(start_date,end_date)).count()
                if conteo_pedido > 0:
                    queryset=''
            if tipo_pedido == 2:
                conteo_pedido=Pedido.objects.filter(pedido_tipo=tipo_pedido, pedido_id_depo=departamento.pertenece_empresa, pedido_fecha_pedido__range=(start_date,end_date)).count()
                if conteo_pedido > 0:
                    queryset=''
            if tipo_pedido == 3:
                conteo_pedido=Pedido.objects.filter(pedido_tipo=tipo_pedido, pedido_id_depo=departamento.pertenece_empresa, pedido_fecha_pedido__range=(start_date,end_date)).count()
                if conteo_pedido > 0:
                    queryset=''

            return queryset
        except ObjectDoesNotExist as error:
            return queryset.filter(producto_es_kit=False, producto_categoria=self.kwargs.get('tipo'))        
        

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoCompraList, self).dispatch(request, *args, **kwargs)           


    def post(self, request, *args, **kwargs):
        from decimal import Decimal
        codigo = request.POST.get('nombre')
        cantidad = request.POST.get('catidad')
        tipo_mensaje=True 
        mensaje=''
        

        if Decimal(cantidad) <= 0:
            mensaje='Ingrese un numero positivo por favor'
            tipo_mensaje=False
        else: 
            tipo_pedido=self.kwargs.get('tipo')
            empresa_pertenece = Pertenece_empresa.objects.get(pertenece_id_usuario=request.user)
            producto = Producto.objects.get(producto_codigo=codigo)

            if tipo_pedido == 1:# PEDIDO DE TIPO DE LIMPIEZA
                # SE OBTINE EL LIMITE DE GASTOS DE CADA CASO
                limite_gasto=empresa_pertenece.pertenece_empresa.departamento_limite_limpieza

                suma_pedido=Detalle_pedido.objects.filter(detallepedido_creado_por=request.user, detallepedido_status=False, detallepedido_categoria=tipo_pedido).aggregate(suma_total=Sum(F('detallepedido_precio') * F('detallepedido_cantidad')))
                total=(Decimal(producto.producto_precio) * Decimal(cantidad)) + Decimal(Obtenernumero(suma_pedido['suma_total']))
                if total <= limite_gasto:
                    if producto.producto_kit:
                        queryset = Producto.objects.filter(producto__producto_codigo=producto.producto_codigo)
                        for producto_list in queryset:
                            GuardaDetallePedido(
                                producto_list.producto_codigo, 
                                cantidad, 
                                request.user, 
                                producto_list.producto_precio, 
                                producto_list.producto_categoria)
                        mensaje='Agregado Correctamente'
                    else:
                        GuardaDetallePedido(
                            producto.producto_codigo, 
                            cantidad, 
                            request.user, 
                            producto.producto_precio, 
                            producto.producto_categoria)
                        mensaje='Agregado Correctamente'
                    
                else:
                    tipo_mensaje=False
                    mensaje='Supera el limite de gasto admitido para limpieza '+ str(limite_gasto)
            elif tipo_pedido == 2:# PEDIDO DE TIPO DE PAPELERIA
                
                limite_gasto=empresa_pertenece.pertenece_empresa.departamento_limite_papeleria

                suma_pedido=Detalle_pedido.objects.filter(detallepedido_creado_por=request.user, detallepedido_status=False, detallepedido_categoria=tipo_pedido).aggregate(suma_total=Sum(F('detallepedido_precio') * F('detallepedido_cantidad')))
                total=(Decimal(producto.producto_precio) * Decimal(cantidad)) + Decimal(Obtenernumero(suma_pedido['suma_total']))
                if total <= limite_gasto:
                    if producto.producto_kit:
                        queryset = Producto.objects.filter(producto__producto_codigo=producto.producto_codigo)
                        for producto_list in queryset:
                            GuardaDetallePedido(
                                producto_list.producto_codigo, 
                                cantidad, 
                                request.user, 
                                producto_list.producto_precio, 
                                producto_list.producto_categoria)
                        mensaje='Agregado Correctamente'
                    else:
                        GuardaDetallePedido(
                            producto.producto_codigo, 
                            cantidad, 
                            request.user, 
                            producto.producto_precio, 
                            producto.producto_categoria)
                        mensaje='Agregado Correctamente'
                    
                else:
                    tipo_mensaje=False
                    mensaje='Supera el limite de gasto admitido para papeleria '+ str(limite_gasto)
            elif tipo_pedido == 3:# PEDIDO DE TIPO VENTA TIENDA
                
                limite_gasto=empresa_pertenece.pertenece_empresa.departamento_limite_venta

                suma_pedido=Detalle_pedido.objects.filter(detallepedido_creado_por=request.user, detallepedido_status=False, detallepedido_categoria=tipo_pedido).aggregate(suma_total=Sum(F('detallepedido_precio') * F('detallepedido_cantidad')))
                total=(Decimal(producto.producto_precio) * Decimal(cantidad)) + Decimal(Obtenernumero(suma_pedido['suma_total']))
                if total <= limite_gasto:
                    if producto.producto_kit:
                        queryset = Producto.objects.filter(producto__producto_codigo=producto.producto_codigo)
                        for producto_list in queryset:
                            GuardaDetallePedido(
                                producto_list.producto_codigo, 
                                cantidad, 
                                request.user, 
                                producto_list.producto_precio, 
                                producto_list.producto_categoria)
                        mensaje='Agregado Correctamente'
                    else:
                        GuardaDetallePedido(
                            producto.producto_codigo, 
                            cantidad, 
                            request.user, 
                            producto.producto_precio, 
                            producto.producto_categoria)
                        mensaje='Agregado Correctamente'
                    
                else:
                    tipo_mensaje=False
                    mensaje='Supera el limite de gasto admitido para consumo venta '+ str(limite_gasto)

        pedido_conteo=Detalle_pedido.objects.filter(detallepedido_creado_por=request.user, detallepedido_status=False).count()
        json = JsonResponse(
            {
                'content':{
                    'mensaje': mensaje,
                    'conteo': pedido_conteo,
                    'tipo_mensaje': tipo_mensaje,
                }
            }
        )

        return json

def GuardaDetallePedido(codigo, cantidad, creado_por, precio, categoria):
    detalle_pedido=Detalle_pedido(
    detallepedido_producto_id_id=codigo,
    detallepedido_cantidad=cantidad,
    detallepedido_creado_por=creado_por,
    detallepedido_precio=precio,
    detallepedido_categoria=categoria,
    )
    detalle_pedido.save()

def Obtenernumero(numero):
    if numero == None:
        return 0
    else:
        return numero

class DetalleList(ListView):  
    paginate_by = 10
    model = Detalle_pedido
    template_name = 'pedidos/listado_pre_pedido.html' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conteo'] = Detalle_pedido.objects.filter(detallepedido_creado_por=self.request.user, detallepedido_status=False).count()
        context['usuario'] = self.request.user
        context['Limpieza'] = Detalle_pedido.objects.filter(detallepedido_creado_por=self.request.user, detallepedido_status=False, detallepedido_categoria=1)
        context['Papeleria'] = Detalle_pedido.objects.filter(detallepedido_creado_por=self.request.user, detallepedido_status=False, detallepedido_categoria=2)
        context['Venta'] = Detalle_pedido.objects.filter(detallepedido_creado_por=self.request.user, detallepedido_status=False, detallepedido_categoria=3)
        return context
    def get_queryset(self):
        queryset = super(DetalleList, self).get_queryset()
        return queryset.filter(detallepedido_creado_por=self.request.user, detallepedido_status=False)

class DetalleDelete(DeleteView):
    model = Detalle_pedido
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('pedidos:pedido_tienda_listado')
    def get_context_data(self, **kwargs):
        context = super(DetalleDelete, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Eliminar'
        context['usuario'] = self.request.user

        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

# def Crear_pedido_tienda(request): 
#     empresa_pertenece = Pertenece_empresa.objects.get(pertenece_id_usuario=request.user)
#     departamento=empresa_pertenece.pertenece_empresa.departamento_id_depo
    
#     pedido=Pedido(pedido_id_depo_id=departamento)
#     pedido.save()
#     Detalle_pedido.objects.filter(detallepedido_creado_por=request.user, detallepedido_status=False).update(detallepedido_pedido_id=pedido.pk, detallepedido_status=True)

#     return redirect('pedidos:pedido_tienda')


class Crear_pedido_tiendaView(View):
    def get(self, request, *args, **kwargs):
        empresa_pertenece = Pertenece_empresa.objects.get(pertenece_id_usuario=request.user)
        departamento=empresa_pertenece.pertenece_empresa.departamento_id_depo
        if self.kwargs.get('tipo') == 1:
            pedido=Pedido(pedido_id_depo_id=departamento, pedido_tipo=1)
            pedido.save()
            Detalle_pedido.objects.filter(detallepedido_creado_por=request.user, detallepedido_status=False, detallepedido_categoria=1).update(detallepedido_pedido_id=pedido.pk, detallepedido_status=True)
        elif self.kwargs.get('tipo') == 2:
            pedido=Pedido(pedido_id_depo_id=departamento, pedido_tipo=2)
            pedido.save()
            Detalle_pedido.objects.filter(detallepedido_creado_por=request.user, detallepedido_status=False, detallepedido_categoria=2).update(detallepedido_pedido_id=pedido.pk, detallepedido_status=True)
        elif self.kwargs.get('tipo') == 3:
            pedido=Pedido(pedido_id_depo_id=departamento, pedido_tipo=3)
            pedido.save()
            Detalle_pedido.objects.filter(detallepedido_creado_por=request.user, detallepedido_status=False, detallepedido_categoria=3).update(detallepedido_pedido_id=pedido.pk, detallepedido_status=True)

        return redirect('pedidos:pedido_tienda_listado') 

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')


class PedidoList(ListView): 
    model = Pedido
    template_name = 'pedidos/pedido/pedido_admin.html'
    ordering = ['pedido_id_pedido']
    def get_context_data(self, **kwargs):
        context = super(PedidoList, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Actualizar'
        context['usuario'] = self.request.user 
       
        return context

    def get_queryset(self):
        from django.utils.dateparse import parse_datetime
        import pytz
        queryset = super(PedidoList, self).get_queryset()
        status = self.request.GET.get('status')
        inicio = self.request.GET.get('inicio')
        fin = self.request.GET.get('fin')      

        if status != None:
            if status == '0':
                pass
            else:
                queryset = queryset.filter(pedido_status=status)
        else: 
            queryset = queryset.filter(pedido_status=1)

        if inicio != None and fin != None:            
            if inicio != '' and fin != '':
                queryset=Pedido.objects.filter(pedido_fecha_pedido__range=(inicio, fin))
        return queryset
    @method_decorator(permission_required('pedidos.view_pedido',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(PedidoList, self).dispatch(*args, **kwargs)

class dowload_pedido_detalles(TemplateView):
    def get(self, request , *args, **kwargs):
        from openpyxl.styles import Font, Fill, Alignment
        from django.http import HttpResponse
        from openpyxl import Workbook
        from openpyxl.utils import get_column_letter
        from decimal import Decimal
        wb = Workbook()
        ws=wb.active
        id_pedido=self.kwargs.get('pk')
        ped = Pedido.objects.get(pedido_id_pedido=id_pedido)
        query = Departamento.objects.get(departamento_id_depo=ped.pedido_id_depo.departamento_id_depo)
        nombre_sucursal = query.departamento_id_sucursal

        ws['A1'] = 'Detalle Pedido '+str(nombre_sucursal)+' N°'+ str(id_pedido)
        st=ws['A1']
        st.font = Font(size=14, b=True, color="004ee0")
        st.alignment = Alignment(horizontal='center')
        ws.merge_cells('A1:F1')
        ws.sheet_properties.tabColor = "1072BA"

        ws['A2'] = 'Producto'
        ws['B2'] = 'Descripcion'
        ws['C2'] = 'Departamento'
        ws['D2'] = 'Cantidad'
        ws['E2'] = 'Precio'
        ws['F2'] = 'Total'
        cont = 3
        detalle=Detalle_pedido.objects.filter(detallepedido_pedido_id=id_pedido)
        for cto in detalle:
            ws.cell(row=cont, column=1).value = str(cto.detallepedido_producto_id.producto_codigo)
            ws.cell(row=cont, column=2).value = str(cto.detallepedido_producto_id.producto_descripcion)
            ws.cell(row=cont, column=3).value = str(cto.detallepedido_pedido_id.pedido_id_depo)
            ws.cell(row=cont, column=4).value = cto.detallepedido_cantidad
            ws.cell(row=cont, column=5).value = cto.detallepedido_precio
            ws.cell(row=cont, column=6).value = (Decimal(cto.detallepedido_cantidad) * Decimal(cto.detallepedido_precio))
            ws.cell(row=cont, column=6).number_format = '#,##0'
            cont += 1

        ws["F"+str(cont)] = "=SUM(F3:F"+str(cont-1)+")"
        ws["F"+str(cont)].number_format = '#,##0'

        dims = {}
        for row in ws.rows:
            for cell in row:
                if cell.value:
                    if cell.row != 1:
                        dims[cell.column] = max((dims.get(cell.column, 0), len(str(cell.value))))

        for col, value in dims.items():
            ws.column_dimensions[get_column_letter(col)].width = value+1



        nombre_archivo='detalle_pedido_'+str(id_pedido)+'.xls'
        response = HttpResponse(content_type="application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition']=content
        wb.save(response)
        return response

class PedidoUpdate(UpdateView): 
    model = Pedido
    form_class = PedidoForm 
    template_name = 'pedidos/pedido/pedido_create.html'
    success_url = reverse_lazy('pedidos:pedidos_list')

    def get_context_data(self, **kwargs):
        context = super(PedidoUpdate, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Actualizar'
        context['usuario'] = self.request.user
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        if form.instance.pedido_status == 2:
            self.object.pedido_autorizo=self.request.user
        elif form.instance.pedido_status == 3:
            self.object.pedido_rechazado=self.request.user
            Detalle_pedido.objects.filter(detallepedido_pedido_id=self.kwargs.get('pk')).update(detallepedido_status=False)
        return super().form_valid(form)
    @method_decorator(permission_required('pedidos.change_pedido',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(PedidoUpdate, self).dispatch(*args, **kwargs)


class PedidoListSucursal(ListView): 
    model = Pedido
    template_name = 'pedidos/pedido/pedido_admin.html'
    ordering = ['pedido_id_pedido']

    def get_context_data(self, **kwargs):
        context = super(PedidoListSucursal, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Actualizar'
        context['usuario'] = self.request.user
        return context

    def get_queryset(self):
        queryset = super(PedidoListSucursal, self).get_queryset()
        queryset_init=queryset
        # OBTENER A QUE SUCURSAL PERTENECE EL USUARIO
        pertenece=Pertenece_empresa.objects.get(pertenece_id_usuario=self.request.user)
        # FILTRAMOS EN QUERY PARA MOSTRAR
        
        status = self.request.GET.get('status')
        inicio = self.request.GET.get('inicio')
        fin = self.request.GET.get('fin')

        if status != None:
            if status == '0':
                queryset = queryset_init.filter(pedido_id_depo=pertenece.pertenece_empresa)
            else:
                queryset = queryset_init.filter(pedido_status=status, pedido_id_depo=pertenece.pertenece_empresa)
        else:
            
            if inicio != None and fin != None:            
                if inicio != '' and fin != '':
                    queryset=Pedido.objects.filter(pedido_id_depo=pertenece.pertenece_empresa, pedido_fecha_pedido__range=(inicio, fin))
            else:
                queryset=queryset.filter(pedido_id_depo=pertenece.pertenece_empresa, pedido_status=1)

        return queryset
 
class SelectTipoCompraView(TemplateView):
    template_name = "pedidos/select_compra.html"
    def get_context_data(self, **kwargs):
        import datetime
        context = super(SelectTipoCompraView, self).get_context_data(**kwargs)
        context['conf'] = Configuracion_pedido.objects.all()
        context['conteo'] = Detalle_pedido.objects.filter(detallepedido_creado_por=self.request.user, detallepedido_status=False).count()
        hoy=datetime.datetime.now()
        for config in context['conf']:
            if config.conf_fecha_inicio <= hoy.date() and config.conf_fecha_fin >= hoy.date():
                context['estado_rango_fechas']=True  
        return context 


class ConfigPedidoListView(ListView):
    model = Configuracion_pedido
    template_name = "pedidos/pedido/config_list.html"

class ConfigPedidoCreate(CreateView):
    model = Configuracion_pedido
    form_class = ConfigForm 
    template_name = "pedidos/pedido/conf_create.html"
    success_url = reverse_lazy('pedidos:pedido_config')
class ConfigPedidoUpdate(UpdateView):
    model = Configuracion_pedido
    form_class = ConfigForm 
    template_name = "pedidos/pedido/conf_create.html"
    success_url = reverse_lazy('pedidos:pedido_config')








# ---------------------------------------------------------------------------------------------------------