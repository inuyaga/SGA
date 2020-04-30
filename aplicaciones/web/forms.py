from django import forms
from aplicaciones.web.models import CorreoCco, RegistroExpo, Postulacion

class CooreoForm(forms.ModelForm):
    class Meta:
        model = CorreoCco
        fields = '__all__'
        widgets = {
        'corr_mensaje': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

    def __init__(self, *args, **kwargs):
        super(CooreoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class IncribirForm(forms.ModelForm):
    class Meta:
        model = RegistroExpo
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(IncribirForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(PostulacionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})