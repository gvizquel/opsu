# Generated by Django 2.2.13 on 2020-07-04 01:14

# Django Libraries
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oeuconfig", "0004_auto_20200619_0015"),
    ]

    operations = [
        migrations.AlterField(
            model_name="titulo",
            name="nombre",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]