"""Vistas para el LOEU
"""
# Standard Libraries
import json
import logging

# Django Libraries
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

# Thirdparty Libraries
from dal import autocomplete
from oeu.models import (
    AreaConocimiento,
    Carrera,
    CarreraTitulo,
    Ieu,
    Localidad,
    SubAreaConocimiento,
    SubTipoInstitucion,
    TipoEspecificoInstitucion,
    TipoInstitucion,
)

#  logging
LOGGER = logging.getLogger("standart")


# ########################################################################## #
class TipoIeuAutoComplete(autocomplete.Select2QuerySetView):
    """Servicio de auto completado para el modelo TipoInstitucion
    """

    def get_queryset(self):
        queryset = TipoInstitucion.objects.filter(
            Q(cod_activacion="11000001") | Q(cod_activacion="10000001")
        )

        if self.q:
            queryset = queryset.filter(nombre__icontains=self.q)

        return queryset


# ########################################################################## #
class SubTipoIeuAutoComplete(autocomplete.Select2QuerySetView):
    """Servicio de auto completado para el modelo TipoInstitucion
    """

    def get_queryset(self):

        tipo_ieu_edit = self.forwarded.get("tipo_ieu_edit", None)

        queryset = SubTipoInstitucion.objects.filter(
            Q(cod_activacion="11000011") | Q(cod_activacion="10000011")
        )

        if tipo_ieu_edit:
            queryset = queryset.filter(tipo_ieu=tipo_ieu_edit)

        if self.q:
            queryset = queryset.filter(
                Q(nombre__icontains=self.q) | Q(tipo_ieu__nombre__icontains=self.q)
            )

        return queryset


# ########################################################################## #
class TipoEspecificoIeuAutocomplete(autocomplete.Select2QuerySetView):
    """Servicio de auto completado para el modelo SubTipoInstitucion
    """

    def get_queryset(self):

        sub_tipo_ieu_edit = self.forwarded.get("sub_tipo_ieu_edit", None)

        queryset = TipoEspecificoInstitucion.objects.filter(
            Q(cod_activacion="11000111") | Q(cod_activacion="10000111")
        )

        if sub_tipo_ieu_edit:
            queryset = queryset.filter(sub_tipo_ieu=sub_tipo_ieu_edit)

        if self.q:
            queryset = queryset.filter(
                Q(nombre__icontains=self.q) | Q(sub_tipo_ieu__nombre__icontains=self.q)
            )

        return queryset


# ########################################################################## #
class IeuAutocomplete(autocomplete.Select2QuerySetView):
    """Servicio de auto completado para el modelo Institucion
    """

    def get_queryset(self):
        queryset = Ieu.objects.filter(
            (Q(cod_activacion="11001111") | Q(cod_activacion="10001111"))
        )

        if self.q:
            queryset = queryset.filter(
                institucion_ministerial__nombre__icontains=self.q
            )

        return queryset


# ########################################################################## #
class LocalidadIeuAutocomplete(autocomplete.Select2QuerySetView):
    """Servicio de auto completado para el modelo Localidad
    """

    def get_queryset(self):

        institucion_ministerial_edit = self.forwarded.get(
            "institucion_ministerial_edit", None
        )

        queryset = Localidad.objects.filter(
            (Q(cod_activacion="11011111") | Q(cod_activacion="10011111"))
        )

        if institucion_ministerial_edit:
            queryset = queryset.filter(ieu=institucion_ministerial_edit)

        if self.q:
            queryset = queryset.filter(
                Q(nombre__icontains=self.q)
                | Q(ieu__institucion_ministerial__nombre__icontains=self.q)
                | Q(ieu__tipo_especifico_ieu__nombre__icontains=self.q)
            )

        return queryset


# ########################################################################## #
class CarreraAutocomplete(autocomplete.Select2QuerySetView):
    """Servicio de auto completado para el modelo Carrera
    """

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Carrera.objects.none()

        localidad = self.forwarded.get("localidad", None)

        queryset = Carrera.objects.filter(id_localidad_pub=localidad)

        if self.q:
            queryset = queryset.filter(nombre_carrera_pub__icontains=self.q)

        return queryset


