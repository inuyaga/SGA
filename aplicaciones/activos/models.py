from django.db import models
from aplicaciones.pedidos.models import Area, Marca

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
    def __str__(self):
        return self.activo_nombre

class Especificacion(models.Model):
    especificacion=models.AutoField(primary_key=True)
    esp_activo=models.ForeignKey(Activo, verbose_name='Activo perteneciente', on_delete=models.CASCADE)
    esp_item=models.CharField('Item', max_length=120)
    esp_valor=models.CharField('Especificación', max_length=100)
    esp_tiene_costo=models.BooleanField('Tiene algun costo?', default=False)
    esp_costo=models.FloatField('Costo de la especificacion', default=0.0)
    def __str__(self):
        return self.esp_item
    
    
