# Generated by Django 2.1.7 on 2019-09-24 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenservicio',
            name='ods_diagnostico',
            field=models.CharField(max_length=600, null=True, verbose_name='Diagnostico Tecnico'),
        ),
        migrations.AlterField(
            model_name='ordenservicio',
            name='ods_doc',
            field=models.FileField(null=True, upload_to='ods/documento/validacion', verbose_name='PDF firmado'),
        ),
        migrations.AlterField(
            model_name='ordenservicio',
            name='ods_falla_rep',
            field=models.CharField(max_length=600, null=True, verbose_name='Falla reportada por el usuario'),
        ),
        migrations.AlterField(
            model_name='ordenservicio',
            name='ods_observacion',
            field=models.CharField(max_length=600, null=True, verbose_name='Observaciones'),
        ),
        migrations.AlterField(
            model_name='ordenservicio',
            name='ods_user_seguimiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserTecnicoOds', to=settings.AUTH_USER_MODEL, verbose_name='Usuario tecnico atendiendo ods'),
        ),
    ]
