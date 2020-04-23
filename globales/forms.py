# Standard Libraries
import re

# Django Libraries
from django import forms
from django.forms import ModelForm

# Thirdparty Libraries
from globales.models import InstitucionMinisterial


class InstitucionMinisterialForm(ModelForm):
    """
    Formulario ajustado para manipular las instituciones ministeriales
    """

    class Meta:
        model = InstitucionMinisterial
        fields = ("nombre", "siglas", "rif", "dep_admin", "tipo_institucion")

        labels = {
            "nombre": "Nombre de la Institución",
            "siglas": "Siglas de la Institución",
            "rif": "R.I.F de la Institución",
            "dep_admin": "Dependencia Administrativa",
            "tipo_institucion": "Tipo de Institución",
        }

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escriba el Nombre completo de la Institución Ministerial",
                    "minlength": "30",
                    "maxlength": "100",
                }
            ),
            "siglas": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escriba en Siglas el Nombre de la Institución Ministerial",
                    "minlength": "4",
                    "maxlength": "50",
                }
            ),
            "rif": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escriba el R.I.F incluyendo la letra G ó J",
                }
            ),
            "dep_admin": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Selecciona la dependencia administrativa",
                }
            ),
            "tipo_institucion": forms.Select(attrs={"class": "form-control select2"}),
        }

    def clean(self):
        diccionario_limpio = super(InstitucionMinisterialForm, self).clean()
        rif = diccionario_limpio.get("rif")

        ## validamos que el R.I.F. tenga la forma G-99999999-9
        reg_rif = re.compile("^[G,J]\-\d{5,8}\-\d{1}$")
        if reg_rif.match(rif) is None:
            self.add_error(
                "rif",
                "El R.I.F. debe comenzar por la letra 'G u J'\
                seguido de un guión + ocho números + el último número \
                separdo por un guión, complete los caracteres del R.I.F.",
            )
