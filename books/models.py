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


def image_path_person(instance, filename):
    """Ruta para almacenar las fotos de las personas (autore, editores) de los libros
    """
    return os.path.join("persona", str(instance.pk) + "." + filename.rsplit(".", 1)[1])


def image_path_portada(instance, filename):
    """Ruta para almacenar las portadas de los libros
    """
    return os.path.join("portada", str(instance.pk) + "." + filename.rsplit(".", 1)[1])


def image_path_pdf(instance, filename):
    """Ruta para almacenar los pdf de los libros
    """
    return os.path.join("pdf", str(instance.pk) + "." + filename.rsplit(".", 1)[1])


# #################################################################################### #
class BooksPerson(models.Model):
    """
    Este modelo almacena las personas (autore, editores) de los libros
    """

    name = models.CharField(_("Nombre"), max_length=30)
    other_name = models.CharField(
        _("Otro Nombre"), max_length=30, blank=True, null=True
    )
    last_name = models.CharField(_("Apellido"), max_length=30)
    other_last_name = models.CharField(
        _("Otro Apellido"), max_length=30, blank=True, null=True
    )
    birth_date = models.DateField(_("Fecha de Nacimiento"), blank=True, null=True)
    pais_nacimiento = models.ForeignKey(
        "globales.Pais",
        on_delete=models.PROTECT,
        db_index=True,
        related_name="persona_pais_born",
        blank=True,
        null=True,
    )
    ciudad_nacimiento = models.CharField(
        _("Ciudad de Nacimiento"), max_length=120, blank=True, null=True
    )
    fecha_defuncion = models.DateField(_("Fecha de Defunción"), blank=True, null=True)
    pais_defuncion = models.ForeignKey(
        "globales.Pais",
        on_delete=models.PROTECT,
        db_index=True,
        related_name="persona_pais_dead",
        blank=True,
        null=True,
    )
    ciudad_defuncion = models.CharField(
        _("Ciudad de Defunción"), max_length=120, blank=True, null=True
    )
    resumen_biografico = RichTextField(_("Resumen Biográfico"), blank=True, null=True)
    foto = models.ImageField(
        max_length=255,
        null=True,
        default="books_persona/default.png",
        storage=SobreEscribirImagen(),
        upload_to=image_path_person,
        blank=True,
    )
    is_autor = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.name, self.last_name)

    @property
    def full_name(self):
        return "{} {} {} {}".format(
            self.name, self.other_name, self.last_name, self.other_last_name
        )

    class Meta:
        ordering = ["name", "last_name"]
        verbose_name = _("Autor")
        verbose_name_plural = _("Autores")


# #################################################################################### #
class BooksEditorial(models.Model):
    """
    Este modelo almacena lAs EDITORIALES de los libros
    """

    name = models.CharField(_("Nombre"), max_length=30)
    direction = models.TextField(_("Dirección"), blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Editorial")
        verbose_name_plural = _("Editoriales")


# #################################################################################### #
class BooksCategoria(models.Model):
    """
    Este modelo almacena las categoriaS de los libros
    """

    name = models.CharField(_("Name"), max_length=30)
    description = models.CharField(
        _("Descripción"), max_length=120, blank=True, null=True
    )

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")


# #################################################################################### #
class BooksPublicacion(models.Model):
    """ Modelo para almacenar las publicaciones
    """

    fecha_edicion = models.DateField(_("Fecha de Edición"), blank=True, null=True)
    autor = models.ManyToManyField(
        BooksPerson, verbose_name=_("Autor"), related_name="autores", blank=True
    )
    edition_number = models.IntegerField(_("Edición N°"), blank=True, null=True)
    editor = models.ManyToManyField(
        BooksPerson, verbose_name=_("Editor"), related_name="editores", blank=True
    )
    editorial = models.ManyToManyField(
        BooksEditorial,
        verbose_name=_("Editorial (es)"),
        related_name="editoriales",
        blank=True,
    )
    fecha_publicacion = models.DateField(
        _("Fecha de Publicación"), blank=True, null=True
    )
    isbn = models.CharField(_("ISBN"), max_length=17, blank=True, null=True)
    issn = models.CharField(_("ISSN"), max_length=9, blank=True, null=True)
    pais_edicion = models.ForeignKey(
        "globales.Pais",
        verbose_name=_("País de Edición"),
        on_delete=models.PROTECT,
        db_index=True,
        related_name="book_pais",
        blank=True,
        null=True,
    )
    numero = models.IntegerField(_("Número"), blank=True, null=True)
    titulo = models.TextField(_("Título"), max_length=256, blank=True, null=True)
    sub_titulo = models.TextField(
        _("Sub Título"), max_length=256, blank=True, null=True
    )
    volumen = models.CharField(_("Volumen"), max_length=256, blank=True, null=True)
    resumen = RichTextField(_("Resumen"), blank=True, null=True)
    cantidad_paginas = models.IntegerField(blank=True, null=True)
    portada = models.ImageField(
        _("Portada"),
        max_length=255,
        null=True,
        default="books_portada/default.png",
        storage=SobreEscribirImagen(),
        upload_to=image_path_portada,
        blank=True,
    )
    pdf = models.ImageField(
        _("PDF"),
        max_length=255,
        null=True,
        default="books_pdf/default.png",
        storage=SobreEscribirImagen(),
        upload_to=image_path_pdf,
        blank=True,
    )
    categoria = models.ForeignKey(
        BooksCategoria,
        verbose_name=_("Categoría"),
        on_delete=models.PROTECT,
        db_index=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "{} {}".format(self.titulo, self.sub_titulo)

    class Meta:
        ordering = ["titulo"]
        verbose_name = _("Publicacion")
        verbose_name_plural = _("Publicaciones")
