# Generated by Django 2.1.7 on 2019-11-21 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0009_catalogo_productos_tp_orientacion_t'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogo_productos',
            name='tp_orientacion_t',
            field=models.IntegerField(choices=[(1, 'Derecha'), (2, 'Izquierda')], default=1, verbose_name='Orientacion de tabla'),
        ),
    ]
