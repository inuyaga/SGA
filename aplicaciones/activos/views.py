from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView, View
from aplicaciones.activos.models import Categoria, Activo, Especificacion, Asignacion, TramiteBaja, ESTADO, VIDA_ACTIVO, SITUACION
from aplicaciones.pedidos.models import Marca
from aplicaciones.activos.forms import (CategoriaForm, EspecificacionForm, ActivoForm, AsignacionForm, AsignacionValidarForm, AsignacionReasignacionForm,
TramiteBajaForm, TramiteBajaValidarForm)
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from io import BytesIO

from django.contrib.sites.shortcuts import get_current_site

from django.utils.formats import localize

from aplicaciones.empresa.models import Pertenece_empresa
#Librerias reportlab a usar:
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm



from reportlab.lib.units import inch
from django.contrib.humanize.templatetags.humanize import intcomma, naturalday
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT, TA_LEFT
PAGE_WIDTH = letter[0]
PAGE_HEIGHT = letter[1]



import qrcode.image.svg
from svglib.svglib import svg2rlg
import tempfile
import datetime 
import qrcode
from reportlab.lib.utils import ImageReader
from io import StringIO
from reportlab.graphics import renderPDF
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
        context['vida'] = VIDA_ACTIVO 
        context['situacion'] = SITUACION 
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
        status=self.request.GET.get('status')
        situacion=self.request.GET.get('situacion')
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
        if status != None:
            queryset=queryset.filter(activo_status=status)
        if situacion != None:
            queryset=queryset.filter(activo_situacion=situacion)
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
    paginate_by=100
    template_name='activos/asignacion_list.html'  

    def get_context_data(self, **kwargs):
        # from aplicaciones.pedidos.models import Detalle_pedido, Tipo_Pedido, Pedido
        context = super(AsignacionList, self).get_context_data(**kwargs)
        context['estado'] = ESTADO
        urls_formateada = self.request.GET.copy()
        if 'page' in urls_formateada:
            del urls_formateada['page']
        context['urls_formateada'] = urls_formateada 
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        search_status=self.request.GET.get('search_status')
        search_id=self.request.GET.get('search_id')
        if search_status != None:
            queryset=queryset.filter(asig_estado=search_status)
        
        if search_id != None:
            queryset=queryset.filter(id=search_id)
        
        return queryset


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

class AsignacionValidar(UpdateView):
    model=Asignacion 
    template_name="activos/activo_crear.html"
    form_class=AsignacionValidarForm
    success_url=reverse_lazy('activos:activo_asignar_list') 

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.asig_estado=1
        ID_activo=form.instance.asig_activo.activo
        Activo.objects.filter(activo=ID_activo).update(activo_situacion=1)
        # self.object = form.save()
        return super().form_valid(form) 
    
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        url = "{}?{}".format(self.success_url, self.request.GET.urlencode())  
           
        return url  # success_url may be lazy

class ReasignacionActivo(UpdateView):
    model=Asignacion 
    template_name="activos/activo_crear.html"
    form_class=AsignacionReasignacionForm
    success_url=reverse_lazy('activos:activo_asignar_list') 

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user_reasignado=form.instance.asig_user
        activo=form.instance.asig_activo
        observacion=form.instance.asig_observacion
        id_asig=self.kwargs.get('pk')
        # ACTUALIZACION DE HISTORICO
        Asignacion.objects.filter(id=id_asig).update(asig_estado=2, asig_user_edit=user_reasignado)
        # CREACION NUEVA ASIGNACION
        new_asig=Asignacion(asig_activo=activo,asig_user=user_reasignado, asig_observacion=observacion, asig_user_edit=self.request.user)
        new_asig.save() 

        url=reverse('activos:activo_asignar_list')
        return redirect(url)







