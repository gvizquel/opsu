# Generated by Django 2.2.13 on 2020-12-06 22:48

# Django Libraries
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("globales", "0009_auto_20200621_1803"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="municipio", options={"ordering": ["nombre"]},
        ),
        migrations.AlterModelOptions(
            name="parroquia", options={"ordering": ["nombre"]},
        ),
    ]
