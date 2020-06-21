# Generated by Django 2.2.13 on 2020-06-19 04:17

# Django Libraries
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oeu", "0028_auto_20200619_0017"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subareaconocimiento",
            name="area_conocimiento",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="areaConocimiento4",
                to="oeu.AreaConocimiento",
                verbose_name="Área de conocimiento",
            ),
        ),
    ]