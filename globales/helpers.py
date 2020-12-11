# Standard Libraries
import math

# Thirdparty Libraries
from rest_framework import pagination
from rest_framework.response import Response


def set_if_not_none(mapping, key, value):
    """ Esta función agrega valores a los kwargs de filtrado de una consulta del ORM,
    Siempre y cuando estos valores sean distintos de None y distintos de vacio
    """

    if isinstance(value, (bool, int, float, str)):
        mapping[key] = value


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "countItemsOnPage": self.page_size,
                "page": self.page.number,
                "totalPages": math.ceil(self.page.paginator.count / self.page_size),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
