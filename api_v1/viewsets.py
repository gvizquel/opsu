"""Viwesets for oeu app EndPoints
"""
# Django Libraries
from django.shortcuts import get_object_or_404

# Thirdparty Libraries
from globales.models import Estado, Municipio, Parroquia
from oeu.models import Carrera
from rest_framework import viewsets
from rest_framework.response import Response

# Local Folders Libraries
from .serializers import (
    CarreraSerializer,
    EstadoSerializer,
    MunicipioSerializer,
    ParroquiaSerializer,
)


class ProgramaAcademicoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Programas Academicos
    Este EndPoint puede devolver uno o una lista de los programas académicos de pregrado del subsistema
    de educación universitaria.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * Parametros político territoriales:
            * **id_estado**: tipo int que filtra los programa académicos del
                correspondiente estado.
            * **id_municipio**: tipo int que filtra los programa académicos del
                correspondiente municipio.
            * **id_parroquia**: tipo int que filtra los programa académicos de la
                correspondiente parroquia.
        * Parametros académicos:
            * **id_tipo_programa**: tipo int que filtra los programa académicos del
                correspondiente tipo de programa académico.
            * **id_titulo**:  tipo int que filtra los programa académicos del
                correspondiente titulo de grado que otorga.
            * **area_conocimiento**: tipo int que filtra los programa académicos de la
                correspondiente area conocimiento.
            * **sub_area_conocimiento**: tipo int que filtra los programa académicos de
                la correspondiente sub area conocimiento.
        * Parametros institucionales:
            * **id_ieu**: tipo int que filtra los programa académicos de la
                correspondiente institución de educación universitaria.
            * **id_tipo_ieu**: tipo int que filtra los programa académicos del
                correspondiente tipo de institución de educación universitaria.
            * **id_localidad**: tipo int que filtra los programa académicos de la
                correspondiente localidad de una institución de educación universitaria.
            * **dep_admin**: tipo str que filtra los programa académicos por su
                dependencia adinstrativa ("PÚBLICA" o "PRIVADA").

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": cantidad de registro devueltos por el endpoint,
                "next": "url a la siguiente página de resultados, hay 25 objetos por página",
                "previous": "url a la página anterior de resultados, hay 25 objetos por página",
                "results": [
                    {
                        "id": identificador único de la carrera (int),
                        "nombre": nombre del programa académico (str) ,
                        "tipo_programa": tipo de programa académico (str),
                        "descripcion": descripcion del programa académico (str),
                        "titulo": título de grado del programa académico (str),
                        "mercado_ocupacional": sectores laborales para el egresado del programa académico (str),
                        "periodicidad": periodos académicos del programa académico (str),
                        "duracion": duración del programa académico (str),
                        "prioritaria": indica si es programa académico es prioritario para el desarrollo económico de la nación (bool),
                        "activo": indica si el programa académico está activo o no (bool),
                        "area_conocimiento": indica el área de conocimiento del programa académico (str),
                        "sub_area_conocimiento": indica la sub área del programa académico (str),
                        "localidad": {
                            "id": identificador único de la localidad a la que pertenece el programa académico (int),
                            "tipo_localidad": tipo de localidad a la que pertenece el programa académico (str),
                            "nombre": nombre de la localidad a la que pertenece el programa académico (str),
                            "web_site": URL del web site de la localidad a la que pertenece el programa académico (str)",
                            "direccion": dirección de la que pertenece el programa académico (str),
                            "estado": estado de la localidad a la que pertenece el programa académico (str),
                            "municipio": municipio de la localidad a la que pertenece el programa académico (str),
                            "parroquia": parroquia de la localidad  a la que pertenece el programa académico (str),
                            "centro_poblado": centro poblado de la localidad a la que pertenece el programa académico (str),
                            "punto": punto georeferenciado de la localidad a la que pertenece el programa académico (str),
                            "poligonal": poligonal georeferenciada de la localidad a la que pertenece el programa académico (str),
                            "fachada": ruta de la fachada de la localidad a la que pertenece el programa académico (str),
                            "activo": indica si la localidad de la IEU a la que pertenece el programa académico está activa o no (bool)
                            "ieu": {
                                "id": identificador único de la IEU a la que pertenece el programa académico (int),
                                "tipo_ieu": tipo de institución a la que pertenece el programa académico (str),
                                "localidad_principal": indica la localidad principal de la IEU a la que pertenece el programa académico (str),
                                "logo": ruta de la imagen del logo de la IEU a la que pertenece el programa académico (str),
                                "fachada": ruta de la imagen de la fachada de la IEU a la que pertenece el programa académico (str),
                                "activo": indica si la IEU a la que pertenece el programa académico está activa o no (bool)
                                "institucion_ministerial": {
                                    "nombre": nombre de la IEU a la que pertenece el programa académico (str),
                                    "siglas": siglas de la IEU a la que pertenece el programa académico (str),
                                    "rif": R.I.F. de la IEU a la que pertenece el programa académico (str),
                                    "dep_admin": indica si la IEU a la que pertenece el programa académico es publica o provada (str)
                                },
                            },
                        }
                    }
                ]
            }
    """

    serializer_class = CarreraSerializer
    queryset = Carrera.objects.all()

    def list(self, request):
        """
        Viewset to list all academic programs
        """
        queryset = self.filter_queryset(self.get_queryset())

        #################### Parametros que pueden venir en la url #####################
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

        ############################# Filtrando el queryset ############################
        if id_estado:
            queryset = queryset.filter(localidad__estado=id_estado)
        if id_municipio:
            queryset = queryset.filter(localidad__municipio=id_municipio)
        if id_parroquia:
            queryset = queryset.filter(localidad__parroquia=id_parroquia)
        if id_tipo_programa:
            queryset = queryset.filter(tipo_carrera=id_tipo_programa)
        if id_titulo:
            queryset = queryset.filter(titulo=id_titulo)
        if id_area:
            queryset = queryset.filter(area_conocimiento=id_area)
        if id_sub_area:
            queryset = queryset.filter(sub_area_conocimiento=id_sub_area)
        if id_ieu:
            queryset = queryset.filter(localidad__ieu=id_ieu)
        if id_tipo_ieu:
            queryset = queryset.filter(localidad__ieu__tipo_especifico_ieu=id_tipo_ieu)
        if id_localidad:
            queryset = queryset.filter(localidad=id_localidad)
        if dep_admin:
            queryset = queryset.filter(
                localidad__ieu__institucion_ministerial__dep_admin=dep_admin
            )

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, id_obj=None):
        """
        metodo to detail municipio
        """
        obj = get_object_or_404(self.model, pk=id_obj)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class ParroquiaViewset(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Parroquia
    Este EndPoint puede devolver uno o una lista de las parroquias de Venezuela.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * **id_estado**: tipo int que filtra las parroquias del correspondiente estado.
        * **id_municipio**: tipo int que filtra las parroquias del correspondiente
            municipio.
        * **id_parroquia**: tipo int que filtra la
            correspondiente parroquia.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": 1144,
                "next": "http://127.0.0.1:8083/api-v1/parroquia/listar/?page=2",
                "previous": null,
                "results": [
                    {
                        "id": 1144,
                        "nombre": "DEPENDENCIAS FEDERALES",
                        "municipio": 337,
                        "estado": 25
                    }
                ]
            }
    """

    serializer_class = ParroquiaSerializer
    queryset = Parroquia.objects.all()
    model = Parroquia

    def list(self, request):
        """
        Metodo to list all academic programs
        """
        queryset = self.filter_queryset(self.get_queryset())

        #################### Parametros que pueden venir en la url #####################
        id_estado = self.request.query_params.get("id_estado", None)
        id_municipio = self.request.query_params.get("id_municipio", None)
        id_parroquia = self.request.query_params.get("id_parroquia", None)

        ############################# Filtrando el queryset ############################
        if id_estado:
            queryset = queryset.filter(estado=id_estado)
        if id_municipio:
            queryset = queryset.filter(municipio=id_municipio)
        if id_parroquia:
            queryset = queryset.filter(pk=id_parroquia)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, id_obj=None):
        """
        metodo to detail municipio
        """
        obj = get_object_or_404(self.model, pk=id_obj)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class MunicipioViewset(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Municipio
    Este EndPoint puede devolver uno o una lista de los municipios de Venezuela.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * **id_estado**: tipo int que filtra las parroquias del correspondiente estado.
        * **id_municipio**: tipo int que filtra las parroquias del correspondiente
            municipio.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": 337,
                "next": "http://127.0.0.1:8083/api-v1/municipio/listar/?page=2",
                "previous": null,
                "results": [
                    {
                        "id": 337,
                        "nombre": "DEPENDENCIAS FEDERALES",
                        "estado": 25
                    }
                ]
            }
    """

    serializer_class = MunicipioSerializer
    queryset = Municipio.objects.all()
    model = Municipio

    def list(self, request):
        """
        Metodo to list municipios
        """
        queryset = self.filter_queryset(self.get_queryset())

        #################### Parametros que pueden venir en la url #####################
        id_estado = self.request.query_params.get("id_estado", None)
        id_municipio = self.request.query_params.get("id_municipio", None)

        ############################# Filtrando el queryset ############################
        if id_estado:
            queryset = queryset.filter(estado=id_estado)
        if id_municipio:
            queryset = queryset.filter(municipio=id_municipio)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, id_obj=None):
        """
        metodo to detail municipio
        """
        obj = get_object_or_404(self.model, pk=id_obj)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class EstadoViewset(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Estado
    Este EndPoint puede devolver uno o una lista de los estados de Venezuela.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * **id_estado**: tipo int que filtra las parroquias del correspondiente estado.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": 25,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "id": 25,
                        "nombre": "DEPENDENCIAS FEDERALES"
                    }
                ]
            }
    """

    serializer_class = EstadoSerializer
    queryset = Estado.objects.all()
    model = Estado

    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        #################### Parametros que pueden venir en la url #####################
        id_estado = self.request.query_params.get("id_estado", None)

        ############################# Filtrando el queryset ############################
        if id_estado:
            queryset = queryset.filter(estado=id_estado)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, id_obj=None):
        """
        metodo to detail estado
        """
        obj = get_object_or_404(self.model, pk=id_obj)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
