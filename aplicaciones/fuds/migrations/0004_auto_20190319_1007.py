# Generated by Django 2.1.7 on 2019-03-19 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fuds', '0003_auto_20190301_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalConformidad',
            fields=[
                ('conformidad_id', models.IntegerField(blank=True, db_index=True)),
                ('conformidad_descripcion', models.CharField(max_length=150, verbose_name='Descripción de conformidad')),
                ('conformidad_fechaAlta', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical conformidad',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalFactura',
            fields=[
                ('factura_id', models.IntegerField(blank=True, db_index=True)),
                ('FechaFactura', models.DateField(default='2019-03-19')),
                ('factura_folio', models.CharField(db_index=True, max_length=100, verbose_name='Folio de factura')),
                ('factura_total', models.FloatField(verbose_name='Valor de la factura')),
                ('factura_fechaAlta', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical factura',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalFud',
            fields=[
                ('Folio', models.IntegerField(blank=True, db_index=True)),
                ('FechaFactura', models.DateField(blank=True, null=True)),
                ('NumeroCliente', models.IntegerField(default=1, verbose_name='Número de cliente')),
                ('NombreCliente', models.CharField(default='no identificado', max_length=80, verbose_name='Nombre de cliente')),
                ('ZonaCliente', models.CharField(default='no identificado', max_length=80, verbose_name='Zona que pertence el cliente')),
                ('VendedorCliente', models.CharField(default='no identificado', max_length=80, verbose_name='Vendedor asignado al cliente')),
                ('devolucion', models.IntegerField(blank=True, choices=[(1, 'Total'), (2, 'Parcial'), (3, 'N/A')], default=1, null=True, verbose_name='Estado')),
                ('responsable', models.CharField(max_length=80)),
                ('observaciones', models.CharField(max_length=80)),
                ('fecha_creacion', models.DateTimeField(blank=True, editable=False)),
                ('creado_por', models.CharField(max_length=150)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('Motivo', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='fuds.Motivo')),
                ('conformidad', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='fuds.Conformidad')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('tramite', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='fuds.Tramite')),
            ],
            options={
                'verbose_name': 'historical fud',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalMotivo',
            fields=[
                ('motivo_id', models.IntegerField(blank=True, db_index=True)),
                ('motivo_descripcion', models.CharField(max_length=150, verbose_name='Descripción de motivo')),
                ('motivo_fechaAlta', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical motivo',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalTramite',
            fields=[
                ('tramite_id', models.IntegerField(blank=True, db_index=True)),
                ('tramite_descripcion', models.CharField(max_length=150, verbose_name='Descripción de trámite')),
                ('tramite_fechaAlta', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical tramite',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalVendedor',
            fields=[
                ('vendedor_id', models.IntegerField(blank=True, db_index=True)),
                ('vendedor_nombre', models.CharField(max_length=150, verbose_name='Nombre de vendedor')),
                ('vendedor_estatus', models.IntegerField(default=1, verbose_name='Estado de vendedor')),
                ('vendedor_fechaAlta', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical vendedor',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AlterField(
            model_name='factura',
            name='FechaFactura',
            field=models.DateField(default='2019-03-19'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='factura_folio',
            field=models.CharField(max_length=100, unique=True, verbose_name='Folio de factura'),
        ),
    ]
