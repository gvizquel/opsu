# -*- coding: utf-8 -*-
"""
Formularios de aplicación OEU
"""
# Django Libraries
from django import forms
from django.contrib import messages
from django.forms import ModelForm, widgets
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe

# Thirdparty Libraries
from dal import autocomplete
from globales.models import Municipio, Parroquia
from leaflet.forms.widgets import LeafletWidget
from oeu.models import (
    Ieu,
    IeuSfc,
    Localidad,
    LocalidadActividadCultural,
    LocalidadAgrupacionCivica,
    LocalidadAyudaEconomica,
    LocalidadDisciplinaDeportiva,
    LocalidadOrganizacionEstudiantil,
    LocalidadRedSocial,
    LocalidadRequisitoIngreso,
    LocalidadServicio,
    LocalidadSfc,
    SubTipoInstitucion,
    SubTipoInstitucionSfc,
    TipoEspecificoIeuSfc,
    TipoEspecificoInstitucion,
    TipoInstitucion,
    TipoInstitucionSfc,
)

LEAFLET_WIDGET_POINT_ATTRS = {
    # "map_height": "400px",
    "map_width": "100%",
    "display_raw": False,
    "geom_type": "Point",
    "zoom": 10,
}

LEAFLET_WIDGET_POLYGON_ATTRS = {
    # "map_height": "500px",
    "map_width": "100%",
    "display_raw": False,
    "geom_type": "Polygon",
}


# ########################################################################## #
def valida_editor(self, editor):
    """
    Esta función valida si el usuario editor no existe previamente lo agrego
    """
    if editor and (self.request.user.username not in editor):
        return editor + ", " + self.request.user.username
    elif editor and (self.request.user.username in editor):
        return editor
    else:
        return self.request.user.username


# ########################################################################## #
class TipoInstitucionForm(ModelForm):
    """
    Formulario ajustado para manipular los tipos de institución de la oferta
    académica
    """

    nombre_tipo = forms.CharField(
        disabled=True, label="Nombre Tipo IEU", required=False
    )
    orden = forms.CharField(disabled=True, label="Orden IEU", required=False)
    usuario_revisor = forms.CharField(
        disabled=True, label="Revisor(es)", required=False
    )
    usuario_editor = forms.CharField(disabled=True, label="Editor", required=False)
    revisor_edit = forms.CharField(disabled=True, label="")
    cod_activacion = forms.ChoiceField(
        widget=forms.RadioSelect(), label="Activo/Inactivo"
    )

    class Meta:
        model = TipoInstitucion
        fields = ("cod_activacion",)
        labels = {"nombre_edit": (""), "orden_edit": (""), "revisor_edit": ("")}

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop("request", None)
        super(TipoInstitucionForm, self).__init__(*args, **kwargs)

        # self.fields['revisor_edit'].widget.attrs['readonly'] = True

        # Concateno a los revisores
        # self.initial['revisor_edit'] = 'a' #valida_editor(self, self.instance.revisor_edit)

        # Si estoy editando un registro incializo los campos
        if self.instance.pk:
            self.initial["nombre_tipo"] = self.instance.nombre
            self.initial["orden"] = self.instance.orden
            self.initial["usuario_revisor"] = self.instance.revisor
            self.initial["usuario_editor"] = self.instance.editor
            current_cod_activacion = self.instance.cod_activacion

            # Construyo su codigo de validadción de acuerdo al modelo (tabla) correspondiente
            # tratarse del modelo TipoInstitucion debemos controlar el bit 8 (posición 7 en la
            # lista) del cod_activacion.

            # Al guardar siempre se debe inactivar el bit de revisado (bit 2 posicion 1 en la lista)
            # para indicar que este registro fue revisado por alguien
            current_cod_activacion = list(current_cod_activacion)
            current_cod_activacion[1] = "0"
            current_cod_activacion = "".join(current_cod_activacion)

            if current_cod_activacion[7:8] == "1":
                activo = current_cod_activacion
                inactivo = list(activo)
                inactivo[7] = "0"
                inactivo = "".join(inactivo)
            else:
                inactivo = list(current_cod_activacion)
                activo = list(inactivo)
                activo[7] = "1"
                activo = "".join(activo)
        else:
            activo = "00000001"
            inactivo = "00000000"
            current_cod_activacion = activo

        CODACTIVACION = ((activo, "Activo"), (inactivo, "Inactivo"))

        self.fields["cod_activacion"].choices = CODACTIVACION
        self.initial["cod_activacion"] = current_cod_activacion

        # Preparar mensaje de inactivación:
        if (
            current_cod_activacion != "01000001"
            and current_cod_activacion != "11000001"
            and current_cod_activacion != "10000001"
            and current_cod_activacion != "00000001"
            and self.instance.pk
        ):
            mensaje = mark_safe("Este tipo de IEU se encuentra inactivo:")
            if current_cod_activacion[7:8] == "0":
                mensaje += mark_safe("<br><b>Tipo IEU</b>: Inactivo")
            messages.error(self.request, mensaje)

        # Solo si no es un publicador desabilito las opciones de revisor
        if not self.request.user.has_perm("oeu.post_oeu"):
            self.fields["publicar"].disabled = True
            self.fields["cod_activacion"].disabled = True


