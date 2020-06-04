from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from aplicaciones.inicio.models import User
# Register your models here.

from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('__all__')

class UserConfig(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'departamento', 'fecha_nacimiento', 'telefono', 'is_user_web', 'rfc')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(User, UserConfig)