from django import forms
from aplicaciones.ods.models import OrdenServicio, Refaccion
from aplicaciones.activos.models import Asignacion 
from ajax_select.fields import AutoCompleteSelectField

class OdsForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = ('ods_asignacion', 'ods_delegar', 'ods_tipo_serv', 'ods_falla_rep')
        # exclude = ['ods_user_creo', 'ods_user_seguimiento', '']
        widgets = {
            'ods_falla_rep': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        update = kwargs.pop('update')
        super(OdsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        if update:
            self.fields['ods_asignacion'].queryset=Asignacion.objects.filter(asig_estado=1)
        else:
            self.fields['ods_asignacion'].queryset=Asignacion.objects.filter(asig_estado=1, asig_user=user)  
            
         

class OdsSoporteTerminadoForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = ('ods_doc', )
        # exclude = ['ods_user_creo', 'ods_user_seguimiento', '']
    def __init__(self, *args, **kwargs):
        super(OdsSoporteTerminadoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class OdsSeguirForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        # fields = ('ods_asignacion', 'ods_delegar', 'ods_tipo_serv', 'ods_falla_rep')
        exclude = ('ods_asignacion', 
        'ods_delegar', 
        'ods_user_creo', 
        'ods_user_seguimiento',
        'ods_tipo_serv',
        'ods_falla_rep',
        'ods_diagnostico',
        'ods_observacion',
        'ods_doc',
        'ods_status',
        )
        # widgets = {
        #     'ods_falla_rep': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        # }
    def __init__(self, *args, **kwargs):
        super(OdsSeguirForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
class OdsTecnicoForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = ('ods_falla_rep', 'ods_diagnostico', 'ods_observacion')
        # exclude = ['ods_user_creo', 'ods_user_seguimiento', '']
        widgets = {
            'ods_falla_rep': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
            'ods_diagnostico': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
            'ods_observacion': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }
    def __init__(self, *args, **kwargs):
        super(OdsTecnicoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        self.fields['ods_falla_rep'].widget.attrs.update({'readonly': 'true'})

class RefaccionCrearForm(forms.ModelForm):
    class Meta:
        model = Refaccion
        # fields = ('ods_falla_rep', 'ods_diagnostico', 'ods_observacion')
        exclude = ['ref_precio', 'ref_ods', 'ref_departamento']
        widgets = {
            'ref_obsrv': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }
    ref_produc=AutoCompleteSelectField('productos_tags_ods',required=True, help_text='Escriba el codigo a buscar..', label='Codigo Producto')
    def __init__(self, *args, **kwargs):
        super(RefaccionCrearForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # self.fields['ods_falla_rep'].widget.attrs.update({'readonly': 'true'})