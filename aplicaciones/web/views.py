from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from aplicaciones.web.models import Marca, Catalagos, Promocion, Evento, RegistroExpo, Vacante, Postulacion, Detalle_Compra_Web, Domicilio, CompraWeb
from aplicaciones.web.forms import CooreoForm, IncribirForm, PostulacionForm, DomicilioForm
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from aplicaciones.pedidos.models import Producto, Area, Marca as MarcaProducto

from aplicaciones.inicio.models import User
from aplicaciones.inicio.forms import UserForm

from django.http import JsonResponse
from aplicaciones.empresa.models import Cliente

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import json
from django.db.models import Avg, Sum, F, FloatField, Count
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class Home(TemplateView):
    template_name="web/index.html"

    def get_context_data(self, **kwargs): 
        context = super(Home, self).get_context_data(**kwargs)
        # context['galeria_list'] = Galeria.objects.all()
        # context['form_correo'] = CorreoForm()
        # context['even_nombre'] = Evento.objects.all()
        context['marca_list'] = Marca.objects.all()
        context['catagolo_list'] = Catalagos.objects.all()[:8]
        context['promo_list'] = Promocion.objects.all()
        context['evento_list'] = Evento.objects.all()
        context['msn_ccs'] = CooreoForm()
        return context
    def post(self, request, *args, **kwargs):
        form = CooreoForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje guardado correctamente')
        else:
            messages.warning(request, 'Error al guardar')
        url=reverse('web:inicio')
        url=url+'#contact'
        return redirect(url)


class IncribirCreate(CreateView):
    template_name = 'form_create.html'
    model = RegistroExpo
    form_class = IncribirForm
    def get_success_url(self):
        url=reverse('web:inicio')
        url=url+'#expos'
        messages.success(self.request, 'Inscrito guardado correctamente')
        return url
    
    def get_context_data(self, **kwargs): 
        context = super(IncribirCreate, self).get_context_data(**kwargs)
        context['detalle_object'] = Evento.objects.get(id=self.request.GET.get('codex'))
        return context



class VacanteView(ListView):
    template_name = "web/vacantes.html"
    model = Vacante


class PostularCreate(CreateView):
    template_name = 'form_create.html'
    model = Postulacion
    form_class = PostulacionForm
    def get_success_url(self):
        url=reverse('web:vacantes')
        messages.success(self.request, 'Postulacion exitosa, si cumple con los requisitos un agente de RH se comunicara con usted.')
        return url


class ProductosListWebView(ListView):
    model = Producto
    template_name = "web/productos_list.html"  
    paginate_by = 20
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(producto_visible=True)
        
        if len(self.request.GET) > 0:
            area=self.request.GET.getlist('area')
            marca=self.request.GET.getlist('marca')
            print(len(marca))
            prod_name=self.request.GET.get('prod_name')
            if len(area) > 0:
                queryset = queryset.filter(producto_area__in=area)
            if len(marca) > 0:
                queryset = queryset.filter(producto_marca__in=marca)
            if prod_name != '' and prod_name != None:
                queryset = queryset.filter(producto_descripcion__icontains=prod_name)
        return queryset

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['marca'] = Producto.objects.values('producto_marca__marca_id_marca', 'producto_marca__marca_nombre').filter(producto_visible=True).annotate(cuenta=Count('producto_marca__marca_id_marca')).order_by('producto_marca__marca_nombre')
        context['area'] = Producto.objects.values('producto_area__area_id_area', 'producto_area__area_nombre').filter(producto_visible=True).annotate(cuenta=Count('producto_area__area_id_area')).order_by('producto_area__area_nombre')
        context['marca_lista'] = self.request.GET.getlist('marca')
        context['area_lista'] = self.request.GET.getlist('area')

        urls_formateada = self.request.GET.copy()
        if 'page' in urls_formateada:
            del urls_formateada['page']
        context['urls_formateada'] = urls_formateada 
       
        return context



class ProductoDetalleView(DetailView):
    model = Producto
    template_name="web/producto_detalles.html"


from django.contrib.auth.admin import UserAdmin
class CreateUser(CreateView):
    model = UserAdmin
    form_class = UserForm
    template_name = 'web/registrar.html'
    success_url = reverse_lazy('inicio')
    def form_valid(self, form):
        instancia = form.save(commit=False)
        instancia.is_user_web=True
        instancia.save()
        return super(CreateUser, self).form_valid(form)