# ########################################################################## #
class SubTipoInstitucionForm(ModelForm):
    """
    Formulario ajustado para manipular los tipos de institución de la oferta académica
    """

    tipo_ieu = forms.CharField(disabled=True, label="Tipo IEU", required=False)
    nombre_sub_tipo = forms.CharField(
        disabled=True, label="Sub Tipo Institucion", required=False
    )
    orden = forms.CharField(disabled=True, label="Orden IEU", required=False)
    # usuario_revisor = forms.CharField(disabled=True, label='Revisor(es)', required=False)
    # usuario_editor = forms.CharField(disabled=True, label='Editor', required=False)
    # revisor_edit = forms.CharField(disabled=True, label='')
    cod_activacion = forms.ChoiceField(
        widget=forms.RadioSelect(), label="Activo/Inactivo"
    )

    class Meta:
        model = SubTipoInstitucion
        fields = ("cod_activacion", "tipo_ieu_edit")
        widgets = {
            "cod_activacion": widgets.RadioSelect(attrs={}),
            "tipo_ieu_edit": autocomplete.ModelSelect2(
                url="oeu:tipo-ieu", attrs={"data-placeholder": "Tipo IEU ..."}
            ),
        }
        labels = {
            "tipo_ieu_edit": (""),
            "nombre_edit": (""),
            "orden_edit": (""),
            "revisor_edit": (""),
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop("request", None)
        super(SubTipoInstitucionForm, self).__init__(*args, **kwargs)

        # self.fields['revisor_edit'].widget.attrs['readonly'] = True

        # Concateno a los revisores
        # self.initial['revisor_edit'] = valida_editor(self, self.instance.revisor_edit)

        # Si estoy editando un registro incializo los campos
        if self.instance.pk:
            self.initial["nombre_sub_tipo"] = self.instance.nombre
            self.initial["tipo_ieu"] = self.instance.tipo_ieu
            self.initial["orden"] = self.instance.orden
            # self.initial['usuario_revisor'] = self.instance.revisor
            # self.initial['usuario_editor'] = self.instance.editor
            current_cod_activacion = self.instance.cod_activacion

            # Construyo su codigo de validadción de acuerdo al modelo (tabla) correspondiente
            # tratarse del modelo TipoInstitucion debemos controlar el bit 8 (posición 7 en la
            # lista) del cod_activacion.

            # Al guardar siempre se debe inactivar el bit de revisado (bit 2 posicion 1 en la lista)
            # para indicar que este registro fue revisado por alguien
            current_cod_activacion = list(current_cod_activacion)
            current_cod_activacion[1] = "0"
            current_cod_activacion = "".join(current_cod_activacion)

            if current_cod_activacion[6:7] == "1":
                activo = current_cod_activacion
                inactivo = list(activo)
                inactivo[6] = "0"
                inactivo = "".join(inactivo)
            else:
                inactivo = current_cod_activacion
                activo = list(inactivo)
                activo[6] = "1"
                activo = "".join(activo)
        else:
            activo = "00000011"
            inactivo = "00000001"
            current_cod_activacion = activo

        CODACTIVACION = ((activo, "Activo"), (inactivo, "Inactivo"))

        self.fields["cod_activacion"].choices = CODACTIVACION
        self.initial["cod_activacion"] = current_cod_activacion

        # Preparar mensaje de inactivación:
        if (
            current_cod_activacion != "01000011"
            and current_cod_activacion != "11000011"
            and current_cod_activacion != "10000011"
            and current_cod_activacion != "00000011"
            and self.instance.pk
        ):
            mensaje = mark_safe("Este Sub Tipo IEU se encuentra inactivo:")
            if current_cod_activacion[7:8] == "0":
                mensaje += mark_safe(
                    "<br><b>Tipo IEU</b>: Inactivo" + activo[7:8] + activo[6:7]
                )
            if current_cod_activacion[6:7] == "0":
                mensaje += mark_safe("<br><b>Sub Tipo Institucion</b>: Inactivo")
            messages.error(self.request, mensaje)

        # Solo si no es un publicador desabilito las opciones de revisor
        if not self.request.user.has_perm("oeu.post_oeu"):
            self.fields["publicar"].disabled = True
            self.fields["cod_activacion"].disabled = True


# ########################################################################## #
class TipoIeuForm(ModelForm):
    """
    Formulario ajustado para manipular los tipos de institución de la oferta
    académica
    """

    class Meta:
        model = TipoInstitucion
        fields = ("nombre_edit", "cod_activacion", "orden_edit", "publicar", "editor")
        labels = {"nombre_edit": "Nombre", "orden_edit": "Orden"}
        widgets = {
            "nombre_edit": forms.TextInput(
                attrs={"style": "text-transform:uppercase;", "class": "form-control"}
            ),
            "orden_edit": forms.NumberInput(attrs={"class": "form-control"}),
        }


# ########################################################################## #
# FormSet Soporte Formal de Cambio en instituciones para el formulario tipo IEU
TIPOIEUSFC_FORMSET = inlineformset_factory(
    TipoInstitucion,
    TipoInstitucionSfc,
    fields=["sfc"],
    widgets={
        "sfc": forms.Select(
            attrs={"class": "form-control formset-select2", "style": "width:100%"}
        )
    },
    extra=1,
)

# ########################################################################## #
"""FormSet Soporte Formal de Cambio en instituciones para el formulario
Sub Tipo IEU
"""
SUBTIPOIEUSFC_FORMSET = inlineformset_factory(
    SubTipoInstitucion,
    SubTipoInstitucionSfc,
    fields=["sfc"],
    widgets={
        "sfc": forms.Select(
            attrs={"class": "form-control formset-select2", "style": "width:100%"}
        )
    },
    extra=1,
)

# ########################################################################## #
"""FormSet Soporte Formal de Cambio en instituciones para el formulario
Tipo especifico IEU
"""
TIPOESPECIFICOIEUSFC_FORMSET = inlineformset_factory(
    TipoEspecificoInstitucion,
    TipoEspecificoIeuSfc,
    fields=["sfc"],
    widgets={
        "sfc": forms.Select(
            attrs={"class": "form-control formset-select2", "style": "width:100%"}
        )
    },
    extra=1,
)


# ########################################################################## #
class SubTipoIeuForm(ModelForm):
    """
    Formulario ajustado para manipular los tipos de institución de la oferta
    académica
    """

    class Meta:
        model = SubTipoInstitucion
        fields = (
            "tipo_ieu_edit",
            "nombre_edit",
            "cod_activacion",
            "orden_edit",
            "publicar",
            "editor",
        )
        labels = {
            "tipo_ieu_edit": "Tipo IEU",
            "nombre_edit": "Nombre",
            "orden_edit": "Orden",
        }
        widgets = {
            "tipo_ieu_edit": autocomplete.ModelSelect2(
                url="oeu:tipo-ieu-au",
                attrs={"class": "form-control", "data-placeholder": "Tipo IEU ..."},
            ),
            "nombre_edit": forms.TextInput(
                attrs={"style": "text-transform:uppercase;", "class": "form-control"}
            ),
            "orden_edit": forms.NumberInput(attrs={"class": "form-control"}),
        }


# ########################################################################## #
class TipoEspecificoIeuForm(ModelForm):
    """
    Formulario ajustado para manipular los tipos de institución de la oferta
    académica
    """

    class Meta:
        model = TipoEspecificoInstitucion
        fields = (
            "tipo_ieu_edit",
            "sub_tipo_ieu_edit",
            "nombre_edit",
            "cod_activacion",
            "orden_edit",
            "publicar",
            "editor",
        )
        labels = {
            "tipo_ieu_edit": "Tipo IEU",
            "sub_tipo_ieu_edit": "Sub Tipo IEU",
            "nombre_edit": "Nombre",
            "orden_edit": "Orden",
        }
        widgets = {
            "tipo_ieu_edit": autocomplete.ModelSelect2(
                url="oeu:tipo-ieu-au",
                attrs={"class": "form-control", "data-placeholder": "Tipo IEU ..."},
            ),
            "sub_tipo_ieu_edit": autocomplete.ModelSelect2(
                url="oeu:sub-tipo-ieu-au",
                forward=["tipo_ieu_edit"],
                attrs={"class": "form-control", "data-placeholder": "Sub Tipo IEU ..."},
            ),
            # 'sub_tipo_ieu_edit': forms.Select(attrs={'class':'form-control'}),
            "nombre_edit": forms.TextInput(
                attrs={"style": "text-transform:uppercase;", "class": "form-control"}
            ),
            "orden_edit": forms.NumberInput(attrs={"class": "form-control"}),
        }


# ########################################################################## #
class IeuForm(ModelForm):
    """
    Formulario ajustado para manipular las IEU de la oferta académica
    """

    class Meta:
        model = Ieu
        fields = (
            "tipo_especifico_ieu_edit",
            "institucion_ministerial_edit",
            "localidad_principal_edit",
            "logo_edit",
            "fachada_edit",
            "cod_activacion",
            "publicar",
            "editor",
        )
        labels = {
            "tipo_especifico_ieu_edit": "Tipo Específico",
            "institucion_ministerial_edit": "Institución Ministerial",
            "localidad_principal_edit": "Localidad Principal",
            "logo_edit": "Logo",
            "fachada_edit": "Fachada",
        }
        widgets = {
            "tipo_especifico_ieu_edit": autocomplete.ModelSelect2(
                url="oeu:tipo-especifico-ieu",
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Tipo Especifico IEU ...",
                },
            ),
            "institucion_ministerial_edit": autocomplete.ModelSelect2(
                url="globales:institucion-ministerial-ieu",
                forward=["tipo_especifico_ieu_edit"],
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Institución Ministerial ...",
                },
            ),
            "localidad_principal_edit": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width:100%",
                    "data-placeholder": "Localidad Principal...",
                }
            ),
        }

    def __init__(self, obj=None, *args, **kwargs):
        super(IeuForm, self).__init__(*args, **kwargs)
        self.fields["localidad_principal_edit"].queryset = Municipio.objects.none()
        if self.instance.pk:
            self.fields["tipo_especifico_ieu_edit"].widget.attrs["disabled"] = True
            self.fields["institucion_ministerial_edit"].widget.attrs["disabled"] = True

        if "localidad_principal_edit" in self.data:
            try:
                ieu_id = self.instance.pk
                self.fields[
                    "localidad_principal_edit"
                ].queryset = Localidad.objects.filter(ieu=ieu_id).order_by("nombre")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields[
                "localidad_principal_edit"
            ].queryset = self.instance.localidad_set.order_by("nombre")


