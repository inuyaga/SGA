# Generated by Django 2.2 on 2019-04-10 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0006_auto_20190222_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='producto_precio',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Precio'),
        ),
    ]
