# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-16 14:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('tipo', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id_sucursal', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_suc', models.CharField(max_length=150)),
                ('direccion', models.CharField(max_length=250)),
                ('tipo_sucursal', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('zona_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_zona', models.CharField(max_length=80)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admon_empresa.Empresa')),
            ],
        ),
        migrations.AddField(
            model_name='sucursal',
            name='zona_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admon_empresa.Zona'),
        ),
    ]
