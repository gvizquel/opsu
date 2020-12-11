# Thirdparty Libraries
from books.models import BooksCategoria
from books.serializers import BooksBaseSerializer


# #################################################################################### #
class BooksCategoriaSerializer(BooksBaseSerializer):
    class Meta:
        model = BooksCategoria
        fields = ["name", "description"]
