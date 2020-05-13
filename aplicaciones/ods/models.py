from django.db import models
from aplicaciones.activos.models import Asignacion
from aplicaciones.pedidos.models import Producto
from aplicaciones.empresa.models import Empresa, Departamento
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
Usuario = settings.AUTH_USER_MODEL
TIPO_SERVICIO=((1, 'Preventivo'), (2, 'Correctivo'))
STATUS=((1, 'Abierto'), (2, 'Asignado y en Proceso'), (3, 'Soporte terminado'), (4, 'Cerrado'))

# Create your models here.

class OrdenServicio(models.Model): 
    ods=models.BigAutoField(primary_key=True)
    ods_adicion=models.DateField(auto_now_add=True) 
    ods_asignacion=models.ForeignKey(Asignacion, verbose_name='Seleccione asignación', on_delete=models.CASCADE, blank=False, null=True)
    ods_delegar=models.ForeignKey(Empresa, verbose_name='Empresa ala que desea delegar orden de servicio', on_delete=models.CASCADE)
    ods_user_creo=models.ForeignKey(Usuario, verbose_name='Usuario creó', on_delete=models.CASCADE)
    ods_user_seguimiento=models.ForeignKey(Usuario, verbose_name='Usuario tecnico atendiendo ods', related_name='UserTecnicoOds', on_delete=models.CASCADE, blank=True, null=True)
    ods_tipo_serv=models.IntegerField('Tipo de servicio',choices=TIPO_SERVICIO)
    ods_falla_rep=models.CharField('Falla reportada por el usuario', max_length=600, blank=False, null=True)
    ods_diagnostico=models.CharField('Diagnostico Tecnico', max_length=600, blank=False, null=True)
    ods_observacion=models.CharField('Observaciones', max_length=600, blank=False, null=True)
    ods_doc=models.FileField('PDF firmado', upload_to='ods/documento/validacion', blank=False, null=True)
    ods_status=models.IntegerField('Estatus',choices=STATUS) 
    def __str__(self):
        return "ODS N°:{}".format(self.ods)
    class Meta:
        permissions = [('usuario_soporte_tecnico_ods', 'Usuario soporte tecnico')]


class Refaccion(models.Model):
    ref=models.BigAutoField(primary_key=True)
    ref_ods=models.ForeignKey(OrdenServicio, verbose_name='Elija un ODS', on_delete=models.CASCADE, blank=False, null=True)
    ref_produc=models.ForeignKey(Producto, verbose_name='Elija un producto', on_delete=models.CASCADE)
    ref_departamento=models.ForeignKey(Departamento, verbose_name='Departamento', on_delete=models.CASCADE, blank=False, null=True)
    ref_add_fecha=models.DateField(auto_now_add=True)
    ref_precio=models.FloatField('Precio refaccion')
    ref_cantidad=models.FloatField('Cantidad', validators=[MinValueValidator(1)])
    ref_obsrv=models.CharField('Observacion',max_length=200)

    def subtotal(self):
        sub_t=self.ref_precio * self.ref_cantidad
        return round(sub_t, 2)
    def __str__(self):
        return "Refación ID: {} ODS: {}".format(self.ref, self.ref_produc)
