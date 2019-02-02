from django import forms
from appis.pago_proveedor.models import Proveedor, Contrato

class NuevoProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ('proveedor_nombre', 'proveedor_rfc', 'proveedor_email',)
        widgets= {
        'proveedor_nombre' : forms.TextInput(),
        'proveedor_rfc': forms.TextInput(),
        'proveedor_email': forms.EmailInput(),
        }
    def __init__(self, *args, **kwargs):
        super(NuevoProveedorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ContratosForms(forms.ModelForm):
    class Meta:
        provedores=Proveedor.objects.all()
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
