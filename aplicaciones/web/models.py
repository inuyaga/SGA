from django.db import models
from django.core.validators import FileExtensionValidator
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

