"""Viwesets for oeu app EndPoints
"""
# Standard Libraries
import logging

# Thirdparty Libraries
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
from rest_framework import viewsets

# Local Folders Libraries
from .serializers import (
    AreaSerializer,
    CarreraSerializer,
    EstadoSerializer,
    IeuSerializer,
    LocalidadSerializer,
    MunicipioSerializer,
    ParroquiaSerializer,
    SubAreaSerializer,
    TipoIeuEspecificoSerializer,
    TipoProgramaSerializer,
    TituloSerializer,
)

#  logging
LOGGER = logging.getLogger("standart")


class ProgramaAcademicoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Programas Académicos
    Este EndPoint puede devolver uno o una lista de los programas académicos de pregrado del subsistema
    de educación universitaria.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * Parametros político territoriales:
            * **id_estado**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades del correspondiente
                estado.
            * **id_municipio**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades del correspondiente
                municipio.
            * **id_parroquia**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades de la correspondiente
                parroquia.
        * Parametros académicos:
            * **id_tipo_programa**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades del correspondiente
                tipo de programa académico.
            * **id_titulo**:  tipo int que filtra las localidades del correspondiente
                titulo de grado que otorga.
            * **area_conocimiento**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades de la correspondiente
                area conocimiento.
            * **sub_area_conocimiento**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades de la
                correspondiente sub area conocimiento.
        * Parametros institucionales:
            * **id_ieu**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades de la correspondiente
                institución de educación universitaria.
            * **id_tipo_ieu**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades del correspondiente
                tipo de institución de educación universitaria.
            * **id_localidad**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades de la correspondiente
                localidad de una institución de educación universitaria.
            * **dep_admin**: tipo str que filtra las localidades por su dependencia
                adinstrativa ("PÚBLICA" o "PRIVADA").

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": Cantidad de objetos que devuelve el EndPoint,
                "next": URL con la siguiente página (25 objetos) de resultados del EndPoint,
                "previous": URL con la pagina anterior (25 objetos) de resultados del EndPoint,
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

        if id_estado:
            queryset = queryset.filter(localidad__estado__in=id_estado.split(","))
        if id_municipio:
            queryset = queryset.filter(localidad__municipio__in=id_municipio.split(","))
        if id_parroquia:
            queryset = queryset.filter(localidad__parroquia__in=id_parroquia.split(","))
        if id_tipo_programa:
            queryset = queryset.filter(tipo_carrera__in=id_tipo_programa.split(","))
        if id_titulo:
            queryset = queryset.filter(titulo__in=id_titulo.split(","))
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
        * **id**: lista de valores (1,2,n) sin paréntesis tipo int que filtra el correspondiente estado.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": Cantidad de objetos que devuelve el EndPoint,
                "next": URL con la siguiente página (25 objetos) de resultados del EndPoint,
                "previous": URL con la pagina anterior (25 objetos) de resultados del EndPoint,
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

    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))

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
        * **id_estado**: lista de valores (1,2,n) sin paréntesis tipo int que filtra los municipios del estado correspondiente.
        * **id**: lista de valores (1,2,n) sin paréntesis tipo int que filtra el municipio correspondiente
            municipio.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": Cantidad de objetos que devuelve el EndPoint,
                "next": URL con la siguiente página (25 objetos) de resultados del EndPoint,
                "previous": URL con la pagina anterior (25 objetos) de resultados del EndPoint,
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
        * **id_estado**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las parroquias del correspondiente estado.
        * **id_municipio**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las parroquias del correspondiente
            municipio.
        * **id_parroquia**: lista de valores (1,2,n) sin paréntesis tipo int que filtra la
            correspondiente parroquia.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": Cantidad de objetos que devuelve el EndPoint,
                "next": URL con la siguiente página (25 objetos) de resultados del EndPoint,
                "previous": URL con la pagina anterior (25 objetos) de resultados del EndPoint,
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

    def list(self, request):
        """
        Metodo to list all academic programs
        """
        queryset = self.filter_queryset(self.get_queryset())

        id_estado = self.request.query_params.get("id_estado", None)
        id_municipio = self.request.query_params.get("id_municipio", None)
        id_parroquia = self.request.query_params.get("id_parroquia", None)
        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))
        if id_estado:
            queryset = queryset.filter(estado__in=id_estado.split(","))
        if id_municipio:
            queryset = queryset.filter(municipio__in=id_municipio.split(","))
        if id_parroquia:
            queryset = queryset.filter(pk__in=id_parroquia.split(","))

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
        * **id**: lista de valores (1,2,n) sin paréntesis tipo int que filtra el tipo de Institución de Educación Universitaria.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": Cantidad de objetos que devuelve el EndPoint,
                "next": URL con la siguiente página (25 objetos) de resultados del EndPoint,
                "previous": URL con la pagina anterior (25 objetos) de resultados del EndPoint,
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

    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))

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
        * **id**: lista de valores (1,2,n) sin paréntesis tipo int que filtra la correspondiente IEU.
        * **id_tipo_ieu**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las IEU del correspondiente tipo de institución de educación universitaria.
        * **dep_admin**: tipo str que filtra las IEU por su dependencia adinstrativa ("PÚBLICA" o "PRIVADA").

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": Cantidad de objetos que devuelve el EndPoint,
                "next": URL con la siguiente página (25 objetos) de resultados del EndPoint,
                "previous": URL con la pagina anterior (25 objetos) de resultados del EndPoint,
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

        object_id = self.request.query_params.get("id", None)
        id_tipo_ieu = self.request.query_params.get("id_tipo_ieu", None)
        dep_admin = self.request.query_params.get("dep_admin", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))
        if id_tipo_ieu:
            queryset = queryset.filter(tipo_especifico_ieu__in=id_tipo_ieu.split(","))
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
            * **id_estado**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades del correspondiente
                estado.
            * **id_municipio**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades del correspondiente
                municipio.
            * **id_parroquia**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades de la correspondiente
                parroquia.
        * Parametros institucionales:
            * **id_ieu**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades de la correspondiente
                institución de educación universitaria.
            * **id_tipo_ieu**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades del correspondiente
                tipo de institución de educación universitaria.
            * **id**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las localidades de la correspondiente
                localidad de una institución de educación universitaria.
            * **dep_admin**: tipo str que filtra las localidades por su dependencia
                adinstrativa ("PÚBLICA" o "PRIVADA").

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": Cantidad de objetos que devuelve el EndPoint,
                "next": URL con la siguiente página (25 objetos) de resultados del EndPoint,
                "previous": URL con la pagina anterior (25 objetos) de resultados del EndPoint,
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

        id_estado = self.request.query_params.get("id_estado", None)
        id_municipio = self.request.query_params.get("id_municipio", None)
        id_parroquia = self.request.query_params.get("id_parroquia", None)
        id_ieu = self.request.query_params.get("id_ieu", None)
        id_tipo_ieu = self.request.query_params.get("id_tipo_ieu", None)
        object_id = self.request.query_params.get("id", None)
        dep_admin = self.request.query_params.get("dep_admin", None)

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

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Area de Conocimiento de los Programas Académicos
    Este EndPoint puede devolver uno o una lista de las Áreas del Conocimeinto que agrupan a los Programas Académicos.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * **id**: lista de valores (1,2,n) sin paréntesis tipo int que filtra el tipo de Institución de Educación Universitaria.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": Cantidad de objetos que devuelve el EndPoint,
                "next": URL con la siguiente página (25 objetos) de resultados del EndPoint,
                "previous": URL con la pagina anterior (25 objetos) de resultados del EndPoint,
                "results": [
                    {
                        "id": identificador único del áreas del conocimeinto (int),
                        "nombre": nombre del áreas del conocimeinto (str)"
                    }
                ]
            }
    """

    serializer_class = AreaSerializer
    queryset = AreaConocimiento.objects.all()

    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class SubAreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Subarea de Conocimiento de los Programas Académicos ##
    Este EndPoint puede devolver uno o una lista de las Subareas del Conocimeinto que agrupan a los Programas Académicos.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * **id**: lista de valores (1,2,n) sin paréntesis tipo int que filtra el
            subáreas del conocimeinto.
        * **id_area**: lista de valores (1,2,n) sin paréntesis tipo int que filtra las
            subáreas del conocimeinto de acuerdo al id del área.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": Cantidad de objetos que devuelve el EndPoint,
                "next": URL con la siguiente página (25 objetos) de resultados del EndPoint,
                "previous": URL con la anterior página (25 objetos) de resultados del EndPoint,
                "results": [
                    {
                        "id": identificador único del subáreas del conocimeinto (int),
                        "nombre": nombre del subáreas del conocimeinto (str)",
                        "area": nombre del área del conocimeinto (str)"
                    }
                ]
            }
    """

    serializer_class = SubAreaSerializer
    queryset = SubAreaConocimiento.objects.all()

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

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class TituloViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Títulos de Grado de los Programas Académicos
    Este EndPoint puede devolver uno o una lista de los título de grado de los Programas Académicos.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * **id**: lista de valores (1,2,n) sin paréntesis tipo int que filtra el título de grado.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": Cantidad de objetos que devuelve el EndPoint,
                "next": URL con la siguiente página (25 objetos) de resultados del EndPoint,
                "previous": URL con la pagina anterior (25 objetos) de resultados del EndPoint,
                "results": [
                    {
                        "id": identificador único del título (int),
                        "nombre": nombre del título (str)"
                    }
                ]
            }
    """

    serializer_class = TituloSerializer
    queryset = Titulo.objects.all()

    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class TipoProgramaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ## Obtener Tipos de Programas Académicos
    Este EndPoint puede devolver uno o una lista de los Tipos de Programas Académicos.

    * Method: **GET**
    * Content-Type: **application/json**
    * Url Params:
        * **id**: lista de valores (1,2,n) sin paréntesis tipo int que filtra el tipo de programas académicos.

    * Respuesta exitosa:
        * HTTP code: 200
        * Objeto:

            {\n
                "count": Cantidad de objetos que devuelve el EndPoint,
                "next": URL con la siguiente página (25 objetos) de resultados del EndPoint,
                "previous": URL con la pagina anterior (25 objetos) de resultados del EndPoint,
                "results": [
                    {
                        "id": identificador único del tipo de programas académicos (int),
                        "nombre": nombre del tipo de programas académicos (str)"
                    }
                ]
            }
    """

    serializer_class = TipoProgramaSerializer
    queryset = TipoCarrera.objects.all()

    def list(self, request):
        """
        Metodo to list estados
        """
        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)

        if object_id:
            queryset = queryset.filter(pk__in=object_id.split(","))

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
