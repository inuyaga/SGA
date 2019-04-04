# Generated by Django 2.1.7 on 2019-03-19 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pedidos', '0006_auto_20190222_0949'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalProducto',
            fields=[
                ('producto_codigo', models.CharField(db_index=True, max_length=15)),
                ('producto_nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('producto_descripcion', models.CharField(max_length=150, verbose_name='Descripcion')),
                ('producto_imagen', models.TextField(max_length=100, verbose_name='Imagen')),
                ('producto_precio', models.FloatField(blank=True, null=True, verbose_name='Precio')),
                ('tipo_producto', models.IntegerField(blank=True, choices=[(1, 'Uso Interno'), (2, 'Activo Fijo')], null=True)),
                ('producto_es_kit', models.BooleanField(default=False, verbose_name='Pertenecera a un Kit')),
                ('producto_kit', models.BooleanField(default=False, verbose_name='Kit')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('producto_area', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='pedidos.Area', verbose_name='Area')),
                ('producto_marca', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='pedidos.Marca', verbose_name='Marca')),
            ],
            options={
                'verbose_name': 'historical producto',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
