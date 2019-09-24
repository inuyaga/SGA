from django.db import models
from aplicaciones.activos.models import Asignacion
from aplicaciones.empresa.models import Empresa
from django.contrib.auth import get_user_model
Usuario = get_user_model()
TIPO_SERVICIO=((1, 'Preventivo'), (2, 'Correctivo'))
STATUS=((1, 'Abierto'), (2, 'Asignado'), (3, 'En Proceso'), (4, 'Finalizado'))

# Create your models here.

class OrdenServicio(models.Model):
    ods=models.BigAutoField(primary_key=True)
    ods_adicion=models.DateField(auto_now_add=True)
    ods_asignacion=models.ForeignKey(Asignacion, verbose_name='Seleccione asignación', on_delete=models.CASCADE)
    ods_delegar=models.ForeignKey(Empresa, verbose_name='Empresa ala que desea delegar orden de servicio', on_delete=models.CASCADE)
    ods_user_creo=models.ForeignKey(Usuario, verbose_name='Usuario creó', on_delete=models.CASCADE)
    ods_user_seguimiento=models.ForeignKey(Usuario, verbose_name='Usuario tecnico atendiendo ods', related_name='UserTecnicoOds', on_delete=models.CASCADE)
    ods_tipo_serv=models.IntegerField('Tipo de servicio',choices=TIPO_SERVICIO)
    ods_falla_rep=models.CharField('Falla reportada por el usuario', max_length=600)
    ods_diagnostico=models.CharField('Diagnostico Tecnico', max_length=600)
    ods_observacion=models.CharField('Observaciones', max_length=600)
    ods_doc=models.FileField('PDF fimrado', upload_to='ods/documento/validacion')
    ods_status=models.IntegerField('Estatus',choices=STATUS)

