# Django Libraries
from django.contrib import admin

# Thirdparty Libraries
from books.models import BooksCategoria, BooksEditorial, BooksPerson, BooksPublicacion

# Register your models here.


@admin.register(BooksPerson)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(BooksEditorial)
class EditorialAdmin(admin.ModelAdmin):
    pass


@admin.register(BooksCategoria)
class CategoriaAdmin(admin.ModelAdmin):
    pass


@admin.register(BooksPublicacion)
class PublicacionAdmin(admin.ModelAdmin):
    pass