def FindRfcUserView(request):
    rfc = request.GET.get('rfc')
    try:
        client=Cliente.objects.get(cli_rfc=rfc)
        responseData = {
        'nombre':client.cli_nombre,
        'email':client.cli_email,
        }
        return JsonResponse(status=200, data=responseData)
    except ObjectDoesNotExist as err:
        return JsonResponse(status=204, data={})


def AddProductoCarrito(request): 
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    cantidad_prod = body_data['cantidad']
    producto_obj = Producto.objects.get(producto_codigo=body_data['producto'])

    suma_prod_futura = Detalle_Compra_Web.objects.filter(dcw_producto_id=producto_obj, dcw_status=False).aggregate(suma=Sum('dcw_cantidad'))['suma']
    suma_prod_futura = 0 if suma_prod_futura == None else suma_prod_futura
    total_suma_pendiente=suma_prod_futura+ int(cantidad_prod)
    if int(cantidad_prod) <= 0:
        contenido={
            'msn':'Cantidad de producto debe ser mayor a 0',
        }
        return JsonResponse(status=400, data=contenido)
    elif total_suma_pendiente <= producto_obj.prducto_existencia:
        try:
            find_prod_user = Detalle_Compra_Web.objects.get(dcw_creado_por=request.user, dcw_status=False, dcw_producto_id=body_data['producto'])
            Detalle_Compra_Web.objects.filter(dcw_creado_por=request.user, dcw_status=False, dcw_producto_id=body_data['producto']).update(dcw_cantidad=F('dcw_cantidad')+int(cantidad_prod))
        except ObjectDoesNotExist as erro:
            dt_cw=Detalle_Compra_Web(dcw_producto_id=producto_obj, dcw_cantidad=cantidad_prod, dcw_creado_por=request.user, dcw_precio=producto_obj.producto_precio)
            dt_cw.save()

        conteo_shop=Detalle_Compra_Web.objects.filter(dcw_creado_por=request.user, dcw_status=False).count()
        contenid={
            'ok':'¡Producto agregado correctamente!',
            'shoping':conteo_shop,
        }
        return JsonResponse(status=201, data=contenid)
    else:
        contenido={
            'msn':'Supera el limite de producto en existencia',
        }
        return JsonResponse(status=400, data=contenido)

def get_carro_compras(request):
    if request.user.is_authenticated:
        conteo_shop=Detalle_Compra_Web.objects.filter(dcw_creado_por=request.user, dcw_status=False).count()
        conteo_shop = '' if conteo_shop == 0 else conteo_shop
        contenid={
            'shoping':conteo_shop,
        }
        return JsonResponse(status=200, data=contenid)
    else:
        return JsonResponse(status=200, data={})

    
    

class CarritoComprasView(LoginRequiredMixin, TemplateView): 
    login_url = reverse_lazy('inicio')
    redirect_field_name = 'redirect_to'
    template_name = "web/carrito_compra.html"
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['carrito'] = Detalle_Compra_Web.objects.filter(dcw_creado_por=self.request.user, dcw_status=False)    
        context['subtotal'] = Detalle_Compra_Web.objects.filter(dcw_creado_por=self.request.user, dcw_status=False).aggregate(suma_total=Sum(F('dcw_precio') * F('dcw_cantidad'), output_field=FloatField()))['suma_total']  
        context['subtotal'] = 0 if context['subtotal'] == None else context['subtotal']
        context['iva'] = context['subtotal'] * 0.16  
        context['total'] = context['subtotal']+context['iva']
        return context


