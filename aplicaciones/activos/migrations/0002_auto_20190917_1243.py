# Generated by Django 2.1.7 on 2019-09-17 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tramitebaja',
            name='tb_user_valido',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserValido', to=settings.AUTH_USER_MODEL, verbose_name='Usuario validó'),
        ),
        migrations.AlterField(
            model_name='asignacion',
            name='asig_archivo_dig',
            field=models.FileField(null=True, upload_to='AsignacionFiles/', verbose_name='Archivo digitalizado'),
        ),
        migrations.AlterField(
            model_name='asignacion',
            name='asig_estado',
            field=models.IntegerField(choices=[(1, 'Vigente'), (2, 'Historio'), (3, 'Pendiente')], default=3, verbose_name='Status Asignación'),
        ),
        migrations.AlterField(
            model_name='tramitebaja',
            name='tb_user_edit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ultimo usuario editó'),
        ),
    ]
