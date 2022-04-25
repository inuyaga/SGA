from django.db import models
from django.core.validators import FileExtensionValidator
import datetime
from dateutil import rrule
from django.db import models
from django.db.models import Sum

class Proveedor(models.Model):
    proveedor_nombre = models.CharField(max_length=100, verbose_name='Nombre')
    proveedor_rfc = models.CharField(max_length=15, verbose_name='RFC', default = 'none', unique=True)
    proveedor_email = models.EmailField(verbose_name='Correo')
    proveedor_cuenta = models.CharField(max_length=100, verbose_name='Número de cuenta')
    proveedor_banco = models.CharField(max_length=100, verbose_name='Nombre del banco')
    
    def __str__(self):
        return self.proveedor_nombre

class Renta(models.Model):
    depto = models.CharField(max_length=100, verbose_name='Casa o depto en renta')
    direccion = models.CharField(max_length=120, verbose_name='Dirección de la locación', default = 'none', unique=True)
    
    def __str__(self):
        return self.depto


class Contrato(models.Model):
    contrato_id = models.AutoField(primary_key=True)
    contrato_proveedor_id = models.ForeignKey(
        Proveedor, null=False, blank=False, on_delete=models.PROTECT)
    contrato_documento = models.FileField(
        upload_to='Contratos/', verbose_name='Documento')
    contrato_fecha_inicio = models.DateField(verbose_name='Inicio')
    contrato_fecha_termino = models.DateField(verbose_name='Termino')
    contrato_dias_pago = models.CharField(
        max_length=100, verbose_name='Describa fechas de pago')
    contrato_monto = models.FloatField(
        null=False, blank=False, verbose_name='Monto')
    contrato_deposito = models.FloatField(
        null=False, blank=False, default=0, verbose_name='Deposito')
    contrato_autorizado = models.BooleanField(
        default=False, verbose_name='Autorizado')
    contrato_status = models.BooleanField(default=True, verbose_name='Estado')
    contrato_sucursal=models.ForeignKey(Renta, verbose_name="Casa o departamento", on_delete=models.PROTECT, null=True, blank=True,)

    def __str__(self):
        return str(self.contrato_sucursal)

    def costo_contrato(self):
        contratoI = rrule.rrule(rrule.MONTHLY, dtstart=self.contrato_fecha_inicio, until=self.contrato_fecha_termino).count()
        return str(contratoI* self.contrato_monto)

    def contrato_pagado(self):
        # contratoI = Pago.objects.
        contratoI = Pago.objects.filter(contrato_id_id=self.contrato_id).aggregate(Sum('pago_monto'))
        return contratoI


class Pago(models.Model):
    METODO_PAGO = (('EFECTIVO', 'EFECTIVO'),
                   ('TRANSFERENCIA', 'TRANSFERENCIA'),('TDD','TDD'),('TDC','TDC'))
    pago_id = models.AutoField(primary_key=True)
    contrato_id = models.ForeignKey(Contrato, null=False, blank=False, on_delete=models.PROTECT)
    pago_pdf = models.FileField(null=True, blank=True, upload_to='Facturas/pagos/', verbose_name="Comprobante PDF (obligatorio)")
    pago_monto = models.FloatField(null=True, blank=True, verbose_name="Monto del pago (obligatorio)")
    pago_metodo = models.CharField(null=True, blank=True, max_length=40, choices=METODO_PAGO, verbose_name="Método de pago (obligatorio)")
    pago_creado = models.DateTimeField(auto_now_add=True)
    factura_xml = models.FileField(
        upload_to='Facturas/xml/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['xml'])])
    factura_pdf = models.FileField(
        upload_to='Facturas/pdf/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    pago_observacion=models.CharField(max_length=300, verbose_name='Observación', default="")

    def __str__(self):
        return str(self.pago_id)