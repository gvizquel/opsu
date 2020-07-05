"""
Serializers for oeu app
"""
# Standard Libraries
import logging

# Thirdparty Libraries
from globales.models import Estado, Municipio, Parroquia
from oeu.models import (
    AreaConocimiento,
    Carrera,
    CarreraTitulo,
    Ieu,
    Localidad,
    SubAreaConocimiento,
)
from oeuconfig.models import TipoCarrera, Titulo
from rest_framework import serializers

#  logging
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("services")


# #################################################################################### #
class ListaEstadoSerializer(serializers.ModelSerializer):
    """Serializador para los Estados.
    """

    class Meta:
        model = Estado
        fields = [
            "id",
            "nombre",
        ]
        read_only_fields = [
            "id",
            "nombre",
        ]


# #################################################################################### #
class ListaMunicipioSerializer(serializers.ModelSerializer):
    """Serializador para los Estados.
    """

    class Meta:
        model = Municipio
        fields = [
            "id",
            "nombre",
            "estado",
        ]
        read_only_fields = [
            "id",
            "nombre",
            "estado",
        ]


# #################################################################################### #
class ListaParroquiaSerializer(serializers.ModelSerializer):
    """Serializador para los Parroquias.
    'activo' representa un metodo para identificar si un registro de este modelo de
    datos esta activo o no.
    """

    class Meta:
        model = Parroquia
        fields = [
            "id",
            "nombre",
            "estado",
            "municipio",
        ]
        read_only_fields = [
            "id",
            "nombre",
            "estado",
            "municipio",
        ]


class ListaIeuSerializer(serializers.ModelSerializer):
    """Serializador para las Instituciones de Educación Universitaria.
    'activo' representa un metodo para identificar si un registro de este modelo de
    datos esta activo o no.
    """

    nombre = serializers.CharField(
        source="institucion_ministerial.nombre", read_only=True
    )
    siglas = serializers.CharField(
        source="institucion_ministerial.siglas", read_only=True
    )
    dep_admin = serializers.CharField(
        source="institucion_ministerial.dep_admin", read_only=True
    )
    activo = serializers.SerializerMethodField("registro_activo", read_only=True)
    tipo_ieu = serializers.CharField(source="tipo_especifico_ieu", read_only=True)
    logo = serializers.CharField(read_only=True)
    fachada = serializers.CharField(read_only=True)

    class Meta:
        model = Ieu
        fields = [
            "id",
            "nombre",
            "siglas",
            "dep_admin",
            "tipo_ieu",
            "logo",
            "fachada",
            "activo",
        ]
        read_only_fields = [
            "id",
            "nombre",
            "siglas",
            "dep_admin",
            "tipo_ieu",
            "logo",
            "fachada",
            "activo",
        ]

    def registro_activo(self, obj):
        if obj.cod_activacion == "11001111" or obj.cod_activacion == "10001111":
            return True
        return False


# #################################################################################### #
class ListaLocalidadSerializer(serializers.ModelSerializer):
    """Serializador para las Instituciones de Educación Universitaria.
    'activo' representa un metodo para identificar si un registro de este modelo de
    datos esta activo o no.
    """

    siglas = serializers.CharField(
        source="ieu.institucion_ministerial.siglas", read_only=True
    )
    dep_admin = serializers.CharField(
        source="ieu.institucion_ministerial.dep_admin", read_only=True
    )
    activo = serializers.SerializerMethodField("registro_activo")
    nombre = serializers.SerializerMethodField("get_nombre_localidad")
    punto = serializers.DictField(read_only=True)
    localidad_principal = serializers.SerializerMethodField("get_localidad_principal")

    class Meta:
        model = Localidad
        fields = [
            "id",
            "nombre",
            "siglas",
            "punto",
            "dep_admin",
            "localidad_principal",
            "activo",
        ]
        read_only_fields = [
            "id",
            "nombre",
            "siglas",
            "punto",
            "dep_admin",
            "localidad_principal",
            "activo",
        ]

    def registro_activo(self, obj):
        if obj.cod_activacion == "11011111" or obj.cod_activacion == "10011111":
            return True
        return False

    def get_nombre_localidad(self, obj):
        return "{} {} {}".format(
            obj.ieu.institucion_ministerial, obj.tipo_localidad, obj.nombre,
        )

    def get_localidad_principal(self, obj):
        if obj.id == obj.ieu.localidad_principal_id:
            return True
        return False

    def get_fachada(self, obj):
        return "{}".format(obj.fachada)


