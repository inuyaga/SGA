from django.db import models
from django.contrib.auth import get_user_model
from aplicaciones.empresa.models import Cliente
from django.utils import timezone
from django.db import IntegrityError
Usuario = get_user_model()
# Create your models here.
class Plan_trabajo(models.Model): 
    pt=models.AutoField(primary_key=True, verbose_name='ID')
    pt_cliente=models.OneToOneField(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    pt_vendedor=models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario vendedor')
    pt_lunes=models.BooleanField(verbose_name='Lunes', default=False)
    pt_martes=models.BooleanField(verbose_name='Martes', default=False)
    pt_miercoles=models.BooleanField(verbose_name='Miercoles', default=False)
    pt_jueves=models.BooleanField(verbose_name='Jueves', default=False)
    pt_viernes=models.BooleanField(verbose_name='Viernes', default=False)
    pt_sabado=models.BooleanField(verbose_name='Sabado', default=False)
    pt_domingo=models.BooleanField(verbose_name='Domingo', default=False)

    class Meta:
        # verbose_name_plural = "Es parte de"
        verbose_name = "Plan de Trabajo"

    def __str__(self):
        return "{}".format(self.pt)


class Registro_actividad(models.Model):
    ra=models.AutoField(primary_key=True, verbose_name='ID')
    ra_cliente=models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    ra_hora_inicio=models.TimeField(verbose_name='Hora Inicio')
    ra_hora_final=models.TimeField(verbose_name='Hora Termino', auto_now_add=True)
    ra_monto_compra=models.FloatField('Monto de compra')
    ra_observacion=models.CharField(max_length=300, verbose_name='Observación')
    ra_fecha_creacion=models.DateField(auto_now_add=True, verbose_name='Creado')
    ra_user=models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario vendedor', null=True, blank=True)

    def __str__(self):
        return "{}".format(self.ra)
    class Meta:
        verbose_name = "Registro actividad vendedor"
        verbose_name_plural = "Registro actividad vendedores"
        unique_together = (("ra_cliente", "ra_fecha_creacion"),) 
        permissions = [('reg_activ_supervisor', 'Usuario con permiso de supervisor')]



