from django.db import models
from aplicaciones.pedidos.models import Area, Marca
from django.contrib.auth import get_user_model
Usuario = get_user_model()

ESTADO=((1, 'Vigente'), (2,'Historio'), (3, 'Pendiente'))
VIDA_ACTIVO=((1, 'Nuevo'), (2,'Buen estado'), (3,'Deteriorado'), (4,'-------'), (5,'Tramite de baja'), (6,'Baja'))
SITUACION=((1, 'Asignado'), (2,'Stock'))
# Create your models here.
class Categoria(models.Model):
    cat_area=models.ForeignKey(Area, verbose_name='Area a la que pertenece', on_delete=models.CASCADE)
    cat_nombre=models.CharField('Nombre de categoria', max_length=50, unique=True)
    def __str__(self):
        return self.cat_nombre

class Activo(models.Model): 
    activo=models.AutoField(primary_key=True)
    activo_nombre=models.CharField('Nombre', max_length=80)
    activo_categoria=models.ForeignKey(Categoria, verbose_name='Categoria a la que pertenece', on_delete=models.CASCADE)
    activo_marca=models.ForeignKey(Marca, verbose_name='Marca', on_delete=models.CASCADE)
    activo_modelo=models.CharField('Modelo', max_length=50)
    activo_serie=models.CharField('Serie', max_length=30)
    activo_codigo_barra=models.CharField('Codigo de Barra', max_length=20)
    activo_costo=models.FloatField('Costo de activo')
    activo_observacion=models.TextField('Observación')
    activo_status=models.IntegerField('Status', choices=VIDA_ACTIVO, default=2)
    activo_situacion=models.IntegerField('Situación del activo', choices=SITUACION, default=2)
    def __str__(self):
        return "ID:{} Activo:{} NS:{} --- CB:{}".format(self.activo, self.activo_nombre, self.activo_serie, self.activo_codigo_barra)

class Especificacion(models.Model):
    especificacion=models.AutoField(primary_key=True)
    esp_activo=models.ForeignKey(Activo, verbose_name='Activo perteneciente', on_delete=models.CASCADE)
    esp_item=models.CharField('Item', max_length=120)
    esp_valor=models.CharField('Especificación', max_length=100)
    esp_tiene_costo=models.BooleanField('Tiene algun costo?', default=False)
    esp_costo=models.FloatField('Costo de la especificacion', default=0.0)
    def __str__(self):
        return self.esp_item

class Asignacion(models.Model):
    asig_activo=models.ForeignKey(Activo, verbose_name='Seleccione activo', on_delete=models.CASCADE)
    asig_user=models.ForeignKey(Usuario, verbose_name='Usuario a asignar', on_delete=models.CASCADE) 
    asig_fecha_adicion=models.DateField(auto_now_add=True)
    asig_fecha_actualizacion=models.DateField(auto_now=True)
    asig_estado=models.IntegerField(choices=ESTADO, verbose_name='Status Asignación', default=3)
    asig_user_edit=models.ForeignKey(Usuario, verbose_name='Ultimo usuario editó', on_delete=models.CASCADE, related_name='UserEdit', blank=True, null=True)
    asig_archivo_dig=models.FileField('Archivo digitalizado', upload_to='AsignacionFiles/', blank=False, null=True)
    asig_observacion=models.CharField('Observacion', max_length=300)

    class Meta:
        ordering = ["asig_fecha_adicion"]

    def __str__(self):
        return "{} --> {}".format(self.asig_activo, self.asig_user)

    # class Meta: 
    #     unique_together = (("asig_activo", "asig_user"),)

class TramiteBaja(models.Model):
    tb_activo=models.ForeignKey(Asignacion, verbose_name='Seleccione activo asignado', on_delete=models.CASCADE)
    tb_fecha_creacion=models.DateField(auto_now_add=True)
    tb_fecha_actualizacion=models.DateField(auto_now=True)
    tb_observacion=models.CharField('Observacion o motivo por el cual se dará de baja',max_length=600)
    tb_validacion=models.FileField(upload_to='TramitesBajas/Files/', blank=True, null=True)
    tb_user_edit=models.ForeignKey(Usuario, verbose_name='Ultimo usuario editó', on_delete=models.CASCADE, blank=False, null=True)
    tb_user_valido=models.ForeignKey(Usuario, verbose_name='Usuario validó', on_delete=models.CASCADE, related_name='UserValido', blank=True, null=True)
    tb_validado=models.BooleanField('Validar Baja',default=0)
    class Meta:
        permissions = [('puede_validar_Tramite', 'Puede validar tramite de baja')]



    
    
