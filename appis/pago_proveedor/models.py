# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import FileExtensionValidator

from django.db import models

# Create your models here.


class Proveedor(models.Model):
    proveedor_nombre = models.CharField(max_length=100, verbose_name='Nombre')
    proveedor_email = models.EmailField(verbose_name='Correo')

    def __str__(self):
        return self.proveedor_nombre


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
    contrato_direccion = models.CharField(
        max_length=150, verbose_name='Direccion')
    contrato_monto = models.FloatField(
        null=False, blank=False, verbose_name='Monto')
    contrato_autorizado = models.BooleanField(
        default=False, verbose_name='Autorizado')
    contrato_status = models.BooleanField(default=True, verbose_name='Status')

    def __str__(self):
        return str(self.contrato_id)


class Factura(models.Model):
    factura_id = models.AutoField(primary_key=True)
    factura_contrato_id = models.ForeignKey(
        Contrato, null=True, blank=True, on_delete=models.CASCADE)
    TIPO_FACTURA = ((1, 'Persona Fisica'), (2, 'Persona Moral'))
    factura_tipo = models.IntegerField(choices=TIPO_FACTURA)
    factura_xml = models.FileField(
        upload_to='Facturas/xml/', validators=[FileExtensionValidator(allowed_extensions=['xml'])])
    factura_pdf = models.FileField(
        upload_to='Facturas/pdf/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    factura_monto_total = models.FloatField(null=True, blank=True)
    factura_iva_trasladado = models.FloatField(null=True, blank=True)
    factura_iva_retenido = models.FloatField(null=True, blank=True)
    factura_isr_retenido = models.FloatField(null=True, blank=True)
    factura_corresponde_mes = models.DateField()
    factura_creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.factura_id)


class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    pago_factura_id = models.ForeignKey(
        Factura, null=True, blank=True, on_delete=models.CASCADE)
    pago_pdf = models.FileField(upload_to='Facturas/pagos/')
    pago_monto = models.FloatField(null=True, blank=True)
    METODO_PAGO = (('EFECTIVO', 'EFECTIVO'),
                   ('TRANSFERENCIA', 'TRANSFERENCIA'))
    pago_metodo = models.CharField(max_length=40, choices=METODO_PAGO)
    pago_creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pago_id)


class Complemento(models.Model):
    complemento_id = models.AutoField(primary_key=True)
    complemento_pago_id = models.ForeignKey(
        Pago, null=True, blank=True, on_delete=models.CASCADE)
    complemento_pdf = models.FileField(upload_to='Facturas/complementos/')
    complemento_monto = models.FloatField(null=True, blank=True)
    METODO_PAGO = (('EFECTIVO', 'EFECTIVO'),
                   ('TRANSFERENCIA', 'TRANSFERENCIA'))
    complemento_metodo = models.CharField(max_length=40, choices=METODO_PAGO)
    complemento_creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.complemento_id)
