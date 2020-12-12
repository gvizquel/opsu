# Thirdparty Libraries
from books.models import BooksEditorial
from books.serializers import BooksBaseSerializer


# #################################################################################### #
class BooksEditorialSerializer(BooksBaseSerializer):
    class Meta:
        model = BooksEditorial
        fields = ["name", "direction"]
