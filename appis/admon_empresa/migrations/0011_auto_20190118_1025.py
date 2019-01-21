# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-18 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admon_empresa', '0010_auto_20190118_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamento',
            name='departamento_nombre',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='empresa_abrebiacion',
            field=models.CharField(max_length=10, verbose_name='Abrebiacion'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='empresa_nombre',
            field=models.CharField(max_length=120, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='empresa_tipo',
            field=models.CharField(max_length=20, verbose_name='Tipo de empresa'),
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='sucursal_direccion',
            field=models.CharField(max_length=250, verbose_name='Direccion'),
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='sucursal_tipo_sucursal',
            field=models.CharField(max_length=10, verbose_name='Tipo sucursal'),
        ),
        migrations.AlterField(
            model_name='zona',
            name='zona_nombre',
            field=models.CharField(max_length=80, verbose_name='Nombre de zona'),
        ),
    ]
