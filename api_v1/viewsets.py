"""Viwesets for oeu app EndPoints
"""
# Standard Libraries
import logging
import math

# Django Libraries
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Thirdparty Libraries
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from globales.models import Estado, Municipio, Parroquia
from oeu.models import (
    AreaConocimiento,
    Carrera,
    Ieu,
    Localidad,
    SubAreaConocimiento,
    TipoEspecificoInstitucion,
)
from oeuconfig.models import TipoCarrera, Titulo
from rest_framework import pagination, viewsets
from rest_framework.response import Response

# Local Folders Libraries
from .serializers import (
    AreaSerializer,
    DetalleLocalidadSerializer,
    DetalleProgramaAcademicoSerializer,
    ListaEstadoSerializer,
    ListaIeuSerializer,
    ListaLocalidadSerializer,
    ListaMunicipioSerializer,
    ListaParroquiaSerializer,
    ListaProgramaAcademicoNombreSerializer,
    ListaProgramaAcademicoSerializer,
    SubAreaSerializer,
    TipoIeuEspecificoSerializer,
    TipoProgramaSerializer,
    TituloSerializer,
)

#  logging
LOGGER = logging.getLogger("standart")


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "countItemsOnPage": self.page_size,
                "page": self.page.number,
                "totalPages": math.ceil(self.page.paginator.count / self.page_size),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


