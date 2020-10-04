"""Vistas para el LOEU
"""
# Standard Libraries
import csv
import datetime
import functools
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
        rows = []
        today = datetime.datetime.now()
        print(today)

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

        rows.append(
            [
                "INSTITUCIÓN DE EDUCACIÓN UNIVERSITARIA",
                "COD_IEU",
                "SIGLAS",
                "TIPO DE GESTIÓN",
                "TIPO DE LOCALIDAD",
                "LOCALIDAD",
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
        )

        for programa in oferta_academica.iterator():
            if programa.cod_activacion == "11111111":
                activo = "SI"
            else:
                activo = "NO"

            rows.append(
                [
                    programa.localidad.ieu.institucion_ministerial.nombre,
                    programa.localidad.ieu.pk,
                    programa.localidad.ieu.institucion_ministerial.siglas,
                    programa.localidad.ieu.institucion_ministerial.dep_admin,
                    programa.localidad.tipo_localidad.nombre,
                    programa.localidad.nombre,
                    programa.localidad.pk,
                    programa.area_conocimiento.nombre,
                    programa.area_conocimiento.pk,
                    programa.sub_area_conocimiento.nombre,
                    programa.sub_area_conocimiento.pk,
                    programa.nombre,
                    programa.pk,
                    programa.tipo_carrera.nombre,
                    activo,
                ]
            )

        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse(
            (writer.writerow(row) for row in rows), content_type="text/csv"
        )
        response[
            "Content-Disposition"
        ] = "attachment; filename=loe_reporte_general_{:%Y%m%d%H%M%S}.csv".format(today)

        return response

        # return super(GeneralReportView, self).form_valid(form)


# ########################################################################## #
class ListarReportes(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    """Con esta clase se puede
    """

    template_name = "reporte_loeu/listar.html"