# ########################################################################## #
"""FormSet Soporte Formal de Cambio de Institucion de educacion Universitaria
"""
IEUSFC_FORMSET = inlineformset_factory(
    Ieu,
    IeuSfc,
    fields=["sfc"],
    widgets={
        "sfc": forms.Select(
            attrs={"class": "form-control formset-select2", "style": "width:100%"}
        )
    },
    extra=1,
)


# ########################################################################## #
class LocalidadForm(ModelForm):
    """
    Formulario ajustado para manipular las IEU de la oferta académica
    """

    class Meta:
        model = Localidad
        fields = (
            "ieu_edit",
            "tipo_localidad_edit",
            "nombre_edit",
            "web_site_edit",
            "direccion_edit",
            "estado_edit",
            "municipio_edit",
            "parroquia_edit",
            "centro_poblado_edit",
            "punto_edit",
            "poligonal_edit",
            "fachada_edit",
            "cod_activacion",
            "publicar",
            "editor",
        )
        labels = {
            "ieu_edit": "IEU",
            "tipo_localidad_edit": "Tipo localidad",
            "nombre_edit": "Nombre",
            "web_site_edit": "Web",
            "estado_edit": "Estado",
            "municipio_edit": "Municipio",
            "parroquia_edit": "Parroquia",
            "centro_poblado_edit": "Centro poblado",
            "direccion_edit": "Dirección",
            "punto_edit": "Coordenada",
            "poligonal_edit": "Poligonal",
            "fachada_edit": "Fachada",
        }
        widgets = {
            "ieu_edit": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width:100%",
                    "data-placeholder": "IEU...",
                }
            ),
            "tipo_localidad_edit": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width:100%",
                    "data-placeholder": "Tipo de Localidad",
                }
            ),
            "nombre_edit": forms.TextInput(
                attrs={"style": "text-transform:uppercase;", "class": "form-control"}
            ),
            "web_site_edit": forms.URLInput(attrs={"class": "form-control"}),
            "direccion_edit": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "estado_edit": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width:100%",
                    "data-placeholder": "Estado...",
                }
            ),
            "municipio_edit": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width:100%",
                    "data-placeholder": "Municipio...",
                }
            ),
            "parroquia_edit": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width:100%",
                    "data-placeholder": "Parroquia...",
                }
            ),
            "centro_poblado_edit": forms.TextInput(
                attrs={"style": "text-transform:uppercase;", "class": "form-control"}
            ),
            "punto_edit": LeafletWidget(attrs=LEAFLET_WIDGET_POINT_ATTRS),
            "poligonal_edit": LeafletWidget(attrs=LEAFLET_WIDGET_POLYGON_ATTRS),
        }

    def __init__(self, *args, **kwargs):
        super(LocalidadForm, self).__init__(*args, **kwargs)
        self.fields["web_site_edit"].required = False
        self.fields["centro_poblado_edit"].required = False
        self.fields["municipio_edit"].queryset = Municipio.objects.none()
        self.fields["parroquia_edit"].queryset = Parroquia.objects.none()
        if self.instance.pk:
            del self.fields["ieu_edit"]

        if "municipio_edit" in self.data:
            try:
                estado_edit = int(self.data.get("estado_edit"))
                self.fields["municipio_edit"].queryset = Municipio.objects.filter(
                    estado=estado_edit
                ).order_by("nombre")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields[
                "municipio_edit"
            ].queryset = self.instance.estado_edit.municipio_set.order_by("nombre")

        if "parroquia_edit" in self.data:
            try:
                municipio_edit = int(self.data.get("municipio_edit"))
                self.fields["parroquia_edit"].queryset = Parroquia.objects.filter(
                    municipio=municipio_edit
                ).order_by("nombre")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields[
                "parroquia_edit"
            ].queryset = self.instance.municipio_edit.parroquia_set.order_by("nombre")


