# Django Libraries
from django.contrib import admin

# Thirdparty Libraries
from books.models import Autor, Categoria, Editor, Editorial, Publicacion

# Register your models here.


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    pass


@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    pass


@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    pass


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    pass


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    pass
