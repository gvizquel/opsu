# Generated by Django 2.2.11 on 2020-04-30 01:27

# Django Libraries
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oeu", "0018_auto_20200415_0026"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="carrera",
            options={
                "ordering": [
                    "localidad__ieu__institucion_ministerial__nombre",
                    "localidad",
                    "area_conocimiento",
                    "sub_area_conocimiento",
                    "nombre",
                ],
                "verbose_name": "Programa Académico",
                "verbose_name_plural": "Programas Académicos",
            },
        ),
        migrations.AlterModelOptions(
            name="tipoespecificoinstitucion",
            options={
                "ordering": ["tipo_ieu__nombre", "sub_tipo_ieu__nombre", "nombre"],
                "verbose_name": "Tipo IEU Específico",
                "verbose_name_plural": "Tipos IEU Específicos",
            },
        ),
        migrations.RenameField(
            model_name="carrerarevisor", old_name="carrera_pre", new_name="carrera",
        ),
        migrations.RenameField(
            model_name="carrerarevisoredit", old_name="carrera_pre", new_name="carrera",
        ),
        migrations.RenameField(
            model_name="carrerasfc", old_name="carrera_pre", new_name="carrera",
        ),
        migrations.AlterField(
            model_name="carrera",
            name="revisor",
            field=models.ManyToManyField(
                related_name="revisor_carrera_publicado",
                through="oeu.CarreraRevisor",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="carrera",
            name="revisor_edit",
            field=models.ManyToManyField(
                related_name="revisores_carrera_edit",
                through="oeu.CarreraRevisorEdit",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
