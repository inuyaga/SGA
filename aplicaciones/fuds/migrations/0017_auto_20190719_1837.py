# Generated by Django 2.1.7 on 2019-07-19 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuds', '0016_auto_20190719_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='Client_numero',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Número de cliente'),
        ),
    ]