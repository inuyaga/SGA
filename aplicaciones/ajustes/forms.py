from django import forms
from aplicaciones.ajustes.models import Ajuste, AjusteProduct, STATUS as STATUS_AJUSTE
from datetime import datetime, timedelta
from aplicaciones.empresa.models import Sucursal
# pylint: disable = E1101
class AjusteCreateForm(forms.ModelForm):
    # add_products=forms.CharField(label="Productos", help_text="Escriba codigo de producto para añadir", widget=forms.TextInput(attrs={'onkeyup':'onKeyUp(event)'}))
    class Meta:
        model = Ajuste
        exclude = ['aj_cresendo','aj_cresendo_salida', 'aj_producs', 'aj_sucursal', 'aj_status']
        # fields = ('__all__')
        # widgets ={
        #     'observacion': forms.Textarea(),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class AjusteUpdateForm(forms.ModelForm):
    # add_products=forms.CharField(label="Productos", help_text="Escriba codigo de producto para añadir", widget=forms.TextInput(attrs={'onkeyup':'onKeyUp(event)'}))
    class Meta:
        model = Ajuste        
        fields = ('aj_cresendo', 'aj_cresendo_salida')
        # widgets ={
        #     'observacion': forms.Textarea(),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class FiltroAjusteForm(forms.Form):
    id_aj = forms.IntegerField(required=False, label="ID")
    ajuste_crescendo = forms.IntegerField(required=False, label='Entrada')
    ajuste_crescendo_s = forms.IntegerField(required=False, label='Salida')
    sucursal = forms.ModelChoiceField(Sucursal.objects.all(), empty_label="Todo", required=False)    
    estatus = forms.ChoiceField(choices=STATUS_AJUSTE, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})             

        lst = list(self.fields['estatus']._choices)
        lst.insert(0, ('', 'Todo'))
        self.fields['estatus'].choices=lst