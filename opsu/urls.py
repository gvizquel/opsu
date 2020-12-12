"""opsu URL Configuration
"""
# Django Libraries
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.static import serve

urlpatterns = [
    path("api-v1/", include("api_v1.urls")),
    path("books/", include("books.urls")),
    path("loeu/", include("oeu.urls")),
    path("loeu/configuracion/", include("oeuconfig.urls")),
    path("loeu/programas-academicos/", include("oeuacademic.urls")),
    path("loeu/reportes/", include("reporte_loeu.urls")),
    path("", include("cuenta.urls")),
    path("configuraciones/", include("globales.urls")),
    path("admin/", admin.site.urls),
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
    path("static/<path:path>", serve, {"document_root": settings.STATIC_ROOT}),
]
