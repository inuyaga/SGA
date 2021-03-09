from django import forms
from aplicaciones.gasto.models import *
from django.forms.models import inlineformset_factory

from aplicaciones.empresa.models import Empresa, Departamento

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
            'g_depo',
            'g_userCreador',
            'g_estado',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ItemGastoForm(forms.ModelForm): 
    # itm_fecha_hora = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M:%S %Z"], widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))    
    class Meta:
        model = ItemGasto 
        exclude = [
            'itm_gastID',
            'itm_ok',            
        ]
        widgets = {
            'itm_fecha': forms.DateTimeInput(attrs={'type': 'date'}, format='%Y-%m-%d'),        
            'item_descripcion': forms.Textarea(attrs={"rows":2,}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    # def clean_itm_fecha_hora(self):
    #     itm_fecha_hora = self.cleaned_data['itm_fecha_hora']        
    #     my_date_time = datetime.strptime(itm_fecha_hora, '%Y-%m-%d %H:%M:%S')
    #     print(my_date_time)
    #     return my_date_time
        




class FiltrosGastoForm(forms.Form): 
    week=forms.DateField(widget=forms.DateInput(attrs={'type':'week'}, format='%Y-%m-%d'), required=False, label='Semana')
    departamento=forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)
    empresa=forms.ModelChoiceField(queryset=Empresa.objects.all(), required=False)
    # tip_gasto=forms.ModelChoiceField(queryset=TipoGasto.objects.all(), required=False, label='Tipo de Gasto')
    status=forms.ChoiceField(choices=((0, '-----'),)+STATUS, required=False, label='Estatus')
    
    # reembolsoID
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


ItemGastoInlineFormSet = inlineformset_factory(Gasto, ItemGasto, form=ItemGastoForm, extra=10, can_delete=True, validate_min=True)