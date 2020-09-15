from django.contrib import admin
from aplicaciones.empresa.models import Empresa, Sucursal, Zona, Departamento, Cliente
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

import qrcode.image.svg
from svglib.svglib import svg2rlg
import qrcode
import tempfile

from django.http import HttpResponse
from io import BytesIO
#Librerias reportlab a usar:
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT, TA_LEFT
class EmpresaInstanceInline(admin.TabularInline):
    model = Sucursal


class DepartamentoInstanceInline(admin.TabularInline):
    model = Departamento


class AdminSuc(admin.ModelAdmin):
    inlines = [EmpresaInstanceInline]


class Suc(admin.ModelAdmin):
    raw_id_fields = ('sucursal_id_zona',)
    inlines = [DepartamentoInstanceInline]
    list_display = ('sucursal_nombre', 'sucursal_id_zona',
                    'sucursal_empresa_id',)


class DepoConfig(admin.ModelAdmin):
    list_display = ('departamento_nombre',
                    'departamento_id_sucursal', 'nombre_empresa',) 
    list_filter = ('departamento_id_sucursal__sucursal_empresa_id', 'departamento_id_sucursal')


# class ConfigEmpresa(admin.StackedInline):
#     model = Pertenece_empresa
#     can_delete = False
#     verbose_name_plural = 'Pertenece a'
#     raw_id_fields = ['pertenece_empresa', ]


# class UserAdminConfig(BaseUserAdmin):
#     inlines = (ConfigEmpresa,)

class ClienteConfigAdmin(admin.ModelAdmin):
    list_display = [
        'cli',
        'cli_clave',
        'cli_nombre',
        'cli_calle',
        'cli_colonia',
        'cli_cp',
        'cli_estado',
        'cli_telefono',
        'cli_rfc',
        'cli_email',
        'cli_status',
        'cli_vndedor_asignado',
        'cli_actualizado',
        ]
    search_fields = ['cli_clave', 'cli_nombre']
    list_filter = ['cli_status', 'cli_actualizado'] 
    actions = ['DowloadQRActions']

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
    def DowloadQRActions(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        buff = BytesIO()
        aviso_empresa_style = ParagraphStyle('parrafo', alignment = TA_JUSTIFY, fontSize = 8, fontName="Times-Roman", spaceBefore=15)
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=60,
                                bottomMargin=18,
                                title='QR Clientes'
                                )
        items = [] 
        
        for client in queryset:
            data_QR = self.make_qr_code_drawing(client.cli_clave, 15)
            texto="Cliente:{}".format(client.cli_nombre)
            p=Paragraph(texto, aviso_empresa_style)
            items.append(p) 
            items.append(data_QR)
        
        doc.build(items) 
        response.write(buff.getvalue())
        buff.close()
        return response
            
          
    DowloadQRActions.short_description = "Generar QR"



# Re-register UserAdmin
# admin.site.unregister(User)
admin.site.register(Empresa, AdminSuc)
admin.site.register(Sucursal, Suc)
admin.site.register(Zona)
admin.site.register(Departamento, DepoConfig)

admin.site.register(Cliente, ClienteConfigAdmin)