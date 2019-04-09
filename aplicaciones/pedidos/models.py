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
    producto_descripcion = models.CharField(
        max_length=150, verbose_name='Descripcion')
    producto_imagen = models.ImageField(blank=False, null=False, upload_to="img_productos/", verbose_name='Imagen')
    producto_marca = models.ForeignKey(
        Marca, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Marca')
    producto_area = models.ForeignKey(
        Area, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Area')
    producto_precio = models.FloatField(
        null=True, blank=True, verbose_name='Precio')

    TIPO_PRODUCTO = ((1, 'Uso Interno'), (2, 'Activo Fijo'),)
    tipo_producto = models.IntegerField(
        choices=TIPO_PRODUCTO, null=True, blank=True)
    producto_es_kit=models.BooleanField(verbose_name='Pertenecera a un Kit', default=False)
    producto_kit=models.BooleanField(verbose_name='Kit', default=False)
    producto_productos=models.ManyToManyField("Producto")
    

    def __str__(self):
        return self.producto_nombre


class Pedido(models.Model):
    pedido_id_pedido = models.AutoField(primary_key=True)
    pedido_fecha_pedido = models.DateTimeField(auto_now_add=True)
    pedido_actualizado = models.DateTimeField(auto_now=True)
    pedido_id_depo = models.ForeignKey(
        Departamento, null=False, blank=False, on_delete=models.CASCADE, verbose_name='Departamento')
    STATUS = ((1, 'Creado'), (2, 'Aprobado'), (3, 'Rechazado'),)
    pedido_status = models.IntegerField(
        choices=STATUS, default=1, verbose_name='Status')

    def __str__(self):
        return str(self.pedido_id_pedido)
# Obtiene nombre de la sucursal

    def nombre_sucursal(self):
        query = Departamento.objects.get(
            departamento_id_depo=self.pedido_id_depo.departamento_id_depo)
        idDepo = query.departamento_id_sucursal
        return idDepo

    def limite_gastos(self):
        query = Departamento.objects.get(
            departamento_id_depo=self.pedido_id_depo.departamento_id_depo)
        return query.departamento_limite_gasto
# Obtiene nombre de la empresa

    def empresa(self):
        query = Sucursal.objects.get(
            id_sucursal=self.nombre_sucursal().id_sucursal)
        return query.sucursal_empresa_id

    def total(self):
        total_importe = Detalle_pedido.objects.filter(detallepedido_pedido_id=self.pedido_id_pedido).aggregate(
            total=Sum(F('detallepedido_cantidad')*F('detallepedido_precio')))
        return total_importe['total']


class Detalle_pedido(models.Model):
    detallepedido_pedido_id = models.ForeignKey(
        Pedido, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Numero de pedido')
    detallepedido_producto_id = models.ForeignKey(
        Producto, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Producto')
    detallepedido_cantidad = models.FloatField(
        null=True, blank=True, verbose_name='Cantidad')
    detallepedido_creado_por = models.ForeignKey(
        Usuario, null=True, blank=True, on_delete=models.PROTECT,)
    #precio = auto_save_precio(self)
    detallepedido_precio = models.FloatField(
        null=False, blank=False, default=0)
    detallepedido_status = models.BooleanField(default=False)

    class Meta:
        ordering = ["detallepedido_pedido_id"]
        verbose_name_plural = "Detalle de pedidos"

    def __str__(self):
        return str(self.detallepedido_producto_id)
