# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from aplicaciones.empresa.models import Departamento, Sucursal, Empresa
from django.db.models import Avg, Sum, F

from django.conf import settings
Usuario = settings.AUTH_USER_MODEL

# Create your models here.
STATUS = ((1, 'Creado'), (2, 'Aprobado'), (3, 'Cancelado'),(4, 'Venta'),(5, 'Facturado'), (6, 'Finalizado'), (7, 'Descargado'))
CONTEO=((1, 'CONTEO 1'), (2, 'CONTEO 2'), (3, 'CONTEO 3'))
TIPO_PRODUCTO = ((1, 'Uso Interno'), (2, 'Activo Fijo'), (3, 'Temporada'), (4, 'Normal'))
class Marca(models.Model):
    marca_id_marca = models.AutoField(primary_key=True)
    marca_nombre = models.CharField(
        max_length=80, verbose_name='Nombre de Marca') 

    def __str__(self):
        return self.marca_nombre
    
    class Meta:
        ordering = ["marca_nombre"]


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
    tipo_producto = models.IntegerField(choices=TIPO_PRODUCTO, null=True, blank=True)
    producto_es_kit=models.BooleanField(verbose_name='¿Pertenecerá a un Kit?', default=False)
    producto_kit=models.BooleanField(verbose_name='Kit', default=False)
    producto_productos=models.ManyToManyField("Producto")
    producto_visible=models.BooleanField('¿Producto visible?', default=True)

    prducto_codigo_barras=models.CharField(max_length=50, verbose_name='Codigo Barras', null=True, blank=True)
    prducto_localizacion=models.CharField(max_length=50, verbose_name='Localizacion', null=True, blank=True)
    prducto_unidad=models.CharField(max_length=100, verbose_name='Unidad', null=True, blank=True)
    prducto_resguardo=models.CharField(max_length=50, verbose_name='Localizacion en resguardo', null=True, blank=True)
    prducto_existencia=models.IntegerField(verbose_name='Existencia', null=True, blank=True)

    producto_descripcion_web=models.TextField('Descripcion enriquecido para sitio web', blank=True, null=True)


    class Meta:
        permissions = [
            ('puede_actualizar_precio_volumen', 'Puede actualizar precios de productos en volumen'),
            ]
        ordering = ["producto_nombre"]
     

    def __str__(self):
        return self.producto_codigo

    def inventario_conteo_resguardo(self):
        total=Inventario.objects.filter(inv_producto=self.producto_codigo, inv_cant_resguardo__gt=0).count()
        return total
    def inventario_conteo_pikin(self):
        total=Inventario.objects.filter(inv_producto=self.producto_codigo, inv_cant_piking__gt=0).count()
        return total


class Tipo_Pedido(models.Model):
    tp=models.AutoField(primary_key=True)
    tp_empresa=models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa', null=True, blank=False)
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
        return 'ID:{}, Producto:{}, Detalle:{}'.format(self.detallepedido_pedido_id, self.detallepedido_producto_id, self.detallepedido_producto_id.producto_descripcion)

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
    
class Catalogo_Productos(models.Model):
    tp_empresa=models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa', null=True, blank=False)
    tp_catalogo=models.CharField('Nombre', max_length=50)
    tp_descripcion=models.CharField('Descripción', max_length=100)
    tp_no_licitacion=models.CharField('N° de Licitacion', max_length=100, blank=False, null=True)
    tp_imagen = models.ImageField(verbose_name='Imagen empresa a licitar', upload_to='catalogo_prod/licitacion/', blank=False, null=True)
    tp_productos=models.ManyToManyField(Producto, verbose_name='Productos')
    ORIENTACION=((1, 'Derecha'), (2, 'Izquierda'))
    tp_orientacion_t=models.IntegerField(choices=ORIENTACION, default=1, verbose_name='Orientacion de tabla')

    





# CODIGO PARA INVENTARIO CSS
class Inventario(models.Model):
    inv=models.BigAutoField(primary_key=True)
    inv_producto=models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Codigo producto', null=True, blank=False)
    
    inv_cant_resguardo=models.IntegerField('Cantidad encontrada en resguardo', default=0)
    inv_cant_piking=models.IntegerField('Cantidad encontrada en piking', default=0)
    inv_cant_otros=models.IntegerField('Cantidad encontrada en otras ubicaciones', default=0)
    inv_cant_merma=models.IntegerField('Merma', default=0) 
    
    inv_fecha_add=models.DateTimeField(auto_now_add=True)
    inv_user_catura=models.ForeignKey(Usuario, verbose_name='Usuario capturador', on_delete=models.CASCADE)
    inv_sup_autorizo_merma=models.ForeignKey(Usuario, verbose_name='Supervisor autorizador merma', related_name='autoriza_merma', blank=False, null=True, on_delete=models.CASCADE)
    inv_descripcion=models.CharField(max_length=500, verbose_name='Descripción', help_text='Describa la ubicacion encontrada y comentarios', blank=True, null=True)
    inv_validacion=models.BooleanField('Status',default=True)
    inv_edicion=models.ForeignKey(Usuario, verbose_name='Ultimo Usuario edito', related_name='usr_edit', blank=False, null=True, on_delete=models.CASCADE)
    inv_conteo=models.IntegerField('Numero de conteo', choices=CONTEO, default=1)
    UBICATIONS=((1, 'RESGUARDO'), (2, 'PIKING'), (3, 'OTROS'), (4, 'MERMA'))
    inv_tipo_sitio=models.IntegerField('Ubicacion conteo', choices=UBICATIONS, blank=False, null=True)
    def __str__(self):
        return 'ID: {} / Producto: {}'.format(self.inv, self.inv_producto)
    class Meta:
        permissions = [
            ('puede_visualizar_avance_conteo_inventario', 'Puede Ver avance del conteo de inventario'),
            ('inventario_perm_supervisor', 'Permiso de supervisor para inventario'),
            ]
        ordering = ["-inv_fecha_add"]
        unique_together = (("inv_producto", "inv_conteo", 'inv_tipo_sitio'),)

    



    
