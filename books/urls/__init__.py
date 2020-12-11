# Django Libraries
from django.conf.urls import include
from django.urls import path

app_name = "books"

urlpatterns = [
    path("person/", include("books.urls.books_person")),
]
