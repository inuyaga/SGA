# Generated by Django 2.1.7 on 2019-03-25 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fuds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motivo',
            name='motivo_idconformidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fuds.Conformidad', verbose_name='Id conformidad'),
        ),
    ]