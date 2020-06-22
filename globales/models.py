# -*- coding: utf-8
"""
Modelo de datos de la app globales
"""

# Future Libraries
from __future__ import unicode_literals

# Standard Libraries
from datetime import datetime

# Django Libraries
from django.db import models


class Pais(models.Model):
    """Gestión de paises
    """

    cod_iso = models.CharField(max_length=3, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    nombre_iso = models.CharField(max_length=255, blank=True, null=True)
    alfa2 = models.CharField(max_length=2, blank=True, null=True)
    alfa3 = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "pais"


class Estado(models.Model):
    """Gestión de estados
    """

    id_estado_ine = models.CharField(max_length=2)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "estado"
        ordering = ["nombre"]


class Municipio(models.Model):
    """Gestión de municipios
    """

    id_municipio_completo_ine = models.CharField(max_length=4)
    id_estado_ine = models.CharField(Estado, max_length=2)
    id_municipio_ine = models.CharField(max_length=2)
    nombre = models.CharField(max_length=255)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, db_column="estado")

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "municipio"
        ordering = ["estado__nombre", "nombre"]


class Parroquia(models.Model):
    """Gestión de parroquias
    """

    id_parroquia_completo_ine = models.CharField(max_length=6)
    id_municipio_completo_ine = models.CharField(max_length=4)
    id_estado_ine = models.CharField(max_length=2)
    id_municipio_ine = models.CharField(max_length=2)
    id_parroquia_ine = models.CharField(max_length=2)
    nombre = models.CharField(max_length=255)
    municipio = models.ForeignKey(
        Municipio, on_delete=models.PROTECT, db_column="municipio_id"
    )
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, db_column="estado_id")

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "parroquia"
        ordering = ["estado__nombre", "municipio__nombre", "nombre"]


class Etnia(models.Model):
    """Gestión de etnias
    """

    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "etnia"


##############################################################################
class InstitucionMinisterial(models.Model):
    """Este modelo sirve para almacenar las Instituciones que dependen del
    MPPEU
    """

    TIPO_INSTITUCION_CHOICES = (
        ("IEU", "INSTITUCIÓN DE EDUCACIÓN UNIVERSITARIA"),
        ("ENTE ADSCRITO", "ENTE ADSCRITO"),
        ("OTRO", "OTRO"),
    )
    DEP_ADMIN_CHOICES = (("PÚBLICA", "PÚBLICA"), ("PRIVADA", "PRIVADA"))
    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=10)
    rif = models.CharField(max_length=45)
    dep_admin = models.CharField(max_length=7, choices=DEP_ADMIN_CHOICES)
    tipo_institucion = models.CharField(max_length=37, choices=TIPO_INSTITUCION_CHOICES)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        db_table = "institucion_ministerial"
        verbose_name = "Ente Adscrito"
        verbose_name_plural = "Entes Adscritos"

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.siglas = self.siglas.upper()
        self.rif = self.rif.upper()
        super().save(*args, **kwargs)


##############################################################################
class CorreoInstitucion(models.Model):
    """agregar comentario de la clase
    """

    institucion = models.ForeignKey(
        "InstitucionMinisterial", on_delete=models.PROTECT, db_index=True
    )
    instancia_administrativa = models.ForeignKey(
        "oeuconfig.InstanciaAdministrativa", on_delete=models.PROTECT, db_index=True
    )
    correo = models.EmailField(max_length=255)

    class Meta:
        db_table = "correo_institucion"
        verbose_name = "Correo Institución"
        verbose_name_plural = "Correos Institución"


##############################################################################
class AutoridadInstitucion(models.Model):
    """Autoridades
    """

    institucion = models.ForeignKey(
        "InstitucionMinisterial", on_delete=models.PROTECT, db_index=True
    )
    persona = models.ForeignKey(
        "cuenta.Persona", on_delete=models.PROTECT, db_index=True
    )
    instancia_administrativa = models.ForeignKey(
        "oeuconfig.InstanciaAdministrativa", on_delete=models.PROTECT, db_index=True
    )
    correo = models.EmailField(max_length=255)
    telefono = models.EmailField(max_length=19)
    celular = models.EmailField(max_length=19)

    class Meta:
        db_table = "autoridad_institucion"
        verbose_name = "Autoridad Institución"
        verbose_name_plural = "Autoridades Institución"
