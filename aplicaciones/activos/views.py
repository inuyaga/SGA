from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView
from aplicaciones.activos.models import Categoria, Activo, Especificacion
from aplicaciones.pedidos.models import Marca
from aplicaciones.activos.forms import CategoriaForm, EspecificacionForm, ActivoForm
from django.urls import reverse_lazy
from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
# Create your views here.
class Prueba(TemplateView):
    template_name='activos/p.html'

class CategoriaList(ListView):
    model=Categoria
    template_name='activos/cat_list.html' 
    @method_decorator(permission_required('activos.view_categoria',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CategoriaList, self).dispatch(*args, **kwargs)

class CategoriaCrear(CreateView): 
    model=Categoria
    form_class=CategoriaForm
    template_name='activos/categoria_crear.html' 
    success_url=reverse_lazy('activos:cat_list')

    @method_decorator(permission_required('activos.add_categoria',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CategoriaCrear, self).dispatch(*args, **kwargs)

class CategoriaUpdate(UpdateView): 
    model=Categoria
    form_class=CategoriaForm
    template_name='activos/categoria_crear.html' 
    success_url=reverse_lazy('activos:cat_list')

    @method_decorator(permission_required('activos.change_categoria',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CategoriaUpdate, self).dispatch(*args, **kwargs)

class CategoriaDelete(DeleteView):
    model = Categoria
    template_name = "pedidos/delete_forever.html"
    success_url=reverse_lazy('activos:cat_list') 

    @method_decorator(permission_required('activos.delete_categoria',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CategoriaDelete, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategoriaDelete, self).get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

class ActivoList(ListView):
    model=Activo
    template_name='activos/activo_list.html' 

    @method_decorator(permission_required('activos.view_activo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ActivoList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs): 
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['obj_list'] = Categoria.objects.all()
        context['list_marca'] = Marca.objects.all() 
        return context
    def get_queryset(self):
        queryset = super(ActivoList, self).get_queryset()
        categoria=self.request.GET.get('categoria')
        marca=self.request.GET.get('marca')
        serie=self.request.GET.get('serie')
        barra=self.request.GET.get('barra')
        if categoria != None:
            queryset=queryset.filter(activo_categoria=categoria)
        if marca != None:
            queryset=queryset.filter(activo_marca=marca)
        if serie != None:
            if serie != '':
                queryset=queryset.filter(activo_serie=serie)
        if barra != None:
            if barra != '':
                 queryset=queryset.filter(activo_codigo_barra=barra)
        return queryset


class ActivoCrear(CreateView): 
    model=Activo
    form_class=ActivoForm
    template_name='activos/activo_crear.html' 
    success_url=reverse_lazy('activos:activo_list')

    @method_decorator(permission_required('activos.add_activo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ActivoCrear, self).dispatch(*args, **kwargs)

class ActivoUpdate(UpdateView): 
    model=Activo
    form_class=ActivoForm
    template_name='activos/activo_crear.html' 
    success_url=reverse_lazy('activos:activo_list')

    @method_decorator(permission_required('activos.change_activo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ActivoUpdate, self).dispatch(*args, **kwargs)

class ActivoDelete(DeleteView):
    model = Activo
    template_name = "pedidos/delete_forever.html"
    success_url=reverse_lazy('activos:activo_list') 

    @method_decorator(permission_required('activos.delete_activo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ActivoDelete, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ActivoDelete, self).get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

class EspecificacioCreate(CreateView):
    model=Especificacion
    form_class=EspecificacionForm
    template_name='activos/especificacion_crear.html' 
    success_url=reverse_lazy('activos:cat_list')

    @method_decorator(permission_required('activos.add_especificacion',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(EspecificacioCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['obj_list'] = Especificacion.objects.filter(esp_activo=self.kwargs.get('pk'))
        return context
    
    def form_valid(self, form):
        form.instance.esp_activo=Activo.objects.get(activo=self.kwargs.get('pk'))
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('activos:activo_especificacion_crear', kwargs={'pk':self.kwargs.get('pk')})

class EspUpdate(UpdateView):
    model=Especificacion
    form_class=EspecificacionForm
    template_name='activos/categoria_crear.html' 
    success_url=reverse_lazy('activos:cat_list')

    @method_decorator(permission_required('activos.change_especificacion',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(EspUpdate, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        return reverse_lazy('activos:activo_especificacion_crear', kwargs={'pk':self.kwargs.get('activo')})

class EspDelete(DeleteView):
    model = Especificacion
    template_name = "pedidos/delete_forever.html"
    success_url=reverse_lazy('activos:activo_list') 

    @method_decorator(permission_required('activos.delete_especificacion',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(EspDelete, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EspDelete, self).get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context
    def get_success_url(self):
        return reverse_lazy('activos:activo_especificacion_crear', kwargs={'pk':self.kwargs.get('activo')})