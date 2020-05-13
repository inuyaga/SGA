from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView, UpdateView, DeleteView, ListView
from aplicaciones.ods.forms import OdsForm, OdsSeguirForm, OdsTecnicoForm, OdsSoporteTerminadoForm, RefaccionCrearForm
from aplicaciones.ods.models import OrdenServicio, STATUS, Refaccion
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Sum, F
from django.core.exceptions import ObjectDoesNotExist

from django.utils.formats import localize
# IMPORTACION DECORADOR PARA VEIFICACION DE PERMISOS
from django.utils.decorators import method_decorator
from aplicaciones.pago_proveedor.eliminaciones import get_deleted_objects
from django.contrib.auth.decorators import permission_required
#Librerias reportlab a usar:
from django.http import HttpResponse
from io import BytesIO
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,Paragraph, Table, TableStyle, Spacer)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT, TA_LEFT
PAGE_WIDTH = letter[0]
PAGE_HEIGHT = letter[1]

from aplicaciones.empresa.models import Departamento
class OrdenServiciotListView(ListView): 
    model = OrdenServicio
    paginate_by = 200
    template_name = "ods/OrdenServicioList.html" 

    def get_context_data(self, **kwargs):
        context = super(OrdenServiciotListView, self).get_context_data(**kwargs)
        urls_formateada = self.request.GET.copy()
        if 'page' in urls_formateada:
            del urls_formateada['page']
        context['urls_formateada'] = urls_formateada

        context['status']=STATUS 
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        ID=self.request.GET.get('ID')
        Status=self.request.GET.get('Status')

        if self.request.user.has_perm('ods.change_ordenservicio'):
            pass
        else:
            queryset=queryset.filter(ods_asignacion__asig_user=self.request.user)
        
        if ID != None:
            queryset=queryset.filter(ods=ID)
        if Status != None:
            queryset=queryset.filter(ods_status=Status)
        return queryset

    @method_decorator(permission_required('ods.view_ordenservicio',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrdenServicioCreateView(CreateView): 
    model = OrdenServicio
    form_class = OdsForm
    template_name = "ods/ods_crear.html"
    success_url = reverse_lazy('orden_serv:list_ods')

    def get_success_url(self):
        get=self.request.GET.copy()
        url=self.success_url+'?'+get.urlencode()
        return url

    def get_form_kwargs(self):
        # print(self.request.user.has_perm('ods.add_ordenservicio'))
        kwargs = super(OrdenServicioCreateView, self).get_form_kwargs()
        kwargs.update({
            'user':self.request.user,
            'update':self.request.user.has_perm('ods.change_ordenservicio'),
            })
        return kwargs 

    @method_decorator(permission_required('ods.add_ordenservicio',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

    def form_valid(self, form):
        # activo_id=form['asig_activo'].value()
        form.instance.ods_user_creo=self.request.user
        form.instance.ods_status=1
        return super().form_valid(form)

class OrdenServicioSeguirCreate(UpdateView): 
    model = OrdenServicio
    form_class = OdsSeguirForm
    template_name = "ods/ods_tecnico_dar_seguimiento.html"
    success_url = reverse_lazy('orden_serv:list_ods')

    def get_success_url(self):
        get=self.request.GET.copy()
        url=self.success_url+'?'+get.urlencode()
        return url

    @method_decorator(permission_required('ods.usuario_soporte_tecnico_ods',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # activo_id=form['asig_activo'].value()
        form.instance.ods_user_seguimiento=self.request.user
        form.instance.ods_status=2
        return super().form_valid(form)

class OrdenServicioTerminarSoporteCreate(UpdateView):  
    model = OrdenServicio
    form_class = OdsSeguirForm 
    template_name = "ods/ods_terminar_soporte.html"
    success_url = reverse_lazy('orden_serv:list_ods')

    def get_success_url(self):
        get=self.request.GET.copy()
        url=self.success_url+'?'+get.urlencode()
        return url

    @method_decorator(permission_required('ods.usuario_soporte_tecnico_ods',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # activo_id=form['asig_activo'].value()
        form.instance.ods_status=3
        return super().form_valid(form)

class OrdenServicioEditTecnico(UpdateView):  
    model = OrdenServicio
    form_class = OdsTecnicoForm
    template_name = "ods/ods_crear.html"
    success_url = reverse_lazy('orden_serv:list_ods')

    def get_success_url(self):
        get=self.request.GET.copy()
        url=self.success_url+'?'+get.urlencode()
        return url

    @method_decorator(permission_required('ods.usuario_soporte_tecnico_ods',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrdenServicioDelete(DeleteView):
    model = OrdenServicio
    template_name = "pedidos/delete_forever.html"
    success_url=reverse_lazy('orden_serv:list_ods') 

    def get_success_url(self):
        get=self.request.GET.copy()
        url=self.success_url+'?'+get.urlencode()
        return url

    @method_decorator(permission_required('ods.delete_ordenservicio',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(OrdenServicioDelete, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrdenServicioDelete, self).get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

class OdsValidarPorUser(UpdateView):
    model = OrdenServicio
    form_class = OdsSeguirForm
    template_name = "ods/validar_ods_user.html"
    success_url = reverse_lazy('orden_serv:list_ods')

    def get_success_url(self):
        get=self.request.GET.copy()
        url=self.success_url+'?'+get.urlencode()
        return url

    @method_decorator(permission_required('ods.view_ordenservicio',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # activo_id=form['asig_activo'].value()
        id_ods=self.kwargs.get('pk')
        ods_object=OrdenServicio.objects.get(ods=id_ods)
        if ods_object.ods_asignacion.asig_user == self.request.user:
            form.instance.ods_status=4
            messages.add_message(self.request, messages.INFO, 'Orden de servicio validado por usuario')
        else:
            messages.add_message(self.request, messages.INFO, 'Solo el usuario asignado al activo puede validar  ')
        return super().form_valid(form)

class OdsGeneraPDF(View):
    id_osd=0
    ods_object=OrdenServicio.objects.none()
    def myFirstPage(self, canvas, doc):
        print('soy lo encabezado')
        # CABECERA DE PAGINA 
        Title = "ORDEN DE SERVICIO"
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - 50, Title)
        
        # # Footer.
        # canvas.setFont('Times-Roman', 7)
        # canvas.drawString( PAGE_WIDTH/6, 1.5*cm, '{}'.format(self.ods_object.ods_user_seguimiento.get_full_name()))
        # canvas.drawString( PAGE_WIDTH/6, 0.9*cm, '______________________    __________________    ____________________')
        # canvas.drawString( PAGE_WIDTH/6, 0.5*cm, 'Realizo Servicio   Asigna Sub Gerente TI    Nombre y Firma usuario')
        stylo = ParagraphStyle('firma_style', alignment=TA_CENTER, fontSize=6, fontName="Times-Roman")
        stylo2 = ParagraphStyle('firma_style', alignment=TA_CENTER, fontSize=8, fontName="Times-Bold")
        dta=[
            (Paragraph('Realizo Servicio', stylo2), Paragraph('Vo Bo', stylo2), Paragraph('Recibio', stylo2)),
            (Paragraph('{}({})'.format(self.ods_object.ods_user_seguimiento.get_full_name(), self.ods_object.ods_user_seguimiento), stylo), Paragraph('', stylo), Paragraph("{}".format(self.ods_object.ods_asignacion.asig_user.get_full_name()), stylo)),
            (Paragraph('Nombre y firma', stylo), Paragraph('Gerente o Sub Gerente', stylo), Paragraph('Nombre y firma usuario', stylo)),
            ]

        tabla=Table(dta, colWidths=[6 * cm, 6 * cm, 6 * cm])
        tabla.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (2, -1), 1, colors.dodgerblue),
                # ('LINEBELOW', (0, 0), (-1, 0), 0, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.transparent)
            ]
        ))
        tabla.wrapOn(canvas, PAGE_WIDTH, PAGE_HEIGHT)
        tabla.drawOn(canvas, 50, 0.6*cm)

        canvas.restoreState() 

    # @method_decorator(permission_required('ods.usuario_soporte_tecnico_ods',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        self.id_osd=self.kwargs.get('pk')
        self.ods_object=OrdenServicio.objects.get(ods=self.id_osd)
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        response = HttpResponse(content_type='application/pdf')
        buff = BytesIO()
        doc = SimpleDocTemplate(buff, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=18, title='Formato ODS')
        items = []
        data_tabla=[]


        stylo_p = ParagraphStyle('parrafo', alignment=TA_LEFT, fontSize=11, fontName="Times-Roman", spaceBefore=15) 
        stylo_titulo = ParagraphStyle('titulo', alignment=TA_CENTER, fontSize=11, fontName="Times-Bold")
        folio_format = ParagraphStyle('folio_serv', alignment = TA_LEFT, fontSize = 9, fontName="Times-Roman")
        fecha_format = ParagraphStyle('fecha_stylo', alignment = TA_RIGHT, fontSize = 9, fontName="Times-Roman")

        folio_txt="<strong>N° DE SERVICIO:</strong><em><u>{}</u></em>".format(self.ods_object.ods)
        p1=Paragraph(folio_txt, folio_format)
        # items.append(p)
        dta=[[p1]]

        folio_txt="<strong>FECHA:</strong><em><u>{}</u></em>".format(localize(self.ods_object.ods_adicion))
        p2=Paragraph(folio_txt, fecha_format)
        # items.append(p)

        dta=[(p1, p2)]

        tabla=Table(dta, colWidths=[9 * cm, 10 * cm])
        items.append(tabla)
        items.append(Spacer(0,20))



        
        dta=[
            ('Clave de equipo(ID activo):', self.ods_object.ods_asignacion.asig_activo.activo),
            ('Empresa:', request.user.departamento.departamento_id_sucursal.sucursal_empresa_id),
            ('Sucursal:', request.user.departamento.departamento_id_sucursal),
            ('Departamento:', request.user.departamento),
            ('Usuario:', "{}  -->  {}".format(self.ods_object.ods_asignacion.asig_user, self.ods_object.ods_asignacion.asig_user.get_full_name())),
            ('Tipo de Servicio:', self.ods_object.get_ods_tipo_serv_display()),
            ('Estado ods:', self.ods_object.get_ods_status_display()),
            ]
        
        
        
        
        

        tabla=Table(dta, colWidths=[5 * cm, 14 * cm])
        tabla.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (1, -1), 1, colors.dodgerblue),
                # ('LINEBELOW', (0, 0), (-1, 0), 0, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.transparent)
            ]
        ))
        items.append(tabla)
        items.append(Spacer(0,20))


        

        txt="FALLA REPORTADA POR EL USUSARIO" 
        p=Paragraph(txt, stylo_titulo)
        data_tabla =[[p]]
        

        txt="{}".format(self.ods_object.ods_falla_rep)
        p=Paragraph(txt, stylo_p)
        data_tabla += [[p]]

        txt="DIAGNOSTICO TECNICO"
        p=Paragraph(txt, stylo_titulo)
        data_tabla +=[[p]]
        txt="{}".format(self.ods_object.ods_diagnostico)
        p=Paragraph(txt, stylo_p)
        data_tabla +=[[p]]

        

        txt="OBSERVACIONES"
        p=Paragraph(txt, stylo_titulo)
        data_tabla +=[[p]]
        txt="{}".format(self.ods_object.ods_observacion)
        p=Paragraph(txt, stylo_p)
        data_tabla +=[[p]]
        

        tabla=Table(data_tabla, colWidths=[18 * cm]) 
        tabla.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (0, -1), 1, colors.dodgerblue),
                # ('LINEBELOW', (0, 0), (-1, 0), 0, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.transparent)
            ]
        ))
        items.append(tabla)
        
        

        doc.build(items, onFirstPage=self.myFirstPage) 
        response.write(buff.getvalue())
        buff.close()
        return response



# class RefaccionCrearOds(CreateView):
class RefaccionOdsList(ListView): 
    model = Refaccion
    # paginate_by = 200
    template_name = "ods/refaccion_list.html" 

    def get_context_data(self, **kwargs):
        context = super(RefaccionOdsList, self).get_context_data(**kwargs)
        suma_refaccion=Refaccion.objects.filter(ref_ods=self.kwargs.get('pk')).aggregate(suma_total=Sum(F('ref_precio') * F('ref_cantidad')))
        context['total_refaccion']=suma_refaccion['suma_total']
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset=queryset.filter(ref_ods=int(self.kwargs.get('pk')))
        return queryset


class RefaccionCrear(CreateView):
    model = Refaccion
    form_class = RefaccionCrearForm
    template_name = "ods/ods_crear.html"
    success_url = reverse_lazy('orden_serv:ods_refaccion')

    def form_valid(self, form):
        form.instance.ref_precio=form.instance.ref_produc.producto_precio
        ods_id=int(self.kwargs.get('ID_ods'))
        form.instance.ref_ods_id=ods_id
        form.instance.ref_departamento=form.instance.ref_ods.ods_asignacion.asig_user.departamento
        # id_user=form.instance.ref_ods.ods_asignacion.asig_user.departamento
        # try:
        #     depo=Pertenece_empresa.objects.get(pertenece_id_usuario=id_user) 
            
        # except ObjectDoesNotExist as obj_no_exits:
        #     messages.info(self.request, 'Es necesario que el usuario asignado al activo, esté asignado algun departamento')
        #     context = super().get_context_data()
        #     return render(self.request, self.template_name, context=context)
        return super().form_valid(form)

    def get_success_url(self):
        ursl_destino=reverse_lazy('orden_serv:ods_refaccion', kwargs={'pk':self.kwargs.get('ID_ods')})
        url=ursl_destino+'?'+self.request.GET.urlencode()
        return url


class RefaccionDelete(DeleteView):
    model = Refaccion
    template_name = "pedidos/delete_forever.html"
    success_url=reverse_lazy('orden_serv:ods_refaccion') 

    def get_success_url(self):
        ursl_destino=reverse_lazy('orden_serv:ods_refaccion', kwargs={'pk':self.kwargs.get('ID_ods')})
        url=ursl_destino+'?'+self.request.GET.urlencode()
        return url

    @method_decorator(permission_required('ods.delete_refaccion',reverse_lazy('inicio:need_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(RefaccionDelete, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RefaccionDelete, self).get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        #
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

    

