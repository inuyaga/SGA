from django import forms
from django.contrib.auth.forms import UserCreationForm
from aplicaciones.inicio.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('rfc','email','first_name','username', 'telefono')
        # widgets = {
        # 'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        # }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Razón social o Persona Física'
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['rfc'].widget.attrs.update({'v-model': 'rfc_vue'})
        self.fields['rfc'].widget.attrs.update({'@input': 'rfc_vue=$event.target.value.toUpperCase()'})
        self.fields['rfc'].widget.attrs.update({'@blur': 'eventText()'})

        self.fields['first_name'].widget.attrs.update({'v-model': 'first_name'})
        self.fields['email'].widget.attrs.update({'v-model': 'email'})