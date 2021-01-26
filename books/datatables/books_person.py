# Django Libraries
from django.db.models import Q

# Thirdparty Libraries
from books.models import BooksPerson
from django_datatables_view.base_datatable_view import BaseDatatableView


class BooksPersonDatatable(BaseDatatableView):
    model = BooksPerson
    columns = [
        "full_name",
        "name",
        "other_name",
        "last_name",
        "other_last_name",
        "pais_nacimiento",
        "botones",
    ]

    def filter_queryset(self, qs):
        """ If search['value'] is provided then filter all searchable columns using filter_method (istartswith
            by default).

            Automatic filtering only works for Datatables 1.10+. For older versions override this method
        """
        # columns = self._columns
        if not self.pre_camel_case_notation:
            # get global search value
            search = self._querydict.get("search[value]", None)
            pais_id = self.request.GET.get("pais_id", None)
            if search:
                qs = qs.filter(
                    Q(name__icontains=search)
                    | Q(other_name__icontains=search)
                    | Q(last_name__icontains=search)
                    | Q(other_last_name__icontains=search)
                    | Q(pais_nacimiento__nombre__icontains=search)
                )
            if pais_id:
                qs = qs.filter(pais_nacimiento__pk=pais_id)
        return qs

    def render_column(self, row, column):
        """ Renders a column on a row. column can be given in a module notation eg. document.invoice.type
        """

        if column == "botones":
            obj = {
                "id": row.id,
                "name": row.name if row.name else "-",
                "other_name": row.other_name if row.other_name else "-",
                "last_name": row.last_name if row.last_name else "-",
                "other_last_name": row.other_last_name if row.other_last_name else "-",
            }
            boton = """ <a
                        class="btn btn-default btn-xs"
                        title="Detalle de"
                        onclick="detail({})">
                            <i class="fa fa-eye"></i>
                        </a> """.format(
                obj
            )
            return boton

        return super().render_column(row, column)
