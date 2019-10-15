from django.db import models
from django.contrib.auth import get_user_model
Usuario = get_user_model()
STATUS=((1, 'Activo'), (2, 'Inactivo'))
# Create your models here.
# pylint: disable = E1101
class Empresa(models.Model):
    empresa_nombre = models.CharField(max_length=120, verbose_name='Nombre')
    empresa_tipo = models.CharField(max_length=20, verbose_name='Tipo de empresa')
    empresa_abrebiacion = models.CharField(max_length=10, verbose_name='Abrebiacion')

    def __str__(self):
        return self.empresa_nombre


class Zona(models.Model):
    zona_id = models.AutoField(primary_key=True)
    zona_nombre = models.CharField(max_length=80, verbose_name='Nombre de zona')

    def __str__(self):
        return self.zona_nombre


class Sucursal(models.Model): 
    id_sucursal = models.AutoField(primary_key=True)
    sucursal_nombre = models.CharField(max_length=150, verbose_name='Nombre de Sucursal')
    sucursal_direccion = models.CharField(max_length=250, verbose_name='Direccion')
    TIPO_SUC=((1, 'Premium'), (2, 'Estandar'), (3, 'Basico'))
    sucursal_tipo_sucursal = models.IntegerField('Tipo sucursal', choices=TIPO_SUC, default=2)
    sucursal_id_zona = models.ForeignKey(Zona, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Zona')
    sucursal_empresa_id = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Empresa')

    class Meta:
        ordering = ["sucursal_nombre"]
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return self.sucursal_nombre


class Departamento(models.Model):
    departamento_id_depo = models.AutoField(primary_key=True)
    departamento_nombre = models.CharField(max_length=80, verbose_name='Nombre')
    departamento_id_sucursal = models.ForeignKey(Sucursal, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Sucursal')

    class Meta:
        ordering = ["departamento_nombre"]

    def __str__(self):
        return str(self.departamento_nombre)
    # def nombre_empresa(self):
    #    query = Sucursal.objects.get(id_sucursal=self.departamento_id_sucursal.id_sucursal)
    #    return query.sucursal_empresa_id

    def nombre_empresa(self):
        query = Sucursal.objects.select_related().get(id_sucursal=self.departamento_id_sucursal.id_sucursal)
        return query.sucursal_empresa_id


class Pertenece_empresa(models.Model):
    #pertenece_id = models.AutoField(primary_key=True)
    pertenece_id_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    pertenece_empresa = models.ForeignKey(Departamento, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Es parte de"
        verbose_name = "Es parte de"
    def __str__(self):
        return str(self.pertenece_empresa)


class Cliente(models.Model):
    cli = models.AutoField(primary_key=True)
    cli_clave=models.CharField('Clave Cliente', max_length=15, unique=True)
    cli_calle=models.CharField('Calle',max_length=200)
    cli_colonia=models.CharField('Colonia',max_length=250)
    cli_cp=models.CharField('Codigo Postal',max_length=5)
    cli_estado=models.CharField('Estado',max_length=100)
    cli_telefono=models.CharField('Telefono',max_length=11)
    cli_rfc=models.CharField('R.F.C',max_length=15)
    cli_email=models.CharField('Email',max_length=80)
    cli_status=models.IntegerField('Status',choices=STATUS)
    cli_nombre=models.CharField('Nombre',max_length=80, null=True, blank=False)
    cli_vndedor_asignado=models.ForeignKey(Usuario, verbose_name='Vendedor asignado', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.cli_clave

    

        