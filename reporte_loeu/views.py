"""Vistas para el LOEU
"""
# Standard Libraries
import csv
import datetime
import functools
import io
import logging
import operator

# Django Libraries
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, StreamingHttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

# Thirdparty Libraries
import xlsxwriter
from oeu.models import Carrera
from reporte_loeu.forms import GeneralReportForm

#  logging
LOGGER = logging.getLogger("standart")


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def set_if_not_none(mapping, key, value):
    """ Esta función agrega valores a los kwargs de filtrado de una consulta del ORM,
    Siempre y cuando estos valores sean distintos de None y distintos de vacio
    """
    if (value is not None and value) or (isinstance(value, bool)) or (value == 0):
        mapping[key] = value


class GeneralReportView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """ESta clase
    """

    form_class = GeneralReportForm
    template_name = "reporte_loeu/reporte_formulario.html"
    success_url = reverse_lazy("reporte_loeu:listar")

    def form_valid(self, form):
        data = form.cleaned_data
        filters_kwargs = {}
        filters_args = []
        today = datetime.datetime.now()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        headers = [
            "INSTITUCIÓN DE EDUCACIÓN UNIVERSITARIA",
            "TIPO DE INSTITUCIÓN DE EDUCACIÓN UNIVERSITARIA",
            "COD_IEU",
            "SIGLAS",
            "TIPO DE GESTIÓN",
            "TIPO DE LOCALIDAD",
            "LOCALIDAD",
            "ESTADO",
            "MUNICIPIO",
            "PARROQUIA",
            "COD_LOCALIDAD",
            "ÁREA DE CONOCIMINETO",
            "COD_AREA",
            "sUB ÁREA DE CONOCIMINETO",
            "COD_SUB_AREA",
            "PROGRAMA ACADÉMICO",
            "COD_PROGRAMA",
            "TIPO DE PROGRAMA",
            "ACTIVO",
        ]

        for count, header in enumerate(headers):
            worksheet.write(0, count, header)

        worksheet.autofilter("A1:S1")

        worksheet.set_column("A:A", 102)
        worksheet.set_column("B:B", 61)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 23)
        worksheet.set_column("G:G", 10)
        worksheet.set_column("H:H", 18)
        worksheet.set_column("I:I", 30)
        worksheet.set_column("J:J", 48)
        worksheet.set_column("K:K", 20)
        worksheet.set_column("L:L", 48)
        worksheet.set_column("M:M", 20)
        worksheet.set_column("N:N", 64)
        worksheet.set_column("O:O", 20)
        worksheet.set_column("P:P", 89)
        worksheet.set_column("Q:Q", 20)
        worksheet.set_column("R:R", 23)
        worksheet.set_column("S:S", 20)

        # Preparo los argumentos para filtrar las fotos del reporte en un diccionario
        set_if_not_none(
            filters_kwargs,
            "localidad__ieu__institucion_ministerial__pk",
            data["ieu"].pk if data["ieu"] else None,
        )
        set_if_not_none(
            filters_kwargs,
            "localidad__ieu__institucion_ministerial__dep_admin",
            data["gestion"] if data["gestion"] else None,
        )
        # set_if_not_none(filters_kwargs, "photo__pub_date__gte", date_inti)
        # set_if_not_none(filters_kwargs, "photo__pub_date__lte", date_edn)
        # set_if_not_none(filters_kwargs, "photo__place_obj__zonCodigo__icontains", zona)
        # set_if_not_none(filters_kwargs, "photo__place_obj__unnNombre", zona)
        # set_if_not_none(filters_kwargs, "photo__place_obj__regnombre", direccion)
        # set_if_not_none(filters_kwargs, "photo__place_obj__gerNombre", gerencia)
        # set_if_not_none(filters_kwargs, "photo__place_obj__tipoAtencion", type_atention)

        LOGGER.warning("Inciando la descarga")
        LOGGER.info("Filters Kwargs: {}".format(filters_kwargs))

        oferta_academica = Carrera.objects.select_related(
            "localidad", "tipo_carrera", "area_conocimiento", "sub_area_conocimiento",
        ).filter(**filters_kwargs)

        # Preparo los argumentos complejos para filtrar las fotos del reporte en una lista
        if data["cod_activacion"] == "ACTIVA":
            filters_args = (
                Q(cod_activacion="11111111"),
                Q(cod_activacion="10111111"),
            )
            filters_args = functools.reduce(operator.or_, filters_args)
        elif data["cod_activacion"] == "INACTIVA":
            filters_args = (
                ~Q(cod_activacion="11111111"),
                ~Q(cod_activacion="10111111"),
            )
            filters_args = functools.reduce(operator.and_, filters_args)

        if filters_args:
            oferta_academica = oferta_academica.filter(filters_args)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="somefilename.csv"'

        for count, programa in enumerate(oferta_academica.iterator()):
            if programa.cod_activacion == "11111111":
                activo = "SI"
            else:
                activo = "NO"

            worksheet.write(
                count + 1, 0, programa.localidad.ieu.institucion_ministerial.nombre
            )
            worksheet.write(
                count + 1, 1, programa.localidad.ieu.tipo_especifico_ieu.__str__()
            )
            worksheet.write(count + 1, 2, programa.localidad.ieu.pk)
            worksheet.write(
                count + 1, 3, programa.localidad.ieu.institucion_ministerial.siglas
            )
            worksheet.write(
                count + 1, 4, programa.localidad.ieu.institucion_ministerial.dep_admin
            )
            worksheet.write(count + 1, 5, programa.localidad.tipo_localidad.nombre)
            worksheet.write(count + 1, 6, programa.localidad.nombre)
            worksheet.write(count + 1, 7, programa.localidad.estado.nombre)
            worksheet.write(count + 1, 8, programa.localidad.municipio.nombre)
            worksheet.write(count + 1, 9, programa.localidad.parroquia.nombre)
            worksheet.write(count + 1, 10, programa.localidad.pk)
            worksheet.write(count + 1, 11, programa.area_conocimiento.nombre)
            worksheet.write(count + 1, 12, programa.area_conocimiento.pk)
            worksheet.write(count + 1, 13, programa.sub_area_conocimiento.nombre)
            worksheet.write(count + 1, 14, programa.sub_area_conocimiento.pk)
            worksheet.write(count + 1, 15, programa.nombre)
            worksheet.write(count + 1, 16, programa.pk)
            worksheet.write(count + 1, 17, programa.tipo_carrera.nombre)
            worksheet.write(count + 1, 18, activo)

        workbook.close()

        output.seek(0)

        filename = "loe_reporte_general_{:%Y%m%d%H%M%S}.xlsx".format(today)

        response = HttpResponse(
            output,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=%s" % filename

        return response

        # return super(GeneralReportView, self).form_valid(form)


# ########################################################################## #
class ListarReportes(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    """Con esta clase se puede
    """

    template_name = "reporte_loeu/listar.html"
