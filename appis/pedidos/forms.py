from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from appis.pedidos.models import UserCustom


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = UserCustom
        fields = ('pertenece_sucursal',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserCustom
        fields = ('pertenece_sucursal',)
