from django.db import models
from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Compra(models.Model):
    compra_id=models.AutoField(primary_key=True)
    compra_numEntrada = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99999999)], unique=True, verbose_name="Número de entrada")
    compra_factura = models.CharField(max_length=10, verbose_name="Folio de factura")
    compra_nota = models.CharField(max_length=1500, verbose_name="Nota")
    compra_fechaCompra = models.DateTimeField(auto_now_add=True)
    compra_fechaLastChange = models.DateTimeField(auto_now=True)
    compra_codigo = models.CharField(max_length=11, verbose_name="Código de crescendo")
  
    def __str__(self):
        return '%s' % (self.compra_numEntrada)
