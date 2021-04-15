from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, TemplateView
from aplicaciones.solicitud.models import TipoServicio, Servicio
from aplicaciones.solicitud.forms import *

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.contrib.auth.mixins import PermissionRequiredMixin

class TipoServicioCreate(CreateView, PermissionRequiredMixin):
    permission_required = 'solicitud.add_tiposervicio'
    model = TipoServicio
    template_name = "solicitud/tipo_servicio_create.html"
    form_class = TipoServicioForm
    success_url = reverse_lazy('solicitud:crear_tipo_servicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tiposervicio_list']=TipoServicio.objects.all()
        return context


class TipoServicioEdit(UpdateView, PermissionRequiredMixin):
    permission_required = 'solicitud.change_tiposervicio'
    model = TipoServicio
    template_name = "solicitud/tipo_servicio_create.html"
    form_class = TipoServicioForm
    success_url = reverse_lazy('solicitud:crear_tipo_servicio')


class TipoServicioDelete(DeleteView, PermissionRequiredMixin): 
    permission_required = 'solicitud.delete_tiposervicio'
    model = TipoServicio
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('solicitud:crear_tipo_servicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   

        deletable_objects, model_count, protected = get_deleted_objects([self.object])        
        context['deletable_objects'] = deletable_objects
        context['model_count'] = dict(model_count).items()
        context['protected'] = protected
        return context
    


class ServicioList(ListView, PermissionRequiredMixin):
    permission_required = 'solicitud.view_servicio'
    model = Servicio
    template_name = "solicitud/solicitud_list.html"
    paginate_by = 50
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('s_estatus')
        
        s_fecha=self.request.GET.get('s_fecha')
        s_fecha2=self.request.GET.get('s_fecha2') 
        s_tipo=self.request.GET.get('s_tipo')
        s_empresa=self.request.GET.get('s_empresa')        
        s_estatus=self.request.GET.get('s_estatus')

        if s_fecha and s_fecha2:
            queryset = queryset.filter(s_fecha__range=(s_fecha, s_fecha2))        
        if s_tipo:
             queryset = queryset.filter(s_tipo=s_tipo)
        if s_empresa:
             queryset = queryset.filter(s_empresa=s_empresa)
        if s_estatus:
             queryset = queryset.filter(s_estatus=s_estatus)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms_filtro']=FiltroServicioForm(self.request.GET)        
        return context
    

class ServicioCreate(CreateView, PermissionRequiredMixin):
    permission_required = 'solicitud.add_servicio'
    model = Servicio
    template_name = "solicitud/generic_form.html"
    form_class = ServicioForm
    success_url = reverse_lazy('solicitud:servicios') 
    def form_valid(self, form):
        form.instance.s_depo = self.request.user.departamento
        form.instance.s_user = self.request.user
        form.instance.s_user_cambio = self.request.user
        self.object = form.save()
        return super().form_valid(form)

class ServicioValidarView(UpdateView, PermissionRequiredMixin):
    permission_required = 'solicitud.validar_servicio'
    model = Servicio
    template_name = "solicitud/generic_form.html"
    form_class = ServicioValidarForm
    success_url = reverse_lazy('solicitud:servicios') 
    def form_valid(self, form):
        form.instance.s_estatus = 2
        form.instance.s_user_cambio = self.request.user        
        self.object = form.save()
        return super().form_valid(form)


class ServicioDelete(DeleteView, PermissionRequiredMixin): 
    permission_required = 'solicitud.delete_servicio'
    model = Servicio
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('solicitud:servicios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   

        deletable_objects, model_count, protected = get_deleted_objects([self.object])        
        context['deletable_objects'] = deletable_objects
        context['model_count'] = dict(model_count).items()
        context['protected'] = protected
        return context


class UpdateStatusServicioView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        servicio_id = request.data["id"]   
        user = request.data["changue"]   
        resp=Servicio.objects.filter(id=servicio_id).update(s_estatus=3, s_user_cambio=user)
        data = {
            'respuesta': resp,        
        }
        return Response(data, status=status.HTTP_202_ACCEPTED)

    
