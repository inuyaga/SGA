# Generated by Django 2.1.7 on 2019-12-27 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0022_inventario_inv_tipo_sitio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventario',
            options={'ordering': ['-inv_fecha_add'], 'permissions': [('puede_visualizar_avance_conteo_inventario', 'Puede Ver avance del conteo de inventario')]},
        ),
    ]
