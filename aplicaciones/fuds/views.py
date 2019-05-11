from django.shortcuts import render
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from aplicaciones.fuds.models import Fud,Motivo,Tramite,Conformidad,Vendedores,Zona,PartidasFud
from django.contrib import messages
from datetime import datetime, timedelta
from aplicaciones.fuds.forms import FudForm,MotivoForm,ConformidadForm,TramiteForm, FudFormEdit,ZonaForm,VendedorForm,PartidaFudForm
from django.db.models import Sum,F
from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects
from aplicaciones.pedidos.models import Producto
from django.db.models import ProtectedError, Q, F, Sum, FloatField


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

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            contex = {
        'proveedores': 'proveedor'
                        }
        return render(request, 'pagoproveedor/protecteError.html', contex)

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

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            contex = {
        'proveedores': 'proveedor'
                        }
        return render(request, 'pagoproveedor/protecteError.html', contex)



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
    template_name = 'fuds/fud/create.html'
    form_class = FudFormEdit
    success_url = reverse_lazy('fuds:fud_list')

    @method_decorator(permission_required('fuds.change_fud',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(FudUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        context['resultados'] = PartidasFud.objects.filter(Partida_fud = self.kwargs.get('pk'))
        context['total_partidas'] = PartidasFud.objects.filter(Partida_fud = self.kwargs.get('pk')).aggregate(total=Sum( F('Partida_Cantidad') * F('Partida_Precio'), output_field=FloatField() ))['total']
        context['total_iva'] = PartidasFud.objects.filter(Partida_fud = self.kwargs.get('pk')).aggregate(total_iva=Sum( F('Partida_Cantidad') * F('Partida_Precio')*0.16, output_field=FloatField() ))['total_iva']
        context['total_total'] = PartidasFud.objects.filter(Partida_fud = self.kwargs.get('pk')).aggregate(total_total=Sum( F('Partida_Cantidad') * F('Partida_Precio')*1.16, output_field=FloatField() ))['total_total']
        


        return context

class FudDelete(DeleteView): 
    model= Fud
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
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            contex = {
        'proveedores': 'proveedor'
                        }
        return render(request, 'pagoproveedor/protecteError.html', contex)


class ZonaCreate(CreateView):
    model= Zona
    form_class = ZonaForm
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarZona")

    @method_decorator(permission_required('fuds.add_zona',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaCreate, self).dispatch(*args, **kwargs)

class ZonaList(ListView):
    model= Zona
    template_name='fuds/ViewZona.html'

    @method_decorator(permission_required('fuds.view_zona',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaList, self).dispatch(*args, **kwargs)

class ZonaUpdate(UpdateView):
    model= Zona
    form_class = ZonaForm
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarZona")

    @method_decorator(permission_required('fuds.change_zona',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaUpdate, self).dispatch(*args, **kwargs)

class ZonaDelete(DeleteView):
    model= Zona
    template_name='fuds/DeleteMotivo.html'
    success_url=reverse_lazy("fuds:ListarZona")

    @method_decorator(permission_required('fuds.delete_zona',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaDelete, self).dispatch(*args, **kwargs)
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

class VendedorCreate(CreateView):
    model= Vendedores
    form_class = VendedorForm
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarVendedor")

    @method_decorator(permission_required('fuds.add_vendedores',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(VendedorCreate, self).dispatch(*args, **kwargs)


class VendedorList(ListView):
    model= Vendedores
    template_name='fuds/ViewVendedores.html'

    @method_decorator(permission_required('fuds.view_vendedores',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(VendedorList, self).dispatch(*args, **kwargs)

class VendedorUpdate(UpdateView):
    model= Vendedores
    form_class = VendedorForm
    template_name='fuds/CreateMotivo.html'
    success_url=reverse_lazy("fuds:ListarVendedor")

    @method_decorator(permission_required('fuds.change_vendedores',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(VendedorUpdate, self).dispatch(*args, **kwargs)

class VendedorDelete(DeleteView):
    model= Vendedores
    template_name='fuds/DeleteMotivo.html'
    success_url=reverse_lazy("fuds:ListarVendedor")

    @method_decorator(permission_required('fuds.delete_vendedores',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(VendedorDelete, self).dispatch(*args, **kwargs)
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



class PartidaCreate(CreateView):
    model= PartidasFud
    form_class = PartidaFudForm
    template_name='fuds/CreatePartida.html'
    success_url=reverse_lazy("fuds:ListarVendedor")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['usuario'] = self.request.user
        context['resultados'] =productoFiltrado= PartidasFud.objects.filter(Partida_fud = self.kwargs.get('pk'))

        return context

    @method_decorator(permission_required('fuds.add_vendedores',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(PartidaCreate, self).dispatch(*args, **kwargs)
    def post(self, request, *args, **kwargs):
        producto=Producto.objects.get(producto_codigo=request.POST.get('Partida_nombre'))
        pf=PartidasFud(
                Partida_nombre=producto,
                Partida_fud_id=request.POST.get('Partida_fud'),
                Partida_Precio=request.POST.get('Partida_Precio'),
                Partida_Cantidad=request.POST.get('Partida_Cantidad'),
                )
        pf.save()
        respuesta="""
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            {Partida_nombre} agredado al FUD!
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
        """.format(
            Partida_nombre = request.POST.get('Partida_nombre'),
        )
        productoFiltrado= PartidasFud.objects.filter(Partida_fud = request.POST.get('Partida_fud'))
        String2= ""
        for pd2 in productoFiltrado:
            String2 += """
            <tr>
                <th scope="row">{Partida_nombre}</th>
                <th scope="row">{Partida_fud}</th>
                <th scope="row">{Partida_Precio}</th>
                <th scope="row">{Partida_Cantidad}</th>
                
            </tr>
            """.format(
                Partida_nombre = pd2.Partida_nombre,
                Partida_fud = pd2.Partida_fud,
                Partida_Precio = pd2.Partida_Precio,
                Partida_Cantidad = pd2.Partida_Cantidad,
            )

        return JsonResponse({'cp':String2,'rsp':respuesta})




class PartidaView(View):
    
    # template_name='fuds/ViewVendedores.html'
    def post(self, request, *args, **kwargs):
        resultado = request.POST.get("txt_search")
        idfud = request.POST.get("txt_idfud")
        producto= Producto.objects.filter(Q(producto_descripcion__icontains = resultado) | Q(producto_codigo= resultado) )
        productoFiltrado= PartidasFud.objects.filter(Partida_fud = idfud )
        String = """
         <thead class="thead-dark">
                <tr>
                <th scope="col">Partida</th>
                <th scope="col">Descripción</th>
                <th scope="col">Precio</th>
                <th scope="col">Cantidad</th>
                <th scope="col">Acciones</th>
                </tr>
            </thead>"""
        for pd in producto:
            String += """
            <form action="asdasdasd.com" method="POST" >
            <tr>
                <th scope="row">{Partida}</th>
                <th scope="row">{Descripcion} </th>
                <th scope="row"><input type="number" step="any" class="form-control" id="Partida_Precio{Partida}"></th>
                <th scope="row"><input type="number" class="form-control" id="Partida_Cantidad{Partida}"></th>
                <th> <input type="submit" class="btn btn-info" onclick="guardar_partida('{Partida}',{idfud})" value="Agregar a fud" placeholder="Busqueda de producto"> </th>
            </tr>
            </form>
            """.format(
                Partida = pd.producto_codigo,
                Descripcion = pd.producto_descripcion,
                idfud = idfud,
            )

        String2= ''
        for pd2 in productoFiltrado:
            String2 += """
            <tr>
                <th scope="row">{Partida_nombre}</th>
                <th scope="row">{Partida_fud}</th>
                <th scope="row">{Partida_Precio}</th>
                <th scope="row">{Partida_Cantidad}</th>
            </tr>
            """.format(
                Partida_nombre = pd2.Partida_nombre,
                Partida_fud = pd2.Partida_fud,
                Partida_Precio = pd2.Partida_Precio,
                Partida_Cantidad = pd2.Partida_Cantidad,
            )

        data = {
                'cuerpoT': String,
                'cuerpoF': String2,
            }
        return JsonResponse(data)