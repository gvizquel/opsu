"""EndPoints for api V1
"""
# Django Libraries
from django.urls import path
from django.views.generic import TemplateView

# Local Folders Libraries
from .viewsets import (
    EstadoViewset,
    IeuViewSet,
    LocalidadViewSet,
    MunicipioViewset,
    ParroquiaViewset,
    ProgramaAcademicoViewSet,
    TipoIeuViewSet,
)

app_name = "api_v1"

urlpatterns = [
    path("", TemplateView.as_view(template_name="api_v1_doc.html")),
    # ###################### Programas Academicos de Pre Grado ####################### #
    path(
        "programa-academico/pre-grado/listar/",
        ProgramaAcademicoViewSet.as_view({"get": "list"}),
        name="pre-programa",
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
