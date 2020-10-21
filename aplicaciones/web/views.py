from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from aplicaciones.web.models import Marca, Catalagos, Promocion, Evento, RegistroExpo, Vacante, Postulacion, Detalle_Compra_Web, Domicilio, CompraWeb, CorreoCco
from aplicaciones.web.forms import CorreoForm, IncribirForm, PostulacionForm, DomicilioForm
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
from django.db.models import Avg, Sum, F, FloatField, Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.web.models import Blog
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
# Create your views here.
class Home(TemplateView): 
    template_name="web/V2/inicio.html" 

    def get_context_data(self, **kwargs): 
        context = super(Home, self).get_context_data(**kwargs)
        # context['galeria_list'] = Galeria.objects.all()
        # context['form_correo'] = CorreoForm()
        # context['even_nombre'] = Evento.objects.all()
        # context['marca_list'] = Marca.objects.all()
        # context['catagolo_list'] = Catalagos.objects.all()[:8]
        context['promo_list'] = Promocion.objects.all()
        # context['evento_list'] = Evento.objects.all()
        # context['msn_ccs'] = CorreoForm()
        context['portadas'] = Blog.objects.filter(blog_tipo=2)
        context['ofert_semana'] = Blog.objects.filter(blog_tipo=3)
        context['oferta_especial'] = Blog.objects.filter(blog_tipo=4)
        context['blogs'] = Blog.objects.filter(blog_tipo=1).order_by('-blog_creado')[:6]
        context['marcas_logo'] = MarcaProducto.objects.filter(marca_activar_web=True)
        productos_cat_top = Detalle_Compra_Web.objects.values('dcw_producto_id__producto_linea__l_subcat__sc_area__area_id_area','dcw_producto_id__producto_linea__l_subcat__sc_area__area_nombre', 'dcw_producto_id__producto_linea__l_subcat__sc_area__area_icono').annotate(cuenta_cat=Count('dcw_producto_id__producto_linea__l_subcat__sc_area__area_id_area')).order_by('-dcw_producto_id__producto_linea__l_subcat__sc_area__area_id_area')
        context['productos'] = productos_cat_top.order_by('-cuenta_cat')[:7]
        trending = Detalle_Compra_Web.objects.filter(dcw_status=True).values(
            'dcw_producto_id', 
            'dcw_producto_id__producto_codigo', 
            'dcw_producto_id__producto_imagen', 
            'dcw_producto_id__producto_precio', 
            'dcw_producto_id__producto_descripcion', 
            'dcw_producto_id__producto_nombre').order_by('dcw_producto_id').annotate(veces_pedido=Sum('dcw_cantidad'))
        context['trendings'] = trending.order_by('-veces_pedido')[:5]
        return context
    def post(self, request, *args, **kwargs):
        form = CorreoForm(data=request.POST)
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
    template_name = "web/comprar.html"  
    paginate_by = 11
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(producto_visible=True)   

        area = self.request.GET.get('area')        
        marca = self.request.GET.getlist('marca')
        order = self.request.GET.get('order')
        linea = self.request.GET.get('linea')
        sub_cat = self.request.GET.get('sub_cat')
        busqueda = self.request.GET.get('busqueda')
        if area != None and area != 'None':
            queryset = queryset.filter(producto_linea__l_subcat__sc_area=area)
        if busqueda != None and busqueda != 'None':
            queryset = queryset.filter(Q(producto_nombre__icontains=busqueda)|Q(producto_descripcion__icontains=busqueda))
        if len(marca) > 0:
            queryset = queryset.filter(producto_marca__in=marca)

        if order == 'desc':
            queryset = queryset.order_by('producto_precio')            
        elif order == 'asc':
            queryset = queryset.order_by('-producto_precio')
        elif order == 'date_new':
            queryset = queryset.order_by('producto_fecha_creado')
        
        if linea != None:
            queryset = queryset.filter(producto_linea=linea)
        if sub_cat != None:
            queryset = queryset.filter(producto_linea__l_subcat=sub_cat)
           
        return queryset

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        area = self.request.GET.get('area')               
        linea = self.request.GET.get('linea')
        sub_cat = self.request.GET.get('sub_cat')
        busqueda = self.request.GET.get('busqueda')

        q_marca = Producto.objects.filter(producto_visible=True)

        context['area_count'] = Producto.objects.filter(producto_visible=True).values('producto_linea__l_subcat__sc_area__area_nombre', 'producto_linea__l_subcat__sc_area').annotate(total_produc=Count('producto_codigo')).order_by('producto_linea__l_subcat__sc_area')
        context['marca_lista'] = self.request.GET.getlist('marca')
               
        if area != None and area != 'None':
            q_marca = q_marca.filter(producto_linea__l_subcat__sc_area=area)               
        if linea != None:
            q_marca = q_marca.filter(producto_linea=linea)
        if sub_cat != None:
            q_marca = q_marca.filter(producto_linea__l_subcat=sub_cat)
        
        if busqueda != None and busqueda != 'None':
            q_marca = q_marca.filter(Q(producto_nombre__icontains=busqueda)|Q(producto_descripcion__icontains=busqueda))
        
        context['marca_object_list'] = q_marca.values('producto_marca', 'producto_marca__marca_nombre').annotate(c_marca=Count('producto_marca')).order_by('producto_marca')
        context['banners'] = Blog.objects.filter(blog_tipo=5).order_by('-blog_creado')

        urls_formateada = self.request.GET.copy()
        if 'page' in urls_formateada:
            del urls_formateada['page']
        context['urls_formateada'] = urls_formateada 
       
        return context



