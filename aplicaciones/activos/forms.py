from django import forms
from aplicaciones.activos.models import Activo, Especificacion, Categoria, Asignacion

class ActivoForm(forms.ModelForm):
    class Meta:
        model = Activo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ActivoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class EspecificacionForm(forms.ModelForm):
    class Meta:
        model = Especificacion
        exclude = ('esp_activo',)
    def __init__(self, *args, **kwargs):
        super(EspecificacionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
        self.fields['esp_tiene_costo'].widget.attrs.update({'class': 'custom-control-input'})

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        # fields = '__all__'
        fields = ('asig_activo', 'asig_user', 'asig_observacion')
        widgets = {
            'asig_observacion': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
    def __init__(self, *args, **kwargs):
        super(AsignacionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['asig_activo'].queryset = Activo.objects.filter(activo_situacion=2)