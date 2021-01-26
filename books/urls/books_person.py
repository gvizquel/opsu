# Django Libraries
from django.urls import path
from django.views.generic import TemplateView

# Thirdparty Libraries
from books.datatables import BooksPersonDatatable
from books.viewsets import BooksPersonViewSet
from rest_framework.routers import DefaultRouter

app_name = "person"


# En esta sección se crean las rutas de los endpoints del ModelViewSet
PERSON_ROUTER = DefaultRouter()
PERSON_ROUTER.register("api/v1", BooksPersonViewSet)

urlpatterns = [
    path(
        "list/",
        TemplateView.as_view(
            template_name="books_person.html",
            extra_context={
                "dt_view_name": "dt-person",
                "api_list_name": "api_person_list",
                "api_detail_name": "api_person_detail",
                "add_title": "Añadir nueva persona",
                "title": "Listando Personas",
                "palabraClave": "Personas",
            },
        ),
        name="list",
    ),
    path("datatable/", BooksPersonDatatable.as_view(), name="dt-person"),
] + PERSON_ROUTER.urls