class ProductoDetalleView(DetailView):
    model = Producto
    template_name="web/detalle_producto.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.producto_linea != None:
            context['prod_relacionado']=Producto.objects.filter(producto_linea=self.object.producto_linea).exclude(producto_codigo=self.object)            
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        cantidad_prod = request.POST.get('quantity')
        pk = kwargs.get('pk')
        producto_obj = Producto.objects.get(producto_codigo=pk)

        suma_prod_futura = Detalle_Compra_Web.objects.filter(dcw_producto_id=pk, dcw_status=False).aggregate(suma=Sum('dcw_cantidad'))['suma']
        suma_prod_futura = 0 if suma_prod_futura == None else suma_prod_futura
        total_suma_pendiente=suma_prod_futura + int(cantidad_prod)

        if int(cantidad_prod) <= 0:
            messages.warning(request, 'Cantidad de producto debe ser mayor a 0.')
            return self.render_to_response(context=context) 
        elif total_suma_pendiente <= producto_obj.prducto_existencia: 
            try:
                find_prod_user = Detalle_Compra_Web.objects.get(dcw_creado_por=request.user, dcw_status=False, dcw_producto_id=pk)
                Detalle_Compra_Web.objects.filter(dcw_creado_por=request.user, dcw_status=False, dcw_producto_id=pk).update(dcw_cantidad=F('dcw_cantidad')+int(cantidad_prod))
            except ObjectDoesNotExist as erro:
                dt_cw=Detalle_Compra_Web(dcw_producto_id=producto_obj, dcw_cantidad=cantidad_prod, dcw_creado_por=request.user, dcw_precio=producto_obj.producto_precio)
                dt_cw.save()
            # conteo_shop=Detalle_Compra_Web.objects.filter(dcw_creado_por=request.user, dcw_status=False).count()           
            messages.success(request, '¡Producto agregado correctamente!')
            return self.render_to_response(context=context) 
        else:          
            messages.warning(request, 'Supera el limite de producto en existencia')
            return self.render_to_response(context=context) 
    



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

    
    
#se cambio la direccioón del template a la versión 2
class CarritoComprasView(LoginRequiredMixin, ListView):  
    model=Detalle_Compra_Web
    template_name = "web/V2/carrito.html"
    login_url = reverse_lazy('inicio') 
    redirect_field_name = 'redirect_to'
    context_object_name = 'carrito'
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(dcw_creado_por=self.request.user, dcw_status=False) 
        return queryset
    def post(self, request, *args, **kwargs):
        url=reverse_lazy('web:carrito')                
        post = request.POST       
        exclude_items=[] 
        for item in post:
            if 'csrfmiddlewaretoken' != item:
                if int(post[item]) <= 0:
                    pass
                else:
                    Detalle_Compra_Web.objects.filter(dcw_producto_id=item, dcw_creado_por=request.user, dcw_status=False).update(dcw_cantidad=post[item])                        
            exclude_items.append(item)
        
        Detalle_Compra_Web.objects.filter(dcw_creado_por=request.user, dcw_status=False).exclude(dcw_producto_id__in=exclude_items).delete()


        return redirect(url)

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        # context['carrito'] = Detalle_Compra_Web.objects.filter(dcw_creado_por=self.request.user, dcw_status=False)    
        
        
        return context
    
    


