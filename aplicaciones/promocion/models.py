from django.db.models import Sum, F, FloatField, Case, When
from django.db import models
from django.conf import settings
Usuario = settings.AUTH_USER_MODEL
# Create your models here.
PROVEEDORES = (('855', 'RODIN'), ('255', 'NORMA'), ('261', 'ESCRIMEX'), ('440', 'ARIMANY'), ('022', 'HENKEL'),('009', 'PELIKAN'), ('623', 'JUMBO'), ('111', 'KOLA LOKA'), ('801', 'ESTILO'),)
class Promocion(models.Model):
    venta=models.CharField('Venta',  max_length=15)
    no_cliente=models.CharField('Número de cliente',  max_length=15)
    cod_prod=models.CharField('Código del producto',max_length=12)
    descripcion=models.CharField('Descripción del producto', max_length=700)
    importeNeto = models.DecimalField('Importe Neto', max_digits=10, decimal_places=2, default=0.00)
    fecha_fac=models.DateField('Fecha de expedición de factura')
    fac=models.CharField('Folio de factura',max_length=15)
    proveedor=models.CharField(choices= PROVEEDORES, verbose_name='Proveedor', max_length=15)

    def __str__(self):
        return self.venta

    def mismejores(self):
        consulta = self.objects.annotate(puntosR = Case(
            When(proveedor="440", then= (Sum(F('importeNeto'))/10000)*15),
            When(proveedor="623", then= (Sum(F('importeNeto'))/10000)*6),
            When(proveedor="255", then= (Sum(F('importeNeto'))/10000)*15),
            When(proveedor="855", then= (Sum(F('importeNeto'))/10000)*15),
            When(proveedor="261", then= (Sum(F('importeNeto'))/10000)*9),
            When(proveedor="022", then= (Sum(F('importeNeto'))/10000)*9),
            When(proveedor="009", then= (Sum(F('importeNeto'))/10000)*9),
            When(proveedor="111", then= (Sum(F('importeNeto'))/10000)*3),
            When(proveedor="801", then= (Sum(F('importeNeto'))/10000)*3),
            default=Sum(F('importeNeto')),
            output_field=FloatField()
        )).order_by('no_cliente')
        return consulta

    class Meta:
        verbose_name = "Productos con puntos de promoción por cada 10 mil"