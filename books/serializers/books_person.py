# Thirdparty Libraries
from books.models import BooksPerson
from books.serializers import BooksBaseSerializer


# #################################################################################### #
class BooksPersonSerializer(BooksBaseSerializer):
    class Meta:
        model = BooksPerson
        fields = [
            "name",
            "other_name",
            "last_name",
            "other_last_name",
            "birth_date",
            "pais_nacimiento",
            "fecha_defuncion",
            "pais_defuncion",
            "resumen_biografico",
            "foto",
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["pais_nacimiento"] = instance.pais_nacimiento
        rep["pais_defuncion"] = instance.pais_defuncion

        return rep
