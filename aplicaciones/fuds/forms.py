from django import forms
from aplicaciones.fuds.models import Fud,Factura,Motivo,Conformidad
from datetime import datetime, timedelta
# pylint: disable = E1101
class FudForm(forms.ModelForm):
    class Meta:
        hoy=datetime.now()
        dias = timedelta(days=90)
        hoy_menos_90_dias=hoy-dias
        context={}
        context['maximo']= hoy.strftime("%Y-%m-%d")
        context['minimo']= hoy_menos_90_dias.strftime("%Y-%m-%d")
        model = Fud
        exclude = ['creado_por']
        # fields = ('__all__')
        widgets ={
            'FechaFactura': forms.DateInput(attrs={'type':'date', 'min':context['minimo'],'max':context['maximo']}),
        }


    def __init__(self, *args, **kwargs):
        super(FudForm, self).__init__(*args, **kwargs)
        hoy=datetime.now()
        self.fields['Factura'].queryset = Factura.objects.filter(FechaFactura__gte =  hoy- timedelta(days=90))

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        # exclude = ['']
        fields = ('__all__')
        # widgets ={
        #     'FechaFactura': forms.DateInput(attrs={'type':'date', 'min':context['minimo'],'max':context['maximo']}),
        # }


    def __init__(self, *args, **kwargs):
        super(FacturaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class MotivoForm(forms.ModelForm):
    class Meta:
        model = Motivo
        fields = ('__all__')


    def __init__(self, *args, **kwargs):
        super(MotivoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ConformidadForm(forms.ModelForm):
    class Meta:
        model = Conformidad
        fields = ('__all__')


    def __init__(self, *args, **kwargs):
        super(ConformidadForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})