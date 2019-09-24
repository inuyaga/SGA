from django import forms
from aplicaciones.activos.models import Activo, Especificacion, Categoria, Asignacion, TramiteBaja, TemplateItem, TemplateItemGroup

class ActivoInitForm(forms.ModelForm):
    class Meta:
        model = Activo
        # fields = '__all__'
        exclude = ['activo_situacion']

    def __init__(self, *args, **kwargs):
        super(ActivoInitForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
class ActivoForm(forms.ModelForm):
    class Meta:
        model = Activo
        # fields = '__all__'
        exclude = ['activo_situacion']

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
            
        # self.fields['esp_tiene_costo'].widget.attrs.update({'class': 'custom-control-input'})

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


class AsignacionValidarForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        # fields = '__all__'
        fields = ('asig_archivo_dig',)
        help_texts = {'asig_archivo_dig': "Documento valido y firmado correctamnete",}
    def __init__(self, *args, **kwargs):
        super(AsignacionValidarForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class AsignacionReasignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        # fields = '__all__'
        fields = ('asig_user','asig_observacion')
        widgets = {
            'asig_observacion': forms.Textarea(attrs={'cols': 80, 'rows': 5}), 
        }
    def __init__(self, *args, **kwargs):
        super(AsignacionReasignacionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class TramiteBajaForm(forms.ModelForm):
    class Meta:
        model = TramiteBaja
        # fields = '__all__'
        fields = ('tb_activo','tb_observacion')
        widgets = {
            'tb_observacion': forms.Textarea(attrs={'cols': 80, 'rows': 5}), 
        }
    def __init__(self, *args, **kwargs):
        super(TramiteBajaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        self.fields['tb_activo'].queryset=Asignacion.objects.filter(asig_estado=1)

class TramiteBajaValidarForm(forms.ModelForm):
    class Meta:
        model = TramiteBaja
        # fields = '__all__'
        fields = ('tb_validado',)
    def __init__(self, *args, **kwargs):
        super(TramiteBajaValidarForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class TemplateItemForm(forms.ModelForm):
    class Meta:
        model = TemplateItem
        fields = '__all__'
        # fields = ('tb_validado',)
    def __init__(self, *args, **kwargs):
        super(TemplateItemForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class TemplateItemGroupForm(forms.ModelForm):
    class Meta:
        model = TemplateItemGroup
        fields = '__all__'
        widgets = {
            'itmg_items': forms.SelectMultiple(attrs={'size': 30,}), 
        }
    def __init__(self, *args, **kwargs):
        super(TemplateItemGroupForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        