# Django Libraries
from django import forms

# Thirdparty Libraries
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    HTML,
    ButtonHolder,
    Column,
    Div,
    Field,
    Fieldset,
    Layout,
    Row,
    Submit,
)
from globales.models import Estado, InstitucionMinisterial, Municipio, Parroquia
from oeu.models import AreaConocimiento, Carrera, Localidad, SubAreaConocimiento
from oeuconfig.models import Titulo

GESTION_CHOICES = (
    (None, "SELECCIONE TIPO DE GESTIÓN..."),
    ("PRIVADA", "PRIVADA"),
    ("PÚBLICA", "PÚBLICA"),
)
ESTADO_CHOICES = (
    (None, "OFERTA ACTIVA..."),
    ("ACTIVA", "SI"),
    ("INACTIVA", "NO"),
)


class GeneralReportForm(forms.Form):
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.none(), label="ESTADO", required=False,
    )
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.none(), label="MUNICIPIO", required=False,
    )
    parroquia = forms.ModelChoiceField(
        queryset=Parroquia.objects.none(), label="PARROQUIA", required=False,
    )
    gestion = forms.ChoiceField(
        choices=GESTION_CHOICES, label="TIPO DE GESTIÓN", required=False
    )
    cod_activacion = forms.ChoiceField(
        choices=ESTADO_CHOICES, label="OFERTA ACTIVA", required=False
    )
    area = forms.ModelChoiceField(
        queryset=AreaConocimiento.objects.none(),
        label="ÁREA DE CONOCIMIENTO",
        required=False,
    )
    sub_area = forms.ModelChoiceField(
        queryset=SubAreaConocimiento.objects.none(),
        label="SUB ÁREA DE CONOCIMIENTO",
        required=False,
    )
    titulo = forms.ModelChoiceField(
        queryset=Titulo.objects.none(), label="TITULO DE GRADO", required=False
    )
    ieu = forms.ModelChoiceField(
        queryset=InstitucionMinisterial.objects.none(),
        label="INSTIUCIÓN DE EDUCACIÓN UNIVERSITARIA",
        required=False,
    )
    localidad = forms.ModelChoiceField(
        queryset=Localidad.objects.none(), label="LOCALIDAD", required=False,
    )
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.none(), label="PROGRAMA ACADÉMICO", required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Criapy init
        self.helper = FormHelper()
        self.helper.form_id = "tabular-report-form"
        self.helper.form_method = "post"
        self.helper.attrs["autocomplete"] = "off"
        self.helper.include_media = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        "estado", css_class="form-control select2", style="width:100%"
                    ),
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    Field(
                        "municipio",
                        css_class="form-control select2",
                        style="width:100%",
                    ),
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    Field(
                        "parroquia",
                        css_class="form-control select2",
                        style="width:100%",
                    ),
                    css_class="form-group col-md-4 mb-0",
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field(
                        "gestion", css_class="form-control select2", style="width:100%"
                    ),
                    css_class="form-group col-md-2 mb-0",
                ),
                Column(
                    Field(
                        "cod_activacion",
                        css_class="form-control select2",
                        style="width:100%",
                    ),
                    css_class="form-group col-md-2 mb-0",
                ),
                Column(
                    Field("area", css_class="form-control select2", style="width:100%"),
                    css_class="form-group col-md-4 mb-0",
                ),
                Column(
                    Field(
                        "sub_area",
                        css_class="form-control select2",
                        style="width:100%",
                    ),
                    css_class="form-group col-md-4 mb-0",
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field(
                        "titulo", css_class="form-control select2", style="width:100%",
                    ),
                    css_class="form-group col-md-12 mb-0",
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field("ieu", css_class="form-control select2", style="width:100%",),
                    css_class="form-group col-md-12 mb-0",
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field(
                        "localidad",
                        css_class="form-control select2",
                        style="width:100%",
                    ),
                    css_class="form-group col-md-12 mb-0",
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field(
                        "carrera", css_class="form-control select2", style="width:100%",
                    ),
                    css_class="form-group col-md-12 mb-0",
                ),
                css_class="form-row",
            ),
        )
        self.helper.add_input(Submit("submit", "Descargar Archivo"))
