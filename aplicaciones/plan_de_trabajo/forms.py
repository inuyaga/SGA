from django import forms
from aplicaciones.plan_de_trabajo.models import Registro_actividad
import datetime
import time
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
class Registro_actividadForm(forms.ModelForm):
    class Meta:
        model=Registro_actividad
        fields = ('__all__')
        fecha=timezone.localtime(timezone.now())
        widgets ={
            'ra_hora_inicio': forms.TextInput(attrs={'readonly':True},),
        } 
    

    # ra_hora_inicio = forms.TimeField(initial=datetime.time()) 