# ########################################################################## #
#              Vistas para la gestión de los Modelos Complejos               #
# ########################################################################## #
class ListarModeloComplejo(LoginRequiredMixin, ListView):
    """Con esta clase se puede listar los modelos que gestionan la estructura
    de datos de las institucuines de educación universitaría: TipoInstitucion,
    SubTipoInstitucion, TipoEspecificoInstitucion, Institucion, Localidad,
    Carrera.
    """

    filtro_por = None

    def get_queryset(self):
        queryset = self.model.objects.all()
        filtro = self.request.GET.get("filtro")
        if filtro:
            filtro = {self.filtro_por: filtro}
            queryset = queryset.filter(**filtro)

        return queryset


# ########################################################################## #
class AgregarModeloComplejo(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Con esta clase se puede agregar los modelos que gestionan la estructura
    de datos de las institucuines de educación univeristaría: TipoInstitucion,
    SubTipoInstitucion, TipoEspecificoInstitucion, Institucion, Localidad,
    Carrera.
    """

    posicion = None
    revisor_edit = None
    model = None
    SfcFormSet = None
    AyudaFormSet = None
    AgrupacionFormSet = None
    ActividadFormSet = None
    DisciplinaFormSet = None
    RedSocialFormSet = None
    OrganizacionFormSet = None
    RequisitoFormSet = None
    ServicioFormSet = None
    relacion_id = None
    TituloFormSet = None

    def get_cod_activacion(self):
        """Prepara la brekera del código de activación de cada uno los modelos
        correspondientes para insertar o editar los registros en la base de
        datos
        """
        cod_activacion = list("00000000")
        for posicion in range(self.posicion, 8):
            cod_activacion[posicion] = "1"
        cod_activacion = "".join(cod_activacion)

        return cod_activacion

    def get_context_data(self, **kwargs):
        contexto = super(AgregarModeloComplejo, self).get_context_data(**kwargs)
        contexto["agregar"] = True
        contexto["sfc_form"] = self.SfcFormSet()
        # los FormSet unicamente se mostraran en el template de localidad IEU cuando el
        # parametro del modelo sea igual a Localidad entendiendose que la clase es
        # generica
        if self.model == Localidad:
            contexto["ayuda_form"] = self.AyudaFormSet()
            contexto["agrupacion_form"] = self.AgrupacionFormSet()
            contexto["actividad_form"] = self.ActividadFormSet()
            contexto["disciplina_form"] = self.DisciplinaFormSet()
            contexto["redsocial_form"] = self.RedSocialFormSet()
            contexto["organizacion_form"] = self.OrganizacionFormSet()
            contexto["requisito_form"] = self.RequisitoFormSet()
            contexto["servicio_form"] = self.ServicioFormSet()
        if self.model == Carrera:
            contexto["form"] = self.form_class(
                filtro=self.request.GET.get("filtro", None)
            )
            contexto["titulo_form"] = self.TituloFormSet()
        return contexto

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)
        formsets_form = [self.SfcFormSet(self.request.POST)]

        """ distintos formsets que pueden llegar al formulario complejo
        """

        if self.model == Localidad:
            formsets_form.append(self.AyudaFormSet(self.request.POST))
            formsets_form.append(self.AgrupacionFormSet(self.request.POST))
            formsets_form.append(self.ActividadFormSet(self.request.POST))
            formsets_form.append(self.DisciplinaFormSet(self.request.POST))
            formsets_form.append(self.RedSocialFormSet(self.request.POST))
            formsets_form.append(self.OrganizacionFormSet(self.request.POST))
            formsets_form.append(self.RequisitoFormSet(self.request.POST))
            formsets_form.append(self.ServicioFormSet(self.request.POST))
        if self.model == Carrera:
            formsets_form.append(self.TituloFormSet(self.request.POST))

        for formset in formsets_form:
            if not formset.is_valid():
                return self.form_invalid(form)
        if not form.is_valid():
            return self.form_invalid(form)

        return self.form_valid(form, formsets_form)

    def form_valid(self, form, formsets_form):
        self.object = form.save(commit=False)
        self.object.cod_activacion = self.get_cod_activacion()
        self.object.publicar = False
        with transaction.atomic():
            LOGGER.info("AQUI")
            self.object.save()
            for formulario in formsets_form:
                formulario.instance = self.object
                formulario.save()

            # Ahora guardo el regisro en la tabla de revisores edit.
            filtro = {self.relacion_id: self.object, "persona": self.request.user}
            rev = self.revisor_edit(**filtro)
            rev.save()

            messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if "filtro" in self.request.GET:
            LOGGER.info(
                "{}?filtro={}".format(self.success_url, self.request.GET["filtro"])
            )
            return str(
                "{}?filtro={}".format(self.success_url, self.request.GET["filtro"])
            )

        return str(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# ########################################################################## #
class EditarModeloComplejo(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Con esta clase se puede editar los modelos que gestionan la estructura
    de datos de las institucuines de educación univeristaría: TipoInstitucion,
    SubTipoInstitucion, TipoEspecificoInstitucion, Institucion, Localidad,
    Carrera.
    """

    posicion = None
    revisor_edit = None
    model = None
    SfcFormSet = None
    AyudaFormSet = None
    AgrupacionFormSet = None
    ActividadFormSet = None
    DisciplinaFormSet = None
    RedSocialFormSet = None
    OrganizacionFormSet = None
    RequisitoFormSet = None
    ServicioFormSet = None
    relacion_id = None
    TituloFormSet = None

    def __init__(self, *args, **kwargs):
        super(EditarModeloComplejo, self).__init__(*args, **kwargs)
        # Para almacenar el código activo e inactivo
        self.cod_acti = None
        self.cod_inac = None
        self.object = None

    def get_cod_activacion(self):
        """Prepara la brekera del código de activación de cada uno los modelos
        correspondientes para insertar o editar los registros en la base de
        datos
        """
        self.object = self.get_object()
        if self.object.cod_activacion[self.posicion] == "1":
            self.cod_acti = self.object.cod_activacion
            lista = list(self.cod_acti)
            lista[self.posicion] = "0"
            self.cod_inac = "".join(lista)
            activo = True
        else:
            self.cod_inac = self.object.cod_activacion
            lista = list(self.cod_inac)
            lista[self.posicion] = "1"
            self.cod_acti = "".join(lista)
            activo = False

        return activo

    def get_revisado(self, cod_activacion):
        """Prepara la brekera del código de activación de cada uno los modelos
        correspondientes para insertar o editar los registros en la base de
        datos
        """
        cod_activacion = list(cod_activacion)
        cod_activacion[1] = "0"
        cod_activacion = "".join(cod_activacion)

        return cod_activacion

    def mensaje_inactivacion(self):
        """Prepara la brekera del código de activación de cada uno los modelos
        correspondientes para insertar o editar los registros en la base de
        datos
        """
        self.object = self.get_object()

        mensaje = "Este registro se encuentra inactivo:"

        if self.posicion <= 7 and self.object.cod_activacion[7] == "0":
            mensaje += "<br><b>Tipo IEU</b>: Inactivo"
        if self.posicion <= 6 and self.object.cod_activacion[6] == "0":
            mensaje += "<br><b>Sub Tipo Institucion</b>: Inactivo"
        if self.posicion <= 5 and self.object.cod_activacion[5] == "0":
            mensaje += "<br><b>Tipo Específico IEU</b>: Inactivo"
        if self.posicion <= 4 and self.object.cod_activacion[4] == "0":
            mensaje += "<br><b>IEU</b>: Inactivo"
        if self.posicion <= 3 and self.object.cod_activacion[3] == "0":
            mensaje += "<br><b>Localidad</b>: Inactivo"
        if self.posicion <= 2 and self.object.cod_activacion[2] == "0":
            mensaje += "<br><b>Programa Académico</b>: Inactivo"

        return mark_safe(mensaje)

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        contexto = super(EditarModeloComplejo, self).get_context_data(**kwargs)
        contexto["agregar"] = False
        contexto["activo"] = self.get_cod_activacion()

        if not contexto["activo"]:
            messages.error(self.request, self.mensaje_inactivacion())

        if (
            self.object.cod_activacion[0] == "0"
            and self.object.cod_activacion[1] == "0"
        ):
            messages.warning(
                self.request,
                "Estás editando un nuevo registro\
            que aún no ha sido publicado",
            )

        if self.request.POST:
            contexto["sfc_form"] = self.SfcFormSet(
                self.request.POST, instance=self.object
            )

            """
            En esta seccion del codigo se muestran, se edita y se agraga nuevos
            registros en los FormSet
            en el template siempre que su modelo sea Localidad
            """
            if self.model == Carrera:
                contexto["titulo_form"] = self.TituloFormSet(
                    self.request.POST, instance=self.object
                )
                contexto["titula"] = CarreraTitulo.objects.filter(carrera=self.object)

            if self.model == Localidad:
                contexto["ayuda_form"] = self.AyudaFormSet(
                    self.request.POST, instance=self.object
                )
                contexto["agrupacion_form"] = self.AgrupacionFormSet(
                    self.request.POST, instance=self.object
                )
                contexto["actividad_form"] = self.ActividadFormSet(
                    self.request.POST, instance=self.object
                )
                contexto["disciplina_form"] = self.DisciplinaFormSet(
                    self.request.POST, instance=self.object
                )
                contexto["redsocial_form"] = self.RedSocialFormSet(
                    self.request.POST, instance=self.object
                )
                contexto["organizacion_form"] = self.OrganizacionFormSet(
                    self.request.POST, instance=self.object
                )
                contexto["requisito_form"] = self.RequisitoFormSet(
                    self.request.POST, instance=self.object
                )
                contexto["servicio_form"] = self.ServicioFormSet(
                    self.request.POST, instance=self.object
                )
        else:
            contexto["sfc_form"] = self.SfcFormSet(instance=self.object)

            if self.model == Carrera:
                contexto["titulo_form"] = self.TituloFormSet(instance=self.object)
                contexto["titula"] = CarreraTitulo.objects.filter(carrera=self.object)

            if self.model == Localidad:
                contexto["ayuda_form"] = self.AyudaFormSet(instance=self.object)
                contexto["agrupacion_form"] = self.AgrupacionFormSet(
                    instance=self.object
                )
                contexto["actividad_form"] = self.ActividadFormSet(instance=self.object)
                contexto["disciplina_form"] = self.DisciplinaFormSet(
                    instance=self.object
                )
                contexto["redsocial_form"] = self.RedSocialFormSet(instance=self.object)
                contexto["organizacion_form"] = self.OrganizacionFormSet(
                    instance=self.object
                )
                contexto["requisito_form"] = self.RequisitoFormSet(instance=self.object)
                contexto["servicio_form"] = self.ServicioFormSet(instance=self.object)

        """ Si estoy editando la IEU debo pasar al contexto del formulario la
        lista de sus localidades activas para dibujarlas en el mapa.
        """
        if self.model == Ieu:
            contexto["localidades"] = Localidad.objects.filter(
                Q(ieu=self.object.pk),
                (Q(cod_activacion="11011111") | Q(cod_activacion="10011111")),
            )

        """ Si estoy editando la localidad debo pasar al contexto del formulario
        la lista de los programas academicos que dictan en esa localidad.
        """
        if self.model == Localidad:
            contexto["programas"] = Carrera.objects.filter(
                Q(localidad=self.object.pk),
                (Q(cod_activacion="11111111") | Q(cod_activacion="10111111")),
            )

        return contexto

    def post(self, request, *args, **kwargs):
        contexto = self.get_context_data(**kwargs)
        form = self.get_form(self.form_class)
        formsets_form = [contexto["sfc_form"]]

        """ distintos formsets que pueden llegar al formulario complejo
        """
        formsets_form.append(contexto.get("ayuda_form")) if contexto.get(
            "ayuda_form"
        ) else formsets_form
        formsets_form.append(contexto.get("agrupacion_form")) if contexto.get(
            "agrupacion_form"
        ) else formsets_form
        formsets_form.append(contexto.get("actividad_form")) if contexto.get(
            "actividad_form"
        ) else formsets_form
        formsets_form.append(contexto.get("disciplina_form")) if contexto.get(
            "disciplina_form"
        ) else formsets_form
        formsets_form.append(contexto.get("redsocial_form")) if contexto.get(
            "redsocial_form"
        ) else formsets_form
        formsets_form.append(contexto.get("organizacion_form")) if contexto.get(
            "organizacion_form"
        ) else formsets_form
        formsets_form.append(contexto.get("requisito_form")) if contexto.get(
            "requisito_form"
        ) else formsets_form
        formsets_form.append(contexto.get("servicio_form")) if contexto.get(
            "servicio_form"
        ) else formsets_form
        formsets_form.append(contexto.get("titulo_form")) if contexto.get(
            "titulo_form"
        ) else formsets_form

        for formset in formsets_form:
            if not formset.is_valid():
                return self.form_invalid(form)
        if not form.is_valid():
            return self.form_invalid(form)

        return self.form_valid(form, formsets_form)

    def form_valid(self, form, formsets_form):

        self.object = self.get_object()
        editor = self.object.editor
        cod_activacion = self.object.cod_activacion
        formulario = form.save(commit=False)

        formulario.cod_activacion = self.get_revisado(cod_activacion)
        formulario.editor = editor

        if formulario.publicar and self.request.user.has_perm("oeu.post_oeu"):
            formulario.editor = self.request.user
            if form.cleaned_data["cod_activacion"] == "True":
                formulario.cod_activacion = self.get_revisado(self.cod_acti)
            elif form.cleaned_data["cod_activacion"] == "False":
                formulario.cod_activacion = self.get_revisado(self.cod_inac)

        with transaction.atomic():

            """ en este caso si se cumple la condicion que el formulario es valido
            y se instancia del formulario principal y se guardan los cambios
            """
            for formset in formsets_form:
                formset.instance = formulario
                formset.save()
            formulario.save()
        """ Ahora guardo el regisro en la tabla de revisores en caso de que
        el revisor ya no esté asociado. """

        if not formulario.publicar:
            filtro = {
                self.relacion_id: self.object,
                "persona": self.request.user.pk,
            }
            revisor = self.revisor_edit.objects.filter(**filtro).exists()

            if not revisor:
                filtro = {
                    self.relacion_id: self.object,
                    "persona": self.request.user,
                }
                rev = self.revisor_edit(**filtro)
                rev.save()

            messages.success(self.request, self.success_message)

        return HttpResponseRedirect(self.get_success_url())

        """cuando el formulario es invalido por causa de un campo no llenado se procede
        a enviar un mensaje de error, y tomando en cuenta si el modelo es localidad los
        parametros que recibe la funcion se declaran None sino se dejan normal
        """

    def get_success_url(self):
        if "filtro" in self.request.GET:
            LOGGER.info(
                "{}?filtro={}".format(self.success_url, self.request.GET["filtro"])
            )
            return str(
                "{}?filtro={}".format(self.success_url, self.request.GET["filtro"])
            )

        return str(self.success_url)

    def form_invalid(self, form):

        messages.error(
            self.request, "<b>Error en los siguientes campos del formulario:</b>"
        )

        return self.render_to_response(self.get_context_data(form=form))


# ########################################################################## #
class EliminarModeloComplejo(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Con esta clase se puede eliminar los modelos que gestionan la estructura
    de datos de las institucuines de educación univeristaría: TipoInstitucion,
    SubTipoInstitucion, TipoEspecificoInstitucion, Institucion, Localidad,
    Carrera.
    """

    relacion = None
    rel_sfc = None
    relacion_id = None

    def __init__(self, *args, **kwargs):
        super(EliminarModeloComplejo, self).__init__(*args, **kwargs)
        # Para almacenar el código activo e inactivo
        self.relacionado = None
        self.object = None

    def get_context_data(self, **kwargs):
        contexto = super(EliminarModeloComplejo, self).get_context_data(**kwargs)

        if self.relacion:
            filtro = {self.relacion_id: self.kwargs["pk"]}
            self.relacionado = self.relacion.objects.filter(**filtro).exists()

        contexto["relacionado"] = self.relacionado

        return contexto

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.get_context_data(**kwargs)

        if not self.relacionado:
            LOGGER.info("Eliminando: {}".format(self.object))
            self.object.delete()
            LOGGER.info("¡Eliminado!")
            messages.success(self.request, self.success_message)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if "filtro" in self.request.GET:
            LOGGER.info(
                "{}?filtro={}".format(self.success_url, self.request.GET["filtro"])
            )
            return str(
                "{}?filtro={}".format(self.success_url, self.request.GET["filtro"])
            )

        return str(self.success_url)


# ########################################################################## #
class DetalleModeloComplejo(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    """Con esta clase se puede eliminar los modelos que gestionan la estructura
    de datos de las institucuines de educación univeristaría: TipoInstitucion,
    SubTipoInstitucion, TipoEspecificoInstitucion, Institucion, Localidad,
    Carrera.
    """

    relacion = None
    rel_sfc = None
    relacion_id = None

    def get_context_data(self, **kwargs):
        contexto = super(DetalleModeloComplejo, self).get_context_data(**kwargs)

        if self.model == Carrera:
            contexto["titula"] = CarreraTitulo.objects.filter(carrera=self.object)

        return contexto

    def get_success_url(self):
        if "filtro" in self.request.GET:
            LOGGER.info(
                "{}?filtro={}".format(self.success_url, self.request.GET["filtro"])
            )
            return str(
                "{}?filtro={}".format(self.success_url, self.request.GET["filtro"])
            )

        return str(self.success_url)


def talero_oeu(request):
    titulo = "Tablero Resumen"
    dict_programa = {}
    dict_programa_gestion = {}
    dict_programa_area = {}
    dict_ieu_tipo = {}
    dict_ieu_gestion = {}
    dict_localidad_gestion = {}

    # ******************************************************************************** #

    total_programas = Carrera.objects.filter(
        Q(cod_activacion="11111111") | Q(cod_activacion="10111111")
    ).count()

    total_localidades = Localidad.objects.filter(
        Q(cod_activacion="11011111") | Q(cod_activacion="10011111")
    ).count()

    programas = (
        Carrera.objects.filter(
            Q(cod_activacion="11111111") | Q(cod_activacion="10111111")
        )
        .values("tipo_carrera__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    for programa in programas:
        dict_programa[programa["tipo_carrera__nombre"]] = programa["total"]

    serial_programa = json.dumps(dict_programa, ensure_ascii=False)

    # ******************************************************************************** #

    localidad_gestion = (
        Localidad.objects.filter(
            Q(cod_activacion="11011111") | Q(cod_activacion="10011111")
        )
        .values("ieu__institucion_ministerial__dep_admin")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    for localidad in localidad_gestion:
        dict_localidad_gestion[
            localidad["ieu__institucion_ministerial__dep_admin"]
        ] = localidad["total"]

    serial_localidad_gestion = json.dumps(dict_localidad_gestion, ensure_ascii=False)

    # ******************************************************************************** #

    total_ieu = Ieu.objects.filter(
        Q(cod_activacion="11001111") | Q(cod_activacion="10001111")
    ).count()

    ieu_gestion = (
        Ieu.objects.filter(Q(cod_activacion="11001111") | Q(cod_activacion="10001111"))
        .values("institucion_ministerial__dep_admin")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    for ieu in ieu_gestion:
        dict_ieu_gestion[ieu["institucion_ministerial__dep_admin"]] = ieu["total"]

    serial_ieu_gestion = json.dumps(dict_ieu_gestion, ensure_ascii=False)

    # ******************************************************************************** #

    ieu_tipo = (
        Ieu.objects.filter(Q(cod_activacion="11001111") | Q(cod_activacion="10001111"))
        .values("tipo_especifico_ieu", "institucion_ministerial__dep_admin")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    for ieu in ieu_tipo:
        tipo = TipoEspecificoInstitucion.objects.get(pk=ieu["tipo_especifico_ieu"])
        if tipo.nombre:
            nombre = "{} ({})".format(
                tipo.__str__(), ieu["institucion_ministerial__dep_admin"]
            )
            dict_ieu_tipo[nombre] = ieu["total"]
        elif tipo.sub_tipo_ieu.nombre:
            nombre = "{} ({})".format(
                tipo.sub_tipo_ieu.__str__(), ieu["institucion_ministerial__dep_admin"]
            )
            dict_ieu_tipo[nombre] = ieu["total"]
        else:
            nombre = "{} ({})".format(
                tipo.sub_tipo_ieu.tipo_ieu.__str__(),
                ieu["institucion_ministerial__dep_admin"],
            )
            dict_ieu_tipo[nombre] = ieu["total"]

    serial_ieu_tipo = json.dumps(dict_ieu_tipo, ensure_ascii=False)

    # ******************************************************************************** #

    programa_area = (
        Carrera.objects.filter(
            Q(cod_activacion="11111111") | Q(cod_activacion="10111111")
        )
        .values("area_conocimiento__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    for programa in programa_area:
        dict_programa_area[programa["area_conocimiento__nombre"]] = programa["total"]

    serial_programa_area = json.dumps(dict_programa_area, ensure_ascii=False)

    # ******************************************************************************** #

    programa_gestion = (
        Carrera.objects.filter(
            Q(cod_activacion="11111111") | Q(cod_activacion="10111111")
        )
        .values("localidad__ieu__institucion_ministerial__dep_admin")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    for programa in programa_gestion:
        dict_programa_gestion[
            programa["localidad__ieu__institucion_ministerial__dep_admin"]
        ] = programa["total"]

    serial_programa_gestion = json.dumps(dict_programa_gestion, ensure_ascii=False)

    # ******************************************************************************** #

    return render(
        request,
        "tablero_oeu.html",
        {
            "titulo": titulo,
            "programas_tipo": serial_programa,
            "total_programas": total_programas,
            "ieu_gestion": serial_ieu_gestion,
            "total_ieu": total_ieu,
            "ieu_tipo": serial_ieu_tipo,
            "total_localidades": total_localidades,
            "localidad_gestion": serial_localidad_gestion,
            "programa_area": serial_programa_area,
            "programa_gestion": serial_programa_gestion,
        },
    )
