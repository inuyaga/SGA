from django.shortcuts import render
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, View, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.urls import reverse, reverse_lazy
from aplicaciones.compra.models import Compra
from aplicaciones.compra.forms import CompraForm,CompraEditForm
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

    @method_decorator(permission_required('fuds.add_compra',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CompraCreate, self).dispatch(*args, **kwargs)

class CompraUpdate(UpdateView):
    model= Compra
    form_class = CompraForm
    template_name='compras/crearcompra.html'
    success_url=reverse_lazy("compra:listacompras")

    @method_decorator(permission_required('fuds.change_compra',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CompraUpdate, self).dispatch(*args, **kwargs)