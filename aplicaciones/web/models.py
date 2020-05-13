from django.db import models
from django.db.models import FloatField, Sum, F
from django.core.validators import FileExtensionValidator
from aplicaciones.pedidos.models import Producto
from django.conf import settings
Usuario = settings.AUTH_USER_MODEL
# Create your models here.
class Departamento(models.Model):
    dp_nombre=models.CharField('Nombre Departamento',  max_length=100)
    def __str__(self):
        return self.dp_nombre
class CorreoCco(models.Model):
    corr_nombre=models.CharField('Nombre',  max_length=200)
    corr_email=models.EmailField('Email',max_length=300)
    corr_telefono=models.CharField('Número teléfonico',max_length=10)
    corr_asunto=models.CharField('Asunto',max_length=150)
    corr_mensaje=models.CharField('Escriba aqui su mensaje',max_length=700)
    corr_depo=models.ForeignKey(Departamento, on_delete=models.PROTECT, verbose_name='Departamento al que se dirige', blank=False, null=True)
    corr_crado=models.DateTimeField(verbose_name='Creado', auto_now_add=True)

    def __str__(self):
        return self.corr_email
    class Meta:
        verbose_name = "Correos de contacto"

class Evento(models.Model):
    event_nombre=models.CharField('Nombre del evento',  max_length=350)
    event_imagen=models.ImageField('Imagen promocional del evento', upload_to='imgEventos/')
    event_fecha_inicial=models.DateField('Fecha inicial del evento')
    event_fecha_final=models.DateField('Fecha final del evento')
    event_ubicacion=models.CharField('Direccion del evento',  max_length=800)
    event_hora_inicio=models.TimeField('Hora de inicio')
    event_hora_fin=models.TimeField('Hora de fianlización')
    event_patrocinado=models.CharField('Patrocinado por', max_length=800)
    event_especificacion=models.CharField('Especificaciones adicionales', max_length=250)
    def __str__(self):
        return self.event_nombre

class RegistroExpo(models.Model):
    re_nombre=models.CharField('Nombres', max_length=100)
    re_apellidos=models.CharField('Apellidos', max_length=100)
    re_correo=models.EmailField('Correo electronico')
    re_telefono=models.CharField('Número teléfonico',max_length=10)
    re_evento=models.ForeignKey(Evento,  on_delete=models.CASCADE, verbose_name='Evento', blank=False, null=True)
    re_creado=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} {} {}".format(self.re_nombre, self.re_apellidos, self.re_evento)

class Marca(models.Model):
    marca_nombre=models.CharField('Nombre Marca', max_length=100)
    marca_img=models.ImageField('Imagen', upload_to='marca_img/')
    def __str__(self):
        return self.marca_nombre


class Catalagos(models.Model):
    cat_nombre=models.CharField('Catalogo', max_length=100)
    cat_img=models.ImageField('Imagen', upload_to='img/catalogo/')
    cat_file=models.FileField('PDF Catalogo', upload_to='pdf/catalogo/')
    def __str__(self):
        return self.cat_nombre

class Promocion(models.Model):
    promo_nombre=models.CharField('Nombre', max_length=150)
    promo_descripcion=models.CharField('Descripcion', max_length=300)
    promo_precio=models.FloatField('Precio')
    promo_imagen=models.ImageField('Imagen', upload_to='img/promociones')
    def __str__(self):
        return self.promo_nombre


class Vacante(models.Model):
    va_departamento=models.ForeignKey(Departamento, on_delete=models.PROTECT, verbose_name='Departamento', blank=False, null=True)
    va_nombre_vacante=models.CharField(max_length=250, verbose_name="Nombre de la vacante")
    va_imagen=models.ImageField(verbose_name="Imagen", upload_to="img/vacantes")
    va_descripcion=models.CharField("Descripción", max_length=1500)
    va_requeriemientos=models.CharField("Requerimientos", max_length=500)
    va_observaciones=models.CharField("Observaciones", max_length=500)
    def __str__(self):
        return self.va_nombre_vacante

class Postulacion(models.Model):
    pos_vacante=models.ForeignKey(Vacante, verbose_name="Vacante deseada", on_delete=models.CASCADE, blank=False, null=True)
    pos_nombre=models.CharField("Nombre Completo", max_length=150)
    pos_correo=models.EmailField("Correo electronico")
    pos_telefono=models.CharField('Número teléfonico',max_length=10)
    pos_cv=models.FileField(verbose_name="Curriculum Vitae", upload_to="file/curriculum", validators=[FileExtensionValidator(allowed_extensions=['pdf'])],help_text="Solo se acepta docuemntos de tipo pdf.")
    pos_creacion=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pos_nombre


