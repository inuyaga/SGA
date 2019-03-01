from __future__ import unicode_literals
from __future__ import absolute_import
from django.db import models

# Create your models here.
class Conformidad(models.Model):
    conformidad_id=models.AutoField(primary_key=True)
    conformidad_descripcion=models.CharField(max_length=150, verbose_name="Descripción de conformidad")
    conformidad_fechaAlta=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.conformidad_descripcion

class Vendedor(models.Model):
    vendedor_id=models.AutoField(primary_key=True)
    vendedor_nombre=models.CharField(max_length=150, verbose_name="Nombre de vendedor")
    vendedor_estatus=models.IntegerField(null=False, blank=False, default=1, verbose_name="Estado de vendedor")
    vendedor_fechaAlta=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vendedor_nombre

class Motivo(models.Model):
    motivo_id=models.AutoField(primary_key=True)
    motivo_descripcion=models.CharField(max_length=150, verbose_name="Descripción de motivo")
    motivo_fechaAlta=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.motivo_descripcion

class Tramite(models.Model):
    tramite_id=models.AutoField(primary_key=True)
    tramite_descripcion=models.CharField(max_length=150, verbose_name="Descripción de trámite")
    tramite_fechaAlta=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tramite_descripcion

class Factura(models.Model):
    factura_id=models.AutoField(primary_key=True)
    FechaFactura = models.DateField(null=False, blank=False, default="2017-01-01")
    factura_folio=models.CharField(max_length=100)
    factura_total=models.FloatField(verbose_name="Valor de la factura")
    factura_fechaAlta=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.factura_folio


class Fud(models.Model):
    Folio = models.AutoField(primary_key=True)
    FechaFactura = models.DateField(null=True, blank=True)
    NumeroCliente = models.IntegerField(null=False, blank=False, default=1, verbose_name="Número de cliente")
    NombreCliente = models.CharField(null=False, blank=False, default="no identificado", max_length=80, verbose_name="Nombre de cliente")
    ZonaCliente = models.CharField(null=False, blank=False, default="no identificado", max_length=80, verbose_name="Zona que pertence el cliente")
    VendedorCliente = models.CharField(null=False, blank=False, default="no identificado", max_length=80, verbose_name="Vendedor asignado al cliente")
    Factura = models.ManyToManyField(Factura)
    Motivo= models.ForeignKey(Motivo, null= True, blank=True, on_delete = models.PROTECT)
    conformidad= models.ForeignKey(Conformidad, null= True, blank=True, on_delete = models.PROTECT)
    tramite= models.ForeignKey(Tramite, null= True, blank=True, on_delete = models.PROTECT)
    DEVOLUCION = ((1,'Total'),(2,'Parcial'),(3,'N/A'))
    devolucion = models.IntegerField(null=True, blank=True, choices= DEVOLUCION, default=1, verbose_name="Estado")
    responsable = models.CharField(max_length =80)
    observaciones = models.CharField(max_length =80)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.CharField(max_length = 150)
    
    def __str__(self):
        return self.Folio