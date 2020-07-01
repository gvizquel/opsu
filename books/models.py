"""
Modelo de datos de la app books
"""

# Future Libraries
from __future__ import unicode_literals

# Standard Libraries
import os

# Django Libraries
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Thirdparty Libraries
from ckeditor.fields import RichTextField
from cuenta.libSobreEscribirImagen import SobreEscribirImagen

# Autor, título, edición, editorial, Lugar de edición, Editorial, año, ISBN
# Título, mención de responsabilidad, ISSN, volumen, número y fecha de publicación.Título, Lugar de edición, fecha de publicación, editor, volumen, número e ISSN


# #################################################################################### #
class Author(models.Model):
    """
    Este modelo almacena loss autores de los libros
    """

    name = models.CharField(_("Name"), max=30)
    other_name_nombre = models.CharField(_("Other Name"), max=30)
    last_name = models.CharField(_("Last Name"), max=30)
    other_last_name = models.CharField(_("Other Last Name"), max=30)
    birth_date = models.DateTimeField(_("Birh Date"))
    # pais_nacimiento =
    # ciudad_nacimiento =
    fecha_defuncion = models.DateTimeField(_("Fecha de Defunción"))
    # pais_defuncion =
    # ciudad_defuncion =

    class Meta:
        ordering = ["name", "other_name"]
        db_table = "books'.'author"
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


# #################################################################################### #
class Book(models.Model):

    # fecha_edicion =
    autor = models.ManyToManyField(Author, through="BookAutor", related_name="autores")
    # edicion =
    # editor =
    # editorial =
    fecha_publicacion = models.DateTimeField(name="Fecha de Publicación")
    # isbn =
    # issn =
    # lugar_edicion =
    # numero =
    # titulo =
    # volumen =


