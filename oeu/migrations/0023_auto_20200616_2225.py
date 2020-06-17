# Generated by Django 2.2.13 on 2020-06-17 02:25

# Django Libraries
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oeu", "0022_auto_20200613_1434"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carrera",
            name="titulo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="oeuconfig.Titulo",
            ),
        ),
        migrations.AlterField(
            model_name="carrera",
            name="titulo_edit",
            field=models.ForeignKey(
                blank=True,
                db_column="titulo_edit",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="titulo",
                to="oeuconfig.Titulo",
            ),
        ),
    ]