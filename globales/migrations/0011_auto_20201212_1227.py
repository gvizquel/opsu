# Generated by Django 2.2.17 on 2020-12-12 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('globales', '0010_auto_20201206_1848'),
    ]

    sql_drop_constraint = """ALTER  TABLE  pais DROP CONSTRAINT  pais_pkey"""
    sql_rename_column = """ALTER  TABLE  pais RENAME COLUMN id_pais TO id"""
    sql_add_pkey = """ALTER  TABLE  pais ADD PRIMARY KEY (id)"""

    operations = [

        migrations.RunSQL(sql_drop_constraint),
        migrations.RunSQL(sql_rename_column),
        migrations.RunSQL(sql_add_pkey),

    ]
