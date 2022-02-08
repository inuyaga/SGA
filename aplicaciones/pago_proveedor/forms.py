from django import forms
from aplicaciones.pago_proveedor.models import Proveedor, Contrato, Pago, Renta
from xml.dom.minidom import parse
from datetime import datetime
# pylint: disable = E1101
class NuevoProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ('proveedor_nombre', 'proveedor_rfc', 'proveedor_email','proveedor_cuenta','proveedor_banco')
        widgets= {
        'proveedor_nombre' : forms.TextInput(),
        'proveedor_rfc': forms.TextInput(),
        'proveedor_email': forms.EmailInput(),
        }
    def __init__(self, *args, **kwargs):
        super(NuevoProveedorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['proveedor_banco'].widget.attrs.update({'class': 'form-control text-uppercase'})
        self.fields['proveedor_rfc'].widget.attrs.update({'class': 'form-control text-uppercase'})

class ContratosForms(forms.ModelForm):
    class Meta:
        model = Contrato
        exclude = ['contrato_autorizado', 'contrato_status']
        widgets = {
        # 'contrato_proveedor_id' : forms.ModelChoiceField(queryset=provedores, empty_label="(Nothing)"),
        # 'contrato_documento' : forms.FileInput(),
        'contrato_fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        'contrato_fecha_termino' : forms.DateInput(attrs={'type': 'date'}),
        'contrato_dias_pago' : forms.TextInput(),
        'contrato_direccion' : forms.Textarea(attrs={'cols': 25, 'rows': 3}),
        'contrato_monto' : forms.NumberInput(),
        }
    def __init__(self, *args, **kwargs):
        super(ContratosForms, self).__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ContratosFormsEdit(forms.ModelForm):
    class Meta:
        model = Contrato
        exclude = ['contrato_status']
        widgets = {
        # 'contrato_fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        # 'contrato_fecha_termino' : forms.DateInput(attrs={'type': 'date'}),

        'contrato_dias_pago' : forms.TextInput(),
        'contrato_direccion' : forms.Textarea(attrs={'cols': 25, 'rows': 3}),
        'contrato_monto' : forms.NumberInput(),
        }
    def __init__(self, *args, **kwargs):
        super(ContratosFormsEdit, self).__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
            self.fields[field].widget.attrs.update({'class': 'form-control'})

# class FacturaForms(forms.ModelForm):
#     class Meta:
#         model = Factura
#         exclude = ['factura_creado', 'factura_pagado_status', 'factura_monto_total', 'factura_iva_trasladado', 'factura_iva_retenido', 'factura_isr_retenido']
#         widgets = {
#         'factura_corresponde_mes': forms.DateInput(attrs={'type': 'date'}),
#         }
#     def __init__(self, *args, **kwargs):
#         super(FacturaForms, self).__init__(*args, **kwargs)
#         hoy=datetime.now()
#         self.fields['factura_contrato_id'].queryset = Contrato.objects.filter(contrato_fecha_termino__gt=hoy)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-control'})

class PagoForms(forms.ModelForm):
    class Meta:
        model = Pago
        exclude = ['pago_creado', 'contrato_id',]
        # widgets = {
        # 'factura_corresponde_mes': forms.DateInput(attrs={'type': 'date'}),
        # }
    def __init__(self, *args, **kwargs):
        super(PagoForms, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

# class ComplementoForm(forms.ModelForm):
#     class Meta:
#         model = Complemento
#         exclude = ['complemento_creado', 'complemento_pago',]

#     def __init__(self, *args, **kwargs):
#         super(ComplementoForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-control'})

class NuevoDeptoCasaForm(forms.ModelForm):
    class Meta:
        model = Renta
        fields = '__all__'
        # fields = ('proveedor_nombre', 'proveedor_rfc', 'proveedor_email',)
        # widgets= {
        # 'proveedor_nombre' : forms.TextInput(),
        # 'proveedor_rfc': forms.TextInput(),
        # 'proveedor_email': forms.EmailInput(),
        # }
    def __init__(self, *args, **kwargs):
        super(NuevoDeptoCasaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})