from django.db import models
from django.db.models import Sum, FloatField, F
from django.contrib.auth import get_user_model
from aplicaciones.pedidos.models import Marca, Producto
from aplicaciones.empresa.models import Cliente
Usuario = get_user_model()



TIPO_VENTA=((1, "TEMPORADA"), (2, "NORMAL"))
# Create your models here.
class AsignacionMarca(models.Model):
    am_user=models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.PROTECT, verbose_name="Usuario promotor o proveedor")
    am_marca=models.ManyToManyField(Marca, verbose_name="Marca")
    def __str__(self):
        return str(self.am_user)




class VentaExpo(models.Model):
    Venta_ID = models.AutoField(primary_key=True)
    venta_e_fecha_pedido = models.DateField(auto_now_add=True)
    venta_e_actualizado = models.DateTimeField(auto_now=True) 
    venta_e_cliente=models.ForeignKey(Cliente, null=False, blank=False, on_delete=models.PROTECT, verbose_name="Cliente")
    venta_e_status = models.BooleanField(default=False)
    venta_e_creado=models.ForeignKey(Usuario, verbose_name='Capturó venta', blank=False, null=True, on_delete=models.CASCADE)
    venta_e_tipo=models.IntegerField(choices=TIPO_VENTA, default=2)

    def __str__(self):
        return str(self.Venta_ID)
    
    def total_venta(self):
        sum_detalle=Detalle_venta.objects.filter(detalle_venta=self.Venta_ID).aggregate(total=Sum(F('detalle_cantidad')*F('detalle_precio'), output_field=FloatField()))['total']
        total = round(sum_detalle, 3) if sum_detalle != None else 0.0
        return total

    

class Detalle_venta(models.Model):
    detalle_venta = models.ForeignKey(VentaExpo, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Numero de Venta')
    detalle_producto_id = models.ForeignKey(Producto, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Producto')
    detalle_cantidad = models.FloatField(null=True, blank=True, verbose_name='Cantidad')
    detalle_precio = models.FloatField(null=False, blank=False, default=0)
    def subtotal(self):
        sub_total=self.detalle_precio * self.detalle_cantidad
        return round(sub_total, 3) if sub_total != None else 0.0
    