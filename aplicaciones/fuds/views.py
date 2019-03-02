from django.shortcuts import render
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from aplicaciones.fuds.models import Fud,Motivo,Tramite,Conformidad,Vendedor,Factura
from django.contrib import messages
from datetime import datetime, timedelta
from aplicaciones.fuds.forms import FudForm,FacturaForm,MotivoForm,ConformidadForm,FacturaFormEdicion,TramiteForm
from django.db.models import Sum,F
from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects


# pylint: disable = E1101
class MotivoCreate(CreateView):
    model= Motivo
    form_class = MotivoForm
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarMotivo")

    @method_decorator(permission_required('fuds.add_motivo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(MotivoCreate, self).dispatch(*args, **kwargs)

class MotivoUpdate(UpdateView):
    model= Motivo
    form_class = MotivoForm
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarMotivo")

    @method_decorator(permission_required('fuds.change_motivo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(MotivoUpdate, self).dispatch(*args, **kwargs)

class MotivoList(ListView):
    model= Motivo
    template_name='fuds/ViewMotivo.html'

    @method_decorator(permission_required('fuds.view_motivo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(MotivoList, self).dispatch(*args, **kwargs)

class MotivoDelete(DeleteView):
    model= Motivo
    template_name='fuds/DeleteMotivo.html'
    success_url=reverse_lazy("fuds:ListarMotivo")

    @method_decorator(permission_required('fuds.delete_motivo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(MotivoDelete, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

class ConformidadCreate(CreateView):
    model= Conformidad
    form_class = ConformidadForm
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarConformidad")

    @method_decorator(permission_required('fuds.add_conformidad',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ConformidadCreate, self).dispatch(*args, **kwargs)

class ConformidadUpdate(UpdateView):
    model= Conformidad
    form_class = ConformidadForm
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarConformidad")

    @method_decorator(permission_required('fuds.change_conformidad',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ConformidadUpdate, self).dispatch(*args, **kwargs)
 
class ConformidadList(ListView):
    model= Conformidad
    template_name='fuds/ViewConformidad.html'

    @method_decorator(permission_required('fuds.view_conformidad',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ConformidadList, self).dispatch(*args, **kwargs)

class ConformidadDelete(DeleteView):
    model= Conformidad
    template_name='fuds/DeleteMotivo.html'
    success_url=reverse_lazy("fuds:ListarConformidad")

    @method_decorator(permission_required('fuds.delete_conformidad',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ConformidadDelete, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context



# CLASES DE FUD

class FudCreate(CreateView):
    model = Fud
    template_name = 'fuds/fud/create.html'
    form_class = FudForm
    success_url = reverse_lazy('fuds:fud_list')

    @method_decorator(permission_required('fuds.add_fud',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(FudCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        context['tituloBrea'] = 'Crear Fud'
        return context

class FudList(ListView):
    model = Fud
    paginate_by = 10
    template_name= 'fuds/fud/list.html'

    @method_decorator(permission_required('fuds.view_fud',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(FudList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class FudUpdate(UpdateView):
    model = Fud
    template_name = 'fud/create.html'
    form_class = FudForm
    success_url = reverse_lazy('fuds:fud_list')

    @method_decorator(permission_required('fuds.change_fud',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(FudUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

class FudDelete(DeleteView):
    model= Motivo
    template_name='fuds/DeleteMotivo.html'
    success_url = reverse_lazy('fuds:fud_list')

    @method_decorator(permission_required('fuds.delete_fud',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(FudDelete, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

class FacturaCreate(CreateView):
    model= Factura
    form_class = FacturaForm
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarFacturas")

    @method_decorator(permission_required('fuds.add_factura',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(FacturaCreate, self).dispatch(*args, **kwargs)

class FacturaUpdate(UpdateView):
    model= Factura
    form_class = FacturaFormEdicion
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarFacturas")

    @method_decorator(permission_required('fuds.change_factura',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(FacturaUpdate, self).dispatch(*args, **kwargs)
 
class FacturaList(ListView):
    model= Factura
    template_name='fuds/ViewFactura.html'

    @method_decorator(permission_required('fuds.view_factura',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(FacturaList, self).dispatch(*args, **kwargs)

class FacturaDelete(DeleteView):
    model= Factura
    template_name='fuds/DeleteMotivo.html'
    success_url=reverse_lazy("fuds:ListarFacturas")

    @method_decorator(permission_required('fuds.delete_factura',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(FacturaDelete, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context


class TramiteCreate(CreateView):
    model= Tramite
    form_class = TramiteForm
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarTramites")

    @method_decorator(permission_required('fuds.add_tramite',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(TramiteCreate, self).dispatch(*args, **kwargs)

class TramiteUpdate(UpdateView):
    model= Tramite
    form_class = TramiteForm
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarTramites")

    @method_decorator(permission_required('fuds.change_tramite',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(TramiteUpdate, self).dispatch(*args, **kwargs)
 
class TramiteList(ListView):
    model= Tramite
    template_name='fuds/ViewTramite.html'

    @method_decorator(permission_required('fuds.view_tramite',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(TramiteList, self).dispatch(*args, **kwargs)

class TramiteDelete(DeleteView):
    model= Tramite
    template_name='fuds/DeleteMotivo.html'
    success_url=reverse_lazy("fuds:ListarTramites")

    @method_decorator(permission_required('fuds.delete_tramite',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(TramiteDelete, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context