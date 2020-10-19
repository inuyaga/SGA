from django import forms
from aplicaciones.web.models import CorreoCco, RegistroExpo, Postulacion, Domicilio, Blog
from tinymce.widgets import TinyMCE

class CorreoForm(forms.ModelForm):
    class Meta:
        model = CorreoCco
        fields = '__all__'
        widgets = {
        'corr_mensaje': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

    def __init__(self, *args, **kwargs):
        super(CorreoForm, self).__init__(*args, **kwargs)
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

class DomicilioForm(forms.ModelForm):
    class Meta:
        model = Domicilio
        # fields = '__all__'
        exclude = ['dom_activo', 'dom_creador']
    def __init__(self, *args, **kwargs):
        super(DomicilioForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 


        self.fields['dom_estado'].widget.attrs.update({':readonly': 'true'})
        self.fields['dom_delegacion'].widget.attrs.update({':readonly': 'true'})
        self.fields['dom_estado'].widget.attrs.update({'v-model': 'Estado'})
        self.fields['dom_delegacion'].widget.attrs.update({'v-model': 'Delegacion'})
        self.fields['dom_codigo_p'].widget.attrs.update({'v-model': 'code_postal'})
        self.fields['dom_codigo_p'].widget.attrs.update({'@blur': 'post_item()'})




class BlogForms(forms.ModelForm):
    blog_contenido = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Blog
        exclude = ('blog_portada','blog_pertenece',)
        widgets = {
        'blog_descripcion': forms.Textarea(attrs={"rows":3, "cols":80}),
        }