class GeneraPdfAsignacion(View):

    def myFirstPage(self, canvas, doc):
        # CABECERA DE PAGINA 
        Title = "RESGUARDO Y ASIGNACIÓN DE EQUIPOS"
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 50, Title)
        
        # Footer.
        canvas.setFont('Times-Roman', 12)
        canvas.drawString( PAGE_WIDTH/6, 1.5*cm, '   Sra. Tere Vázquez Arce')
        canvas.drawString( PAGE_WIDTH/6, 0.9*cm, '______________________    __________________    ____________________')
        canvas.drawString( PAGE_WIDTH/6, 0.5*cm, 'Autoriza Direccion General   Asigna Sub Gerente TI    Nombre y Firma usuario')



        canvas.restoreState()

    def get_espfic(self, list, stylo):
        temporal=[]
        for item in list:
            temporal.append(Paragraph("✔ {}".format(item.esp_item), stylo))
        return temporal
    
    def make_qr_code_drawing(self, data, size):
        qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=size, border=4)
        qr.add_data(data)
        qrcode_svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage)
        svg_file = tempfile.NamedTemporaryFile()
        qrcode_svg.save(svg_file)  # store as an SVG file
        svg_file.flush()
        qrcode_rl = svg2rlg(svg_file.name)  # load SVG file as reportlab graphics
        svg_file.close()
        return qrcode_rl

    
    def get(self, request, *args, **kwargs):
        id_resguardo=self.kwargs.get('id_resguardo')
        get_asignacion=Asignacion.objects.get(id=id_resguardo)
        
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

        folio_format = ParagraphStyle('parrafo', alignment = TA_LEFT, fontSize = 10, fontName="Times-Roman")
        # title = ParagraphStyle('titulo', alignment = TA_CENTER, fontSize = 12, fontName="Times-Roman")
        parrafo2 = ParagraphStyle('parrafo', alignment = TA_RIGHT, fontSize = 10, fontName="Times-Roman")
        parrafo = ParagraphStyle('parrafo', alignment = TA_LEFT, fontSize = 10, fontName="Times-Roman")
        aviso_empresa_style = ParagraphStyle('parrafo', alignment = TA_JUSTIFY, fontSize = 8, fontName="Times-Roman", spaceBefore=15)

        tabla_body=ParagraphStyle('t_body', alignment = TA_LEFT, fontSize = 8, fontName="Times-Roman")
        tabla_head=ParagraphStyle('t_head', alignment = TA_CENTER, fontSize = 9, fontName="Times-Roman")
        
        items = []

        
        depo=Pertenece_empresa.objects.get(pertenece_id_usuario=get_asignacion.asig_user)

        folio_txt="<strong>FOLIO N°:</strong><em><u>{}</u></em>".format(get_asignacion.id)
        p=Paragraph(folio_txt, folio_format)
        items.append(p)

        txt2="<strong>Fecha:</strong>{}".format(localize(get_asignacion.asig_fecha_adicion))
        p=Paragraph(txt2, parrafo2)
        items.append(p)

        texto="<strong>Usuario:</strong> <em><u>{}</u></em>  <strong>Departamento:</strong><em><u>{}</u></em>".format(get_asignacion.asig_user.get_full_name(), depo.pertenece_empresa)
        p=Paragraph(texto, parrafo)
        items.append(p)

        
        texto="Por este medio Comercializadora computel del sureste me asigna las siguientes claves, derechos y equipos para desarrollar las actividades para que fui contratado, es mi responsabilidad, el uso, manejo y protección de la información que en ellos pose, asi como mantener limpios lo equipos y tener los debidos cuidados para mantenerse en buen estado."
        p=Paragraph(texto, aviso_empresa_style)
        items.append(p)

        texto="De detectar cambios en el sofware/hardware(programas no autorizados) seré sancionado de acuerdo a la gravedad y segun las politicas del departamento de TI."
        p=Paragraph(texto, aviso_empresa_style)
        items.append(p) 
        
        
        t_titulos=(
            Paragraph('EQUIPO', tabla_head), 
            Paragraph('DESCRIPCIÓN', tabla_head), 
            Paragraph('ADICIONAL', tabla_head), 
            Paragraph('SERIE', tabla_head), 
            Paragraph('COD. INVENT', tabla_head), 
            Paragraph('MARCA/MODELO', tabla_head))
        t_body=[(
            Paragraph(get_asignacion.asig_activo.activo_categoria.cat_nombre, tabla_body), 
            Paragraph(get_asignacion.asig_activo.activo_nombre, tabla_body), 
            self.get_espfic(Especificacion.objects.filter(esp_activo=get_asignacion.asig_activo), tabla_body), 
            Paragraph(get_asignacion.asig_activo.activo_serie, tabla_body), 
            Paragraph(str(get_asignacion.asig_activo.activo), tabla_body), 
            Paragraph("{}/{}".format(get_asignacion.asig_activo.activo_marca, get_asignacion.asig_activo.activo_modelo), tabla_body)
            )]
        t = Table([t_titulos] + t_body, colWidths=[2 * cm, 3 * cm, 4 * cm, 3 * cm, 2 * cm, 4 * cm])
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (5, -1), 1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))

        items.append(t)


        texto="<strong>OBSERVACIÓN:</strong>{}".format(get_asignacion.asig_observacion)
        p=Paragraph(texto, aviso_empresa_style)
        items.append(p) 


        current_site = str(get_current_site(self.request))
        revers=reverse_lazy('activos:activo_asignar_pdf', args={id_resguardo:get_asignacion.id})
                
        url="http://{}{}".format(current_site, revers)
        
        qrcode_rl = self.make_qr_code_drawing(url, 8)

        items.append(qrcode_rl)

            

        doc.build(items, onFirstPage=self.myFirstPage) 
        response.write(buff.getvalue())
        buff.close()
        return response

class TramiteBajaList(ListView):
    model=TramiteBaja
    paginate_by=100
    template_name='activos/tramite_baja_list.html'  

    def get_context_data(self, **kwargs):
        # from aplicaciones.pedidos.models import Detalle_pedido, Tipo_Pedido, Pedido
        context = super().get_context_data(**kwargs)
        urls_formateada = self.request.GET.copy()
        if 'page' in urls_formateada:
            del urls_formateada['page']
        context['urls_formateada'] = urls_formateada 
        return context

    

class TramiteBajaCrear(CreateView):
    model=TramiteBaja
    template_name="activos/activo_crear.html"
    form_class=TramiteBajaForm
    success_url=reverse_lazy('activos:tb_list') 
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.tb_user_edit=self.request.user
        asignacion=form.instance.tb_activo
        asg=Asignacion.objects.get(id=asignacion)
        Activo.objects.filter(activo=asg.asig_activo.activo).update(activo_status=5)
        return super().form_valid(form) 


class TramiteBajaUpdate(UpdateView):
    model=TramiteBaja
    template_name="activos/activo_crear.html"
    form_class=TramiteBajaValidarForm
    success_url=reverse_lazy('activos:tb_list') 
    def form_valid(self, form):
        """If the form is valid, save the associated model."""

        form.instance.tb_user_valido=self.request.user
        asignacion=form.instance.tb_activo.id
        asg=Asignacion.objects.get(id=asignacion)
        Asignacion.objects.filter(id=asignacion).update(asig_estado=2)
        Activo.objects.filter(activo=asg.asig_activo.activo).update(activo_status=6)
        return super().form_valid(form) 
