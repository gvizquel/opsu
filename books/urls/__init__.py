# Django Libraries
from django.conf.urls import include
from django.urls import path

from books.datatables import BooksPersonDatatable

app_name = "books"

urlpatterns = [
    path("person/", include("books.urls.books_person")),
    path("datatable/person", BooksPersonDatatable.as_view(), name="dt-person"),
]
