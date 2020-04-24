"""Viwesets for oeu app EndPoints
"""

# Thirdparty Libraries
from globales.models import Estado, Municipio, Parroquia
from oeu.models import Carrera, TipoEspecificoInstitucion, Ieu, Localidad
from rest_framework import viewsets

# Local Folders Libraries
from .serializers import (
    CarreraSerializer,
    EstadoSerializer,
    IeuSerializer,
    LocalidadSerializer,
    MunicipioSerializer,
    ParroquiaSerializer,
    TipoIeuEspecificoSerializer,
)


class ProgramaAcademicoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Programas Académicos
    Este EndPoint puede devolver uno o una lista de los programas académicos de pregrado del subsistema
    de educación universitaria.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * Parametros político territoriales:
            * **id_estado**: tipo int que filtra las localidades del correspondiente
                estado.
            * **id_municipio**: tipo int que filtra las localidades del correspondiente
                municipio.
            * **id_parroquia**: tipo int que filtra las localidades de la correspondiente
                parroquia.
        * Parametros académicos:
            * **id_tipo_programa**: tipo int que filtra las localidades del correspondiente
                tipo de programa académico.
            * **id_titulo**:  tipo int que filtra las localidades del correspondiente
                titulo de grado que otorga.
            * **area_conocimiento**: tipo int que filtra las localidades de la correspondiente
                area conocimiento.
            * **sub_area_conocimiento**: tipo int que filtra las localidades de la
                correspondiente sub area conocimiento.
        * Parametros institucionales:
            * **id_ieu**: tipo int que filtra las localidades de la correspondiente
                institución de educación universitaria.
            * **id_tipo_ieu**: tipo int que filtra las localidades del correspondiente
                tipo de institución de educación universitaria.
            * **id_localidad**: tipo int que filtra las localidades de la correspondiente
                localidad de una institución de educación universitaria.
            * **dep_admin**: tipo str que filtra las localidades por su dependencia
                adinstrativa ("PÚBLICA" o "PRIVADA").

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
                            "id": identificador único de la localidad (int),
                            "tipo_localidad": tipo de localidad (str),
                            "nombre": nombre de la localidad (str),
                            "web_site": URL del web site de la localidad (str)",
                            "direccion": dirección de la que pertenece el programa académico (str),
                            "estado": estado de la localidad (str),
                            "municipio": municipio de la localidad (str),
                            "parroquia": parroquia de la localidad  (str),
                            "centro_poblado": centro poblado de la localidad (str),
                            "punto": punto georeferenciado de la localidad (str),
                            "poligonal": poligonal georeferenciada de la localidad (str),
                            "fachada": ruta de la fachada de la localidad (str),
                            "activo": indica si la localidad de la IEU está activa o no (bool)
                            "ieu": {
                                "id": identificador único de la IEU (int),
                                "nombre": nombre de la IEU (str),
                                "siglas": siglas de la IEU (str),
                                "dep_admin": indica si la IEU es publica o provada (str)
                                "tipo_ieu": "Institutos Universitarios Militares",
                                "logo": ruta de la imagen del logo de la IEU (str),
                                "fachada": ruta de la imagen de la fachada de la IEU (str),
                                "activo": false
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


class EstadoViewset(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Estado
    Este EndPoint puede devolver uno o una lista de los estados de Venezuela.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * **id**: tipo int que filtra el correspondiente estado.

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
        object_id = self.request.query_params.get("id", None)

        ############################# Filtrando el queryset ############################
        if object_id:
            queryset = queryset.filter(pk=object_id)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class MunicipioViewset(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Municipio
    Este EndPoint puede devolver uno o una lista de los municipios de Venezuela.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * **id_estado**: tipo int que filtra los municipios del estado correspondiente.
        * **id**: tipo int que filtra el municipio correspondiente
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
        object_id = self.request.query_params.get("id", None)

        ############################# Filtrando el queryset ############################
        if object_id:
            queryset = queryset.filter(pk=object_id)
        if id_estado:
            queryset = queryset.filter(estado=id_estado)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


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
        object_id = self.request.query_params.get("id", None)

        ############################# Filtrando el queryset ############################
        if object_id:
            queryset = queryset.filter(pk=object_id)
        if id_estado:
            queryset = queryset.filter(estado=id_estado)
        if id_municipio:
            queryset = queryset.filter(municipio=id_municipio)
        if id_parroquia:
            queryset = queryset.filter(pk=id_parroquia)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class TipoIeuViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Tipo de Institución de Educación Universitaria
    Este EndPoint puede devolver uno o una lista de los Tipo de Institución de Educación
    Universitaria.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * **id**: tipo int que filtra el tipo de Institución de Educación Universitaria.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": 14,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "id": identificador único del tipo de institución (int),
                        "nombre": nombre del tipo de institución (str)"
                    }
                ]
            }
    """

    serializer_class = TipoIeuEspecificoSerializer
    queryset = TipoEspecificoInstitucion.objects.all()
    model = TipoEspecificoInstitucion

    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        #################### Parametros que pueden venir en la url #####################
        object_id = self.request.query_params.get("id", None)

        ############################# Filtrando el queryset ############################
        if object_id:
            queryset = queryset.filter(pk=object_id)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class IeuViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Instituciones de Educación Universitaria (IEU)
    Este EndPoint puede devolver uno o una lista de las Instituciones de Educación Universitaria.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * **id**: tipo int que filtra la correspondiente IEU.
        * **id_tipo_ieu**: tipo int que filtra las IEU del correspondiente tipo de institución de educación universitaria.
        * **dep_admin**: tipo str que filtra las IEU por su dependencia adinstrativa ("PÚBLICA" o "PRIVADA").

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": 210,
                "next": "http://127.0.0.1:8083/api-v1/ieu/?page=2",
                "previous": null,
                "results": [
                    {
                        "id": identificador único de la IEU (int),
                        "nombre": nombre de la IEU (str),
                        "siglas": siglas de la IEU (str),
                        "dep_admin": indica si la IEU es publica o provada (str)
                        "tipo_ieu": "Institutos Universitarios Militares",
                        "logo": ruta de la imagen del logo de la IEU (str),
                        "fachada": ruta de la imagen de la fachada de la IEU (str),
                        "activo": false
                    }
                ]
            }
    """

    serializer_class = IeuSerializer
    queryset = Ieu.objects.all()

    def list(self, request):
        """
        Viewset to list all academic programs
        """
        queryset = self.filter_queryset(self.get_queryset())

        #################### Parametros que pueden venir en la url #####################
        object_id = self.request.query_params.get("id", None)
        id_tipo_ieu = self.request.query_params.get("id_tipo_ieu", None)
        dep_admin = self.request.query_params.get("dep_admin", None)

        ############################# Filtrando el queryset ############################
        if object_id:
            queryset = queryset.filter(pk=object_id)
        if id_tipo_ieu:
            queryset = queryset.filter(tipo_especifico_ieu=id_tipo_ieu)
        if dep_admin:
            queryset = queryset.filter(institucion_ministerial__dep_admin=dep_admin)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class LocalidadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Localidad de las Instituciones de Educación Universitaria
    Este EndPoint puede devolver uno o una lista de las localidades de las IEU.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * Parametros político territoriales:
            * **id_estado**: tipo int que filtra las localidades del correspondiente
                estado.
            * **id_municipio**: tipo int que filtra las localidades del correspondiente
                municipio.
            * **id_parroquia**: tipo int que filtra las localidades de la correspondiente
                parroquia.
        * Parametros institucionales:
            * **id_ieu**: tipo int que filtra las localidades de la correspondiente
                institución de educación universitaria.
            * **id_tipo_ieu**: tipo int que filtra las localidades del correspondiente
                tipo de institución de educación universitaria.
            * **id_localidad**: tipo int que filtra las localidades de la correspondiente
                localidad de una institución de educación universitaria.
            * **dep_admin**: tipo str que filtra las localidades por su dependencia
                adinstrativa ("PÚBLICA" o "PRIVADA").

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": cantidad de registro devueltos por el endpoint,
                "next": "url a la siguiente página de resultados, hay 25 objetos por página",
                "previous": "url a la página anterior de resultados, hay 25 objetos por página",
                "results": [
                    {
                        "id": identificador único de la localidad (int),
                        "tipo_localidad": tipo de localidad (str),
                        "nombre": nombre de la localidad (str),
                        "web_site": URL del web site de la localidad (str)",
                        "direccion": dirección de la que pertenece el programa académico (str),
                        "estado": estado de la localidad (str),
                        "municipio": municipio de la localidad (str),
                        "parroquia": parroquia de la localidad  (str),
                        "centro_poblado": centro poblado de la localidad (str),
                        "punto": punto georeferenciado de la localidad (str),
                        "poligonal": poligonal georeferenciada de la localidad (str),
                        "fachada": ruta de la fachada de la localidad (str),
                        "activo": indica si la localidad de la IEU está activa o no (bool)
                        "ieu": {
                            "id": identificador único de la IEU (int),
                            "nombre": nombre de la IEU (str),
                            "siglas": siglas de la IEU (str),
                            "dep_admin": indica si la IEU es publica o provada (str)
                            "tipo_ieu": "Institutos Universitarios Militares",
                            "logo": ruta de la imagen del logo de la IEU (str),
                            "fachada": ruta de la imagen de la fachada de la IEU (str),
                            "activo": false
                            },
                        },
                    }
                ]
            }
    """

    serializer_class = LocalidadSerializer
    queryset = Localidad.objects.all()

    def list(self, request):
        """
        Viewset to list all academic programs
        """
        queryset = self.filter_queryset(self.get_queryset())

        #################### Parametros que pueden venir en la url #####################
        id_estado = self.request.query_params.get("id_estado", None)
        id_municipio = self.request.query_params.get("id_municipio", None)
        id_parroquia = self.request.query_params.get("id_parroquia", None)
        id_ieu = self.request.query_params.get("id_ieu", None)
        id_tipo_ieu = self.request.query_params.get("id_tipo_ieu", None)
        object_id = self.request.query_params.get("id", None)
        dep_admin = self.request.query_params.get("dep_admin", None)

        ############################# Filtrando el queryset ############################
        if id_estado:
            queryset = queryset.filter(estado=id_estado)
        if id_municipio:
            queryset = queryset.filter(municipio=id_municipio)
        if id_parroquia:
            queryset = queryset.filter(parroquia=id_parroquia)
        if id_ieu:
            queryset = queryset.filter(ieu=id_ieu)
        if id_tipo_ieu:
            queryset = queryset.filter(ieu__tipo_especifico_ieu=id_tipo_ieu)
        if object_id:
            queryset = queryset.filter(pk=object_id)
        if dep_admin:
            queryset = queryset.filter(
                ieu__institucion_ministerial__dep_admin=dep_admin
            )

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
