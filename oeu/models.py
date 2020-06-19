"""
Modelo de datos de la app OEU
"""

# Future Libraries
from __future__ import unicode_literals

# Standard Libraries
import os

# Django Libraries
from django.db import models

# Thirdparty Libraries
from ckeditor.fields import RichTextField
from cuenta.libSobreEscribirImagen import SobreEscribirImagen
from djgeojson.fields import PointField, PolygonField


def image_path_logo(instance, filename):
    """Ruta para almacenar los logos de las IEU
    """
    return os.path.join("ieu_logo", str(instance.pk) + "." + filename.rsplit(".", 1)[1])


def image_path_fachada(instance, filename):
    """Ruta para almacenar las fachadas de las IEU
    """
    return os.path.join(
        "ieu_fachada", str(instance.pk) + "." + filename.rsplit(".", 1)[1]
    )


def image_path_localidad(instance, filename):
    """Ruta para almacenar las fachadas de las IEU
    """
    return os.path.join(
        "localidad_fachada", str(instance.pk) + "." + filename.rsplit(".", 1)[1],
    )


# ########################################################################## #
class AreaConocimiento(models.Model):
    """Modelo asignado para almacenar las areas de conocimiento que se imparten
    en las IEU
    """

    nombre = models.CharField(verbose_name="Área de Conocimiento", max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = [
            "nombre",
        ]
        db_table = 'oeu"."area_conocimiento'
        verbose_name = "Área de Conocimiento"
        verbose_name_plural = "Áreas de Conocimiento"


# ########################################################################## #
class SubAreaConocimiento(models.Model):
    """Son las divisiones de las areas de conocimiento usadas en las IEU
    """

    area_conocimiento = models.ForeignKey(
        AreaConocimiento,
        on_delete=models.PROTECT,
        db_index=True,
        verbose_name="Área de conocimiento",
        related_name="areaConocimiento4",
    )
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = [
            "nombre",
        ]
        db_table = 'oeu"."sub_area_conocimiento'
        verbose_name = "Sub Área de Conocimiento"
        verbose_name_plural = "Sub Áreas de Conocimiento"


# ########################################################################## #
class CorreoLocalidad(models.Model):
    """Son las direcciones de correo electronico utilizados por las IEU locales
    """

    localidad = models.ForeignKey("Localidad", on_delete=models.PROTECT, db_index=True)
    instancia_administrativa = models.ForeignKey(
        "oeuconfig.InstanciaAdministrativa", on_delete=models.PROTECT, db_index=True
    )
    correo = models.EmailField(max_length=255)

    class Meta:
        db_table = 'oeu"."correo_localidad'
        verbose_name = "Correo Localidad"
        verbose_name_plural = "Correos Localidad"


# ########################################################################## #
class GrupoCarrera(models.Model):
    """son las carreras impartidas en las IEU
    """

    id_grupo_carrera = models.AutoField(primary_key=True)
    nombre_grupo_carrera = models.CharField(max_length=255)

    class Meta:
        db_table = 'oeu"."grupo_carrera'


# ########################################################################## #
class GrupoRamaEducacion(models.Model):
    """agregar comentario de la clase
    """

    id_grupo_rama_educacion = models.AutoField(primary_key=True)
    nombre_grupo_rama_educacion = models.CharField(max_length=255)

    class Meta:
        db_table = 'oeu"."grupo_rama_educacion'


# ########################################################################## #
class TipoInstitucion(models.Model):
    """Este modelo sirve para almacenar los tipos de instituciones de
    educación universitaria
    """

    nombre = models.CharField(max_length=100)
    orden = models.SmallIntegerField()
    revisor = models.ManyToManyField(
        "cuenta.Persona",
        through="TipoInstitucionRevisor",
        related_name="revisores_tipo_publicados",
    )
    editor = models.ForeignKey(
        "cuenta.Persona",
        on_delete=models.PROTECT,
        db_index=True,
        db_column="persona_editor_id",
        blank=True,
        null=True,
    )
    nombre_edit = models.CharField(max_length=100)
    orden_edit = models.SmallIntegerField()
    revisor_edit = models.ManyToManyField(
        "cuenta.Persona",
        through="TipoInstitucionRevisorEdit",
        related_name="revisores_tipo_editando",
    )
    publicar = models.BooleanField(default=False)
    cod_activacion = models.CharField(
        max_length=9, blank=True, null=True, default="00000001"
    )
    sfc = models.ManyToManyField(
        "oeuconfig.SoporteFormalCambio", through="TipoInstitucionSfc"
    )

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.pk is None:
            self.nombre = self.nombre_edit
            self.orden = self.orden_edit

    class Meta:
        ordering = [
            "nombre",
        ]
        db_table = 'oeu"."tipo_ieu'
        verbose_name = "Tipo IEU"
        verbose_name_plural = "Tipos IEU"


# ########################################################################## #
class TipoInstitucionRevisor(models.Model):
    """Modelo para gestionar los revisores en publicación de los tipos de
    instituciones de educación universitaria
    """

    tipo_ieu = models.ForeignKey("TipoInstitucion", on_delete=models.CASCADE)
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."tipo_ieu_revisor'


# ########################################################################## #
class TipoInstitucionRevisorEdit(models.Model):
    """Modelo para gestionar los revisores en edición de los tipos de
    instituciones de educación universitaria
    """

    tipo_ieu = models.ForeignKey("TipoInstitucion", on_delete=models.CASCADE)
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."tipo_ieu_revisor_edit'


# ########################################################################## #
class TipoInstitucionSfc(models.Model):
    """Modelo para gestionar los soportes formales de cambio de los tipos de
    instituciones de educación universitaria
    """

    tipo_ieu = models.ForeignKey("TipoInstitucion", on_delete=models.CASCADE)
    sfc = models.ForeignKey(
        "oeuconfig.SoporteFormalCambio", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."tipo_ieu_sfc'


# ########################################################################## #
class SubTipoInstitucion(models.Model):
    """Este modelo sirve para almacenar los sub tipos de instituciones de
    educación universitaria
    """

    nombre = models.CharField(max_length=100, blank=True, null=True)
    orden = models.SmallIntegerField()
    tipo_ieu = models.ForeignKey(
        "TipoInstitucion", on_delete=models.PROTECT, db_index=True
    )
    revisor = models.ManyToManyField(
        "cuenta.Persona",
        through="SubTipoInstitucionRevisor",
        related_name="revisores_sub_tipo_publicados",
    )
    editor = models.ForeignKey(
        "cuenta.Persona",
        on_delete=models.PROTECT,
        db_index=True,
        blank=True,
        null=True,
        db_column="persona_editor_id",
    )
    nombre_edit = models.CharField(max_length=255, blank=True, null=True)
    orden_edit = models.SmallIntegerField()
    tipo_ieu_edit = models.ForeignKey(
        "TipoInstitucion",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        db_column="tipo_ieu_edit",
        related_name="oeutipoieu1",
    )
    revisor_edit = models.ManyToManyField(
        "cuenta.Persona",
        through="SubTipoInstitucionRevisorEdit",
        related_name="revisores_sub_tipo_editados",
    )
    publicar = models.BooleanField(default=False)
    cod_activacion = models.CharField(max_length=9, blank=True, null=True)
    sfc = models.ManyToManyField(
        "oeuconfig.SoporteFormalCambio", through="SubTipoInstitucionSfc"
    )

    def __str__(self):
        if self.nombre:
            sub_tipo = "%s %s" % (self.tipo_ieu, self.nombre)
        else:
            sub_tipo = "%s" % (self.tipo_ieu)
        return sub_tipo

    class Meta:
        ordering = [
            "nombre",
        ]
        db_table = 'oeu"."sub_tipo_ieu'
        verbose_name = "Sub Tipo IEU"
        verbose_name_plural = "Sub Tipos IEU"

    def clean(self):
        if self.pk is None:
            self.tipo_ieu = self.tipo_ieu_edit
            self.nombre = self.nombre_edit
            self.orden = self.orden_edit


# ########################################################################## #
class SubTipoInstitucionRevisor(models.Model):
    """Modelo para gestionar los revisores en publicación de los sub tipos de
    instituciones de educación universitaria
    """

    sub_tipo_ieu = models.ForeignKey("SubTipoInstitucion", on_delete=models.CASCADE)
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."sub_tipo_ieu_revisor'


# ########################################################################## #
class SubTipoInstitucionRevisorEdit(models.Model):
    """Modelo para gestionar los revisores en publicación de los sub tipos de
    instituciones de educación universitaria
    """

    sub_tipo_ieu = models.ForeignKey("SubTipoInstitucion", on_delete=models.CASCADE)
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."sub_tipo_ieu_revisor_edit'


# ########################################################################## #
class SubTipoInstitucionSfc(models.Model):
    """Modelo para gestionar los soportes formales de cambio de los tipos de
    instituciones de educación universitaria
    """

    sub_tipo_ieu = models.ForeignKey("SubTipoInstitucion", on_delete=models.CASCADE)
    sfc = models.ForeignKey(
        "oeuconfig.SoporteFormalCambio", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."sub_tipo_ieu_sfc'


# ########################################################################## #
class TipoEspecificoInstitucion(models.Model):
    """Este modelo sirve para almacenar los tipos especificos de instituciones
    de educación universitaria
    """

    nombre = models.CharField(max_length=100, blank=True, null=True)
    orden = models.SmallIntegerField(verbose_name="Orden")
    tipo_ieu = models.ForeignKey(
        "TipoInstitucion", on_delete=models.PROTECT, db_index=True
    )
    sub_tipo_ieu = models.ForeignKey(
        "SubTipoInstitucion", on_delete=models.PROTECT, db_index=True
    )
    revisor = models.ManyToManyField(
        "cuenta.Persona",
        through="TipoEspecificoIeuRevisor",
        related_name="revisores_tipo_especifico_publicados",
    )
    editor = models.ForeignKey(
        "cuenta.Persona",
        on_delete=models.PROTECT,
        db_index=True,
        db_column="persona_editor_id",
        blank=True,
        null=True,
    )
    nombre_edit = models.CharField(max_length=255, blank=True, null=True)
    orden_edit = models.SmallIntegerField()
    tipo_ieu_edit = models.ForeignKey(
        "TipoInstitucion",
        on_delete=models.SET_NULL,
        related_name="tipo_ieu_espec",
        db_column="tipo_ieu_edit",
        blank=True,
        null=True,
    )
    sub_tipo_ieu_edit = models.ForeignKey(
        "SubTipoInstitucion",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="sub_tipo_ieu_edit",
        related_name="oeutipoieuespecifico",
    )
    revisor_edit = models.ManyToManyField(
        "cuenta.Persona",
        through="TipoEspecificoIeuRevisorEdit",
        related_name="revisores_t_e_edit",
    )
    publicar = models.BooleanField(default=False)
    cod_activacion = models.CharField(max_length=9, blank=True, null=True)
    sfc = models.ManyToManyField(
        "oeuconfig.SoporteFormalCambio", through="TipoEspecificoIeuSfc"
    )

    def __str__(self):
        if self.nombre:
            cadena = "%s %s" % (self.sub_tipo_ieu, self.nombre)
        else:
            cadena = "%s" % (self.sub_tipo_ieu)
        return cadena

    class Meta:
        ordering = ["tipo_ieu__nombre", "sub_tipo_ieu__nombre", "nombre"]
        db_table = 'oeu"."tipo_especifico_ieu'
        verbose_name = "Tipo IEU Específico"
        verbose_name_plural = "Tipos IEU Específicos"

    def clean(self):
        if self.pk is None:
            self.tipo_ieu = self.tipo_ieu_edit
            self.sub_tipo_ieu = self.sub_tipo_ieu_edit
            self.nombre = self.nombre_edit
            self.orden = self.orden_edit


# ########################################################################## #
class TipoEspecificoIeuRevisor(models.Model):
    """Modelo para gestionar los revisores en publicación de los tipos especi-
    ficos de las instituciones de educación universitaria
    """

    tipo_especifico_ieu = models.ForeignKey(
        "TipoEspecificoInstitucion", on_delete=models.CASCADE
    )
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."tipo_especifico_ieu_revisor'


# ########################################################################## #
class TipoEspecificoIeuRevisorEdit(models.Model):
    """Modelo para gestionar los revisores en publicación de los sub tipos de
    instituciones de educación universitaria
    """

    tipo_especifico_ieu = models.ForeignKey(
        "TipoEspecificoInstitucion", on_delete=models.CASCADE
    )
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."tipo_especifico_ieu_revisor_edit'


# ########################################################################## #
class TipoEspecificoIeuSfc(models.Model):
    """Modelo para gestionar los soportes formales de cambio de los tipos de
    instituciones de educación universitaria
    """

    tipo_especifico_ieu = models.ForeignKey(
        "TipoEspecificoInstitucion", on_delete=models.CASCADE
    )
    sfc = models.ForeignKey(
        "oeuconfig.SoporteFormalCambio", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."tipo_especifico_ieu_sfc'


# ########################################################################## #
class Ieu(models.Model):
    """Este modelo sirve para almacenar las de IEU
    """

    tipo_especifico_ieu = models.ForeignKey(
        "TipoEspecificoInstitucion", on_delete=models.PROTECT, db_index=True
    )
    institucion_ministerial = models.ForeignKey(
        "globales.InstitucionMinisterial", on_delete=models.PROTECT, db_index=True,
    )
    localidad_principal = models.ForeignKey(
        "Localidad",
        on_delete=models.PROTECT,
        db_index=True,
        related_name="localidades",
    )
    logo = models.ImageField(
        max_length=255, blank=True, null=True, default="ieu_logo/default.png"
    )
    fachada = models.ImageField(
        max_length=255, blank=True, null=True, default="ieu_fachada/default.png",
    )
    revisor = models.ManyToManyField(
        "cuenta.Persona", through="IeuRevisor", related_name="revisor_ieu_publicado"
    )
    editor = models.ForeignKey(
        "cuenta.Persona",
        on_delete=models.PROTECT,
        db_index=True,
        blank=True,
        null=True,
        db_column="persona_editor_id",
    )
    tipo_especifico_ieu_edit = models.ForeignKey(
        TipoEspecificoInstitucion,
        db_column="tipo_especifico_ieu_edit",
        on_delete=models.SET_NULL,
        related_name="oeutipoespecificoedit",
        db_index=True,
        blank=True,
        null=True,
    )
    institucion_ministerial_edit = models.ForeignKey(
        "globales.InstitucionMinisterial",
        related_name="institucionedit",
        on_delete=models.SET_NULL,
        db_column="institucion_ministerial_edit",
        blank=True,
        null=True,
    )
    localidad_principal_edit = models.ForeignKey(
        "Localidad",
        related_name="local_ppal_edi",
        on_delete=models.SET_NULL,
        db_column="localidad_principal_edit",
        blank=True,
        null=True,
    )
    logo_edit = models.ImageField(
        max_length=255,
        null=True,
        default="ieu_logo/default.png",
        storage=SobreEscribirImagen(),
        upload_to=image_path_logo,
        blank=True,
    )
    fachada_edit = models.ImageField(
        max_length=255,
        storage=SobreEscribirImagen(),
        blank=True,
        null=True,
        upload_to=image_path_fachada,
        default="ieu_fachada/default.png",
    )
    revisor_edit = models.ManyToManyField(
        "cuenta.Persona", through="IeuRevisorEdit", related_name="revisores_ieu_edit"
    )
    publicar = models.BooleanField(default=False)
    cod_activacion = models.CharField(max_length=9, blank=True, null=True)
    sfc = models.ManyToManyField("oeuconfig.SoporteFormalCambio", through="IeuSfc")

    def __str__(self):
        return self.institucion_ministerial.nombre

    class Meta:
        ordering = [
            "tipo_especifico_ieu",
            "institucion_ministerial__nombre",
        ]
        db_table = 'oeu"."ieu'
        verbose_name = "Insitución de Educación Universitaria"
        verbose_name_plural = "Instituciones de Educación Universitaria"

    def clean(self):
        if self.pk is None:
            self.tipo_especifico_ieu = self.tipo_especifico_ieu_edit
            self.institucion_ministerial = self.institucion_ministerial_edit
            self.localidad_principal = self.localidad_principal_edit
            self.logo = self.logo_edit
            self.fachada = self.fachada_edit

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.tipo_especifico_ieu_edit = self.tipo_especifico_ieu
            self.institucion_ministerial_edit = self.institucion_ministerial

        super().save(*args, **kwargs)


# ########################################################################## #
class IeuRevisor(models.Model):
    """Modelo para gestionar los revisores en publicación de los sub tipos de
    instituciones de educación universitaria
    """

    ieu = models.ForeignKey("Ieu", on_delete=models.CASCADE)
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."ieu_revisor'


# ########################################################################## #
class IeuRevisorEdit(models.Model):
    """Modelo para gestionar los revisores en publicación de los sub tipos de
    instituciones de educación universitaria
    """

    ieu = models.ForeignKey("Ieu", on_delete=models.CASCADE)
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."ieu_revisor_edit'


# ########################################################################## #
class IeuSfc(models.Model):
    """Modelo para gestionar los soportes formales de cambio de los tipos de
    instituciones de educación universitaria
    """

    ieu = models.ForeignKey("Ieu", on_delete=models.CASCADE)
    sfc = models.ForeignKey(
        "oeuconfig.SoporteFormalCambio", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."ieu_sfc'


# ########################################################################## #
class Localidad(models.Model):
    """Este modelo sirve para almacenar las localidades de las IEU
    """

    ieu = models.ForeignKey("Ieu", on_delete=models.PROTECT, db_index=True)
    tipo_localidad = models.ForeignKey(
        "oeuconfig.TipoLocalidad", on_delete=models.PROTECT, db_index=True
    )
    nombre = models.CharField(max_length=100)
    web_site = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    estado = models.ForeignKey(
        "globales.Estado",
        on_delete=models.PROTECT,
        db_index=True,
        related_name="oeu_estado_pub",
    )
    municipio = models.ForeignKey(
        "globales.Municipio",
        on_delete=models.PROTECT,
        db_index=True,
        related_name="oeu_municipio_pub",
    )
    parroquia = models.ForeignKey(
        "globales.Parroquia",
        on_delete=models.PROTECT,
        db_index=True,
        related_name="oeu_parroquia_pub",
    )
    centro_poblado = models.CharField(max_length=255)
    punto = PointField(blank=True, null=True)
    poligonal = PolygonField(blank=True, null=True)
    fachada = models.ImageField(
        max_length=255, blank=True, null=True, default="localidad_fachada/default.png",
    )
    revisor = models.ManyToManyField(
        "cuenta.Persona",
        through="LocalidadRevisor",
        related_name="revisor_local_publicado",
    )
    editor = models.ForeignKey(
        "cuenta.Persona",
        on_delete=models.PROTECT,
        db_index=True,
        blank=True,
        null=True,
        db_column="persona_editor_id",
    )
    ieu_edit = models.ForeignKey("Ieu", on_delete=models.PROTECT, related_name="ieu")
    tipo_localidad_edit = models.ForeignKey(
        "oeuconfig.TipoLocalidad",
        on_delete=models.PROTECT,
        related_name="tipoLocalidad",
    )
    nombre_edit = models.CharField(max_length=255)
    web_site_edit = models.CharField(max_length=255)
    direccion_edit = models.TextField()
    estado_edit = models.ForeignKey(
        "globales.Estado", on_delete=models.PROTECT, related_name="oeu_estado_edit",
    )
    municipio_edit = models.ForeignKey(
        "globales.Municipio",
        on_delete=models.PROTECT,
        related_name="oeu_municipio_edit",
    )
    parroquia_edit = models.ForeignKey(
        "globales.Parroquia",
        on_delete=models.PROTECT,
        related_name="oeu_parroquia_edit",
    )
    centro_poblado_edit = models.CharField(max_length=255)
    punto_edit = PointField()
    poligonal_edit = PolygonField()
    fachada_edit = models.ImageField(
        max_length=255,
        blank=True,
        null=True,
        upload_to=image_path_localidad,
        storage=SobreEscribirImagen(),
        default="localidad_fachada/default.png",
    )
    revisor_edit = models.ManyToManyField(
        "cuenta.Persona",
        through="LocalidadRevisorEdit",
        related_name="revisores_local_edit",
    )
    publicar = models.BooleanField(default=False)
    cod_activacion = models.CharField(max_length=9, blank=True, null=True)
    sfc = models.ManyToManyField(
        "oeuconfig.SoporteFormalCambio", through="LocalidadSfc"
    )
    ayuda_economica = models.ManyToManyField(
        "oeuconfig.AyudaEconomica", through="LocalidadAyudaEconomica"
    )
    agrupacion_civica = models.ManyToManyField(
        "oeuconfig.AgrupacionCivica", through="LocalidadAgrupacionCivica"
    )
    actividad_cultural = models.ManyToManyField(
        "oeuconfig.ActividadCultural", through="LocalidadActividadCultural"
    )
    red_social = models.ManyToManyField(
        "oeuconfig.RedSocial", through="LocalidadRedSocial"
    )
    disciplina_deportiva = models.ManyToManyField(
        "oeuconfig.DisciplinaDeportiva", through="LocalidadDisciplinaDeportiva"
    )
    organizacion_estudiantil = models.ManyToManyField(
        "oeuconfig.OrganizacionEstudiantil", through="LocalidadOrganizacionEstudiantil"
    )
    requisito_ingreso = models.ManyToManyField(
        "oeuconfig.RequisitoIngreso", through="LocalidadRequisitoIngreso"
    )
    servicio = models.ManyToManyField("oeuconfig.Servicio", through="LocalidadServicio")

    def __str__(self):
        return "%s - %s %s" % (
            self.ieu.institucion_ministerial,
            self.tipo_localidad,
            self.nombre,
        )

    class Meta:
        ordering = ["ieu__institucion_ministerial", "nombre"]
        db_table = 'oeu"."localidad'
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"

    def clean(self):
        if self.pk is None:
            self.ieu = self.ieu_edit
            self.tipo_localidad = self.tipo_localidad_edit
            self.nombre = self.nombre_edit
            self.web_site = self.web_site_edit
            self.direccion = self.direccion_edit
            self.estado = self.estado_edit
            self.municipio = self.municipio_edit
            self.parroquia = self.parroquia_edit
            self.centro_poblado = self.centro_poblado_edit
            self.punto = self.punto_edit
            self.poligonal = self.poligonal_edit

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.ieu_edit = self.ieu

        super().save(*args, **kwargs)


# ########################################################################## #
class LocalidadRevisor(models.Model):
    """Modelo para gestionar los revisores en publicación de los sub tipos de
    instituciones de educación universitaria
    """

    localidad = models.ForeignKey("Localidad", on_delete=models.CASCADE)
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."localidad_revisor'


# ########################################################################## #
class LocalidadRevisorEdit(models.Model):
    """Modelo para gestionar los revisores en publicación de los sub tipos de
    instituciones de educación universitaria
    """

    localidad = models.ForeignKey("Localidad", on_delete=models.CASCADE)
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."localidad_revisor_edit'


# ########################################################################## #
class LocalidadSfc(models.Model):
    """Modelo para gestionar los soportes formales de cambio de los tipos de
    instituciones de educación universitaria
    """

    localidad = models.ForeignKey("Localidad", on_delete=models.CASCADE)
    sfc = models.ForeignKey(
        "oeuconfig.SoporteFormalCambio", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."localidad_sfc'


# ########################################################################## #
class LocalidadRequisitoIngreso(models.Model):
    """Modelo para gestionar los soportes formales de cambio de los tipos de
    instituciones de educación universitaria
    """

    localidad = models.ForeignKey("Localidad", on_delete=models.CASCADE)
    requisito_ingreso = models.ForeignKey(
        "oeuconfig.RequisitoIngreso", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."localidad_requisito_ingreso'


# ########################################################################## #
class LocalidadAyudaEconomica(models.Model):
    """Modelo para gestionar las ayudas económicas de los tipos de
    instituciones de educación universitaria
    """

    localidad = models.ForeignKey("Localidad", on_delete=models.CASCADE)
    ayuda_economica = models.ForeignKey(
        "oeuconfig.AyudaEconomica", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."localidad_ayuda_economica'


# ########################################################################## #
class LocalidadAgrupacionCivica(models.Model):
    """Modelo para gestionar las agrupaciones civicas de cambio de los tipos de
    instituciones de educación universitaria
    """

    localidad = models.ForeignKey("Localidad", on_delete=models.CASCADE)
    agrupacion_civica = models.ForeignKey(
        "oeuconfig.AgrupacionCivica", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."localidad_agrupacion_civica'


# ########################################################################## #
class LocalidadRedSocial(models.Model):
    """Modelo para gestionar las redes sociales de los tipos de
    instituciones de educación universitaria
    """

    localidad = models.ForeignKey("Localidad", on_delete=models.CASCADE)
    red_social = models.ForeignKey(
        "oeuconfig.RedSocial", on_delete=models.PROTECT, db_index=True
    )
    enlace = models.CharField(max_length=255)

    class Meta:
        db_table = 'oeu"."localidad_red_social'


# ########################################################################## #
class LocalidadDisciplinaDeportiva(models.Model):
    """Modelo para gestionar las disciplinas deportivas de los tipos de
    instituciones de educación universitaria
    """

    localidad = models.ForeignKey("Localidad", on_delete=models.CASCADE)
    disciplina_deportiva = models.ForeignKey(
        "oeuconfig.DisciplinaDeportiva", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."localidad_disciplina_deportiva'


# ########################################################################## #
class LocalidadActividadCultural(models.Model):
    """Modelo para gestionar las actividades culturales de los tipos de
    instituciones de educación universitaria
    """

    localidad = models.ForeignKey("Localidad", on_delete=models.CASCADE)
    actividad_cultural = models.ForeignKey(
        "oeuconfig.ActividadCultural", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."localidad_actividad_cultural'


# ########################################################################## #
class LocalidadOrganizacionEstudiantil(models.Model):
    """Modelo para gestionar las organizaciones estudiantiles de los tipos de
    instituciones de educación universitaria
    """

    localidad = models.ForeignKey("Localidad", on_delete=models.CASCADE)
    organizacion_estudiantil = models.ForeignKey(
        "oeuconfig.OrganizacionEstudiantil", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."localidad_organizacion_estudiantil'


# # ########################################################################## #
class LocalidadServicio(models.Model):
    localidad = models.ForeignKey("Localidad", on_delete=models.CASCADE)
    servicio = models.ForeignKey(
        "oeuconfig.Servicio", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."localidad_servicios'


# ########################################################################## #
# class InstanciaAdministrativa(models.Model):
#     """
#     Este modelo controla las instancias administrativas para luego poder
#     referenciar los teléfonos, correos, etc. de las localidades de las IEU
#     """

#     nombre = models.CharField(max_length=100)
#     publicar = models.BooleanField(default=False)

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         ordering = [
#             "nombre",
#         ]
#         db_table = 'oeu"."instancia_administrativa'
#         verbose_name = "Instancia Administrativa"
#         verbose_name_plural = "Instancias Administrativas"


# ########################################################################## #
class CineFCampoAmplio(models.Model):
    """UNESCO CINE-F
    """

    cod_cine_f_campo_amplio = models.CharField(max_length=2)
    descripcion_campo_amplio = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion_campo_amplio

    class Meta:
        db_table = 'oeu"."cine_campo_amplio'
        verbose_name = "CINE Campo Amplio"
        verbose_name_plural = "CINE Campos Amplios"


# ########################################################################## #
class CineFCampoEspecifico(models.Model):
    """UNESCO CINE-F
    """

    cod_cine_f_campo_especifico = models.CharField(max_length=3)
    descripcion_campo_especifico = models.CharField(max_length=255)
    id_cine_f_campo_amplio = models.ForeignKey(
        CineFCampoAmplio, on_delete=models.PROTECT, db_index=True
    )

    def __str__(self):
        return self.descripcion_campo_especifico

    class Meta:
        db_table = 'oeu"."cine_campo_especifico'
        verbose_name = "CINE Campo Especifico"
        verbose_name_plural = "CINE Campos Especificos"


# ########################################################################## #
class CineFCampoDetallado(models.Model):
    """UNESCO CINE-F
    """

    cod_cine_f_campo_detallado = models.CharField(max_length=4)
    descripcion_campo_detallado = models.CharField(max_length=255)
    id_cine_f_campo_especifico = models.ForeignKey(
        CineFCampoEspecifico, on_delete=models.PROTECT, db_index=True
    )

    def __str__(self):
        return self.descripcion_campo_detallado

    class Meta:
        db_table = 'oeu"."cine_campo_detallado'
        verbose_name = "CINE Campo Detallado"
        verbose_name_plural = "CINE Campos Detallados"


# ########################################################################## #
class Carrera(models.Model):
    """
    Este modelo almacena las carreras por cada localidad de las IEU
    """

    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, db_index=True)
    tipo_carrera = models.ForeignKey(
        "oeuconfig.TipoCarrera",
        on_delete=models.PROTECT,
        db_index=True,
        related_name="tipos_carreras",
    )
    area_conocimiento = models.ForeignKey(
        AreaConocimiento,
        on_delete=models.PROTECT,
        db_index=True,
        related_name="AreaConocimiento2",
    )
    sub_area_conocimiento = models.ForeignKey(
        SubAreaConocimiento,
        on_delete=models.PROTECT,
        db_index=True,
        related_name="SubAreaConocimiento2",
    )
    cine_f_campo_amplio = models.ForeignKey(
        CineFCampoAmplio,
        on_delete=models.PROTECT,
        db_index=True,
        related_name="CineFCampoAmplio2",
        null=True,
    )
    cine_f_campo_especifico = models.ForeignKey(
        CineFCampoEspecifico,
        on_delete=models.PROTECT,
        db_index=True,
        related_name="CineFCampoEspecifico2",
        null=True,
    )
    cine_f_campo_detallado = models.ForeignKey(
        CineFCampoDetallado,
        on_delete=models.PROTECT,
        db_index=True,
        related_name="CineFCampoDetallado2",
        null=True,
    )
    titulo = models.ForeignKey(
        "oeuconfig.Titulo",
        on_delete=models.PROTECT,
        db_index=True,
        blank=True,
        null=True,
    )
    institucion_acreditadora = models.ForeignKey(
        "Ieu",
        on_delete=models.PROTECT,
        db_index=True,
        blank=True,
        null=True,
        db_column="institucion_acreditadora",
    )
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    mercado_ocupacional = models.TextField(blank=True, null=True)
    prioritaria = models.BooleanField(default=False)
    periodicidad = models.ForeignKey(
        "oeuconfig.Periodicidad",
        on_delete=models.PROTECT,
        db_column="periodicidad",
        blank=True,
        null=True,
    )
    duracion = models.SmallIntegerField(blank=True, null=True)
    localidad_edit = models.ForeignKey(
        Localidad,
        db_column="localidad_edit",
        on_delete=models.PROTECT,
        related_name="localidad_edit",
    )
    tipo_carrera_edit = models.ForeignKey(
        "oeuconfig.TipoCarrera", db_column="tipo_carrera_edit", on_delete=models.PROTECT
    )
    area_conocimiento_edit = models.ForeignKey(
        AreaConocimiento, db_column="area_conocimiento_edit", on_delete=models.PROTECT,
    )
    sub_area_conocimiento_edit = models.ForeignKey(
        SubAreaConocimiento,
        db_column="sub_area_conocimiento_edit",
        on_delete=models.PROTECT,
        related_name="SubAreaConocimiento3",
    )
    cine_f_campo_amplio_edit = models.ForeignKey(
        "CineFCampoAmplio",
        db_column="cine_f_campo_amplio_edit",
        on_delete=models.PROTECT,
        related_name="CineFCampoAmplio3",
        null=True,
    )
    cine_f_campo_especifico_edit = models.ForeignKey(
        "CineFCampoEspecifico",
        db_column="cine_f_campo_especifico_edit",
        on_delete=models.PROTECT,
        related_name="CineFCampoEspecifico3",
        null=True,
    )
    cine_f_campo_detallado_edit = models.ForeignKey(
        "CineFCampoDetallado",
        db_column="cine_f_campo_detallado_edit",
        on_delete=models.PROTECT,
        related_name="CineFCampoDetallado3",
        null=True,
    )
    titulo_edit = models.ForeignKey(
        "oeuconfig.Titulo",
        db_column="titulo_edit",
        on_delete=models.PROTECT,
        related_name="titulo",
        blank=True,
        null=True,
    )
    ieu_acreditadora_edit = models.ForeignKey(
        "Ieu",
        on_delete=models.PROTECT,
        db_column="institucion_acreditadora_edit",
        related_name="institucionAcreditadora",
        null=True,
        blank=True,
    )
    nombre_edit = models.CharField(max_length=255,)
    descripcion_edit = RichTextField()
    mercado_ocupacional_edit = RichTextField()
    prioritaria_edit = models.BooleanField(default=False)
    periodicidad_edit = models.ForeignKey(
        "oeuconfig.Periodicidad",
        on_delete=models.PROTECT,
        related_name="periodicidad",
        db_column="periodicidad_edit",
        blank=True,
        null=True,
    )
    duracion_edit = models.SmallIntegerField(blank=True, null=True)
    publicar = models.BooleanField(default=False)
    cod_activacion = models.CharField(max_length=9, blank=True, null=True)
    sfc = models.ManyToManyField("oeuconfig.SoporteFormalCambio", through="CarreraSfc")
    titula = models.ManyToManyField(
        "oeuconfig.Titulo", through="CarreraTitulo", related_name="titula"
    )
    titula_edit = models.ManyToManyField(
        "oeuconfig.Titulo", through="CarreraTituloEdit", related_name="titula_e"
    )
    revisor = models.ManyToManyField(
        "cuenta.Persona",
        through="CarreraRevisor",
        related_name="revisor_carrera_publicado",
    )
    revisor_edit = models.ManyToManyField(
        "cuenta.Persona",
        through="CarreraRevisorEdit",
        related_name="revisores_carrera_edit",
    )
    editor = models.ForeignKey(
        "cuenta.Persona",
        on_delete=models.PROTECT,
        db_index=True,
        db_column="persona_editor_id",
        blank=True,
        null=True,
    )

    def __str__(self):
        return "%s" % (self.nombre)

    class Meta:
        ordering = [
            "localidad__ieu__institucion_ministerial__nombre",
            "localidad",
            "area_conocimiento",
            "sub_area_conocimiento",
            "nombre",
        ]
        db_table = 'oeu"."carrera'
        verbose_name = "Programa Académico"
        verbose_name_plural = "Programas Académicos"

    def clean(self):
        if self.pk is None:
            self.localidad = self.localidad_edit
            self.tipo_carrera = self.tipo_carrera_edit
            self.area_conocimiento = self.area_conocimiento_edit
            self.sub_area_conocimiento = self.sub_area_conocimiento_edit
            self.institucion_acreditadora = self.ieu_acreditadora_edit
            self.nombre = self.nombre_edit
            self.descripcion = self.descripcion_edit
            self.titulo = self.titulo_edit
            self.periodicidad = self.periodicidad_edit
            self.duracion = self.duracion_edit
            self.mercado_ocupacional = self.mercado_ocupacional_edit

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.localidad_edit = self.localidad

        super().save(*args, **kwargs)


# ########################################################################## #
class CarreraRevisor(models.Model):
    """Modelo para gestionar los revisores en publicación de los tipos de
    instituciones de educación universitaria
    """

    carrera = models.ForeignKey("Carrera", on_delete=models.CASCADE)
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."carrera_revisor'


# ########################################################################## #
class CarreraRevisorEdit(models.Model):
    """Modelo para gestionar los revisores en edición de los tipos de
    instituciones de educación universitaria
    """

    carrera = models.ForeignKey("Carrera", on_delete=models.CASCADE)
    persona = models.ForeignKey("cuenta.Persona", on_delete=models.PROTECT)

    class Meta:
        db_table = 'oeu"."carrera_revisor_edit'


# ########################################################################## #
class CarreraSfc(models.Model):
    """Modelo para gestionar los soportes formales de cambio de los tipos de
    instituciones de educación universitaria
    """

    carrera = models.ForeignKey("Carrera", on_delete=models.CASCADE)
    sfc = models.ForeignKey(
        "oeuconfig.SoporteFormalCambio", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."carrera_sfc'


# ########################################################################## #
class CarreraTitulo(models.Model):
    """Modelo para gestionar los soportes formales de cambio de los tipos de
    instituciones de educación universitaria
    """

    carrera = models.ForeignKey("Carrera", on_delete=models.CASCADE)
    titulo = models.ForeignKey("oeuconfig.Titulo", on_delete=models.PROTECT)
    periodicidad = models.ForeignKey(
        "oeuconfig.Periodicidad", blank=True, null=True, on_delete=models.PROTECT
    )
    duracion = models.SmallIntegerField()

    def __str__(self):
        return "{} ({} {})".format(
            self.titulo, self.duracion, self.periodicidad.descripcion
        )

    class Meta:
        db_table = 'oeu"."carrera_titulo'
        ordering = ["id"]


# ########################################################################## #
class CarreraTituloEdit(models.Model):
    """Modelo para gestionar los soportes formales de cambio de los tipos de
    instituciones de educación universitaria
    """

    carrera = models.ForeignKey("Carrera", on_delete=models.CASCADE)
    titulo = models.ForeignKey("oeuconfig.Titulo", on_delete=models.PROTECT)
    periodicidad = models.ForeignKey(
        "oeuconfig.Periodicidad", blank=True, null=True, on_delete=models.PROTECT
    )
    duracion = models.SmallIntegerField()

    class Meta:
        db_table = 'oeu"."carrera_titulo_edit'
        ordering = ["id"]


# ########################################################################## #
class CarreraGrupoCarrera(models.Model):
    """No me acuerdo
    """

    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT, db_index=True)
    grupo_carrera = models.ForeignKey(
        GrupoCarrera, on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."carrera_grupo_carrera'


# ########################################################################## #
class CarreraGrupoRamaEducaion(models.Model):
    """No me acuerdo
    """

    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT, db_index=True)
    grupo_rama_educacion = models.ForeignKey(
        GrupoRamaEducacion, on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."carrera_grupo_rama_educaion'


# ########################################################################## #
class TelefonoLocalidad(models.Model):
    """ Teléfonos de las instancias admnistrativas de las localidas de las IEU
    """

    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, db_index=True)
    instancia_administrativa = models.ForeignKey(
        "oeuconfig.InstanciaAdministrativa", on_delete=models.PROTECT, db_index=True
    )
    numero_telefono = models.CharField(max_length=19)

    class Meta:
        db_table = 'oeu"."telefono_localidad'
        verbose_name = "Teléfono Localidad"
        verbose_name_plural = "Teléfonos Localidad"


# ########################################################################## #
# class AyudaEconomica(models.Model):
#     """ modelo de los tipos de ayuda economicas
#     """

#     nombre = models.CharField(max_length=100)
#     descripcion = models.TextField()

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         ordering = ["nombre"]
#         db_table = 'oeu"."tipo_ayuda_economica'
#         verbose_name = "Ayuda Económica"
#         verbose_name_plural = "Ayudas Económicas"


# ########################################################################## #
class AyudaEconomicaLocalidad(models.Model):
    """Ayudas economicas en las loclalidades de las IEU
    """

    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, db_index=True)
    instancia_administrativa = models.ForeignKey(
        "oeuconfig.InstanciaAdministrativa", on_delete=models.PROTECT, db_index=True
    )
    numero_telefono = models.CharField(max_length=19)
    ayuda_economica = models.ForeignKey(
        "oeuconfig.AyudaEconomica", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."tipo_ayuda_economica_localidad'
        verbose_name = "Ayuda Económica"
        verbose_name_plural = "Ayudas Económicas"


# ########################################################################## #
class ActividadCulturalLocalidad(models.Model):
    """Actividades culturales en las loclalidades de las IEU
    """

    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, db_index=True)
    instancia_administrativa = models.ForeignKey(
        "oeuconfig.InstanciaAdministrativa", on_delete=models.PROTECT, db_index=True
    )
    numero_telefono = models.CharField(max_length=19)
    id_actividad_cultural = models.ForeignKey(
        "oeuconfig.ActividadCultural", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."actividad_cultural_localidad'
        verbose_name = "Actividad Cultural"
        verbose_name_plural = "Actividades Culturales"


# ########################################################################## #
class DisciplinaDeportivaLocalidad(models.Model):
    """Disciplinas deportivas en las loclalidades de las IEU
    """

    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, db_index=True)
    instancia_administrativa = models.ForeignKey(
        "oeuconfig.InstanciaAdministrativa", on_delete=models.PROTECT, db_index=True
    )
    numero_telefono = models.CharField(max_length=19)
    disciplina_deportiva = models.ForeignKey(
        "oeuconfig.DisciplinaDeportiva", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."disciplina_deportiva_localidad'
        verbose_name = "Disciplina Deportiva"
        verbose_name_plural = "Disciplinas Deportivas"


# ########################################################################## #
class OrganizacionEstudiantilLocalidad(models.Model):
    """Organizaciones estudiantiles de las loclalidades de las IEU
    """

    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, db_index=True)
    instancia_administrativa = models.ForeignKey(
        "oeuconfig.InstanciaAdministrativa", on_delete=models.PROTECT, db_index=True
    )
    numero_telefono = models.CharField(max_length=19)
    organizacion_estudiantil = models.ForeignKey(
        "oeuconfig.OrganizacionEstudiantil", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."organizacion_estudiantil_localidad'
        verbose_name = "Organizacion Estudiantil"
        verbose_name_plural = "Organizaciones Estudiantiles"


# ########################################################################## #
class AgrupacionCivicaLocalidad(models.Model):
    """Agrupaciones civicas de las localidades de las IEU
    """

    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, db_index=True)
    instancia_administrativa = models.ForeignKey(
        "oeuconfig.InstanciaAdministrativa", on_delete=models.PROTECT, db_index=True
    )
    numero_telefono = models.CharField(max_length=19)
    agrupacion_civica = models.ForeignKey(
        "oeuconfig.AgrupacionCivica", on_delete=models.PROTECT, db_index=True
    )

    class Meta:
        db_table = 'oeu"."agrupacion_civica_localidad'
        verbose_name = "Agrupación Civica"
        verbose_name_plural = "Agrupaciones Civicas"


# ########################################################################## #
class RedSocialLocalidad(models.Model):
    """Redes sociales de las localidades de las IEU
    """

    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, db_index=True)
    instancia_administrativa = models.ForeignKey(
        "oeuconfig.InstanciaAdministrativa", on_delete=models.PROTECT, db_index=True
    )
    red_social = models.ForeignKey(
        "oeuconfig.RedSocial", on_delete=models.PROTECT, db_index=True
    )
    identificador = models.CharField(max_length=255)

    class Meta:
        db_table = 'oeu"."red_social_localidad'
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"


# # ########################################################################## #
# class TipoCarrera(models.Model):
#     """Modelo para gestionar los tipos de carrera que se dictan en las IEU
#     """

#     nombre = models.CharField(max_length=100)
#     descripcion = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         db_table = 'oeu"."tipo_carrera'
#         verbose_name = "Tipo de Programa Académico"
#         verbose_name_plural = "Tipos de Programa Académico"


# ########################################################################## #
# class TipoLocalidad(models.Model):
#     """Modelo para gestionar los tipos de localidad de las IEU.
#     """

#     nombre = models.CharField(max_length=100)
#     descripcion = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         db_table = 'oeu"."tipo_localidad'
#         verbose_name = "Tipo de localidad"
#         verbose_name_plural = "Tipos de localidad"


# ########################################################################## #
# class Titulo(models.Model):
#     """ Modelo para gestionar los titulos que se otorgan en las IEU.
#     """

#     nombre = models.CharField(max_length=255)
#     descripcion = models.TextField()

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         ordering = [
#             "nombre",
#         ]
#         db_table = 'oeu"."titulo'
#         verbose_name = "Título"
#         verbose_name_plural = "Títulos"


# ########################################################################## #
# class TipoTurnoDeEstudio(models.Model):
#     """Modelo para agregar/editar/eliminar/visualizar los turnos que se
#     otorgan en las IEU y clase que pertenece al modulo modelo_simple_listar.
#     """

#     nombre = models.CharField(max_length=100)
#     descripcion = models.TextField()

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         db_table = 'oeu"."turno'
#         verbose_name = "Turno de Estudio"
#         verbose_name_plural = "Turnos de Estudio"


# ########################################################################## #
# class ActividadCultural(models.Model):
#     """Modelo para agregar/editar/eliminar/visualizar las actividades
#     culturales que se otorgan en las IEU y clase que pertenece al modulo
#     modelo_simple_listar.
#     """

#     nombre = models.CharField(max_length=100)
#     descripcion = models.TextField()

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         db_table = 'oeu"."actividad_cultural'
#         verbose_name = "Actividad Cultural"
#         verbose_name_plural = "Actividades Culturales"


# ########################################################################## #
# class DisciplinaDeportiva(models.Model):
#     """ Modelo para agregar/editar/eliminar/visualizar las disciplinas
#     deportivas que se otorgan en las IEU y clase que pertenece al modulo
#     modelo_simple_listar.
#     """

#     nombre = models.CharField(max_length=100)
#     descripcion = models.TextField()

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         db_table = 'oeu"."disciplina_deportiva'
#         verbose_name = "Disciplina Deportiva"
#         verbose_name_plural = "Disciplinas Deportivas"


# ########################################################################## #
# class OrganizacionEstudiantil(models.Model):
#     """ Modelo para agregar/editar/eliminar/visualizar las organizaciones
#     estudiantiles que se otorgan en las IEU y clase que pertenece al modulo
#     modelo_simple_listar.
#     """

#     nombre = models.CharField(max_length=100)
#     descripcion = models.TextField()

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         db_table = 'oeu"."organizacion_estudiantil'
#         verbose_name = "Organizacion Estudiantil"
#         verbose_name_plural = "Organizaciones Estudiantiles"


# ########################################################################## #
# class AgrupacionCivica(models.Model):
#     """ Modelo para agregar/editar/eliminar/visualizar las agrupaciones
#     cívicas que se otorgan en las IEU y clase que pertenece al modulo
#     modelo_simple_listar.
#     """

#     nombre = models.CharField(max_length=100)
#     descripcion = models.TextField()

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         db_table = 'oeu"."agrupacion_civica'
#         verbose_name = "Agrupación Civica"
#         verbose_name_plural = "Agrupaciones Civicas"


# ########################################################################## #
# class RedSocial(models.Model):
#     """ Modelo para agregar/editar/eliminar/visualizar las redes sociales que
#     se otorgan en las IEU y clase que pertenece al modulo modelo_simple_listar.
#     """

#     nombre = models.CharField(max_length=100)
#     descripcion = models.TextField()

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         db_table = 'oeu"."red_social'
#         verbose_name = "Red Social"
#         verbose_name_plural = "Redes Sociales"
