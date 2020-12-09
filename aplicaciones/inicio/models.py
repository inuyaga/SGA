from django.db import models
from aplicaciones.empresa.models import Departamento
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    departamento=models.ForeignKey(Departamento, null=True, blank=True, on_delete=models.CASCADE)
    fecha_nacimiento=models.DateField('Fecha de nacimiento',default=None, null=True, blank=True)
    telefono=models.CharField('Telefono', null=True, blank=False, max_length=10)
    is_user_web = models.BooleanField(verbose_name="Es usuario web", default=False)
    rfc=models.CharField('RFC', null=True, blank=False, max_length=15)
    class Meta:
        db_table = 'auth_user' 