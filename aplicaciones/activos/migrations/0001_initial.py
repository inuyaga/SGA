# Generated by Django 2.1.7 on 2019-09-07 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activo',
            fields=[
                ('activo', models.AutoField(primary_key=True, serialize=False)),
                ('activo_nombre', models.CharField(max_length=80, verbose_name='Nombre')),
                ('activo_modelo', models.CharField(max_length=50, verbose_name='Modelo')),
                ('activo_serie', models.CharField(max_length=30, verbose_name='Serie')),
                ('activo_codigo_barra', models.CharField(max_length=20, verbose_name='Codigo de Barra')),
                ('activo_costo', models.FloatField(verbose_name='Costo de activo')),
                ('activo_observacion', models.TextField(verbose_name='Observación')),
                ('activo_status', models.IntegerField(choices=[(1, 'Nuevo'), (2, 'Buen estado'), (3, 'Deteriorado'), (4, '-------'), (5, 'Tramite de baja'), (6, 'Baja')], default=2, verbose_name='Status')),
                ('activo_situacion', models.IntegerField(choices=[(1, 'Asignado'), (2, 'Stock')], default=2, verbose_name='Situación del activo')),
            ],
        ),
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asig_fecha_adicion', models.DateField(auto_now_add=True)),
                ('asig_fecha_actualizacion', models.DateField(auto_now=True)),
                ('asig_estado', models.IntegerField(choices=[(1, 'Vigente'), (2, 'Historio')], default=1, verbose_name='Status Asignación')),
                ('asig_archivo_dig', models.FileField(blank=True, null=True, upload_to='AsignacionFiles/', verbose_name='Archivo digitalizado')),
                ('asig_observacion', models.CharField(max_length=300, verbose_name='Observacion')),
                ('asig_activo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activos.Activo', verbose_name='Seleccione activo')),
                ('asig_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario a asignar')),
                ('asig_user_edit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserEdit', to=settings.AUTH_USER_MODEL, verbose_name='Ultimo usuario editó')),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_nombre', models.CharField(max_length=50, unique=True, verbose_name='Nombre de categoria')),
                ('cat_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.Area', verbose_name='Area a la que pertenece')),
            ],
        ),
        migrations.CreateModel(
            name='Especificacion',
            fields=[
                ('especificacion', models.AutoField(primary_key=True, serialize=False)),
                ('esp_item', models.CharField(max_length=120, verbose_name='Item')),
                ('esp_valor', models.CharField(max_length=100, verbose_name='Especificación')),
                ('esp_tiene_costo', models.BooleanField(default=False, verbose_name='Tiene algun costo?')),
                ('esp_costo', models.FloatField(default=0.0, verbose_name='Costo de la especificacion')),
                ('esp_activo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activos.Activo', verbose_name='Activo perteneciente')),
            ],
        ),
        migrations.CreateModel(
            name='TramiteBaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tb_fecha_creacion', models.DateField(auto_now_add=True)),
                ('tb_fecha_actualizacion', models.DateField(auto_now=True)),
                ('tb_observacion', models.CharField(max_length=600, verbose_name='Observacion o motivo por el cual se dara de baja')),
                ('tb_validacion', models.FileField(blank=True, null=True, upload_to='TramitesBajas/Files/')),
                ('tb_validado', models.BooleanField(default=0)),
                ('tb_activo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activos.Activo', verbose_name='Seleccione activo')),
                ('tb_user_edit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserValido', to=settings.AUTH_USER_MODEL, verbose_name='Usuario validó')),
            ],
            options={
                'permissions': [('puede_validar_Tramite', 'Puede validar tramite de baja')],
            },
        ),
        migrations.AddField(
            model_name='activo',
            name='activo_categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activos.Categoria', verbose_name='Categoria a la que pertenece'),
        ),
        migrations.AddField(
            model_name='activo',
            name='activo_marca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.Marca', verbose_name='Marca'),
        ),
    ]