STATUS = ((1, 'Creado'), (2, 'Atendiendo'),  (3, 'Surtiendo'), (4, 'En Viaje'),)
# 1 CUANDO EL CLIENTE A CREADO EL PEDIDO
# 2 CUANDO UN ASESOR DE VENTA DESCARGUE LA VENTA
# 3 CUANDO ACTUALIZEN NUMERO DE VENTA EN LA TABLA DE COMPRA WEB
# 4 CUANDO ACTUALIZEN NUMERO DE FACTURA
TIPO_DOMICILIO = ((1, 'Trabajo'), (2, 'Casa'),)
TIPO_PAGO = ((1, 'EFECTIVO'),)

class Domicilio(models.Model):
    dom_nom_ap=models.CharField(max_length=130, verbose_name="Nombre y apellido")
    dom_codigo_p=models.IntegerField(max_length=5, verbose_name="Codigo postal")
    dom_estado=models.CharField(max_length=80, verbose_name="Estado")
    dom_delegacion=models.CharField(max_length=80, verbose_name="Delegacion")
    dom_colonia=models.CharField(max_length=200, verbose_name="Colonia / Asentamiento")
    dom_calle=models.CharField(max_length=200, verbose_name="Calle")
    dom_num_ex=models.IntegerField(verbose_name="N° exterior", help_text='Si no tiene un numero escriba 0')
    dom_num_interior=models.IntegerField(verbose_name="N° interior", blank=True, null=True, help_text="Opcional")
    dom_indicaciones=models.CharField(max_length=700, verbose_name="Indicaciones adicionales para entregar tus compras en esta dirección", help_text="Descripción de la fachada, puntos de referencia para encontrarla, indicaciones de seguridad, etc.")
    dom_tipo=models.IntegerField(verbose_name="¿Es tu trabajo o tu casa?", choices=TIPO_DOMICILIO)
    dom_telefono=models.CharField(max_length=10, verbose_name="Telefono de contacto", help_text="Llamarán a este numero si hay algún problema en el envío")
    dom_activo=models.BooleanField(verbose_name="Default dirección")
    dom_creador=models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario creador', blank=True, null=True)
    def __str__(self):
        return str(self.dom_codigo_p)
    def str_domicilio(self):
        domicilio='C.P:{} calle:{} colonia:{} N° Exterior:{} N° interior:{},  {}, {}. Recibe: {}, Referencias:{} Tipo:{} Tel:{}'.format(
            self.dom_codigo_p, 
            self.dom_calle, 
            self.dom_colonia, 
            self.dom_num_ex,
            self.dom_num_interior,
            self.dom_delegacion,
            self.dom_estado,
            self.dom_nom_ap,
            self.dom_indicaciones,
            self.get_dom_tipo_display(),
            self.dom_telefono,
            )
        return domicilio


class CompraWeb(models.Model):
    cw_id=models.BigAutoField(primary_key=True)
    cw_fecha = models.DateTimeField(auto_now_add=True)
    cw_cliente=models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name='Cliente')
    cw_status=models.IntegerField(verbose_name="Status compra", choices=STATUS, default=1)
    cw_domicilio=models.ForeignKey(Domicilio, on_delete=models.PROTECT, verbose_name="Domicilio de entrega")
    cw_numero_venta=models.IntegerField(verbose_name="Numero venta", blank=True, null=True)
    cw_numero_factura=models.CharField(max_length=10,verbose_name="Numero factura", blank=True, null=True)
    cw_tipo_pago=models.IntegerField(verbose_name="Forma de pago", choices=TIPO_PAGO, default=1)

    class Meta:
        ordering = ["-cw_fecha"]

    def __str__(self):
        return str(self.cw_id)
    def domicilio(self):
        return self.cw_domicilio.str_domicilio()
    def cliente_str(self):
        return "Usuario:{} Cliente:{}".format(self.cw_cliente,self.cw_cliente.rfc)
    def total_compra(self):
        total=Detalle_Compra_Web.objects.filter(dcw_pedido_id=self.cw_id).aggregate(suma_total=Sum(F('dcw_precio') * F('dcw_cantidad'), output_field=FloatField()))['suma_total']
        total=0 if total == None else total
        total = (total * 0.16) + total
        return round(total, 2)



class Detalle_Compra_Web(models.Model):
    dcw_pedido_id = models.ForeignKey(CompraWeb, on_delete=models.CASCADE, verbose_name='Numero de compra', blank=True, null=True)
    dcw_producto_id = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name='Producto')
    dcw_cantidad = models.IntegerField(null=True, blank=True, verbose_name='Cantidad')
    dcw_creado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT,)
    dcw_precio = models.FloatField(default=0)
    dcw_status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.dcw_pedido_id)
    def sub_total(self):
        subtotal=self.dcw_cantidad*self.dcw_precio
        return subtotal







