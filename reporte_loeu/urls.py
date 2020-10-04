# Django Libraries
from django.urls import path

# Thirdparty Libraries
from reporte_loeu.views import GeneralReportView, ListarReportes

app_name = "reporte_loeu"

urlpatterns = [
    path("", ListarReportes.as_view(), name="listar"),
    path("general", GeneralReportView.as_view(), name="general"),
]
