# Generated by Django 2.1.7 on 2019-07-19 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuds', '0013_auto_20190719_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fud',
            name='NumeroVenta',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Número de venta'),
        ),
    ]
