# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from appis.pago_proveedor.forms import NuevoProveedorForm, ContratosForms
from appis.pago_proveedor.models import Proveedor, Contrato
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from django.views.generic.list import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
# Create your views here.
# def proveedor_report(render)


def nuevo_proveedor(request):
    if request.method == "POST":
        form = NuevoProveedorForm(request.POST)
        if form.is_valid():
            # post = form.save(commit=False) Permite no guardar para agregar datos adicionales
            # post.author = request.user
            # post.published_date = timezone.now()
            form.save()
            return redirect('inicio:index')
    else:
        form = NuevoProveedorForm()
        print(form)

    contex = {
        'usuario': request.user,
        'proveedorForm': form,
    }
    return render(request, 'pagoproveedor/create_proveedor.html', contex)


def lista_proveedores(request):
    proveedor = Proveedor.objects.all()
    contex = {
        'proveedores': proveedor
    }
    return render(request, 'pagoproveedor/listar_proveedor.html', contex)


def edicion_proveedor(request, id_proveedor):
    prved = Proveedor.objects.get(id=id_proveedor)
    if request.method == 'GET':
        form = NuevoProveedorForm(instance=prved)
    else:
        form = NuevoProveedorForm(request.POST, instance=prved)
        if form.is_valid():
            form.save()
            return redirect('proveedor:lista')
    return render(request, 'pagoproveedor/create_proveedor.html', {'proveedorForm': form})

# CLASES PARA LA VISTA DE PROVEEDOR
class ProveedorList(ListView):
    paginate_by = 20
    model = Proveedor
    template_name = 'pagoproveedor/listar_proveedor.html'

class ProveedorCreate(CreateView):
    model = Proveedor
    form_class = NuevoProveedorForm
    template_name = 'pagoproveedor/create_proveedor.html'
    success_url = reverse_lazy('proveedor:lista')

    def get_context_data(self, **kwargs):
        context = super(ProveedorCreate, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Crear'
        return context

class ProveedorUpdate(UpdateView):
    model = Proveedor
    form_class = NuevoProveedorForm
    template_name = 'pagoproveedor/create_proveedor.html'
    success_url = reverse_lazy('proveedor:lista')

    def get_context_data(self, **kwargs):
        context = super(ProveedorUpdate, self).get_context_data(**kwargs)
        context['tituloBrea'] = 'Actualizar'
        return context

class ProveedorDelete(DeleteView):
    model = Proveedor
    form_class = NuevoProveedorForm
    template_name = 'pagoproveedor/elimina_proveedor.html'
    success_url = reverse_lazy('proveedor:lista')

class ContratosList(ListView):
    paginate_by = 20
    model = Contrato
    template_name = 'pagoproveedor/contrato/contrato_list.html'

class ContratoCreate(CreateView):
    model = Contrato
    form_class = ContratosForms
    template_name = 'pagoproveedor/contrato/contrato_crear.html'
    success_url = reverse_lazy('proveedor:contrato_listar')
