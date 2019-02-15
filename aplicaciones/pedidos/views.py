from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects
from aplicaciones.pedidos.models import Area, Marca, Producto, Detalle_pedido, Pedido
from aplicaciones.pedidos.froms import AreaForm, MarcaForm, ProductoForm, PedidoForm
from aplicaciones.empresa.models import Pertenece_empresa
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F

from django.http import JsonResponse
# Create your views here.
# pylint: disable=no-member

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
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductoCompraList, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        codigo = request.POST.get('nombre')
        cantidad = request.POST.get('catidad')
        tipo_mensaje=True
        mensaje=''

        if float(cantidad) <= 0:
            mensaje='Ingrese un numero positivo por favor'
            tipo_mensaje=False
        else:
            empresa_pertenece = Pertenece_empresa.objects.get(pertenece_id_usuario=request.user)
            limite_gasto=empresa_pertenece.pertenece_empresa.departamento_limite_gasto
            suma_pedido=Detalle_pedido.objects.filter(detallepedido_creado_por=request.user, detallepedido_status=False).aggregate(suma_total=Sum(F('detallepedido_precio') * F('detallepedido_cantidad')))
            if suma_pedido['suma_total'] == None:
                suma_pedido['suma_total']=0

            producto = Producto.objects.get(producto_codigo=codigo)
            total=(producto.producto_precio * float(cantidad)) + suma_pedido['suma_total']


            if total <= limite_gasto:
                detalle_pedido=Detalle_pedido(
                detallepedido_producto_id_id=producto.producto_codigo,
                detallepedido_cantidad=cantidad,
                detallepedido_creado_por=request.user,
                detallepedido_precio=producto.producto_precio,
                )
                detalle_pedido.save()
                mensaje='Agregado Correctamente'
            else:
                tipo_mensaje=False
                mensaje='Supera el limite de gasto admitido de '+ str(limite_gasto)

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

class DetalleList(ListView):
    paginate_by = 10
    model = Detalle_pedido
    template_name = 'pedidos/listado_pre_pedido.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
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

def Crear_pedido_tienda(request):
    empresa_pertenece = Pertenece_empresa.objects.get(pertenece_id_usuario=request.user)
    departamento=empresa_pertenece.pertenece_empresa.departamento_id_depo

    pedido=Pedido(pedido_id_depo_id=departamento)
    pedido.save()
    Detalle_pedido.objects.filter(detallepedido_creado_por=request.user, detallepedido_status=False).update(detallepedido_pedido_id=pedido.pk, detallepedido_status=True)

    return redirect('pedidos:pedido_tienda')


class PedidoList(ListView):
    model = Pedido
    template_name = 'pedidos/pedido/pedido_admin.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(PedidoList, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Actualizar'
        context['usuario'] = self.request.user
        context['status'] = {1:'Creado', 2:'Aprobado', 3:'Rechazado',}
        return context

    def get_queryset(self):
        queryset = super(PedidoList, self).get_queryset()

        if self.request.method == "GET":
            status = self.request.GET.get('status')

            if status != None:
                queryset = queryset.filter(pedido_status=status)
        # if filter == '1':
        #     queryset = queryset.filter(contrato_autorizado=True)
        # elif filter== '2':
        #     queryset = queryset.filter(contrato_autorizado=False)
        # elif filter== '3':
        #     queryset = queryset.filter(contrato_autorizado=False)
        return queryset
    @method_decorator(permission_required('pedidos.view_pedido',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(PedidoList, self).dispatch(*args, **kwargs)

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
    @method_decorator(permission_required('pedidos.change_pedido',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(PedidoUpdate, self).dispatch(*args, **kwargs)


class PedidoListSucursal(ListView):
    model = Pedido
    template_name = 'pedidos/pedido/pedido_admin.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PedidoListSucursal, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Actualizar'
        context['usuario'] = self.request.user
        context['status'] = {1:'Creado', 2:'Aprobado', 3:'Rechazado',}
        return context

    def get_queryset(self):
        queryset = super(PedidoListSucursal, self).get_queryset()
        empresa_pertenece = Pertenece_empresa.objects.get(pertenece_id_usuario=self.request.user)
        departamento=empresa_pertenece.pertenece_empresa.departamento_id_depo
        return queryset.filter(pedido_id_depo=departamento)



# ---------------------------------------------------------------------------------------------------------