# #################################################################################### #
class EstadoViewset(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Estado
    Este EndPoint puede devolver uno o una lista de los estados de Venezuela.
    """

    serializer_class = ListaEstadoSerializer
    queryset = Estado.objects.all()

    estado_response = openapi.Response("Estado", ListaEstadoSerializer)

    id_param = openapi.Parameter(
        "id",
        in_="query",
        required=False,
        description="Lista de los id de los estados (1,2,n) sin paréntesis. Filtra los estados corespondientes.",
        type="string",
    )

    @swagger_auto_schema(
        name="Lista de estados",
        tags=["EndPoints de División Político Territorial"],
        query_serializer=ListaEstadoSerializer,
        manual_parameters=[id_param],
        operation_description="Devuelve una lista de estados.",
        operation_summary="Lista de estados.",
        responses={"200": estado_response, "400": "Bad Request"},
        operation_id="Lista Estados",
    )
    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# #################################################################################### #
class MunicipioViewset(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Municipio
    Este EndPoint puede devolver uno o una lista de los municipios de Venezuela.
    """

    serializer_class = ListaMunicipioSerializer
    queryset = Municipio.objects.all()

    municipio_response = openapi.Response("Municipio", ListaMunicipioSerializer)

    id_param = openapi.Parameter(
        "id",
        in_="query",
        required=False,
        description="Lista de los id de los Municipios (1,2,n) sin paréntesis. Filtra los Municipios corespondientes.",
        type="string",
    )
    estado_param = openapi.Parameter(
        "id_estado",
        in_="query",
        required=False,
        description="Lista de los id de los Estados (1,2,n) sin paréntesis. Filtra los Municipios de los Estados corespondientes.",
        type="string",
    )

    @swagger_auto_schema(
        name="Lista de Municipios",
        tags=["EndPoints de División Político Territorial"],
        query_serializer=ListaMunicipioSerializer,
        manual_parameters=[id_param, estado_param],
        operation_description="Devuelve una lista de Municipios.",
        operation_summary="Lista de Municipios.",
        responses={"200": municipio_response, "400": "Bad Request"},
        operation_id="Lista de Municipios",
    )
    def list(self, request):
        """
        Metodo to list municipios
        """
        queryset = self.filter_queryset(self.get_queryset())

        id_estado = self.request.query_params.get("id_estado", None)
        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))
        if id_estado:
            queryset = queryset.filter(estado__in=id_estado.split(","))

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# #################################################################################### #
class ParroquiaViewset(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Parroquia
    Este EndPoint puede devolver uno o una lista de las parroquias de Venezuela.
    """

    serializer_class = ListaParroquiaSerializer
    queryset = Parroquia.objects.all()

    parroquia_response = openapi.Response("Parroquia", ListaParroquiaSerializer)

    id_param = openapi.Parameter(
        "id",
        in_="query",
        required=False,
        description="Lista de los id de los Parroquias (1,2,n) sin paréntesis. Filtra los Parroquias corespondientes.",
        type="string",
    )
    estado_param = openapi.Parameter(
        "id_estado",
        in_="query",
        required=False,
        description="Lista de los id de los Estados (1,2,n) sin paréntesis. Filtra los Parroquias de los Estados corespondientes.",
        type="string",
    )
    municipio_param = openapi.Parameter(
        "id_municipio",
        in_="query",
        required=False,
        description="Lista de los id de las Municipios (1,2,n) sin paréntesis. Filtra las Parroquias de los Municipios corespondientes.",
        type="string",
    )

    @swagger_auto_schema(
        name="Lista de Parroquias",
        tags=["EndPoints de División Político Territorial"],
        query_serializer=ListaParroquiaSerializer,
        manual_parameters=[id_param, estado_param],
        operation_description="Devuelve una lista de Parroquias.",
        operation_summary="Lista de Parroquias.",
        responses={"200": parroquia_response, "400": "Bad Request"},
        operation_id="Lista de Parroquias",
    )
    def list(self, request):
        """
        Metodo to list all academic programs
        """
        queryset = self.filter_queryset(self.get_queryset())

        id_estado = self.request.query_params.get("id_estado", None)
        id_municipio = self.request.query_params.get("id_municipio", None)
        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))
        if id_estado:
            queryset = queryset.filter(estado__in=id_estado.split(","))
        if id_municipio:
            queryset = queryset.filter(municipio__in=id_municipio.split(","))

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# #################################################################################### #
class ProgramaAcademicoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Programas Académicos
    Este EndPoint puede devolver uno o una lista de los programas académicos de pregrado
    del subsistema de educación universitaria.
    """

    serializer_class = ListaProgramaAcademicoSerializer
    queryset = Carrera.objects.filter()
    action_serializers = {
        "retrieve": DetalleProgramaAcademicoSerializer,
        "list": ListaProgramaAcademicoSerializer,
    }

    def get_serializer_class(self):

        if hasattr(self, "action_serializers"):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(ProgramaAcademicoViewSet, self).get_serializer_class()

    detail_carrera_response = openapi.Response(
        "Detalle del programa académico", DetalleProgramaAcademicoSerializer
    )

    list_carrera_response = openapi.Response(
        "Lista del programa académico", ListaProgramaAcademicoSerializer
    )

    id_param = openapi.Parameter(
        "id",
        in_="query",
        required=False,
        description="Lista de los id de las Localidades (1,2,n) sin paréntesis. Filtra los programa académico corespondientes.",
        type="string",
    )

    estado_param = openapi.Parameter(
        "id_estado",
        in_="query",
        required=False,
        description="Lista de los id de los estados (1,2,n) sin paréntesis. Filtra los programas académicos de los correspondientes estados.",
        type="string",
    )
    municipio_param = openapi.Parameter(
        "id_municipio",
        in_="query",
        required=False,
        description="Lista de los id de los municipios (1,2,n) sin paréntesis. Filtra los programas académicos de los correspondientes municipios.",
        type="string",
    )
    parroquia_param = openapi.Parameter(
        "id_parroquia",
        in_="query",
        required=False,
        description="Lista de los id de las parroquias (1,2,n) sin paréntesis. Filtra los programas académicos de las correspondientes parroquias.",
        type="string",
    )
    tipo_programa_param = openapi.Parameter(
        "id_tipo_programa",
        in_="query",
        description="Lista de los id de los tipo_programa (1,2,n) sin paréntesis. Filtra los programas académicos de los corespondientes tipo_programa.",
        type="string",
    )
    titulo_param = openapi.Parameter(
        "id_titulo",
        in_="query",
        required=False,
        description="Lista de los id de los títulos (1,2,n) sin paréntesis. Filtra los programas académicos de los corespondientes títulos.",
        type="string",
    )
    area_param = openapi.Parameter(
        "id_area",
        in_="query",
        required=False,
        description="Lista de los id de las áreas de conocimiento (1,2,n) sin paréntesis. Filtra los programas académicos de las corespondientes áreas de conocimiento.",
        type="string",
    )
    sub_area_param = openapi.Parameter(
        "id_sub_area",
        in_="query",
        required=False,
        description="Lista de los id de los sub áreas de conocimiento (1,2,n) sin paréntesis. Filtra los programas académicos de las corespondientes sub áreas de conocimiento.",
        type="string",
    )
    ieu_param = openapi.Parameter(
        "id_ieu",
        in_="query",
        required=False,
        description="Lista de los id de las instituciones de educación universitaria (1,2,n) sin paréntesis. Filtra los programas académicos de las corespondientes instituciones de educación universitaria.",
        type="string",
    )
    tipo_ieu_param = openapi.Parameter(
        "id_tipo_ieu",
        in_="query",
        required=False,
        description="Lista de los id de los tipos de IEU (1,2,n) sin paréntesis. Filtra los programas académicos de los corespondientes tipos de IEU.",
        type="string",
    )
    localidad_param = openapi.Parameter(
        "id_localidad",
        in_="query",
        required=False,
        description="Lista de los id de las localidades (1,2,n) sin paréntesis. Filtra los programas académicos de las corespondientes localidades.",
        type="string",
    )
    admin_param = openapi.Parameter(
        "dep_admin",
        in_="query",
        required=False,
        enum=("PÚBLICA", "PRIVADA"),
        description="Filtra los Programas Académicos por su tipo de gestión PÚBLICA o PRIVADA.",
        type="string",
    )
    nombre_programa_param = openapi.Parameter(
        "nombre_programa",
        in_="query",
        required=False,
        description="Lista de los de los nombres de programas académicos ('ABOGADO','INFORMÁTICA','MEDICINA') sin paréntesis y en mayúscula. Filtra los programas académicos de los corespondientes nombres de programas académicos.",
        type="string",
    )
    activo_param = openapi.Parameter(
        "activo",
        in_="query",
        required=False,
        description="Filtra los Programas Académicos activos o inactivos.",
        type="boolean",
    )

    @swagger_auto_schema(
        name="Lista de Programas Académicos",
        tags=["EndPoints de Datos Académicos"],
        manual_parameters=[
            id_param,
            estado_param,
            municipio_param,
            parroquia_param,
            tipo_programa_param,
            titulo_param,
            area_param,
            sub_area_param,
            ieu_param,
            tipo_ieu_param,
            localidad_param,
            admin_param,
            nombre_programa_param,
            activo_param,
        ],
        operation_description="Devuelve una lista de los programas académicos de pregrado del subsistema de educación universitaria en Venezuela.",
        operation_summary="Lista los programas académicos de Venezuela",
        responses={"200": list_carrera_response, "400": "Bad Request"},
        operation_id="Lista Programas Academicos",
    )
    def list(self, request):
        """
        Viewset to list all academic programs
        """
        queryset = self.filter_queryset(self.get_queryset())

        id_estado = self.request.query_params.get("id_estado", None)
        id_municipio = self.request.query_params.get("id_municipio", None)
        id_parroquia = self.request.query_params.get("id_parroquia", None)
        id_tipo_programa = self.request.query_params.get("id_tipo_programa", None)
        id_titulo = self.request.query_params.get("id_titulo", None)
        id_area = self.request.query_params.get("id_area", None)
        id_sub_area = self.request.query_params.get("id_sub_area", None)
        id_ieu = self.request.query_params.get("id_ieu", None)
        id_tipo_ieu = self.request.query_params.get("id_tipo_ieu", None)
        id_localidad = self.request.query_params.get("id_localidad", None)
        dep_admin = self.request.query_params.get("dep_admin", None)
        nombre_programa = self.request.query_params.get("nombre_programa", None)
        object_id = self.request.query_params.get("id", None)
        activo = self.request.query_params.get("activo", "true")

        if activo == "false":
            queryset = queryset.filter(
                ~Q(cod_activacion="11111111"), ~Q(cod_activacion="10111111")
            )
        elif activo == "true":
            queryset = queryset.filter(
                Q(cod_activacion="11111111") | Q(cod_activacion="10111111")
            )

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))
        if id_estado:
            queryset = queryset.filter(localidad__estado__in=id_estado.split(","))
        if id_municipio:
            queryset = queryset.filter(localidad__municipio__in=id_municipio.split(","))
        if id_parroquia:
            queryset = queryset.filter(localidad__parroquia__in=id_parroquia.split(","))
        if id_tipo_programa:
            queryset = queryset.filter(tipo_carrera__in=id_tipo_programa.split(","))
        if id_area:
            queryset = queryset.filter(area_conocimiento__in=id_area.split(","))
        if id_sub_area:
            queryset = queryset.filter(sub_area_conocimiento__in=id_sub_area.split(","))
        if id_ieu:
            queryset = queryset.filter(localidad__ieu__in=id_ieu.split(","))
        if id_tipo_ieu:
            queryset = queryset.filter(
                localidad__ieu__tipo_especifico_ieu__in=id_tipo_ieu.split(",")
            )
        if id_localidad:
            queryset = queryset.filter(localidad__in=id_localidad.split(","))
        if dep_admin:
            queryset = queryset.filter(
                localidad__ieu__institucion_ministerial__dep_admin=dep_admin
            )
        if nombre_programa:
            queryset = queryset.filter(nombre__in=nombre_programa.split(","))

        if id_titulo:
            queryset = queryset.filter(titula__in=id_titulo.split(","))

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        name="Detalle del Programas Académicos",
        tags=["EndPoints de Datos Académicos"],
        query_serializer=DetalleProgramaAcademicoSerializer,
        manual_parameters=[id_param],
        operation_description="Devuelve el detalle de un progrma académico.",
        operation_summary="Detalle del programa académico.",
        responses={"200": detail_carrera_response, "400": "Bad Request"},
        operation_id="Detalle Programa Académico",
    )
    def retrieve(self, request):
        object_id = self.request.query_params.get("id", -1)
        queryset = get_object_or_404(Carrera, pk=object_id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


# #################################################################################### #
class ProgramaAcademicoNombreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Programas Académicos
    Este EndPoint devuelve lista de los nombres programas académicos de pregrado del
    subsistema de educación universitaria.
    """

    serializer_class = ListaProgramaAcademicoNombreSerializer
    queryset = Carrera.objects.raw(
        "SELECT nombre, ROW_NUMBER ( ) OVER (ORDER BY nombre) AS id FROM (SELECT DISTINCT oeu.carrera.nombre FROM oeu.carrera WHERE (oeu.carrera.cod_activacion = '11111111' OR oeu.carrera.cod_activacion = '10111111') ORDER BY oeu.carrera.nombre ASC) nombres"
    )

    carrera_nombre_response = openapi.Response(
        "Nombres de los Programas Académicos", ListaProgramaAcademicoNombreSerializer
    )

    @swagger_auto_schema(
        name="Lista de los Nombres de los Programas Académicos",
        tags=["EndPoints de Datos Académicos"],
        query_serializer=ListaProgramaAcademicoNombreSerializer,
        operation_description="Devuelve una lista de los Nombres de los Programas Académicos.",
        operation_summary="Lista de los Nombres de los Programas Académicos.",
        responses={"200": carrera_nombre_response, "400": "Bad Request"},
        operation_id="Lista Nombres de Programas Académicos",
    )
    def list(self, request):
        """
        Viewset to list all academic programs
        """
        queryset = self.filter_queryset(self.get_queryset())

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# #################################################################################### #
class TipoIeuViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Tipo de Institución de Educación Universitaria
    Este EndPoint puede devolver uno o una lista de los Tipo de Institución de Educación
    Universitaria.
    """

    serializer_class = TipoIeuEspecificoSerializer
    queryset = TipoEspecificoInstitucion.objects.filter()

    tipo_ieu_response = openapi.Response("Tipos de IEU", TipoIeuEspecificoSerializer)

    id_param = openapi.Parameter(
        "id",
        in_="query",
        required=False,
        description="Lista de los id de los tipos de IEU (1,2,n) sin paréntesis. Filtra los tipos de iue corespondientes.",
        type="string",
    )

    @swagger_auto_schema(
        name="Lista de los Nombres de los Programas Académicos",
        tags=["EndPoints de Instituciones de Educación Universitaria"],
        query_serializer=TipoIeuEspecificoSerializer,
        manual_parameters=[id_param],
        operation_description="Devuelve una lista de los Nombres de los Programas Académicos.",
        operation_summary="Lista de los Nombres de los Programas Académicos.",
        responses={"200": tipo_ieu_response, "400": "Bad Request"},
        operation_id="Lista de los Nombres de los Programas Académicos",
    )
    def list(self, request):
        """
        Metodo to list los Nombres de los Programas Académicos
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)
        activo = self.request.query_params.get("activo", None)

        if activo == "0":
            queryset = queryset.filter(
                ~Q(cod_activacion="11000111"), ~Q(cod_activacion="10000111")
            )
        else:
            queryset = queryset.filter(
                Q(cod_activacion="11000111") | Q(cod_activacion="10000111")
            )

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# #################################################################################### #
class IeuViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Instituciones de Educación Universitaria (IEU)
    Este EndPoint puede devolver uno o una lista de las Instituciones de Educación
    Universitaria.
    """

    serializer_class = ListaIeuSerializer
    queryset = Ieu.objects.all()

    tipo_ieu_response = openapi.Response("Tipos de IEU", ListaIeuSerializer)

    id_param = openapi.Parameter(
        "id",
        in_="query",
        required=False,
        description="Lista de los id de las Instituciones de Educación Universitaria (1,2,n) sin paréntesis. Filtra las Instituciones de Educación Universitaria corespondientes.",
        type="string",
    )
    tipo_ieu__param = openapi.Parameter(
        "id_tipo_ieu",
        in_="query",
        required=False,
        description="Lista de los id de los tipos de IEU (1,2,n) sin paréntesis. Filtra las Instituciones de Educación Universitaria segun los tipos de IEU corespondientes.",
        type="string",
    )
    dep_admin_param = openapi.Parameter(
        "dep_admin",
        in_="query",
        required=False,
        description="Tipo de administración de las (PÚBLICA, PRIVADA) sin paréntesis. Filtra las Instituciones de Educación Universitaria según su tipo de admnistración.",
        type="string",
    )
    activo_param = openapi.Parameter(
        "activo",
        in_="query",
        required=False,
        description="Filtra las Instituciones de Educación Universitaria activos o inactivos.",
        type="boolean",
    )

    @swagger_auto_schema(
        name="Lista de las Instituciones de Educación Universitaria",
        tags=["EndPoints de Instituciones de Educación Universitaria"],
        query_serializer=ListaIeuSerializer,
        manual_parameters=[id_param, tipo_ieu__param, dep_admin_param, activo_param],
        operation_description="Devuelve una lista de las Instituciones de Educación Universitaria",
        operation_summary="Lista de las Instituciones de Educación Universitaria",
        responses={"200": tipo_ieu_response, "400": "Bad Request"},
        operation_id="Lista de las Instituciones de Educación Universitaria",
    )
    def list(self, request):
        """
        Viewset to list all academic programs
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)
        id_tipo_ieu = self.request.query_params.get("id_tipo_ieu", None)
        dep_admin = self.request.query_params.get("dep_admin", None)
        activo = self.request.query_params.get("activo", None)

        if activo == "0":
            queryset = queryset.filter(
                ~Q(cod_activacion="11001111"), ~Q(cod_activacion="10001111")
            )
        else:
            queryset = queryset.filter(
                Q(cod_activacion="11001111") | Q(cod_activacion="10001111")
            )
        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))
        if id_tipo_ieu:
            queryset = queryset.filter(tipo_especifico_ieu__in=id_tipo_ieu.split(","))
        if dep_admin:
            queryset = queryset.filter(institucion_ministerial__dep_admin=dep_admin)

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# #################################################################################### #
class LocalidadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Localidad de las Instituciones de Educación Universitaria
    Este EndPoint puede devolver uno o una lista de las localidades de las IEU.
    """

    serializer_class = ListaLocalidadSerializer
    queryset = Localidad.objects.all()
    action_serializers = {
        "retrieve": DetalleLocalidadSerializer,
        "list": ListaLocalidadSerializer,
    }

    def get_serializer_class(self):

        if hasattr(self, "action_serializers"):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(LocalidadViewSet, self).get_serializer_class()

    detail_localidad_response = openapi.Response(
        "Detalle de las Localidades", DetalleLocalidadSerializer
    )

    list_localidad_response = openapi.Response(
        "Lista de las Localidades", ListaLocalidadSerializer
    )

    id_param = openapi.Parameter(
        "id",
        in_="query",
        required=False,
        description="Lista de los id de las Localidades (1,2,n) sin paréntesis. Filtra las Localidades corespondientes.",
        type="string",
    )

    estado_param = openapi.Parameter(
        "id_estado",
        in_="query",
        required=False,
        description="Lista de los id de los estados (1,2,n) sin paréntesis. Filtra las Localidades de los correspondientes estados.",
        type="string",
    )
    municipio_param = openapi.Parameter(
        "id_municipio",
        in_="query",
        required=False,
        description="Lista de los id de los municipios (1,2,n) sin paréntesis. Filtra las Localidades de los correspondientes municipios.",
        type="string",
    )
    parroquia_param = openapi.Parameter(
        "id_parroquia",
        in_="query",
        required=False,
        description="Lista de los id de las parroquias (1,2,n) sin paréntesis. Filtra las Localidades de las correspondientes parroquias.",
        type="string",
    )
    tipo_programa_param = openapi.Parameter(
        "id_tipo_programa",
        in_="query",
        required=False,
        description="Lista de los id de los tipo_programa (1,2,n) sin paréntesis. Filtra las Localidades de los corespondientes tipo_programa.",
        type="string",
    )
    titulo_param = openapi.Parameter(
        "id_titulo",
        in_="query",
        required=False,
        description="Lista de los id de los títulos (1,2,n) sin paréntesis. Filtra las Localidades de los corespondientes títulos.",
        type="string",
    )
    area_param = openapi.Parameter(
        "id_area",
        in_="query",
        required=False,
        description="Lista de los id de las áreas de conocimiento (1,2,n) sin paréntesis. Filtra las Localidades de las corespondientes áreas de conocimiento.",
        type="string",
    )
    sub_area_param = openapi.Parameter(
        "id_sub_area",
        in_="query",
        required=False,
        description="Lista de los id de los sub áreas de conocimiento (1,2,n) sin paréntesis. Filtra las Localidades de las corespondientes sub áreas de conocimiento.",
        type="string",
    )
    nombre_programa_param = openapi.Parameter(
        "nombre_programa",
        in_="query",
        required=False,
        description="Lista de los de los nombres de programas académicos ('ABOGADO','INFORMÁTICA','MEDICINA') sin paréntesis y en mayúscula. Filtra las Localidades de los corespondientes nombres de programas académicos.",
        type="string",
    )
    activo_param = openapi.Parameter(
        "activo",
        in_="query",
        required=False,
        description="Filtra las Localidades activos o inactivos.",
        type="boolean",
    )

    @swagger_auto_schema(
        name="Lista de las Localidades de las Instituciones de Educación Universitaria en Venezuela",
        tags=["EndPoints de Instituciones de Educación Universitaria"],
        query_serializer=ListaLocalidadSerializer,
        manual_parameters=[
            id_param,
            estado_param,
            municipio_param,
            parroquia_param,
            activo_param,
            tipo_programa_param,
            titulo_param,
            area_param,
            sub_area_param,
            nombre_programa_param,
        ],
        operation_description="Devuelve una lista de las Localidades de pregrado del subsistema de educación universitaria en Venezuela.",
        operation_summary="Lista de las Localidades de las Instituciones de Educación Universitaria en Venezuela",
        responses={"200": list_localidad_response, "400": "Bad Request"},
        operation_id="Lista Localidades de las IEU",
    )
    def list(self, request):
        """
        Viewset to list of Localidad
        """
        queryset = self.filter_queryset(self.get_queryset())

        id_estado = self.request.query_params.get("id_estado", None)
        id_municipio = self.request.query_params.get("id_municipio", None)
        id_parroquia = self.request.query_params.get("id_parroquia", None)
        id_ieu = self.request.query_params.get("id_ieu", None)
        id_tipo_ieu = self.request.query_params.get("id_tipo_ieu", None)
        object_id = self.request.query_params.get("id", None)
        dep_admin = self.request.query_params.get("dep_admin", None)
        id_tipo_programa = self.request.query_params.get("id_tipo_programa", None)
        id_area = self.request.query_params.get("id_area", None)
        id_sub_area = self.request.query_params.get("id_sub_area", None)
        nombre_programa = self.request.query_params.get("nombre_programa", None)
        id_titulo = self.request.query_params.get("id_titulo", None)
        activo = self.request.query_params.get("activo", "true")

        if activo == "true":
            queryset = queryset.filter(
                Q(cod_activacion="11011111") | Q(cod_activacion="10011111")
            )
        elif activo == "false":
            queryset = queryset.filter(
                ~Q(cod_activacion="11011111"), ~Q(cod_activacion="10011111")
            )

        if id_estado:
            queryset = queryset.filter(estado__in=id_estado.split(","))
        if id_municipio:
            queryset = queryset.filter(municipio__in=id_municipio.split(","))
        if id_parroquia:
            queryset = queryset.filter(parroquia__in=id_parroquia.split(","))
        if id_ieu:
            queryset = queryset.filter(ieu__in=id_ieu.split(","))
        if id_tipo_ieu:
            queryset = queryset.filter(
                ieu__tipo_especifico_ieu__in=id_tipo_ieu.split(",")
            )
        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))
        if dep_admin:
            queryset = queryset.filter(
                ieu__institucion_ministerial__dep_admin=dep_admin
            )
        if id_tipo_programa:
            localidades = Carrera.objects.filter(
                tipo_carrera__in=id_tipo_programa.split(",")
            ).values("localidad")
            queryset = queryset.distinct().filter(pk__in=localidades)
        if id_area:
            localidades = Carrera.objects.filter(
                area_conocimiento__in=id_area.split(",")
            ).values("localidad")
            queryset = queryset.distinct().filter(pk__in=localidades)
        if id_sub_area:
            localidades = Carrera.objects.filter(
                sub_area_conocimiento__in=id_sub_area.split(",")
            ).values("localidad")
            queryset = queryset.distinct().filter(pk__in=localidades)
        if nombre_programa:
            localidades = Carrera.objects.filter(
                nombre__in=nombre_programa.split(",")
            ).values("localidad")
            queryset = queryset.distinct().filter(pk__in=localidades)
        if id_titulo:
            localidades = (
                Carrera.objects.distinct()
                .filter(titula__in=id_titulo.split(","))
                .values("localidad")
            )
            queryset = queryset.distinct().filter(pk__in=localidades)

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        name="Detalle de la Localidad",
        tags=["EndPoints de Instituciones de Educación Universitaria"],
        query_serializer=DetalleProgramaAcademicoSerializer,
        manual_parameters=[id_param],
        operation_description="Devuelve el detalle de la Localidad.",
        operation_summary="Detalle de la Localidad.",
        responses={"200": detail_localidad_response, "400": "Bad Request"},
        operation_id="Detalle Localidad IEU",
    )
    def retrieve(self, request):
        """
        Viewset to get one Localidad
        """
        object_id = self.request.query_params.get("id", -1)
        queryset = get_object_or_404(Localidad, pk=object_id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


# #################################################################################### #
class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Area de Conocimiento de los Programas Académicos
    Este EndPoint puede devolver uno o una lista de las Áreas del Conocimeinto que
    agrupan a los Programas Académicos.
    """

    serializer_class = AreaSerializer
    queryset = AreaConocimiento.objects.all()

    area_response = openapi.Response("Áreas de Conocimiento", AreaSerializer)

    id_param = openapi.Parameter(
        "id",
        in_="query",
        required=False,
        description="Lista de los id de las Áreas de Conocimiento (1,2,n) sin paréntesis. Filtra las Áreas de Conocimiento corespondientes.",
        type="string",
    )

    @swagger_auto_schema(
        name="Lista de las Áreas de Conocimiento",
        tags=["EndPoints de Datos Académicos"],
        manual_parameters=[id_param],
        query_serializer=AreaSerializer,
        operation_description="Devuelve una lista de las Áreas de Conocimiento.",
        operation_summary="Lista de las Áreas de Conocimiento.",
        responses={"200": area_response, "400": "Bad Request"},
        operation_id="Lista Áreas de Conocimiento",
    )
    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# #################################################################################### #
class SubAreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Subarea de Conocimiento de los Programas Académicos ##
    Este EndPoint puede devolver uno o una lista de las Subareas del Conocimeinto que agrupan a los Programas Académicos.
    """

    serializer_class = SubAreaSerializer
    queryset = SubAreaConocimiento.objects.all()

    sub_area_response = openapi.Response("Sub Áreas de Conocimiento", SubAreaSerializer)

    id_param = openapi.Parameter(
        "id",
        in_="query",
        required=False,
        description="Lista de los id de las Sub Áreas de Conocimiento (1,2,n) sin paréntesis. Filtra las Sub Áreas de Conocimiento corespondientes.",
        type="string",
    )

    id_area = openapi.Parameter(
        "id_area",
        in_="query",
        required=False,
        description="Lista de los id de las Áreas de Conocimiento (1,2,n) sin paréntesis. Filtra las Áreas de Conocimiento corespondientes a las Sub Áreas de Conocimiento.",
        type="string",
    )

    @swagger_auto_schema(
        name="Lista de las Sub Áreas de Conocimiento",
        tags=["EndPoints de Datos Académicos"],
        manual_parameters=[id_param],
        query_serializer=SubAreaSerializer,
        operation_description="Devuelve una lista de las Sub Áreas de Conocimiento.",
        operation_summary="Lista de las Sub Áreas de Conocimiento.",
        responses={"200": sub_area_response, "400": "Bad Request"},
        operation_id="Lista Sub Áreas de Conocimiento",
    )
    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)
        id_area = self.request.query_params.get("id_area", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))
        if id_area:
            queryset = queryset.filter(area_conocimiento__in=id_area.split(","))

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# #################################################################################### #
class TituloViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Títulos de Grado de los Programas Académicos
    Este EndPoint puede devolver uno o una lista de los título de grado de los Programas Académicos.
    """

    serializer_class = TituloSerializer
    queryset = Titulo.objects.all()

    titulo_response = openapi.Response(
        "Tíulos de Grado de los Programas Académicos", TituloSerializer
    )

    id_param = openapi.Parameter(
        "id",
        in_="query",
        required=False,
        description="Lista de los id de los Tíulos de Grado de los Programas Académicos (1,2,n) sin paréntesis. Filtra los Tíulos de Grado de los Programas Académicos corespondientes.",
        type="string",
    )

    @swagger_auto_schema(
        name="Lista de los Tíulos de Grado de los Programas Académicos",
        tags=["EndPoints de Datos Académicos"],
        manual_parameters=[id_param],
        query_serializer=TituloSerializer,
        operation_description="Devuelve una lista de los Tíulos de Grado de los Programas Académicos.",
        operation_summary="Lista de los Tíulos de Grado de los Programas Académicos.",
        responses={"200": titulo_response, "400": "Bad Request"},
        operation_id="Lista Tíulos de Grado de los Programas Académicos",
    )
    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# #################################################################################### #
class TipoProgramaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Tipos de Programas Académicos
    Este EndPoint puede devolver uno o una lista de los Tipos de Programas Académicos.
    """

    serializer_class = TipoProgramaSerializer
    queryset = TipoCarrera.objects.all()

    tipo_carrera_response = openapi.Response(
        "Tipos de Programa Académico", TipoProgramaSerializer
    )

    id_param = openapi.Parameter(
        "id",
        in_="query",
        required=False,
        description="Lista de los id de los Tipos de Programa Académico (1,2,n) sin paréntesis. Filtra los Tipos de Programa Académico corespondientes.",
        type="string",
    )

    @swagger_auto_schema(
        name="Lista de los Tipos de Programa Académico",
        tags=["EndPoints de Datos Académicos"],
        manual_parameters=[id_param],
        query_serializer=TipoProgramaSerializer,
        operation_description="Devuelve una lista de los Tipos de Programa Académico.",
        operation_summary="Lista de los Tipos de Programa Académico.",
        responses={"200": tipo_carrera_response, "400": "Bad Request"},
        operation_id="Lista Tipos de Programa Académico",
    )
    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
