# Generated by Django 2.1.7 on 2019-10-12 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0002_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='cli_nombre',
            field=models.CharField(max_length=80, null=True, verbose_name='Nombre'),
        ),
    ]
