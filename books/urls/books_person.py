# Django Libraries
from django.urls import path
from django.views.generic import TemplateView

# Thirdparty Libraries
# from books.datatables import DatatableBase
from books.models import BooksPerson
from books.viewsets import BooksPersonViewSet
from rest_framework.routers import DefaultRouter

app_name = "person"


# En esta sección se crean las rutas de los endpoints del ModelViewSet
PERSON_ROUTER = DefaultRouter()
PERSON_ROUTER.register("api/v1", BooksPersonViewSet)

urlpatterns = [
    # path("datatable", DatatableBase.as_view(model=BooksPerson), name="datatable_person"),
    path(
        "list/",
        TemplateView.as_view(
            template_name="",
            extra_context={
                "dt_view_name": "datatable_person",
                "api_list_name": "api_person_list",
                "api_detail_name": "api_person_detail",
                "add_title": "Añadir nueva marca de producto",
                "title": "Listando marcas de producto",
                "palabraClave": "Marcas",
            },
        ),
        name="list",
    ),
] + PERSON_ROUTER.urls
