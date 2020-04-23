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
    tipo_especifico_ieu = serpy.StrField(label="tipo_ieu")
    localidad_principal = serpy.StrField()
    logo = serpy.StrField()
    fachada = serpy.StrField()
    cod_activacion = serpy.MethodField("activo", label="activo")
    institucion_ministerial = InstitucionMinisterialSerializer()

    def activo(self, Ieu):
        if Ieu.cod_activacion == "11001111" or Ieu.cod_activacion == "10001111":
            return True
        return False


class LocalidadSerializer(serpy.Serializer):
    """
    Class to serilize academic programs
    """

    id = serpy.Field()
    tipo_localidad = serpy.StrField()
    nombre = serpy.Field()
    web_site = serpy.Field()
    direccion = serpy.Field()
    estado = serpy.StrField()
    municipio = serpy.StrField()
    parroquia = serpy.StrField()
    centro_poblado = serpy.Field()
    punto = serpy.Field()
    poligonal = serpy.Field()
    fachada = serpy.StrField()
    cod_activacion = serpy.MethodField("activo", label="activo")
    ieu = IeuSerializer()

    def activo(self, Localidad):
        if (
            Localidad.cod_activacion == "11011111"
            or Localidad.cod_activacion == "10011111"
        ):
            return True
        return False


class CarreraSerializer(serpy.Serializer):
    """
    Class to serilize academic programs
    """

    id = serpy.Field()
    nombre = serpy.Field()
    tipo_carrera = serpy.StrField(label="tipo_programa")
    descripcion = serpy.Field()
    titulo = serpy.StrField()
    mercado_ocupacional = serpy.Field()
    periodicidad = serpy.StrField()
    duracion = serpy.Field()
    prioritaria = serpy.Field()
    cod_activacion = serpy.MethodField("activo", label="activo")
    area_conocimiento = serpy.StrField()
    sub_area_conocimiento = serpy.StrField()
    localidad = LocalidadSerializer()

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
    nombre = serpy.Field()
    municipio = serpy.MethodField("municipio_method")
    estado = serpy.MethodField("estado_method")

    def estado_method(self, Parroquia):
        return Parroquia.estado.id

    def municipio_method(self, Parroquia):
        return Parroquia.municipio.id
