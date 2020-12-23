from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


ESTADOS = ((1,'Creado'),(2,'Autorizado'),(3,'Validado'),(4,'Descargado'))
class Descargas(models.Model):
    d_id=models.AutoField(primary_key=True)
    listado = models.FileField(upload_to="descargas/listado/", null=True, blank=True)
    ficha = models.FileField(upload_to="descargas/ficha/", null=True, blank=True)
    observacion = models.CharField(max_length=200, verbose_name="Observación")
    estatus = models.IntegerField(null=True, blank=True, choices= ESTADOS, default=1, verbose_name="Estado")
    compra_fechaCompra = models.DateTimeField(auto_now_add=True)
    compra_fechaLastChange = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return '%s' % (self.d_id)