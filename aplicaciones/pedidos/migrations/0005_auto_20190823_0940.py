# Generated by Django 2.1.7 on 2019-08-23 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0004_auto_20190823_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignar_gasto_sucursal',
            name='ags_sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresa.Departamento', verbose_name='Departamento'),
        ),
    ]