# #################################################################################### #
class DetalleLocalidadSerializer(serializers.ModelSerializer):
    """Serializador para las Instituciones de Educación Universitaria.
    'activo' representa un metodo para identificar si un registro de este modelo de
    datos esta activo o no.
    """

    id_ieu = serializers.IntegerField(source="ieu.id")
    nombre_ieu = serializers.CharField(source="ieu.institucion_ministerial.nombre")
    fachada = serializers.SerializerMethodField("get_fachada")
    logo = serializers.CharField(source="ieu.logo")
    siglas = serializers.CharField(
        source="ieu.institucion_ministerial.siglas", read_only=True
    )
    dep_admin = serializers.CharField(source="ieu.institucion_ministerial.dep_admin")
    activo = serializers.SerializerMethodField("registro_activo")
    nombre = serializers.SerializerMethodField("get_nombre_localidad")
    localidad_principal = serializers.SerializerMethodField("get_localidad_principal")
    punto = serializers.DictField(read_only=True)
    poligonal = serializers.DictField()
    estado = serializers.CharField(source="estado.nombre")
    municipio = serializers.CharField(source="municipio.nombre")
    parroquia = serializers.CharField(source="parroquia.nombre")

    class Meta:
        model = Localidad
        fields = [
            "id",
            "nombre",
            "siglas",
            "id_ieu",
            "nombre_ieu",
            "web_site",
            "direccion",
            "estado",
            "municipio",
            "parroquia",
            "centro_poblado",
            "punto",
            "poligonal",
            "fachada",
            "logo",
            "dep_admin",
            "localidad_principal",
            "activo",
        ]
        read_only_fields = [
            "id",
            "nombre",
            "siglas",
            "id_ieu",
            "nombre_ieu",
            "web_site",
            "direccion",
            "estado",
            "municipio",
            "parroquia",
            "centro_poblado",
            "punto",
            "poligonal",
            "fachada",
            "logo",
            "dep_admin",
            "localidad_principal",
            "activo",
        ]

    def registro_activo(self, obj):
        if obj.cod_activacion == "11011111" or obj.cod_activacion == "10011111":
            return True
        return False

    def get_nombre_localidad(self, obj):
        return "{} {} {}".format(
            obj.ieu.institucion_ministerial, obj.tipo_localidad, obj.nombre,
        )

    def get_localidad_principal(self, obj):
        if obj.id == obj.ieu.localidad_principal_id:
            return True
        return False

    def get_fachada(self, obj):
        return "{}".format(obj.fachada)


# #################################################################################### #
class ListaProgramaAcademicoSerializer(serializers.ModelSerializer):
    """Serializador para los programas academicos.
    'activo' representa un metodo para identificar si un registro de este modelo de
    datos esta activo o no.
    """

    tipo_programa = serializers.CharField(source="tipo_carrera")
    titulo = serializers.SerializerMethodField("get_titulo")
    activo = serializers.SerializerMethodField("registro_activo")
    area_conocimiento = serializers.CharField(
        source="area_conocimiento.nombre", read_only=True
    )
    sub_area_conocimiento = serializers.CharField(
        source="sub_area_conocimiento.nombre", read_only=True
    )
    localidad = serializers.SerializerMethodField("get_localidad")

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

    def get_titulo(self, obj):
        titulo_srt = ""
        titulos = CarreraTitulo.objects.filter(carrera=obj.id)
        for titulo in titulos:
            if titulo_srt:
                titulo_srt = "{}<br>{} ({} {})".format(
                    titulo_srt,
                    titulo.titulo,
                    titulo.duracion,
                    obj.periodicidad.descripcion,
                )
            else:
                titulo_srt = "{} ({} {})".format(
                    titulo.titulo, titulo.duracion, obj.periodicidad.descripcion,
                )
        return titulo_srt

    def get_localidad(self, obj):
        return "{}".format(obj.localidad)