def delete_item_carrito(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    obj=Detalle_Compra_Web.objects.filter(dcw_producto_id=body_data['producto'], dcw_creado_por=request.user, dcw_status=False).delete()
    
    contenid={
        'delete':body_data['producto'],
    }
    return JsonResponse(status=201, data=contenid)

#se cambio el template a la versión 2 
class CheckoutView(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('inicio')
    redirect_field_name = 'redirect_to'
    template_name = "web/V2/checkout.html"
    def post(self, request, *args, **kwargs):
        post_dom = request.POST.get('dominicio')        
        url='/'     
        if post_dom == '0':
            form = DomicilioForm(request.POST)
            if form.is_valid():
                Domicilio.objects.filter(dom_creador=self.request.user).update(dom_activo=False)
                form.instance.dom_activo=True
                form.instance.dom_creador=request.user
                dom_new = form.save()
                
                obj_c=CompraWeb(
                    cw_cliente=request.user,
                    cw_domicilio_id=dom_new.pk
                )
                obj_c.save()
                detalle_compra=Detalle_Compra_Web.objects.filter(dcw_creado_por=self.request.user, dcw_status=False)
                for item in detalle_compra:
                    Producto.objects.filter(producto_codigo=item.dcw_producto_id).update(prducto_existencia=F('prducto_existencia')-item.dcw_cantidad)
                detalle_compra.update(dcw_pedido_id=obj_c, dcw_status=True)
                messages.success(request, 'Su compra ha sido realizada el pago es efectuado en la entrega del paquete en el domicilio.')
                url=reverse_lazy('web:compras_web')
                               
            else:
                messages.success(request, 'Asegurece de rellenar todos los datos del domicilio')
                url=reverse_lazy('web:checkout')
                              
        else:
            obj_c=CompraWeb(
                cw_cliente=request.user,
                cw_domicilio_id=post_dom
            )
            obj_c.save()
            detalle_compra=Detalle_Compra_Web.objects.filter(dcw_creado_por=self.request.user, dcw_status=False)
            for item in detalle_compra:
                Producto.objects.filter(producto_codigo=item.dcw_producto_id).update(prducto_existencia=F('prducto_existencia')-item.dcw_cantidad)
            detalle_compra.update(dcw_pedido_id=obj_c, dcw_status=True)
            messages.success(request, 'Su compra ha sido realizada el pago es efectuado en la entrega del paquete en el domicilio.')
            url=reverse_lazy('web:compras_web')
           
        
        
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



class BlogViewSingle(DetailView):
    model = Blog
    template_name = 'web/blog_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_relacionado'] = Blog.objects.filter(blog_categoria=self.object.blog_categoria).exclude(blog_id=self.object.blog_id).order_by('-blog_creado')[:2]
        context['blog_reciente'] = Blog.objects.exclude(blog_id=self.object.blog_id).order_by('-blog_creado')[:6]
        context['banners'] = Blog.objects.filter(blog_tipo=5).order_by('-blog_creado')
        return context
    


# Pagina computel v2 parte fea lic leo
class NuestraEmpresa(TemplateView):
    template_name = "web/V2/nuestraempresa.html"

class PoliticasDevoluciones(TemplateView):
    template_name = "web/V2/politicas.html"

class ServicioCliente(TemplateView):
    template_name = "web/V2/serviciocliente.html"

class Contacto(CreateView):
    model = CorreoCco
    form_class = CorreoForm
    template_name = 'web/V2/contacto.html'
    success_url=reverse_lazy("web:inicio")
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['blog_relacionado'] = Blog.objects.filter(blog_categoria=self.object.blog_categoria).exclude(blog_id=self.object.blog_id).order_by('-blog_creado')[:2]
    #     context['blog_reciente'] = Blog.objects.exclude(blog_id=self.object.blog_id).order_by('-blog_creado')[:6]
    #     context['banners'] = Blog.objects.filter(blog_tipo=5).order_by('-blog_creado')
    #     return context

class ProductoDetalleViewV2(DetailView):
    model = Producto
    template_name="web/V2/detalle_producto.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.producto_linea != None:
            context['prod_relacionado']=Producto.objects.filter(producto_linea=self.object.producto_linea).exclude(producto_codigo=self.object)            
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        cantidad_prod = request.POST.get('quantity')
        pk = kwargs.get('pk')
        producto_obj = Producto.objects.get(producto_codigo=pk)

        suma_prod_futura = Detalle_Compra_Web.objects.filter(dcw_producto_id=pk, dcw_status=False).aggregate(suma=Sum('dcw_cantidad'))['suma']
        suma_prod_futura = 0 if suma_prod_futura == None else suma_prod_futura
        total_suma_pendiente=suma_prod_futura + int(cantidad_prod)

        if int(cantidad_prod) <= 0:
            messages.warning(request, 'Cantidad de producto debe ser mayor a 0.')
            return self.render_to_response(context=context) 
        elif total_suma_pendiente <= producto_obj.prducto_existencia: 
            try:
                find_prod_user = Detalle_Compra_Web.objects.get(dcw_creado_por=request.user, dcw_status=False, dcw_producto_id=pk)
                Detalle_Compra_Web.objects.filter(dcw_creado_por=request.user, dcw_status=False, dcw_producto_id=pk).update(dcw_cantidad=F('dcw_cantidad')+int(cantidad_prod))
            except ObjectDoesNotExist as erro:
                dt_cw=Detalle_Compra_Web(dcw_producto_id=producto_obj, dcw_cantidad=cantidad_prod, dcw_creado_por=request.user, dcw_precio=producto_obj.producto_precio)
                dt_cw.save()
            # conteo_shop=Detalle_Compra_Web.objects.filter(dcw_creado_por=request.user, dcw_status=False).count()           
            messages.success(request, '¡Producto agregado correctamente!')
            return self.render_to_response(context=context) 
        else:          
            messages.warning(request, 'Supera el limite de producto en existencia')
            return self.render_to_response(context=context) 