"""EndPoints for api V1
"""
# Django Libraries
from django.urls import path
from django.views.generic import TemplateView

# Local Folders Libraries
from .viewsets import (
    AreaViewSet,
    DetalleProgramaAcademicoViewSet,
    EstadoViewset,
    IeuViewSet,
    LocalidadViewSet,
    MunicipioViewset,
    ParroquiaViewset,
    ProgramaAcademicoViewSet,
    SubAreaViewSet,
    TipoIeuViewSet,
    TipoProgramaViewSet,
    TituloViewSet,
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
        "programa-academico/pre-grado/detalle/",
        DetalleProgramaAcademicoViewSet.as_view({"get": "retrieve"}),
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
        "ieu/localidad/", LocalidadViewSet.as_view({"get": "list"}), name="localidad",
    ),
]
