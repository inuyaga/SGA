from django import forms
from aplicaciones.gasto.models import *

class TipoGastoForm(forms.ModelForm): 
    class Meta:
        model = TipoGasto 
        fields = '__all__' 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class GastoForm(forms.ModelForm): 
    class Meta:
        model = Gasto 
        exclude = [
            'g_empresa',
            'g_userCreador',
            'g_estado',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})