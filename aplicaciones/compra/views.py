from django.shortcuts import render
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, View, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.urls import reverse, reverse_lazy
from aplicaciones.compra.models import Compra
from aplicaciones.compra.forms import CompraForm,CompraEditForm
from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects
# Create your views here.
class CompraList(ListView):
    model= Compra
    form_class = CompraForm
    template_name='compras/listaCompras.html'
    ordering = ['-compra_id']
    @method_decorator(permission_required('compra.view_compra',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CompraList, self).dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CompraCreate(CreateView):
    model= Compra
    form_class = CompraForm
    template_name='compras/crearcompra.html'
    success_url=reverse_lazy("compra:listacompras")

    @method_decorator(permission_required('compra.add_compra',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CompraCreate, self).dispatch(*args, **kwargs)

class CompraUpdate(UpdateView):
    model= Compra
    form_class = CompraForm
    template_name='compras/crearcompra.html'
    success_url=reverse_lazy("compra:listacompras")

    @method_decorator(permission_required('compra.change_compra',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CompraUpdate, self).dispatch(*args, **kwargs)

class CompraDelete(DeleteView):
    model= Compra
    template_name='compras/deletecompra.html'
    success_url=reverse_lazy("compra:listacompras")

    @method_decorator(permission_required('compra.delete_compra',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CompraDelete, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            contex = {
        'proveedores': 'proveedor'
                        }
        return render(request, 'pagoproveedor/protecteError.html', contex)