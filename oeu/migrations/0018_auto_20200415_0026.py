# Generated by Django 2.2.11 on 2020-04-15 04:26

# Django Libraries
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("oeu", "0017_auto_20200414_2320"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="carrera",
            options={
                "ordering": ["ieu__nombre", "nombre"],
                "verbose_name": "Programa Académico",
                "verbose_name_plural": "Programas Académicos",
            },
        ),
    ]
