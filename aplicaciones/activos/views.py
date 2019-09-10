from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView, View
from aplicaciones.activos.models import Categoria, Activo, Especificacion, Asignacion
from aplicaciones.pedidos.models import Marca
from aplicaciones.activos.forms import CategoriaForm, EspecificacionForm, ActivoForm, AsignacionForm
from django.urls import reverse_lazy
from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from io import BytesIO
#Librerias reportlab a usar:
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib import colors
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
    paginate_by=50

    @method_decorator(permission_required('activos.view_activo',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ActivoList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs): 
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['obj_list'] = Categoria.objects.all()
        context['list_marca'] = Marca.objects.all() 
        urls_formateada = self.request.GET.copy()
        if 'page' in urls_formateada:
            del urls_formateada['page']
        context['urls_formateada'] = urls_formateada 
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



class AsignacionList(ListView):
    model=Asignacion
    template_name='activos/asignacion_list.html'  

    def get_context_data(self, **kwargs):
        from aplicaciones.pedidos.models import Detalle_pedido, Tipo_Pedido, Pedido
        context = super(AsignacionList, self).get_context_data(**kwargs)

        return context

class AsignacionCrear(CreateView):
    model=Asignacion 
    template_name="activos/activo_crear.html"
    form_class=AsignacionForm
    success_url=reverse_lazy('activos:activo_asignar_list')
    def form_valid(self, form):
        activo_id=form['asig_activo'].value()
        Activo.objects.filter(activo=activo_id).update(activo_situacion=1)
        form.instance.asig_user_edit=self.request.user
        return super().form_valid(form)

class GeneraPdfAsignacion(View):
   
    def get(self, request, *args, **kwargs):
        from django.contrib.humanize.templatetags.humanize import intcomma
        from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "clientes.pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=60,
                                bottomMargin=18,
                                title='Asignacion de activo'
                                )

        title = ParagraphStyle('titulo', 
                           alignment = TA_CENTER,
                           fontSize = 12,
                           fontName="Times-Roman")
        
        items = []

        bogustext = ("RESGUARDO Y ASIGNACIÓN DE EQUIPOS")
        p = Paragraph(bogustext, title)
        items.append(p)
        doc.build(items) 
        # styles = getSampleStyleSheet()
        # total_detalles=DetallePedido.objects.filter(dtl_id_pedido=request.GET.get('pedido_id')).aggregate(total=Sum(F('dtl_cantidad')* F('dtl_precio'), output_field=FloatField()))
        
        # header = Paragraph("DETALLE DE PEDIDO N°"+request.GET.get('pedido_id'), styles['Heading1'])
        # pedido_get=Pedido.objects.get(ped_id_ped=request.GET.get('pedido_id'))
        # sucursal_num = pedido_get.ped_id_Suc.suc_numero
        # sucursal_direccion = pedido_get.ped_id_Suc.suc_direccion

        # txt_sucursal_num=Paragraph('N° de Sucursal: '+'N/A' if sucursal_num == None else  'N° de Sucursal: '+sucursal_num, styles['Heading4'])
        # txt_sucursal_direccion=Paragraph('Direccion: '+'N/A' if sucursal_direccion == None else 'Direccion: '+sucursal_direccion, styles['Heading4'])
        # items.append(header)
        # items.append(txt_sucursal_num)
        # items.append(txt_sucursal_direccion)
        # headings = ('Codigo', 'Descripción', 'Cantidad', 'Precio', 'Subtotal')
        # query_result = [(p.dtl_codigo, Paragraph(p.dtl_descripcion, styles['BodyText']), p.dtl_cantidad,p.dtl_precio, round(p.dtl_cantidad*p.dtl_precio, 2)) for p in DetallePedido.objects.filter(dtl_id_pedido=request.GET.get('pedido_id'))]
        
        # total=0
        # if total_detalles['total'] != None:
        #     total=round(total_detalles['total'], 2)
    
            

        # final_line=[('','','',Paragraph("Total", styles['Heading5']),Paragraph(intcomma(total), styles['Heading5']))]

        # t = Table([headings] + query_result+final_line, colWidths=[2.5 * cm, 10 * cm, 2 * cm, 2 * cm, 2 * cm])
        # t.setStyle(TableStyle(
        #     [
        #         ('GRID', (0, 0), (4, -1), 1, colors.dodgerblue),
        #         ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
        #         ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        #     ]
        # ))
        # items.append(t)
        # doc.build(items)
        response.write(buff.getvalue())
        buff.close()
        return response

        
    