# -*- coding: utf-8 -*-
"""
Vistas de la aplicación globales
"""
# Django Libraries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import CreateView, UpdateView

# Thirdparty Libraries
from dal import autocomplete
from globales.forms import InstitucionMinisterialForm
from globales.models import InstitucionMinisterial

# Local Folders Libraries
from .models import Estado, Etnia, Municipio, Pais, Parroquia


# @login_required
def index(request):
    return render(request, "index.html")


##############################################################################
#          Vistas para la gestión del Modelo Instituciones Miniteriales      #
#                   Agregar e Actualizar los registros                       #
##############################################################################


##############################################################################
class AgregarInstitucionMinisterial(
    LoginRequiredMixin, SuccessMessageMixin, CreateView
):
    """Esta clase sirve para agregar las Instituciones Ministeriales
    """

    model = InstitucionMinisterial
    form_class = InstitucionMinisterialForm
    template_name = "institucion_ministerial_formulario.html"
    success_url = reverse_lazy("globales:listar-institucion-ministerial")


##############################################################################
class EditarInstitucionMinisterial(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Esta clase sirve para actualizar o editar las Instituciones Ministeriales
    almacenadas en la Base de Datos del modelo InstitucionMinisterial
    """

    model = InstitucionMinisterial
    form_class = InstitucionMinisterialForm
    template_name = "institucion_ministerial_formulario.html"
    success_url = reverse_lazy("globales:listar-institucion-ministerial")


##############################################################################
class InstitucionIeuAutoComplete(autocomplete.Select2QuerySetView):
    """Servicio de auto completado para el modelo TipoInstitucion
    """

    def get_queryset(self):
        queryset = InstitucionMinisterial.objects.filter(tipo_institucion="IEU")

        if self.q:
            queryset = queryset.filter(nombre__icontains=self.q)

        return queryset


##############################################################################
class PaisAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if self.q:
            qs = Pais.objects.filter(nombrepais__istartswith=self.q).order_by(
                "nombrepais"
            )

        return qs


##############################################################################
class PaisAutocomplete2(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if self.q:
            qs = Pais.objects.filter(nombrepais__istartswith=self.q).order_by(
                "nombrepais"
            )

        return qs


##############################################################################
class EstadoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Estado.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q).order_by("nombre")

        return qs


##############################################################################
class MunicipioAutocomplete(autocomplete.Select2QuerySetView):
    """
    Clase de autocompletado para los municipios
    """

    def get_queryset(self):

        estado = self.forwarded.get("estado_edit", None)
        if estado:
            qs = Municipio.objects.filter(estado_id=estado)
        else:
            qs = Municipio.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q).order_by("nombre")

        return qs


##############################################################################
class ParroquiaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        municipio = self.forwarded.get("municipio_edit", None)
        if municipio:
            qs = Parroquia.objects.filter(municipio_id=municipio)
        else:
            qs = Parroquia.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q).order_by("nombre")

        return qs


##############################################################################
class EtniaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Etnia.objects.all()

        if self.q:
            qs = qs.filter(nombreetnia__istartswith=self.q)

        return qs


##############################################################################
