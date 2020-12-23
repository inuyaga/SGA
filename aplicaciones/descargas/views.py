from django.shortcuts import render
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, View, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.urls import reverse, reverse_lazy
from aplicaciones.descargas.models import Descargas
from aplicaciones.descargas.forms import DescargasForm, DescargaEditForm
from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects

from django.contrib import messages

class DescargasList(ListView):
    model= Descargas
    form_class = DescargasForm
    template_name='descargas/listaDescargas.html'
    ordering = ['-d_id']
    @method_decorator(permission_required('descargas.view_descarga',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(DescargasList, self).dispatch(*args, **kwargs)


    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset 
        estatus = self.request.GET.get('estatus')

        if estatus != None:
            try:
                estatus = int(estatus)
                if estatus > 0 and estatus < 5 and estatus != None:
                    queryset = queryset.filter(estatus=estatus)
                else:
                    messages.warning(self.request, 'El usuario:{} a ingresado un estatus no existente'.format(self.request.user.username))
                # return queryset
            except ValueError:
                messages.warning(self.request, 'El usuario:{} a ingresado un estatus no existente'.format(self.request.user.username))

        return queryset
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DescargaCreate(CreateView):
    model= Descargas
    form_class = DescargasForm
    template_name='descargas/crearDescarga.html'
    success_url=reverse_lazy("descargas:listadescargas")

    @method_decorator(permission_required('descargas.add_compra',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(DescargaCreate, self).dispatch(*args, **kwargs)

class DescargaUpdate(UpdateView):
    model= Descargas
    form_class = DescargaEditForm
    template_name='descargas/crearDescarga.html'
    success_url=reverse_lazy("descargas:listadescargas")

    @method_decorator(permission_required('descargas.change_descargas',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(DescargaUpdate, self).dispatch(*args, **kwargs)

class DescargaDelete(DeleteView):
    model= Descargas
    template_name='descargas/deleteDescarga.html'
    success_url=reverse_lazy("descargas:listadescargas")

    @method_decorator(permission_required('descargas.delete_descargas',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(DescargaDelete, self).dispatch(*args, **kwargs)
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