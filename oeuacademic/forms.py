# Django Libraries
from django import forms
from django.forms import ModelForm
from django.forms.formsets import DELETION_FIELD_NAME
from django.forms.models import BaseInlineFormSet, inlineformset_factory

# Thirdparty Libraries
from ckeditor.widgets import CKEditorWidget
from dal import autocomplete
from oeu.models import (
    AreaConocimiento,
    Carrera,
    CarreraSfc,
    CarreraTituloEdit,
    Localidad,
    SubAreaConocimiento,
)


class AreaConocimientoForm(ModelForm):
    """
    Formulario ajustado para manipular las áreas de conocimientos
    """

    class Meta:
        """
        Describo mi modelos, los campos y sus atributos
        """

        model = AreaConocimiento

        fields = ["nombre", "descripcion"]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "style": "text-transform:uppercase;",
                    "class": "form-control",
                    "placeholder": "Área de Conocimiento...",
                }
            ),
            "descripcion": CKEditorWidget(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descripción del Área de Conocimiento...",
                    "rows": 2,
                },
            ),
        }


class SubAreaConocimientoForm(ModelForm):
    """
    Formulario ajustado para manipular las sub áreas de conocimientos
    """

    class Meta:
        """
        Describo mi modelos, los campos y sus atributos
        """

        model = SubAreaConocimiento

        fields = ["area_conocimiento", "nombre", "descripcion"]

        widgets = {
            "area_conocimiento": forms.Select(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(
                attrs={
                    "style": "text-transform:uppercase;",
                    "class": "form-control",
                    "placeholder": "Escribe la sub área de conocimiento asociada",
                }
            ),
            "descripcion": CKEditorWidget(),
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
            # "titulo_edit",
            "periodicidad_edit",
            # "duracion_edit",
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
            # "titulo_edit": ("Título"),
            "tipo_carrera_edit": ("Tipo de Programa"),
            # "ieu_acreditadora_edit": ("Institución Acreditadora"),
            "mercado_ocupacional_edit": ("Mercado Ocupacional"),
            "area_conocimiento_edit": ("Área de Conocimiento"),
            "sub_area_conocimiento_edit": ("Sub Área de Conocimiento"),
            "duracion_edit": ("Duración"),
            "periodicidad_edit": ("Periodicidad"),
            "prioritaria_edit": ("Prioritaria"),
        }

        widgets = {
            "localidad_edit": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width:100%",
                    "data-placeholder": "Localidad...",
                }
            ),
            "nombre_edit": forms.TextInput(
                attrs={
                    "style": "text-transform:uppercase;",
                    "class": "form-control",
                    "placeholder": "Escribe el nombre de la Carrera",
                },
            ),
            "descripcion_edit": CKEditorWidget(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descripción de la carrera",
                    "rows": 2,
                },
            ),
            "tipo_carrera_edit": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width:100%",
                    "data-placeholder": "Tipo de Programa...",
                }
            ),
            # "ieu_acreditadora_edit": autocomplete.ModelSelect2(
            #     url="oeuacademic:acreditadora",
            #     attrs={
            #         "class": "form-control",
            #         "data-placeholder": "Institución Acreditadora",
            #     },
            # ),
            "mercado_ocupacional_edit": CKEditorWidget(),
            "area_conocimiento_edit": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width:100%",
                    "data-placeholder": "Área de Conocimiento...",
                }
            ),
            "sub_area_conocimiento_edit": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width:100%",
                    "data-placeholder": "Sub Área de Conocimiento...",
                }
            ),
            # "titulo_edit": autocomplete.ModelSelect2(
            #     url="oeuacademic:titulo",
            #     attrs={
            #         "class": "form-control select2",
            #         "data-placeholder": "Titulo de egreso",
            #     },
            # ),
            "periodicidad_edit": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width:100%",
                    "data-placeholder": "Periodicidad...",
                }
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
            "prioritaria_edit": forms.CheckboxInput(),
            "cod_activacion": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        """Inicializa la clase en modo consulta de registro este pueda colocar
        el campo localidad_edit como no editable, esto se hace para que dicho
        registro no pueda ser manipulado
        """
        self.filtro = kwargs.pop("filtro", None)
        super(CarreraPreGradoForm, self).__init__(*args, **kwargs)
        self.fields[
            "sub_area_conocimiento_edit"
        ].queryset = SubAreaConocimiento.objects.none()
        if self.instance.pk:
            del self.fields["localidad_edit"]
        else:

            if self.filtro:
                self.fields["localidad_edit"].queryset = Localidad.objects.filter(
                    id=self.filtro
                )
            else:
                self.fields["localidad_edit"].queryset = Localidad.objects.all()

        if "sub_area_conocimiento_edit" in self.data:
            try:
                area_conocimiento_edit = int(self.data.get("area_conocimiento_edit"))
                self.fields[
                    "sub_area_conocimiento_edit"
                ].queryset = SubAreaConocimiento.objects.filter(
                    area_conocimiento=area_conocimiento_edit
                ).order_by(
                    "nombre"
                )
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields[
                "sub_area_conocimiento_edit"
            ].queryset = self.instance.area_conocimiento_edit.areaConocimiento4.order_by(
                "nombre"
            )


##############################################################################
"""FormSet ajustado para ser manipulado en el formulario de las carreras
de pre grado o programas academicos
"""
SFC_CARRERA_FORMSET = inlineformset_factory(
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


class BaseProductFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields[DELETION_FIELD_NAME].label = ""
        form.fields[DELETION_FIELD_NAME].widget = forms.HiddenInput(
            attrs={"value": "false"},
        )


##############################################################################
"""FormSet para asociar los titulos a los programas academicos de pregrado
"""

TITULO_FORMSET = inlineformset_factory(
    Carrera,
    CarreraTituloEdit,
    fields=["titulo", "duracion"],
    widgets={
        "titulo": autocomplete.ModelSelect2(
            url="oeuacademic:titulo",
            attrs={
                "class": "form-control formset-select2",
                "style": "width:100%",
                "data-placeholder": "Titulo de egreso",
            },
        ),
        "duracion": forms.NumberInput(attrs={"class": "form-control"},),
    },
    formset=BaseProductFormSet,
    extra=0,
    can_delete=True,
)