#     localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, db_index=True)
#     tipo_carrera = models.ForeignKey(
#         "oeuconfig.TipoCarrera",
#         on_delete=models.PROTECT,
#         db_index=True,
#         related_name="tipos_carreras",
#     )
#     area_conocimiento = models.ForeignKey(
#         AreaConocimiento,
#         on_delete=models.PROTECT,
#         db_index=True,
#         related_name="AreaConocimiento2",
#     )
#     sub_area_conocimiento = models.ForeignKey(
#         SubAreaConocimiento,
#         on_delete=models.PROTECT,
#         db_index=True,
#         related_name="SubAreaConocimiento2",
#     )
#     cine_f_campo_amplio = models.ForeignKey(
#         CineFCampoAmplio,
#         on_delete=models.PROTECT,
#         db_index=True,
#         related_name="CineFCampoAmplio2",
#         null=True,
#     )
#     cine_f_campo_especifico = models.ForeignKey(
#         CineFCampoEspecifico,
#         on_delete=models.PROTECT,
#         db_index=True,
#         related_name="CineFCampoEspecifico2",
#         null=True,
#     )
#     cine_f_campo_detallado = models.ForeignKey(
#         CineFCampoDetallado,
#         on_delete=models.PROTECT,
#         db_index=True,
#         related_name="CineFCampoDetallado2",
#         null=True,
#     )
#     titulo = models.ForeignKey(
#         "oeuconfig.Titulo",
#         on_delete=models.PROTECT,
#         db_index=True,
#         blank=True,
#         null=True,
#     )
#     institucion_acreditadora = models.ForeignKey(
#         "Ieu",
#         on_delete=models.PROTECT,
#         db_index=True,
#         blank=True,
#         null=True,
#         db_column="institucion_acreditadora",
#     )
#     name = models.CharField(max_length=255)
#     segundo_nombre = models.CharField(max_length=255)
#     apellido = models.CharField(max_length=255)
#     segundo_apellido = models.CharField(max_length=255)
#     descripcion = models.TextField()
#     mercado_ocupacional = models.TextField(blank=True, null=True)
#     prioritaria = models.BooleanField(default=False)
#     periodicidad = models.ForeignKey(
#         "oeuconfig.Periodicidad",
#         on_delete=models.PROTECT,
#         db_column="periodicidad",
#         blank=True,
#         null=True,
#     )
#     duracion = models.SmallIntegerField(blank=True, null=True)
#     localidad_edit = models.ForeignKey(
#         Localidad,
#         db_column="localidad_edit",
#         on_delete=models.PROTECT,
#         related_name="localidad_edit",
#     )
#     tipo_carrera_edit = models.ForeignKey(
#         "oeuconfig.TipoCarrera", db_column="tipo_carrera_edit", on_delete=models.PROTECT
#     )
#     area_conocimiento_edit = models.ForeignKey(
#         AreaConocimiento, db_column="area_conocimiento_edit", on_delete=models.PROTECT,
#     )
#     sub_area_conocimiento_edit = models.ForeignKey(
#         SubAreaConocimiento,
#         db_column="sub_area_conocimiento_edit",
#         on_delete=models.PROTECT,
#         related_name="SubAreaConocimiento3",
#     )
#     cine_f_campo_amplio_edit = models.ForeignKey(
#         "CineFCampoAmplio",
#         db_column="cine_f_campo_amplio_edit",
#         on_delete=models.PROTECT,
#         related_name="CineFCampoAmplio3",
#         null=True,
#     )
#     cine_f_campo_especifico_edit = models.ForeignKey(
#         "CineFCampoEspecifico",
#         db_column="cine_f_campo_especifico_edit",
#         on_delete=models.PROTECT,
#         related_name="CineFCampoEspecifico3",
#         null=True,
#     )
#     cine_f_campo_detallado_edit = models.ForeignKey(
#         "CineFCampoDetallado",
#         db_column="cine_f_campo_detallado_edit",
#         on_delete=models.PROTECT,
#         related_name="CineFCampoDetallado3",
#         null=True,
#     )
#     titulo_edit = models.ForeignKey(
#         "oeuconfig.Titulo",
#         db_column="titulo_edit",
#         on_delete=models.PROTECT,
#         related_name="titulo",
#         blank=True,
#         null=True,
#     )
#     ieu_acreditadora_edit = models.ForeignKey(
#         "Ieu",
#         on_delete=models.PROTECT,
#         db_column="institucion_acreditadora_edit",
#         related_name="institucionAcreditadora",
#         null=True,
#         blank=True,
#     )
#     nombre_edit = models.CharField(max_length=255,)
#     descripcion_edit = RichTextField()
#     mercado_ocupacional_edit = RichTextField()
#     prioritaria_edit = models.BooleanField(default=False)
#     periodicidad_edit = models.ForeignKey(
#         "oeuconfig.Periodicidad",
#         on_delete=models.PROTECT,
#         related_name="periodicidad",
#         db_column="periodicidad_edit",
#         blank=True,
#         null=True,
#     )
#     duracion_edit = models.SmallIntegerField(blank=True, null=True)
#     publicar = models.BooleanField(default=False)
#     cod_activacion = models.CharField(max_length=9, blank=True, null=True)
#     sfc = models.ManyToManyField("oeuconfig.SoporteFormalCambio", through="CarreraSfc")
#     titula = models.ManyToManyField(
#         "oeuconfig.Titulo", through="CarreraTitulo", related_name="titula"
#     )
#     titula_edit = models.ManyToManyField(
#         "oeuconfig.Titulo", through="CarreraTituloEdit", related_name="titula_e"
#     )
#     revisor = models.ManyToManyField(
#         "cuenta.Persona",
#         through="CarreraRevisor",
#         related_name="revisor_carrera_publicado",
#     )
#     revisor_edit = models.ManyToManyField(
#         "cuenta.Persona",
#         through="CarreraRevisorEdit",
#         related_name="revisores_carrera_edit",
#     )
#     editor = models.ForeignKey(
#         "cuenta.Persona",
#         on_delete=models.PROTECT,
#         db_index=True,
#         db_column="persona_editor_id",
#         blank=True,
#         null=True,
#     )

#     def __str__(self):
#         return "%s" % (self.nombre)

#     class Meta:
#         ordering = [
#             "localidad__ieu__institucion_ministerial__nombre",
#             "localidad",
#             "area_conocimiento",
#             "sub_area_conocimiento",
#             "nombre",
#         ]
#         db_table = 'oeu"."carrera'
#         verbose_name = "Programa Académico"
#         verbose_name_plural = "Programas Académicos"

#     def clean(self):
#         if self.pk is None:
#             self.localidad = self.localidad_edit
#             self.tipo_carrera = self.tipo_carrera_edit
#             self.area_conocimiento = self.area_conocimiento_edit
#             self.sub_area_conocimiento = self.sub_area_conocimiento_edit
#             self.institucion_acreditadora = self.ieu_acreditadora_edit
#             self.nombre = self.nombre_edit
#             self.descripcion = self.descripcion_edit
#             self.titulo = self.titulo_edit
#             self.periodicidad = self.periodicidad_edit
#             self.duracion = self.duracion_edit
#             self.mercado_ocupacional = self.mercado_ocupacional_edit

#     def save(self, *args, **kwargs):
#         if self.pk is not None:
#             self.localidad_edit = self.localidad

#         super().save(*args, **kwargs)
