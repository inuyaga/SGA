from django.db import models
from aplicaciones.empresa.models import Cliente
from django.utils import timezone
from django.db import IntegrityError
from django.conf import settings
from django.utils.safestring import mark_safe
Usuario = settings.AUTH_USER_MODEL
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

TIPOVISITA = ((1, "Venta"), (2, "Cobranza"), (3, "Sin labor de venta"))
class VisitaVendedor(models.Model):
    vv_fecha=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    vv_cliente=models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    vv_vendedor=models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Vendedor')
    vv_latitude = models.FloatField(verbose_name='Latitude')
    vv_longitude = models.FloatField(verbose_name='Longitude')
    vv_numero_venta = models.IntegerField(verbose_name='N° Venta', null=True, blank=True)
    vv_monto_venta = models.FloatField(verbose_name='Monto Venta', null=True, blank=True)
    vv_numero_factura = models.CharField(max_length=20,verbose_name='N° Factura', null=True, blank=True)
    vv_monto_factura= models.FloatField(verbose_name='Monto Factura', null=True, blank=True) 
    vv_tipo = models.IntegerField("Tipo de visita", choices=TIPOVISITA, default=1)
    def mapa(self):
        return mark_safe('<a href="https://www.google.com/maps/search/?api=1&query={},{}" target="_blank">Sitio captura</a>'.format(self.vv_latitude, self.vv_longitude))
    mapa.allow_tags = True
