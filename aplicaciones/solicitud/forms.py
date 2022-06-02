from django import forms
from aplicaciones.solicitud.models import TipoServicio, Servicio, ESTATUS
from aplicaciones.empresa.models import Empresa
class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = (
            's_empresa',
            's_tipo',
            's_equipo',
            's_serie',
            's_reporte',
            's_img_report',
        )        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ServicioValidarForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = (
            's_provedor_aut',
            's_serv_autorizado',
            's_presupuesto',          
        )        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ServicioCerrarForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = (
            's_img_report_close',
            's_reporte_close',   
        )        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})



class FiltroServicioForm(forms.Form): 
    s_fecha=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}, format='%Y-%m-%d'), required=False, label='Fecha inicio')
    s_fecha2=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}, format='%Y-%m-%d'), required=False, label='Fecha fin')
    s_tipo=forms.ModelChoiceField(queryset=TipoServicio.objects.all(), required=False, label="Tipo servicio")
    s_empresa=forms.ModelChoiceField(queryset=Empresa.objects.all(), required=False, label="Empresa")
    s_estatus=forms.ChoiceField(choices=(('', '-----'),)+ESTATUS, required=False, label='Estatus')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
