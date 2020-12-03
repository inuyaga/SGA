from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView
from aplicaciones.gasto.models import *
from aplicaciones.gasto.forms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class InicioView(TemplateView):
    template_name = "gasto/inicio.html"
    

class CrearTipoGasto(PermissionRequiredMixin, CreateView): 
    permission_required = 'gasto.add_tipogasto'
    model = TipoGasto
    template_name = "gasto/crear.html"
    form_class = TipoGastoForm
    success_url = reverse_lazy('gastos:tipoGastoList')
class UpdateTipoGasto(PermissionRequiredMixin, UpdateView):
    permission_required = 'gasto.change_tipogasto'
    model = TipoGasto
    template_name = "gasto/crear.html"
    form_class = TipoGastoForm
    success_url = reverse_lazy('gastos:tipoGastoList')


class TipoGastoList(PermissionRequiredMixin, ListView):
    permission_required = 'gasto.view_tipogasto'
    model = TipoGasto
    template_name = "gasto/list_tipo_gasto.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TipoGastoForm']=TipoGastoForm
        return context



class TipoGastoDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'gasto.delete_tipogasto'
    model = TipoGasto
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('gastos:tipoGastoList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects'] = deletable_objects
        context['model_count'] = dict(model_count).items()
        context['protected'] = protected
        return context


 

class GastoViewList(ListView): 
    
    model = Gasto
    template_name = "gasto/list_gasto.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset 
        week = self.request.GET.get('week')
        empresa = self.request.GET.get('empresa')
        tip_gasto = self.request.GET.get('tip_gasto')
        status = self.request.GET.get('status')

        
        if not self.request.user.is_superuser:                
            permiso = self.request.user.has_perm('gasto.view_gasto')        
            if permiso == False:
                try:                
                    queryset = queryset.filter(g_depo=self.request.user.departamento)
                except AttributeError as error:
                    messages.warning(self.request, 'Usuario:{} debe tener asignado un departamento para ver gastos de su departamento'.format(self.request.user.username))       

        if week != None and week != '':
            week = week.replace('W','') 
            week = week.split('-')             
            queryset = queryset.filter(g_fechaCreacion__year=week[0]) 
            queryset = queryset.filter(g_fechaCreacion__week=week[1]) 
            
        
        if empresa != None and empresa != '':            
            queryset = queryset.filter(g_depo__departamento_id_sucursal__sucursal_empresa_id__id=empresa)
        if tip_gasto != None and tip_gasto != '':
            queryset = queryset.filter(g_tipoGasto=tip_gasto)
        if status != None and status != '':
            queryset = queryset.filter(g_estado=status)

                   
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        badge = {
            1:'badge badge-info',
            2:'badge badge-success',
            3:'badge badge-primary',
            4:'badge badge-secondary',
            5:'badge badge-danger',
        }
        context['TipoGasto']=TipoGasto.objects.all()
        context['STATUS']=STATUS
        context['Empresa']=Empresa.objects.all()
        context['badge']=badge

        return context
    


class GastoCreate(PermissionRequiredMixin, CreateView): 
    permission_required = 'gasto.add_gasto'
    model = Gasto
    template_name = "gasto/crear.html"
    form_class = GastoForm
    success_url = reverse_lazy('gastos:gasto_list')

    def form_valid(self, form, **kwargs):        
        try:
            self.request.user.departamento.departamento_id_sucursal.sucursal_empresa_id
            form.instance.g_depo = self.request.user.departamento
            form.instance.g_userCreador = self.request.user    
            form.save()        
        except AttributeError as identifier:
            context = self.get_context_data(**kwargs)
            messages.warning(self.request, 'Usuario:{} debe tener asignado un departamento para poder crear gastos'.format(self.request.user.username))
            return self.render_to_response(context)
                    
        return super().form_valid(form)




class GastoUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'gasto.change_gasto'
    model = Gasto
    template_name = "gasto/crear.html"
    form_class = GastoForm
    success_url = reverse_lazy('gastos:gasto_list')





class UpdateStatusView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()
    def post(self, request, *args, **kwargs):
        g_id=request.data["g_id"]
        g_estado=request.data["g_estado"]
        g_estado_filter = 1 if g_estado == 5 else g_estado - 1
        
        Gasto.objects.filter(g_id=g_id, g_estado=g_estado_filter).update(g_estado=g_estado)
        
        data = {
            'id':g_id,
            'new_stado':g_estado,
            'filter_stado':g_estado_filter,
            
        }
        return Response(data, status=status.HTTP_202_ACCEPTED)




class GastoDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'gasto.delete_gasto'
    model = Gasto
    template_name = "pedidos/delete_forever.html"
    success_url = reverse_lazy('gastos:gasto_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects'] = deletable_objects
        context['model_count'] = dict(model_count).items()
        context['protected'] = protected
        return context