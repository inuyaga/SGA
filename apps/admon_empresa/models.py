# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Empresa(models.Model):
    nombre = models.CharField(max_length=120)
    tipo = models.CharField(max_length=20)
    abrebiacion = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.nombre


class Zona(models.Model):
    zona_id = models.AutoField(primary_key=True)
    nombre_zona = models.CharField(max_length=80)

    def __str__(self):
        return self.nombre_zona


class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    nombre_suc = models.CharField(max_length=150)
    direccion = models.CharField(max_length=250)
    tipo_sucursal = models.CharField(max_length=10)
    zona_id = models.OneToOneField(
        Zona, null=True, blank=True, on_delete=models.CASCADE)
    empresa = models.ForeignKey(
        Empresa, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_suc
