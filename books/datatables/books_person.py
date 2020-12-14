from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView
from books.models import BooksPerson


class BooksPersonDatatable(BaseDatatableView):
    model = BooksPerson
    columns = [
        'name', 'other_name', 'last_name',
        'other_last_name', 'pais_nacimiento',
        'botones'
    ]

    def filter_queryset(self, qs):
        """ If search['value'] is provided then filter all searchable columns using filter_method (istartswith
            by default).

            Automatic filtering only works for Datatables 1.10+. For older versions override this method
        """
        columns = self._columns
        if not self.pre_camel_case_notation:
            # get global search value
            search = self._querydict.get('search[value]', None)
            filter_pais = self.request.GET.get('filter_pais', None)
            if search:
                qs = qs.filter(
                    Q(name__icontains=search)
                    | Q(other_name__icontains=search)
                    | Q(last_name__icontains=search)
                    | Q(other_last_name__icontains=search)
                    | Q(pais_nacimiento__nombre__icontains=search)
                    )
            if filter_pais:
                qs = qs.filter(pais_nacimiento__pk=filter_pais)
        return qs

    def render_column(self, row, column):
        """ Renders a column on a row. column can be given in a module notation eg. document.invoice.type
        """

        if column == 'botones':
            obj = {
                'id': row.id,
                'name': row.name if row.name else '-',
                'other_name': row.other_name if row.other_name else '-',
                'last_name': row.last_name if row.last_name else '-',
                'other_last_name': row.other_last_name if row.other_last_name else '-'
            }
            boton = """ <a
                        class="btn btn-sm btn-default"
                        title="Detalle de"
                        onclick="detail({})">
                            <i class="fa fa-eye"></i>
                        </a> """.format(obj)
            return boton

        return super().render_column(row, column)
