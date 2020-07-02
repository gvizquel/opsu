"""EndPoints for api V1
"""
# Django Libraries
from django.conf.urls import re_path
from django.urls import path
from django.views.generic import TemplateView

# Thirdparty Libraries
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Local Folders Libraries
from .viewsets import (
    AreaViewSet,
    EstadoViewset,
    IeuViewSet,
    LocalidadViewSet,
    LocalidadViewSet1,
    MunicipioViewset,
    ParroquiaViewset,
    ProgramaAcademicoNombreViewSet,
    ProgramaAcademicoViewSet,
    SubAreaViewSet,
    TipoIeuViewSet,
    TipoProgramaViewSet,
    TituloViewSet,
)

schema_view = get_schema_view(
    openapi.Info(
        title="LOEU API",
        default_version="v1",
        description="Oportunidades de Estudio en Venezuela",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="gvizquel@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = "api_v1"

urlpatterns = [
    path(
        "test/", TemplateView.as_view(template_name="datatabletest.html"), name="test"
    ),
    path("", TemplateView.as_view(template_name="api_v1_doc.html"), name="api-index"),
    # ###################### Programas Academicos de Pre Grado ####################### #
    path(
        "programa-academico/pre-grado/listar/",
        ProgramaAcademicoViewSet.as_view({"get": "list"}),
        name="pre-programa",
    ),
    path(
        "programa-academico-nombre/pre-grado/listar/",
        ProgramaAcademicoNombreViewSet.as_view({"get": "list"}),
        name="programa-academico-nombre",
    ),
    path(
        "programa-academico/pre-grado/detalle/",
        ProgramaAcademicoViewSet.as_view({"get": "retrieve"}),
        name="detalle-pre-programa",
    ),
    path(
        "programa-academico/area-conocimiento/",
        AreaViewSet.as_view({"get": "list"}),
        name="area",
    ),
    path(
        "programa-academico/subarea-conocimiento/",
        SubAreaViewSet.as_view({"get": "list"}),
        name="subarea",
    ),
    path(
        "programa-academico/titulo/",
        TituloViewSet.as_view({"get": "list"}),
        name="titulo",
    ),
    path(
        "programa-academico/tipo/",
        TipoProgramaViewSet.as_view({"get": "list"}),
        name="tipo-programa",
    ),
    # ######################## División Político Territorial ######################### #
    path("estado/listar/", EstadoViewset.as_view({"get": "list"}), name="estado",),
    path(
        "municipio/listar/",
        MunicipioViewset.as_view({"get": "list"}),
        name="municipio",
    ),
    path(
        "parroquia/listar/",
        ParroquiaViewset.as_view({"get": "list"}),
        name="parroquia",
    ),
    # ################### Istituciones de Educación Universitaria #################### #
    path("ieu/tipo/", TipoIeuViewSet.as_view({"get": "list"}), name="tipo-ieu",),
    path("ieu/", IeuViewSet.as_view({"get": "list"}), name="ieu",),
    path(
        "ieu/localidad/listar/",
        LocalidadViewSet.as_view({"get": "list"}),
        name="localidad",
    ),
    path(
        "ieu/localidad/detalle/",
        LocalidadViewSet.as_view({"get": "retrieve"}),
        name="detalle-localidad",
    ),
    path(
        "ieu/localidad/",
        LocalidadViewSet1.as_view({"get": "list"}),
        name="detalle-localidad",
    ),
    # ################### Swagger #################### #
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
