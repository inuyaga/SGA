from django.db import models
from django.db.models import Sum
from aplicaciones.empresa.models import Departamento, Empresa
from django.conf import settings
Usuario = settings.AUTH_USER_MODEL 


STATUS = ((1,'Creado'), (2,'Validado'), (3, 'Autorizado'), (4, 'Pagado'), (5, 'Rechazado'), (6, 'Reembolsado'))
class TipoGasto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre tipo de gasto')
    def __str__(self):
        return self.nombre


class Gasto(models.Model):
    g_id = models.BigAutoField(primary_key=True, verbose_name="ID")
    g_tipoGasto = models.ForeignKey(TipoGasto, verbose_name="Tipo de Gasto", on_delete=models.CASCADE)
    g_monto = models.FloatField(verbose_name="Monto")
    g_descripcion = models.CharField("Descripcion", max_length=800, help_text="Descripcion del tipo de gasto")
    g_fechaCreacion = models.DateField(auto_now_add=True, verbose_name="Creado")
    g_estado=models.IntegerField(choices=STATUS, default=1, verbose_name="Estado")
    g_depo = models.ForeignKey(Departamento, on_delete=models.PROTECT, verbose_name="Departamento")
    g_userCreador = models.ForeignKey(Usuario, models.CASCADE, verbose_name="Creó")
    g_factura = models.FileField(upload_to='gasto/factura/', verbose_name="Factura", help_text="PDF de la factura escaneada")
    def __str__(self):
        return "{}".format(self.g_id)
    class Meta:
        ordering = ['g_estado']
        permissions = (
            ("puede_pagar_gasto", "Puede pagar gastos"),
            ("puede_validar_gasto", "Puede validar pago de gastos"),
            ("puede_autorizar_gasto", "Puede autorizar pago de gastos"),
            ("puede_rechazar_gasto", "Puede rechazar pago de gastos"),
        )



class Reembolso(models.Model):
    r_id=models.BigAutoField(primary_key=True, verbose_name="ID")
    r_date_add=models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    r_by_user=models.ForeignKey(Usuario, models.CASCADE, verbose_name="Creó")
    r_gastos=models.ManyToManyField(Gasto, verbose_name="Gastos")
    def total(self):        
        return self.r_gastos.all().aggregate(total_reembolso=Sum('g_monto'))
    class Meta:
        ordering = ['-r_id']
        # permissions = (
        #     ("puede_crear_reembolso", "Puede crear reembolso"),            
        # )