##############################################################################
#########                       FormSet Generales                   ##########
##############################################################################

"""formset general que es utilizado por varios modulos y son pasados por
la url de la clase AgregarModeloComplejo y EditarModeloComplejo
"""

"""FormSet Soporte Formal de Cambio
"""

LOCALIDADSFC_FORMSET = inlineformset_factory(
    Localidad,
    LocalidadSfc,
    fields=["sfc"],
    widgets={
        "sfc": forms.Select(attrs={"class": "form-control", "style": "width:100%"})
    },
    extra=1,
)

##############################################################################
#########         Seccion de FormSet para el modulo Localidad       ##########
##############################################################################

"""
Aqui se encuentran el grupo de formset que se encuentran el modulo Localidad
y son utilizados en un template especifico llamado con el mismo nombre y son
pasados por la url de la clase AgregarModeloComplejo y EditarModeloComplejo
"""

"""FormSet Ayuda Económica
"""
LOCALIDADAE_FORMSET = inlineformset_factory(
    Localidad,
    LocalidadAyudaEconomica,
    fields=["ayuda_economica"],
    widgets={
        "ayuda_economica": forms.Select(
            attrs={"class": "form-control", "style": "width:100%"}
        )
    },
    extra=1,
)

"""FormSet Agrupación Cívica
"""
LOCALIDADAC_FORMSET = inlineformset_factory(
    Localidad,
    LocalidadAgrupacionCivica,
    fields=["agrupacion_civica"],
    widgets={
        "agrupacion_civica": forms.Select(
            attrs={"class": "form-control", "style": "width:100%"}
        )
    },
    extra=1,
)

