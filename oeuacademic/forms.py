# Django Libraries
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

# Thirdparty Libraries
from dal import autocomplete
from oeu.models import Carrera, CarreraSfc, CarreraTitulo, SubAreaConocimiento
from oeuconfig.models import Titulo


class SubAreaConocimientoForm(ModelForm):
    """
    Formulario ajustado para manipular las sub áreas de conocimientos
    """

    class Meta:
        """
        Describo mi modelos, los campos y sus atributos
        """

        model = SubAreaConocimiento

        fields = ["area_conocimiento", "nombre"]

        widgets = {
            "area_conocimiento": forms.Select(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escribe la sub área de conocimiento asociada",
                }
            ),
        }


##############################################################################
class CarreraPreGradoForm(ModelForm):
    """
    Formulario ajustado para manipular las carreras de pre grado o programas
    academicos
    """

    class Meta:
        model = Carrera

        fields = [
            "localidad_edit",
            "nombre_edit",
            "descripcion_edit",
            "tipo_carrera_edit",
            # "ieu_acreditadora_edit",
            "mercado_ocupacional_edit",
            "area_conocimiento_edit",
            "sub_area_conocimiento_edit",
            "titulo_edit",
            "periodicidad_edit",
            "duracion_edit",
            # "ieu_acreditadora_edit",
            "prioritaria_edit",
            "cod_activacion",
            "publicar",
            "editor",
        ]

        labels = {
            "localidad_edit": ("Localidad"),
            "nombre_edit": ("Nombre"),
            "descripcion_edit": ("Descripción"),
            "titulo_edit": ("Título"),
            "tipo_carrera_edit": ("Tipo de Programa"),
            # "ieu_acreditadora_edit": ("Institución Acreditadora"),
            "mercado_ocupacional_edit": ("Mercado Ocupacional"),
            "area_conocimiento_edit": ("Área de Conocimiento"),
            "sub_area_conocimiento_edit": ("Sub Área de Conocimiento"),
            "duracion_edit": ("Duración"),
            "periodicidad_edit": ("Periodicidad"),
        }

        widgets = {
            "localidad_edit": autocomplete.ModelSelect2(
                url="oeu:localidad-ieu",
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Selecciona la Localidad",
                },
            ),
            "nombre_edit": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escribe el nombre de la Carrera",
                },
            ),
            "descripcion_edit": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Haz una descripción de la Carrera",
                    "rows": 2,
                },
            ),
            "tipo_carrera_edit": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Seleccione Una Opción",
                },
            ),
            # "ieu_acreditadora_edit": autocomplete.ModelSelect2(
            #     url="oeuacademic:acreditadora",
            #     attrs={
            #         "class": "form-control",
            #         "data-placeholder": "Institución Acreditadora",
            #     },
            # ),
            "mercado_ocupacional_edit": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escribe el mercado ocupacional de la carrera",
                    "rows": 2,
                },
            ),
            "area_conocimiento_edit": autocomplete.ModelSelect2(
                url="oeuacademic:area-conocimiento",
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Área de Conocimiento",
                },
            ),
            "sub_area_conocimiento_edit": autocomplete.ModelSelect2(
                url="oeuacademic:sub-area-conocimiento",
                forward=["area_conocimiento_edit"],
                attrs={
                    "class": "form-control select2",
                    "data-placeholder": "Sub Área de Conocimiento",
                },
            ),
            "titulo_edit": autocomplete.ModelSelect2(
                url="oeuacademic:titulo",
                attrs={
                    "class": "form-control select2",
                    "data-placeholder": "Titulo de egreso",
                },
            ),
            "periodicidad_edit": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Seleccione Una Opción",
                },
            ),
            "cine_f_campo_amplio_edit": autocomplete.ModelSelect2(
                url="oeuacademic:cine-f-campo-amplio",
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Seleccione Una Opción",
                },
            ),
            "cine_f_campo_especifico_edit": autocomplete.ModelSelect2(
                url="oeuacademic:cine-f-campo-especifico",
                forward=["cine_f_campo_amplio_edit"],
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Seleccione Una Opción",
                },
            ),
            "cine_f_campo_detallado_edit": autocomplete.ModelSelect2(
                url="oeuacademic:cine-f-campo-detallado",
                forward=["cine_f_campo_especifico_edit"],
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Seleccione Una Opción",
                },
            ),
            "duracion_edit": forms.NumberInput(attrs={"class": "form-control"},),
            "prioritaria_edit": forms.RadioSelect(),
        }

    def __init__(self, obj=None, *args, **kwargs):
        """Inicializa la clase en modo consulta de registro este pueda colocar
        el campo localidad_edit como no editable, esto se hace para que dicho
        registro no pueda ser manipulado
        """
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            del self.fields["localidad_edit"]


##############################################################################
"""FormSet ajustado para ser manipulado en el formulario de las carreras
de pre grado o programas academicos
"""
CARRERA_FORMSET = inlineformset_factory(
    Carrera,
    CarreraSfc,
    fields=["sfc"],
    widgets={
        "sfc": forms.Select(
            attrs={"class": "form-control formset-select2", "style": "width:100%"}
        )
    },
    extra=1,
)


##############################################################################
"""FormSet para asociar los titulos a los programas academicos de pregrado
"""
CARRERA_TITULO_FORMSET = inlineformset_factory(
    Titulo,
    CarreraTitulo,
    fields=["titulo", "periodicidad", "duracion"],
    widgets={
        "titulo": forms.Select(
            attrs={"class": "form-control formset-select2", "style": "width:100%"}
        ),
        "periodicidad": forms.Select(
            attrs={"class": "form-control formset-select2", "style": "width:100%"}
        ),
        "duracion": forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Escribe el nombre de la Carrera",
            },
        ),
    },
    extra=1,
)