class ListaProgramaAcademicoNombreSerializer(serializers.Serializer):
    """Serializador para los nombres de losprogramas academicos.
    """

    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=200)


class DetalleProgramaAcademicoSerializer(serializers.ModelSerializer):
    """Serializador para los programas academicos.
    'activo' representa un metodo para identificar si un registro de este modelo de
    datos esta activo o no.
    """

    tipo_programa = serializers.CharField(source="tipo_carrera", read_only=True)
    titulo = serializers.SerializerMethodField("get_titulo")
    activo = serializers.SerializerMethodField("registro_activo")
    id_ieu = serializers.IntegerField(source="localidad.ieu.pk", read_only=True,)
    ieu = serializers.CharField(
        source="localidad.ieu.institucion_ministerial.nombre", read_only=True,
    )
    id_localidad = serializers.IntegerField(source="localidad.pk", read_only=True,)
    area_conocimiento = serializers.CharField(
        source="area_conocimiento.nombre", read_only=True,
    )
    sub_area_conocimiento = serializers.CharField(
        source="sub_area_conocimiento.nombre", read_only=True,
    )
    localidad = serializers.CharField(source="localidad.nombre", read_only=True,)

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
        ]

    def registro_activo(self, obj):
        if obj.cod_activacion == "11111111" or obj.cod_activacion == "10111111":
            return True
        return False

    def get_titulo(self, obj):
        titulo_srt = ""
        titulos = CarreraTitulo.objects.filter(carrera=obj.id)
        for titulo in titulos:
            if titulo_srt:
                titulo_srt = "{}<br>{} ({} {})".format(
                    titulo_srt,
                    titulo.titulo,
                    titulo.duracion,
                    obj.periodicidad.descripcion,
                )
            else:
                titulo_srt = "{} ({} {})".format(
                    titulo.titulo, titulo.duracion, obj.periodicidad.descripcion,
                )
        return titulo_srt


class TipoIeuEspecificoSerializer(serializers.ModelSerializer):
    """
    Class to serilize tipo especu¿ifico
    """

    nombre = serializers.SerializerMethodField("get_tipo_especifico_ieu")

    class Meta:
        model = Parroquia
        fields = ["id", "nombre"]
        read_only_fields = ["id", "nombre"]

    def get_tipo_especifico_ieu(self, obj):

        if obj.nombre:
            nombre_tipo_ieu = "{} {}".format(obj.sub_tipo_ieu, obj.nombre)
        else:
            nombre_tipo_ieu = "%s" % (obj.sub_tipo_ieu)
        return nombre_tipo_ieu


class AreaSerializer(serializers.ModelSerializer):
    """
    Class to serilize Areas de conocimiento
    """

    class Meta:
        model = AreaConocimiento
        fields = ["id", "nombre"]
        read_only_fields = ["id", "nombre"]


class SubAreaSerializer(serializers.ModelSerializer):
    """
    Class to serilize Subareas de conocimiento
    """

    class Meta:
        model = SubAreaConocimiento
        fields = ["id", "nombre", "area_conocimiento"]
        read_only_fields = ["id", "nombre", "area_conocimiento"]


class TituloSerializer(serializers.ModelSerializer):
    """
    Class to serilize Titulo
    """

    class Meta:
        model = Titulo
        fields = ["id", "nombre"]
        read_only_fields = ["id", "nombre"]


class TipoProgramaSerializer(serializers.ModelSerializer):
    """
    Class to serilize Titulo
    """

    class Meta:
        model = TipoCarrera
        fields = ["id", "nombre"]
        read_only_fields = ["id", "nombre"]