"""FormSet Actividad Cultural
"""
LOCALIDADACC_FORMSET = inlineformset_factory(
    Localidad,
    LocalidadActividadCultural,
    fields=["actividad_cultural"],
    widgets={
        "actividad_cultural": forms.Select(
            attrs={"class": "form-control", "style": "width:100%"}
        )
    },
    extra=1,
)

"""FormSet Disciplina Deportiva
"""
LOCALIDADDD_FORMSET = inlineformset_factory(
    Localidad,
    LocalidadDisciplinaDeportiva,
    fields=["disciplina_deportiva"],
    widgets={
        "disciplina_deportiva": forms.Select(
            attrs={"class": "form-control", "style": "width:100%"}
        )
    },
    extra=1,
)

"""FormSet Red Social
"""
LOCALIDADRS_FORMSET = inlineformset_factory(
    Localidad,
    LocalidadRedSocial,
    fields=["red_social", "enlace"],
    widgets={
        "red_social": forms.Select(attrs={"class": "form-control"}),
        "enlace": forms.TextInput(
            attrs={"style": "text-transform:uppercase;", "class": "form-control"}
        ),
    },
    extra=1,
)

"""FormSet Organización Estudiantil
"""
LOCALIDADOE_FORMSET = inlineformset_factory(
    Localidad,
    LocalidadOrganizacionEstudiantil,
    fields=["organizacion_estudiantil"],
    widgets={
        "organizacion_estudiantil": forms.Select(
            attrs={"class": "form-control", "style": "width:100%"}
        )
    },
    extra=1,
)

"""FormSet Requisito de Ingreso
"""
LOCALIDADRI_FORMSET = inlineformset_factory(
    Localidad,
    LocalidadRequisitoIngreso,
    fields=["requisito_ingreso"],
    widgets={
        "requisito_ingreso": forms.Select(
            attrs={"class": "form-control", "style": "width:100%"}
        )
    },
    extra=1,
)

"""FormSet Servicios
"""
LOCALIDADSERV_FORMSET = inlineformset_factory(
    Localidad,
    LocalidadServicio,
    fields=["servicio"],
    widgets={
        "servicio": forms.Select(attrs={"class": "form-control", "style": "width:100%"})
    },
    extra=1,
)

# ########################################################################## #
