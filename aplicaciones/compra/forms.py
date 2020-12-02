from django import forms
from aplicaciones.compra.models import Compra
from datetime import datetime, timedelta
# pylint: disable = E1101
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        exclude = ['creado_por']
        fields = ('__all__')
        widgets ={
            'compra_nota': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CompraEditForm(forms.ModelForm):
    class Meta:
        model = Compra
        exclude = ['compra_fechaCompra']

    def __init__(self, *args, **kwargs):
        super(CompraEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})