# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-22 20:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admon_empresa', '0012_auto_20190118_1212'),
        ('pedidos', '0012_auto_20190122_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('pertenece_sucursal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='admon_empresa.Departamento', verbose_name='Sucursal')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
