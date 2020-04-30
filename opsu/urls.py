"""opsu URL Configuration
"""
# Django Libraries
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.views.static import serve

urlpatterns = [
    path("api-v1/", include("api_v1.urls")),
    path("loeu/", include("oeu.urls")),
    path("loeu/configuracion/", include("oeuconfig.urls")),
    path("loeu/programas-academicos/", include("oeuacademic.urls")),
    path("cuenta/", include("cuenta.urls")),
    # path("acto_grado/", include("grado.urls2")),
    # path("sismeu/", include("sismeu.urls")),
    path("configuraciones/", include("globales.urls")),
    # path("sni/", include("snipni.urls")),
    path("admin/", admin.site.urls),
    # path("", TemplateView.as_view(template_name="index.html")),
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
    path("static/<path:path>", serve, {"document_root": settings.STATIC_ROOT}),
]
