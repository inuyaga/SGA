from django import forms
from aplicaciones.descargas.models import Descargas
from datetime import datetime, timedelta
# pylint: disable = E1101
class DescargasForm(forms.ModelForm):
    class Meta:
        model = Descargas
        exclude = ['compra_fechaCompra','compra_fechaLastChange','estatus']
        fields = ('__all__')
        widgets ={
            'observacion': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super(DescargasForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class DescargaEditForm(forms.ModelForm):
    class Meta:
        model = Descargas
        exclude = ['compra_fechaCompra','compra_fechaLastChange']
        widgets ={
            'observacion': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super(DescargaEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})