from django.db import models
from django.db.models import Sum, F, FloatField
from aplicaciones.empresa.models import Sucursal
from aplicaciones.pedidos.models import Producto

STATUS = ((1, 'CREADO'), (2, 'AUTORIZADO'), (3, 'AJUSTADO'))
class Ajuste(models.Model):
    id=models.BigAutoField(verbose_name="ID", primary_key=True)
    aj_sucursal=models.ForeignKey(Sucursal, verbose_name="Sucursal", on_delete=models.SET_NULL, blank=True, null=True)
    aj_fecha=models.DateField(auto_now_add=True, verbose_name="Fecha solicitud")
    aj_cresendo=models.IntegerField(verbose_name="N° Entrada Crescendo", blank=True, null=True)
    aj_cresendo_salida=models.IntegerField(verbose_name="N° Salida Cresendo", blank=True, null=True)
    aj_producs = models.ManyToManyField(Producto, through="AjusteProduct")    
    aj_status=models.IntegerField(choices=STATUS, verbose_name="Estado")

    class Meta:
        permissions = [
            ('puede_autorizar_ajuste', 'Permiso para autorizar un ajuste'),
            ('puede_ajustar_ajuste', 'Permiso para ajustar un ajuste'),
            ('puede_actualizar_no_crescendo', 'Puede actualizar N° Cresendo'),
            ('puede_visualizar_todos_ajustes', 'Puede ver todo el listado de ajustes'),
            ]
    def __str__(self):
        return "{}".format(self.id) 
    
    def total(self):
        query_sum = self.ajusteproduct_set.aggregate(suma_total=Sum(F('exist_sistema')*F('precio'), output_field=FloatField())) 
        return query_sum['suma_total']


class AjusteProduct(models.Model):
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    ajuste=models.ForeignKey(Ajuste, on_delete=models.CASCADE)
    exist_sistema=models.IntegerField(verbose_name="Existencia Sistema")
    exist_fisica=models.IntegerField(verbose_name="Existencia Fisica")
    cantidad=models.IntegerField(verbose_name="Cantidad")
    precio=models.FloatField(verbose_name="Precio unitario")
    vale=models.IntegerField(verbose_name="Vale") 
    def __str__(self):
        return self.producto.producto_codigo




    


