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


def image_path_autor(instance, filename):
    """Ruta para almacenar las fotos de los autores de los libros
    """
    return os.path.join("autor", str(instance.pk) + "." + filename.rsplit(".", 1)[1])


def image_path_editor(instance, filename):
    """Ruta para almacenar las fotos de los editores de los libros
    """
    return os.path.join("editor", str(instance.pk) + "." + filename.rsplit(".", 1)[1])


def image_path_portada(instance, filename):
    """Ruta para almacenar las portadas de los libros
    """
    return os.path.join("portada", str(instance.pk) + "." + filename.rsplit(".", 1)[1])


# Autor, título, edición, editorial, Lugar de edición, Editorial, año, ISBN
# Título, mención de responsabilidad, ISSN, volumen, número y fecha de publicación.Título, Lugar de edición, fecha de publicación, editor, volumen, número e ISSN


# #################################################################################### #
class Autor(models.Model):
    """
    Este modelo almacena loss autores de los libros
    """

    name = models.CharField(_("Name"), max_length=30)
    other_name = models.CharField(_("Other Name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=30)
    other_last_name = models.CharField(
        _("Other Last Name"), max_length=30, blank=True, null=True
    )
    birth_date = models.DateField(_("Birh Date"), blank=True, null=True)
    # pais_nacimiento = models.ForeignKey(
    #     "globales.Pais",
    #     on_delete=models.PROTECT,
    #     db_index=True,
    #     related_name="autor_pais_born",
    #     blank=True,
    #     null=True,
    # )
    ciudad_nacimiento = models.CharField(
        _("Last Name"), max_length=120, blank=True, null=True
    )
    fecha_defuncion = models.DateField(_("Fecha de Defunción"), blank=True, null=True)
    # pais_defuncion = models.ForeignKey(
    #     "globales.Pais",
    #     on_delete=models.PROTECT,
    #     db_index=True,
    #     related_name="autor_pais_dead",
    #     blank=True,
    #     null=True,
    # )
    ciudad_defuncion = models.CharField(
        _("Last Name"), max_length=120, blank=True, null=True
    )
    resumen_biografico = RichTextField(_("Resumen Biográfico"), blank=True, null=True)
    foto = models.ImageField(
        max_length=255,
        null=True,
        default="autor/default.png",
        storage=SobreEscribirImagen(),
        upload_to=image_path_autor,
        blank=True,
    )

    def __str__(self):
        return "{} {}".format(self.name, self.last_name)

    class Meta:
        ordering = ["name", "last_name"]
        verbose_name = _("Autor")
        verbose_name_plural = _("Autores")


# #################################################################################### #
class Editor(models.Model):
    """
    Este modelo almacena loss autores de los libros
    """

    name = models.CharField(_("Name"), max_length=30)
    other_name_nombre = models.CharField(
        _("Other Name"), max_length=30, blank=True, null=True
    )
    last_name = models.CharField(_("Last Name"), max_length=30)
    other_last_name = models.CharField(
        _("Other Last Name"), max_length=30, blank=True, null=True
    )
    birth_date = models.DateField(_("Birh Date"), blank=True, null=True)
    # pais_nacimiento = models.ForeignKey(
    #     "globales.Pais",
    #     on_delete=models.PROTECT,
    #     db_index=True,
    #     related_name="editor_pais_born",
    #     blank=True,
    #     null=True,
    # )
    ciudad_nacimiento = models.CharField(
        _("Last Name"), max_length=120, blank=True, null=True
    )
    fecha_defuncion = models.DateField(_("Fecha de Defunción"), blank=True, null=True)
    # pais_defuncion = models.ForeignKey(
    #     "globales.Pais",
    #     on_delete=models.PROTECT,
    #     db_index=True,
    #     related_name="editor_pais_dead",
    #     blank=True,
    #     null=True,
    # )
    ciudad_defuncion = models.CharField(
        _("Last Name"), max_length=120, blank=True, null=True
    )
    resumen_biografico = RichTextField(_("Resumen Biográfico"), blank=True, null=True)
    foto = models.ImageField(
        max_length=255,
        null=True,
        default="editor/default.png",
        storage=SobreEscribirImagen(),
        upload_to=image_path_editor,
        blank=True,
    )

    def __str__(self):
        return "{} {}".format(self.name, self.last_name)

    class Meta:
        ordering = ["name", "last_name"]
        verbose_name = _("Editor")
        verbose_name_plural = _("Editores")


# #################################################################################### #
class Editorial(models.Model):
    """
    Este modelo almacena lAs EDITORIALES de los libros
    """

    name = models.CharField(_("Nombre"), max_length=30)
    direccion = models.CharField(_("Last Name"), max_length=120, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Editorial")
        verbose_name_plural = _("Editoriales")


# #################################################################################### #
class Categoria(models.Model):
    """
    Este modelo almacena las categoriaS de los libros
    """

    name = models.CharField(_("Name"), max_length=30)
    descripcion = models.CharField(
        _("Descripción"), max_length=120, blank=True, null=True
    )

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")


# #################################################################################### #
class Publicacion(models.Model):

    fecha_edicion = models.DateField(_("Fecha de Edición"), blank=True, null=True)
    autor = models.ManyToManyField(Autor, related_name="autores", blank=True)
    edicion = models.IntegerField(blank=True, null=True)
    editor = models.ManyToManyField("Editor", related_name="editores", blank=True)
    editorial = models.ManyToManyField(
        "Editorial", related_name="editoriales", blank=True
    )
    fecha_publicacion = models.DateField(
        _("Fecha de Publicación"), blank=True, null=True
    )
    isbn = models.CharField(_("ISBN"), max_length=17, blank=True, null=True)
    issn = models.CharField(_("ISSN"), max_length=9, blank=True, null=True)
    # pais_edicion = models.ForeignKey(
    #     "globales.Pais",
    #     on_delete=models.PROTECT,
    #     db_index=True,
    #     related_name="book_pais",
    #     blank=True,
    #     null=True,
    # )
    numero = models.IntegerField(blank=True, null=True)
    titulo = models.TextField(_("Título"), max_length=256, blank=True, null=True)
    sub_titulo = models.TextField(
        _("Sub Título"), max_length=256, blank=True, null=True
    )
    volumen = models.CharField(_("Volumen"), max_length=256, blank=True, null=True)
    resumen = RichTextField(_("Resumen"), blank=True, null=True)
    cantidad_paginas = models.IntegerField(blank=True, null=True)
    # portada =
    # pdf =
    # html =
    portada = models.ImageField(
        max_length=255,
        null=True,
        default="portada/default.png",
        storage=SobreEscribirImagen(),
        upload_to=image_path_portada,
        blank=True,
    )
    categoria = models.ForeignKey(
        "Categoria", on_delete=models.PROTECT, db_index=True, blank=True, null=True
    )

    def __str__(self):
        return "{} {}".format(self.titulo, self.sub_titulo)

    class Meta:
        ordering = ["titulo"]
        verbose_name = _("Publicacion")
        verbose_name_plural = _("Publicaciones")
