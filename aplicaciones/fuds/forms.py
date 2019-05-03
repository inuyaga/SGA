from django import forms
from aplicaciones.fuds.models import Fud,Motivo,Conformidad,Tramite,Zona,Vendedores,PartidasFud
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
            'observaciones': forms.Textarea(),
        }


    def __init__(self, *args, **kwargs):
        super(FudForm, self).__init__(*args, **kwargs)
        # hoy=datetime.now()
        # self.fields['Factura'].queryset = Factura.objects.filter(FechaFactura__gte =  hoy- timedelta(days=90))

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
class FudFormEdit(forms.ModelForm):
    class Meta:
        hoy=datetime.now()
        dias = timedelta(days=90)
        hoy_menos_90_dias=hoy-dias
        context={}
        context['maximo']= hoy.strftime("%Y-%m-%d")
        context['minimo']= hoy_menos_90_dias.strftime("%Y-%m-%d")
        model = Fud
        exclude = ['creado_por']

    def __init__(self, *args, **kwargs):
        super(FudFormEdit, self).__init__(*args, **kwargs)

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
class TramiteForm(forms.ModelForm):
    class Meta:
        model = Tramite
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(TramiteForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(ZonaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedores
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(VendedorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class PartidaFudForm(forms.ModelForm):
    class Meta:
        model = PartidasFud
        # fields = ('__all__')
        exclude = ['Partida_fud']
    def __init__(self, *args, **kwargs):
        super(PartidaFudForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})