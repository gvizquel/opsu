"""
Serializers for oeu app
"""
# Standard Libraries
import logging

# Thirdparty Libraries
import serpy
from oeu.models import Carrera, Ieu
from rest_framework import serializers

#  logging
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("services")


class IeuSerializer(serializers.ModelSerializer):
    """Serializador para las Instituciones de Educación Universitaria.
    'activo' representa un metodo para identificar si un registro de este modelo de
    datos esta activo o no.
    """

    ieu_nombre = serializers.CharField(
        read_only=True, source="institucion_ministerial.nombre"
    )
    siglas = serializers.CharField(
        read_only=True, source="institucion_ministerial.siglas"
    )
    dep_admin = serializers.CharField(
        read_only=True, source="institucion_ministerial.dep_admin"
    )
    activo = serializers.SerializerMethodField("registro_activo")

    class Meta:
        model = Ieu
        fields = [
            "id",
            "ieu_nombre",
            "siglas",
            "dep_admin",
            "tipo_especifico_ieu",
            "logo",
            "fachada",
            "activo",
        ]
        read_only_fields = [
            "id",
            "ieu_nombre",
            "siglas",
            "dep_admin",
            "tipo_especifico_ieu",
            "logo",
            "fachada",
            "activo",
        ]

    def registro_activo(self, obj):
        if obj.cod_activacion == "11001111" or obj.cod_activacion == "10001111":
            return True
        return False


class LocalidadSerializer(serpy.Serializer):
    """
    Class to serilize academic programs
    """

    id = serpy.Field()
    nombre = serpy.MethodField("nombre_localidad")
    ieu = serpy.MethodField("siglas_ieu", label="siglas")
    revisor_edit = serpy.MethodField("id_ieu", label="id_ieu")
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

    def id_ieu(self, Localidad):
        return Localidad.ieu.id

    def logo(self, Localidad):
        return "{}".format(Localidad.ieu.logo)

    def ieu_dep_admin(self, Localidad):
        return "{}".format(Localidad.ieu.institucion_ministerial.dep_admin)

    def sede_principal(self, Localidad):
        if Localidad.id == Localidad.ieu.localidad_principal_id:
            return True
        return False


class CarreraSerializer(serializers.ModelSerializer):
    """Serializador para los programas academicos.
    'activo' representa un metodo para identificar si un registro de este modelo de
    datos esta activo o no.
    """

    tipo_programa = serializers.CharField(source="tipo_carrera")
    titulo = serializers.StringRelatedField(many=True, source="titula")
    activo = serializers.SerializerMethodField("registro_activo")

    class Meta:
        model = Carrera
        fields = [
            "id",
            "nombre",
            "tipo_programa",
            "titulo",
            "area_conocimiento",
            "sub_area_conocimiento",
            "localidad",
            "activo",
        ]
        read_only_fields = [
            "id",
            "nombre",
            "tipo_programa",
            "titulo",
            "area_conocimiento",
            "sub_area_conocimiento",
            "localidad",
            "activo",
        ]

    def registro_activo(self, obj):
        if obj.cod_activacion == "11111111" or obj.cod_activacion == "10111111":
            return True
        return False


class DetalleCarreraSerializer(serializers.ModelSerializer):
    """Serializador para los programas academicos.
    'activo' representa un metodo para identificar si un registro de este modelo de
    datos esta activo o no.
    """

    tipo_programa = serializers.CharField(source="tipo_carrera")
    titulo = serializers.StringRelatedField(many=True, source="titula")
    activo = serializers.SerializerMethodField("registro_activo")
    id_ieu = serializers.CharField(
        source="localidad.ieu.institucion_ministerial.pk", read_only=True,
    )
    ieu = serializers.CharField(
        source="localidad.ieu.institucion_ministerial.nombre", read_only=True,
    )
    id_localidad = serializers.CharField(source="localidad.pk", read_only=True,)

    class Meta:
        model = Carrera
        fields = [
            "id",
            "id_ieu",
            "ieu",
            "id_localidad",
            "localidad",
            "nombre",
            "area_conocimiento",
            "sub_area_conocimiento",
            "tipo_programa",
            "titulo",
            "descripcion",
            "mercado_ocupacional",
            "periodicidad",
            "duracion",
            "prioritaria",
            "activo",
            "localidad",
        ]
        read_only_fields = [
            "id",
            "id_ieu",
            "ieu",
            "id_localidad",
            "localidad",
            "nombre",
            "area_conocimiento",
            "sub_area_conocimiento",
            "tipo_programa",
            "titulo",
            "descripcion",
            "mercado_ocupacional",
            "periodicidad",
            "duracion",
            "prioritaria",
            "activo",
            "localidad",
        ]

    def registro_activo(self, obj):
        if obj.cod_activacion == "11111111" or obj.cod_activacion == "10111111":
            return True
        return False


class EstadoSerializer(serpy.Serializer):
    """
    Class to serilize Estados
    """

    id = serpy.Field(required=False)
    nombre = serpy.Field(required=False)


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
