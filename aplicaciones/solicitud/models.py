import uuid
from django.db import models
from aplicaciones.empresa.models import Empresa, Departamento
from aplicaciones.inicio.models import User


class TipoServicio(models.Model):
    ts_nombre = models.CharField(max_length=250, verbose_name="Nombre")

    def __str__(self):
        return self.ts_nombre


ESTATUS = ((1, 'Creado'), (2, 'Validado'), (3, 'Autorizado'), (4, 'Cerrado'))


class Servicio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    s_fecha = models.DateField(auto_now_add=True, verbose_name="Creado")
    s_fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Modificación")
    s_empresa = models.ForeignKey(Empresa, verbose_name="Empresa solicitante", on_delete=models.CASCADE)
    s_depo = models.ForeignKey(Departamento, verbose_name="Departamento", on_delete=models.CASCADE)
    s_tipo = models.ForeignKey(TipoServicio, verbose_name="Tipo de Servicio", on_delete=models.CASCADE)
    s_user = models.ForeignKey(User, verbose_name="Usuario creador", on_delete=models.CASCADE)
    s_equipo = models.CharField(max_length=250, verbose_name="Unidad o Equipo")
    s_serie = models.CharField(max_length=250, verbose_name="Numero de Serie")
    s_reporte = models.TextField(verbose_name="Reporte")
    s_provedor_aut = models.CharField(verbose_name="Provedor Autorizado", max_length=250, blank=True, null=True)
    s_serv_autorizado = models.CharField(verbose_name="Servicio Autorizado", max_length=200, blank=True, null=True)
    s_presupuesto = models.FloatField(verbose_name="Presupuesto", blank=True, null=True)
    s_estatus = models.IntegerField(choices=ESTATUS, default=1, verbose_name="Estatus")
    s_user_cambio = models.ForeignKey(User, related_name="user_cambio", on_delete=models.CASCADE,
                                      verbose_name="Modifico")

    def __str__(self):
        return "{}".format(self.id)

    class Meta:
        permissions = [
            ('validar_servicio', 'Puede validar el servicio'),
            ('autorizar_servicio', 'Puede autorizar servicio'),
        ]
