from django import forms
from aplicaciones.fuds.models import Fud,Motivo,Conformidad,Tramite,Zona,Vendedores,PartidasFud,Clientes
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
            'NumeroCliente': forms.TextInput(attrs={'readonly':'true'}),
            'Descuento': forms.TextInput(attrs={'min':'0', 'max':'15','type':'number'}),
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

        widgets ={
            'FechaFactura': forms.DateInput(attrs={'type':'date', 'min':context['minimo'],'max':context['maximo']}),
            'observaciones': forms.Textarea(),
            'Descuento': forms.TextInput(attrs={'min':'0', 'max':'15','type':'number'}),
        }

    def __init__(self, *args, **kwargs):
        super(FudFormEdit, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class FudFormEdit2(forms.ModelForm):
    class Meta:
        hoy=datetime.now()
        dias = timedelta(days=90)
        hoy_menos_90_dias=hoy-dias
        context={}
        context['maximo']= hoy.strftime("%Y-%m-%d")
        context['minimo']= hoy_menos_90_dias.strftime("%Y-%m-%d")
        model = Fud
        exclude = ['creado_por','FechaFactura']

        widgets ={
            'observaciones': forms.Textarea(),
            'Descuento': forms.TextInput(attrs={'min':'0', 'max':'15','type':'number'}),
        }

    def __init__(self, *args, **kwargs):
        super(FudFormEdit2, self).__init__(*args, **kwargs)

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

class ClientForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Clientes
        exclude = ['Client_FechaAlta']

    def __init__(self, *args, **kwargs):
        super(ClientEditForm, self).__init__(*args, **kwargs)
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