from __future__ import unicode_literals
from __future__ import absolute_import
from django.db import models
from datetime import datetime
from aplicaciones.pedidos.models import Producto


from django.contrib.auth import get_user_model
Usuario = get_user_model()

class Conformidad(models.Model):
    conformidad_id=models.AutoField(primary_key=True)
    conformidad_descripcion=models.CharField(max_length=150, verbose_name="Descripción de conformidad")
    conformidad_fechaAlta=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.conformidad_descripcion

class Motivo(models.Model):
    motivo_id=models.AutoField(primary_key=True)
    motivo_descripcion=models.CharField(max_length=150, verbose_name="Descripción de motivo")
    motivo_idconformidad=models.ForeignKey(Conformidad, verbose_name="Id conformidad", on_delete=models.CASCADE)
    motivo_fechaAlta=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.motivo_descripcion

class Tramite(models.Model):
    tramite_id=models.AutoField(primary_key=True)
    tramite_descripcion=models.CharField(max_length=150, verbose_name="Descripción de trámite")
    tramite_fechaAlta=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.tramite_descripcion


class Zona(models.Model):
    Zona_id = models.AutoField(primary_key=True)
    Zona_nombre=models.CharField(max_length=80, verbose_name="Nombre de la Zona")
    Zona_FechaAlta=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Zona_nombre

class Vendedores(models.Model):
    Vend_id = models.AutoField(primary_key=True)
    Vend_nombre=models.CharField(max_length=80, verbose_name="Nombre del vendedor")
    Vend_Zona=models.ForeignKey(Zona, null= True, blank=True, on_delete = models.PROTECT, verbose_name="Zona a la que pertenece el vendedor")
    TIPO_ESTADO = ((1, 'Activo'), (2, 'Inactivo'))
    Vend_Estatus=models.IntegerField(choices=TIPO_ESTADO,null=False, blank=False, default=1, verbose_name="Estado de vendedor")
    Vend_FechaAlta=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.Vend_nombre)


class Clientes(models.Model):
    Client_numero=models.IntegerField(primary_key=True, verbose_name="Número de cliente")
    Client_Nombre = models.CharField(null=False, blank=False, max_length=80, verbose_name="Nombre de cliente")
    Client_Estatus=models.BooleanField("Activo")
    Client_FechaAlta=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.Client_numero)+'  '+self.Client_Nombre

class Fud(models.Model):
    Folio = models.AutoField(primary_key=True)
    NumeroVenta=models.IntegerField(verbose_name="Número de venta", default='')
    FechaFactura = models.DateField(null=True, blank=True)
    NumeroCliente = models.ForeignKey(Clientes, null= True, blank=True, on_delete = models.PROTECT, verbose_name="Número de cliente")
    VendedorCliente = models.ForeignKey(Vendedores, null= True, blank=True, on_delete = models.PROTECT, verbose_name="Vendedor asignado al cliente")
    Factura = models.CharField(blank=True, null=True, default="TCA0", max_length=150, verbose_name="Factura")
    FechaFactura = models.DateField(null=False, blank=False, default="2017-01-01")
    factura_total=models.FloatField(verbose_name="Valor de la factura", default="0.00")
    Motivo= models.ForeignKey(Motivo, null= True, blank=True, on_delete = models.PROTECT)
    tramite= models.ForeignKey(Tramite, null= True, blank=True, on_delete = models.PROTECT)
    DEVOLUCION = ((1,'Total'),(2,'Parcial'),(3,'N/A'))
    devolucion = models.IntegerField(null=True, blank=True, choices= DEVOLUCION, default=1, verbose_name="Estado")
    responsable = models.CharField(max_length =80)
    observaciones = models.CharField(max_length =1500)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(Usuario, null= True, blank=True, on_delete = models.CASCADE)
    ESTADOS = ((1,'Creado'),(2,'Autorizado'),(3,'En transito'),(4,"Entregado"),(5,"Finalizado"))
    EstadoFud=models.IntegerField(null=True, blank=True, choices= ESTADOS, default=1, verbose_name="Estado")
    def __str__(self):
        return str(self.Folio)

    class META:
        ordering = ['-fecha_creacion']

    

class PartidasFud(models.Model):
    Partida_id = models.AutoField(primary_key=True)
    Partida_nombre = models.ForeignKey(Producto,on_delete = models.CASCADE, verbose_name="Partida de fud")
    Partida_fud = models.ForeignKey(Fud, on_delete = models.CASCADE, verbose_name="Fud a seleccionar")
    Partida_Precio=models.FloatField(null=False, blank=False, default=0, verbose_name="Precio de la partida")
    Partida_Cantidad=models.IntegerField(null=False, blank=False, default=1, verbose_name="cantidad de partidas")
    Partida_FechaAlta = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.Partida_nombre)
    def get_cantidadXpartidas(self):
        total=self.Partida_Precio * self.Partida_Cantidad
        return total
    def get_cantidadXpartidasIVA(self):
        total="{0:.2f}".format(round((self.Partida_Precio * self.Partida_Cantidad) * 1.16, 2))
        return total