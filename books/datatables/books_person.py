# Django Libraries
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

# Thirdparty Libraries
from books.models import BooksPerson, BooksPublicacion
from books.serializers import BooksPersonSerializer
from globales.helpers import CustomPagination, set_if_not_none
from rest_framework import status, viewsets
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# #################################################################################### #
class BooksPersonViewSet(viewsets.ModelViewSet):

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = [AllowAny]
    serializer_class = BooksPersonSerializer
    model = BooksPerson
    queryset = model.objects.all()

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_cookie)
    def list(self, request):
        filters_kwargs = {}

        queryset = self.filter_queryset(self.get_queryset())

        object_id = self.request.query_params.get("id", None)
        name = self.request.query_params.get("name", None)

        set_if_not_none(
            filters_kwargs, "pk__in", object_id.split(",") if object_id else None
        )
        set_if_not_none(filters_kwargs, "name__icontains", name)
        set_if_not_none(filters_kwargs, "other_name__icontains", name)
        set_if_not_none(filters_kwargs, "last_name__icontains", name)
        set_if_not_none(filters_kwargs, "other_last_name__icontains", name)

        queryset = queryset.filter(**filters_kwargs)

        self.pagination_class = CustomPagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request):
        to_delete = self.get_object()
        relacionado = BooksPublicacion.objects.filter(person=to_delete).exists()

        if relacionado:
            msg = {
                "msg": _(
                    "No se puede eliminar esta persona porque una publicación depende de ella"
                )
            }

            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(to_delete)
        msg = {"msg": _("Registro eliminado exitosamente")}

        return Response(msg, status=status.HTTP_204_NO_CONTENT)
