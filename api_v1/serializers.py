"""
Serializers for oeu app
"""
# Standard Libraries
import logging

# Thirdparty Libraries
import serpy

#  logging
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("services")


class InstitucionMinisterialSerializer(serpy.Serializer):
    """
    Class to serilize academic programs
    """

    nombre = serpy.Field()
    siglas = serpy.Field()
    rif = serpy.Field()
    dep_admin = serpy.Field()


class IeuSerializer(serpy.Serializer):
    """
    Class to serilize academic programs
    """

    id = serpy.Field()
    institucion_ministerial = serpy.MethodField("ieu_nombre", label="nombre")
    siglas = serpy.MethodField("ieu_siglas", label="siglas")
    dep_admin = serpy.MethodField("ieu_dep_admin", label="dep_admin")
    tipo_especifico_ieu = serpy.StrField(label="tipo_ieu")
    logo = serpy.StrField()
    fachada = serpy.StrField()
    cod_activacion = serpy.MethodField("activo", label="activo")

    def activo(self, Ieu):
        if Ieu.cod_activacion == "11001111" or Ieu.cod_activacion == "10001111":
            return True
        return False

    def ieu_nombre(self, Ieu):
        return Ieu.institucion_ministerial.nombre

    def ieu_siglas(self, Ieu):
        return Ieu.institucion_ministerial.siglas

    def ieu_dep_admin(self, Ieu):
        return Ieu.institucion_ministerial.dep_admin


class LocalidadSerializer(serpy.Serializer):
    """
    Class to serilize academic programs
    """

    id = serpy.Field()
    nombre = serpy.MethodField("nombre_localidad")
    ieu = serpy.MethodField("siglas_ieu", label="siglas")
    web_site = serpy.Field()
    direccion = serpy.Field()
    estado = serpy.StrField()
    municipio = serpy.StrField()
    parroquia = serpy.StrField()
    centro_poblado = serpy.Field()
    punto = serpy.Field()
    poligonal = serpy.Field()
    fachada = serpy.StrField()
    ieu_edit = serpy.MethodField("logo", label="logo")
    revisor = serpy.MethodField("ieu_dep_admin", label="dep_admin")
    editor = serpy.MethodField("sede_principal", label="localidad_principal")
    cod_activacion = serpy.MethodField("activo", label="activo")

    def activo(self, Localidad):
        if (
            Localidad.cod_activacion == "11011111"
            or Localidad.cod_activacion == "10011111"
        ):
            return True
        return False

    def nombre_localidad(self, Localidad):
        return "{} {} {}".format(
            Localidad.ieu.institucion_ministerial,
            Localidad.tipo_localidad,
            Localidad.nombre,
        )

    def siglas_ieu(self, Localidad):
        return Localidad.ieu.institucion_ministerial.siglas

    def logo(self, Localidad):
        return "{}".format(Localidad.ieu.logo)

    def ieu_dep_admin(self, Localidad):
        return "{}".format(Localidad.ieu.institucion_ministerial.dep_admin)

    def sede_principal(self, Localidad):
        if Localidad.id != Localidad.ieu.localidad_principal.id:
            return False
        return True


class CarreraSerializer(serpy.Serializer):
    """
    Class to serilize academic programs
    """

    id = serpy.Field()
    nombre = serpy.Field()
    tipo_carrera = serpy.StrField(label="tipo_programa")
    # # descripcion = serpy.Field()
    titulo = serpy.StrField()
    # # mercado_ocupacional = serpy.Field()
    # # periodicidad = serpy.StrField()
    # # duracion = serpy.Field()
    # # prioritaria = serpy.Field()
    # cod_activacion = serpy.MethodField("activo", label="activo")
    area_conocimiento = serpy.StrField()
    sub_area_conocimiento = serpy.StrField()
    localidad = serpy.StrField()

    def activo(self, Carrera):
        if Carrera.cod_activacion == "11111111" or Carrera.cod_activacion == "10111111":
            return True
        return False


class EstadoSerializer(serpy.Serializer):
    """
    Class to serilize Estados
    """

    id = serpy.Field()
    nombre = serpy.Field()


class MunicipioSerializer(serpy.Serializer):
    """
    Class to serilize Municipios
    """

    id = serpy.Field()
    nombre = serpy.Field()
    estado = serpy.MethodField("estado_method")

    def estado_method(self, Parroquia):
        return Parroquia.estado.id


class ParroquiaSerializer(serpy.Serializer):
    """
    Class to serilize parroquias
    """

    id = serpy.Field()
    nombre = serpy.Field()
    municipio = serpy.MethodField("municipio_method")
    estado = serpy.MethodField("estado_method")

    def estado_method(self, Parroquia):
        return Parroquia.estado.id

    def municipio_method(self, Parroquia):
        return Parroquia.municipio.id


class TipoIeuEspecificoSerializer(serpy.Serializer):
    """
    Class to serilize parroquias
    """

    id = serpy.Field()
    tipo = serpy.MethodField("tipo_ieu_method", label="nombre")

    def tipo_ieu_method(self, TipoEspecificoInstitucion):

        if TipoEspecificoInstitucion.nombre:
            nombre_tipo_ieu = "{} {}".format(
                TipoEspecificoInstitucion.sub_tipo_ieu, TipoEspecificoInstitucion.nombre
            )
        else:
            nombre_tipo_ieu = "%s" % (TipoEspecificoInstitucion.sub_tipo_ieu)
        return nombre_tipo_ieu


class AreaSerializer(serpy.Serializer):
    """
    Class to serilize Areas de conocimiento
    """

    id = serpy.Field()
    nombre = serpy.Field()


class SubAreaSerializer(serpy.Serializer):
    """
    Class to serilize Subareas de conocimiento
    """

    id = serpy.Field()
    nombre = serpy.Field()
    area_conocimiento = serpy.StrField()


class TituloSerializer(serpy.Serializer):
    """
    Class to serilize Areas de conocimiento
    """

    id = serpy.Field()
    nombre = serpy.Field()


class TipoProgramaSerializer(serpy.Serializer):
    """
    Class to serilize Areas de conocimiento
    """

    id = serpy.Field()
    nombre = serpy.Field()
