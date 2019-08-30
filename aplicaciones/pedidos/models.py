# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from aplicaciones.empresa.models import Departamento, Sucursal
from django.db.models import Avg, Sum, F

from django.contrib.auth import get_user_model
# pylint: disable = E1101
Usuario = get_user_model()

# Create your models here.
STATUS = ((1, 'Creado'), (2, 'Aprobado'), (3, 'Cancelado'),(4, 'Venta'),(5, 'Facturado'), (6, 'Finalizado'), (7, 'Descargado'))

class Marca(models.Model):
    marca_id_marca = models.AutoField(primary_key=True)
    marca_nombre = models.CharField(
        max_length=80, verbose_name='Nombre de Marca')

    def __str__(self):
        return self.marca_nombre


class Area(models.Model):
    area_id_area = models.AutoField(primary_key=True)
    area_nombre = models.CharField(
        max_length=40, verbose_name='Nombre de area')

    def __str__(self):
        return self.area_nombre


class Producto(models.Model):
    producto_codigo = models.CharField(max_length=15, primary_key=True)  
    producto_nombre = models.CharField(max_length=50, verbose_name='Nombre')
    producto_descripcion = models.CharField(max_length=150, verbose_name='Descripcion')
    producto_imagen = models.ImageField(blank=False, null=False, upload_to="img_productos/", verbose_name='Imagen')
    producto_marca = models.ForeignKey(Marca, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Marca')
    producto_area = models.ForeignKey(Area, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Area')
    producto_precio = models.DecimalField('Precio', max_digits=7, decimal_places=2, default=0.00)
    TIPO_PRODUCTO = ((1, 'Uso Interno'), (2, 'Activo Fijo'),)
    tipo_producto = models.IntegerField(choices=TIPO_PRODUCTO, null=True, blank=True)
    producto_es_kit=models.BooleanField(verbose_name='¿Pertenecerá a un Kit?', default=False)
    producto_kit=models.BooleanField(verbose_name='Kit', default=False)
    producto_productos=models.ManyToManyField("Producto")
    producto_visible=models.BooleanField('¿Producto visible?', default=True)
     

    def __str__(self):
        return self.producto_codigo


class Tipo_Pedido(models.Model):
    tp=models.AutoField(primary_key=True)
    tp_nombre=models.CharField('Nombre', max_length=30)
    tp_descripcion=models.CharField('Descripción', max_length=50)
    tp_max_ped_mes=models.IntegerField('Cantidad de pedidos por mes', default=1)
    tp_imagen=models.ImageField('Imagen', upload_to='imgCategoria/')
    tp_productos=models.ManyToManyField(Producto, verbose_name='Productos') 
    def __str__(self):
        return self.tp_nombre
    
class Asignar_gasto_sucursal(models.Model):
    ags=models.AutoField(primary_key=True)
    ags_tipo_ped=models.ForeignKey(Tipo_Pedido,on_delete=models.CASCADE, verbose_name='Tipo pedido')
    ags_sucursal=models.ForeignKey(Departamento, on_delete=models.CASCADE,verbose_name='Departamento')
    ags_maximo_gasto=models.FloatField('Maximo de gasto')
    class Meta: 
        unique_together = (("ags_tipo_ped", "ags_sucursal"),)
        # ordering = ['-tareaDocumento_actualizado']
    def __str__(self):
        return str(self.ags)


class Pedido(models.Model):     
    pedido_id_pedido = models.AutoField(primary_key=True)  
    pedido_fecha_pedido = models.DateField(auto_now_add=True)
    pedido_actualizado = models.DateTimeField(auto_now=True)
    pedido_id_depo = models.ForeignKey(Departamento, null=False, blank=False, on_delete=models.CASCADE, verbose_name='Departamento')
    pedido_status = models.IntegerField(choices=STATUS, default=1, verbose_name='Status')

    pedido_autorizo=models.ForeignKey(Usuario, verbose_name='Autorizado Por', related_name='Autorizador', blank=True, null=True, on_delete=models.CASCADE)
    pedido_rechazado=models.ForeignKey(Usuario, verbose_name='Rechazado Por', related_name='Cancelo', blank=True, null=True, on_delete=models.CASCADE)

    pedido_Venta=models.ForeignKey(Usuario, verbose_name='Venta Por', related_name='Venta', blank=True, null=True, on_delete=models.CASCADE)
    pedido_Facturado=models.ForeignKey(Usuario, verbose_name='Facturado Por', related_name='Facturado', blank=True, null=True, on_delete=models.CASCADE)
    pedido_Finalizado=models.ForeignKey(Usuario, verbose_name='Finalizado Por', related_name='Finalizado', blank=True, null=True, on_delete=models.CASCADE)
    pedido_Descargado=models.ForeignKey(Usuario, verbose_name='Descargado Por', related_name='Descargado', blank=True, null=True, on_delete=models.CASCADE)

    pedido_tipoPedido=models.ForeignKey(Tipo_Pedido, verbose_name='Tipo de pedido', blank=True, null=True, on_delete=models.PROTECT)
    pedido_n_factura=models.CharField('Folio Factura', max_length=14, blank=True, null=True)
    pedido_n_salida=models.CharField('Numero Salida', max_length=8, blank=True, null=True)
    pedido_n_cresscedo=models.CharField('Venta Cresscendo', max_length=14, blank=True, null=True)

    def get_total(self): 
        total=Detalle_pedido.objects.filter(detallepedido_pedido_id=self.pedido_id_pedido).aggregate(suma_total=Sum(F('detallepedido_precio') * F('detallepedido_cantidad')))['suma_total']
        if total != None:
            total=round(total, 3)
        return total
   
    def __str__(self):
        return str(self.pedido_id_pedido)
  

class Detalle_pedido(models.Model):
    detallepedido_pedido_id = models.ForeignKey(Pedido, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Numero de pedido')
    detallepedido_producto_id = models.ForeignKey(Producto, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Producto')
    detallepedido_cantidad = models.FloatField(null=True, blank=True, verbose_name='Cantidad')
    detallepedido_creado_por = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.PROTECT,)
    detallepedido_precio = models.FloatField(null=False, blank=False, default=0)
    detallepedido_tipo_pedido = models.IntegerField(null=False, blank=False, default=0)
    detallepedido_status = models.BooleanField(default=False)

    class Meta:
        ordering = ["detallepedido_pedido_id"]
        verbose_name_plural = "Detalle de pedidos"

    def __str__(self):
        return str(self.detallepedido_pedido_id) 

    def sucursal(self):
        suc=Pedido.objects.get(pedido_id_pedido=self.detallepedido_pedido_id)
        return suc.pedido_id_depo.departamento_id_sucursal.sucursal_nombre
    def subtotal(self):
        total=self.detallepedido_cantidad * self.detallepedido_precio
        return 0 if total == None else round(total)
    

class Configuracion_pedido(models.Model):
    conf_ID=models.AutoField(primary_key=True)
    conf_fecha_inicio=models.DateField('Fecha inicio')
    conf_fecha_fin=models.DateField('Fecha final') 
    
