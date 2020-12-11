# Thirdparty Libraries
from books.models import BooksPublicacion
from books.serializers import BooksBaseSerializer


# #################################################################################### #
class BooksPublicacionSerializer(BooksBaseSerializer):
    class Meta:
        model = BooksPublicacion
        fields = [
            "fecha_edicion",
            "autor",
            "edition_number",
            "editor",
            "editorial",
            "fecha_publicacion",
            "isbn",
            "issn",
            "pais_edicion",
            "numero",
            "titulo",
            "sub_titulo",
            "volumen",
            "resumen",
            "cantidad_paginas",
            "portada",
            "pdf",
            "categoria",
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["pais_edicion"] = instance.pais_edicion
        rep["autor"] = instance.autor
        rep["autor"] = instance.editor

        return rep
