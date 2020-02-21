from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from aplicaciones.empresa.models import Cliente
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from aplicaciones.empresa.forms import ClienteForm
from django.db.models import Sum, F, Q
class ClienteList(ListView):
    model = Cliente
    template_name = "empresa/clienteslista.html"
    paginate_by = 150

    @method_decorator(permission_required('empresa.view_cliente', reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs) 

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        urls_formateada = self.request.GET.copy()
        if 'page' in urls_formateada:
            del urls_formateada['page']
        context['urls_formateada'] = urls_formateada
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        Buscar=self.request.GET.get('Buscar') 
        if Buscar != None:
            queryset=queryset.filter(Q(cli_clave=Buscar) | Q(cli_nombre__icontains=Buscar))
        return queryset


class ClienteUpdate(UpdateView):
    model = Cliente
    template_name = "empresa/form.html"
    form_class = ClienteForm
    success_url = reverse_lazy('empresa:clientes_list')

    @method_decorator(permission_required('empresa.change_cliente', reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