def delete_item_carrito(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    obj=Detalle_Compra_Web.objects.filter(id=body_data['producto']).delete()
    
    contenid={
        'delete':body_data['producto'],
    }
    return JsonResponse(status=201, data=contenid)



class CompraStep1View(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('inicio')
    redirect_field_name = 'redirect_to'
    template_name = "web/procede_step1.html"
    def post(self, request, *args, **kwargs):
        obj_c=CompraWeb(
            cw_cliente=request.user,
            cw_domicilio_id=request.POST.get('direccion')
        )
        url=''
        try: 
            obj_c.save()
            detalle_compra=Detalle_Compra_Web.objects.filter(dcw_creado_por=self.request.user, dcw_status=False)
            for item in detalle_compra:
                Producto.objects.filter(producto_codigo=item.dcw_producto_id).update(prducto_existencia=F('prducto_existencia')-item.dcw_cantidad)
            detalle_compra.update(dcw_pedido_id=obj_c, dcw_status=True)
            messages.success(request, 'Su compra ha sido realizada el pago es efectuado en la entrega del paquete en el domicilio.')
            url=reverse_lazy('web:compras_web')
        except IntegrityError as e:
            messages.success(request, 'Para finalizar su compra es necesario que proporcione un domicilio.')
            url=reverse_lazy('web:step1') 
        
        return redirect(url)
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['domicilios'] =Domicilio.objects.filter(dom_creador=self.request.user)
        context['domicilioForm'] =DomicilioForm()

        context['carrito'] = Detalle_Compra_Web.objects.filter(dcw_creado_por=self.request.user, dcw_status=False)    
        context['carrito_count'] = Detalle_Compra_Web.objects.filter(dcw_creado_por=self.request.user, dcw_status=False).count()
        context['subtotal'] = Detalle_Compra_Web.objects.filter(dcw_creado_por=self.request.user, dcw_status=False).aggregate(suma_total=Sum(F('dcw_precio') * F('dcw_cantidad'), output_field=FloatField()))['suma_total']  
        context['subtotal'] = 0 if context['subtotal'] == None else context['subtotal']
        context['iva'] = context['subtotal'] * 0.16  
        context['total'] = context['subtotal']+context['iva']
        return context



class DomicilioCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('inicio')
    redirect_field_name = 'redirect_to'
    template_name = 'web/domicilios.html'
    model = Domicilio
    form_class = DomicilioForm
    success_url = reverse_lazy('web:dom_list')
    def form_valid(self, form):
        instancia = form.save(commit=False)
        Domicilio.objects.filter(dom_creador=self.request.user).update(dom_activo=False)
        instancia.dom_activo=True
        instancia.dom_creador=self.request.user
        instancia.save()
        return super(DomicilioCreateView, self).form_valid(form)
    # def get_success_url(self):
    #     url=reverse('web:inicio')
    #     url=url+'#expos'
    #     messages.success(self.request, 'Inscrito guardado correctamente')
    #     return url
    
    # def get_context_data(self, **kwargs): 
    #     context = super(IncribirCreate, self).get_context_data(**kwargs)
    #     context['detalle_object'] = Evento.objects.get(id=self.request.GET.get('codex'))
    #     return context


class DomicilioUpdateView(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('inicio')
    redirect_field_name = 'redirect_to'
    template_name = 'web/domicilios.html'
    model = Domicilio
    form_class = DomicilioForm
    success_url = reverse_lazy('web:dom_list')
    # def form_valid(self, form):
    #     instancia = form.save(commit=False)
    #     Domicilio.objects.filter(dom_creador=self.request.user).update(dom_activo=False)
    #     instancia.dom_activo=True
    #     instancia.dom_creador=self.request.user
    #     instancia.save()
    #     return super(DomicilioCreateView, self).form_valid(form)


class DomicilioListView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('inicio')
    redirect_field_name = 'redirect_to'
    template_name = 'web/domicilios_list.html'
    model = Domicilio

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(dom_creador=self.request.user)
        return queryset

class ComprasWebList(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('inicio')
    redirect_field_name = 'redirect_to'
    template_name = 'web/compras_listar.html'
    model = CompraWeb
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(cw_cliente=self.request.user)
        return queryset

class DetalleCmpraWebView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('inicio')
    redirect_field_name = 'redirect_to'
    template_name = 'web/detalle_compra.html'
    model = Detalle_Compra_Web
    context_object_name='carrito'
    def get_queryset(self): 
        queryset = super().get_queryset()
        queryset = queryset.filter(dcw_pedido_id=self.kwargs.get('pk')) 
        return queryset
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['subtotal'] = Detalle_Compra_Web.objects.filter(dcw_pedido_id=self.kwargs.get('pk')).aggregate(suma_total=Sum(F('dcw_precio') * F('dcw_cantidad'), output_field=FloatField()))['suma_total']  
        context['subtotal'] = 0 if context['subtotal'] == None else context['subtotal']
        context['iva'] = context['subtotal'] * 0.16  
        context['total'] = context['subtotal']+context['iva']
        return context



class DetalleCuentaView(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('inicio')
    redirect_field_name = 'redirect_to'
    template_name = 'web/profile.html'


