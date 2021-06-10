from aplicaciones import ajustes
from aplicaciones.pedidos.models import Asignar_gasto_sucursal, Producto
from django.db import models
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from aplicaciones.ajustes.models import Ajuste, AjusteProduct
from aplicaciones.ajustes.forms import *
from django.urls import reverse_lazy, reverse

from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects

from django.contrib.auth.mixins import PermissionRequiredMixin
# ApiRest importaciones
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

class AjusteListView(PermissionRequiredMixin,ListView): 
    model=Ajuste
    template_name='ajustes/listar.html'
    permission_required = ('ajustes.view_ajuste')
    # ordering = ['-d_id']
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        autorizar = request.GET.get('autorizar')
        ajustar = request.GET.get('ajustar')
        
        if autorizar:
            if request.user.has_perm('ajustes.puede_autorizar_ajuste'):
                Ajuste.objects.filter(id=autorizar).update(aj_status=2)
        if ajustar:
            if request.user.has_perm('ajustes.puede_ajustar_ajuste'):
                Ajuste.objects.filter(id=ajustar).update(aj_status=3)
        return self.render_to_response(context)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-id')

        permiso_listado = self.request.user.has_perms('ajustes.puede_visualizar_todos_ajustes')
        
        if not permiso_listado:
            queryset = queryset.filter(aj_sucursal=self.request.user.departamento.departamento_id_sucursal)        
            

        id_aj=self.request.GET.get('id_aj')
        ajuste_crescendo=self.request.GET.get('ajuste_crescendo')
        ajuste_crescendo_s=self.request.GET.get('ajuste_crescendo_s')
        sucursal=self.request.GET.get('sucursal')
        
        estatus=self.request.GET.get('estatus')

        if id_aj:
            queryset = queryset.filter(id=id_aj)
        if ajuste_crescendo:
            queryset = queryset.filter(aj_cresendo=ajuste_crescendo)
        if sucursal:
            queryset = queryset.filter(aj_sucursal=sucursal)            
        if ajuste_crescendo_s:
            queryset = queryset.filter(aj_cresendo_salida=ajuste_crescendo_s)            
        if estatus:
            queryset = queryset.filter(aj_status=estatus)            

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filtro']=FiltroAjusteForm(self.request.GET)
        return context
    


class AjusteUpdateCresendoView(PermissionRequiredMixin, UpdateView):
    model = Ajuste
    form_class=AjusteUpdateForm
    template_name = "ajustes/crear_generico.html"
    success_url=reverse_lazy('ajustes:listar')

    permission_required = ('ajustes.puede_actualizar_no_crescendo')

class AjusteUpdateView(PermissionRequiredMixin, UpdateView):
    model = Ajuste
    form_class=AjusteCreateForm
    template_name = "ajustes/create.html"
    success_url=reverse_lazy('ajustes:listar')    

    permission_required = ('ajustes.change_ajuste')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)               
        query = AjusteProduct.objects.filter(ajuste=self.object)
        context['ajuste_obj']=query        
        lista_prod = self.object.aj_producs.values('producto_codigo')    
        context['list_product']=[x['producto_codigo'] for x in lista_prod] 
        return context
    def form_valid(self, form):            
        # self.object = form.save()

        productos_delete=self.request.POST.getlist('productos_delete')
        AjusteProduct.objects.filter(id__in=productos_delete).delete()

        producto=self.request.POST.getlist('producto')
        exist_sistema=self.request.POST.getlist('exist_sistema')
        exist_fisica=self.request.POST.getlist('exist_fisica')
        cantidad=self.request.POST.getlist('cantidad')
        precio=self.request.POST.getlist('precio')
        vale=self.request.POST.getlist('vale')

        for i in range(len(producto)):
            product=AjusteProduct(producto_id=producto[i], ajuste= self.object, exist_sistema=exist_sistema[i], exist_fisica=exist_fisica[i], cantidad=cantidad[i], precio=precio[i], vale=vale[i])
            product.save()            

        
        return super().form_valid(form)
    


class AjusteCrearView(PermissionRequiredMixin, CreateView):
    model = Ajuste
    form_class=AjusteCreateForm
    template_name = "ajustes/create.html"
    success_url=reverse_lazy('ajustes:listar')

    permission_required = ('ajustes.add_ajuste')
    def form_valid(self, form):    
        producto=self.request.POST.getlist('producto')
        exist_sistema=self.request.POST.getlist('exist_sistema')
        exist_fisica=self.request.POST.getlist('exist_fisica')
        cantidad=self.request.POST.getlist('cantidad')
        precio=self.request.POST.getlist('precio')
        vale=self.request.POST.getlist('vale')
        tipo=self.request.POST.getlist('tipo')

        if len(producto) > 0:        
            form.instance.aj_sucursal=self.request.user.departamento.departamento_id_sucursal
            form.instance.aj_status=1
            self.object = form.save()
    
            for i in range(len(producto)):
                product=AjusteProduct(producto_id=producto[i], ajuste= self.object, exist_sistema=exist_sistema[i], exist_fisica=exist_fisica[i], cantidad=cantidad[i], precio=precio[i], vale=vale[i], tipo=tipo[i])
                product.save()     
        else:
            messages.warning(self.request, 'No ha ingresado nuevos productos')
            return redirect(reverse_lazy('ajustes:add'))       

        
        return super().form_valid(form)


class AjusteDelete(PermissionRequiredMixin, DeleteView):
    model = Ajuste
    template_name = "pedidos/delete_forever.html"
    success_url=reverse_lazy('ajustes:listar') 

    permission_required = ('ajustes.delete_ajuste')

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context


class ProductoGetCodigo(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        id_producto = request.data["id_producto"]      
                                 
        try:
            producto = Producto.objects.get(producto_codigo=id_producto)

            data = {
            'codigo': producto.producto_codigo,
            'descripcion': producto.producto_descripcion,                                 
                                        
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist as error:            
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        

