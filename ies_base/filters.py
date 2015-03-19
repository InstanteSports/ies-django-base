from django_filters import Filter
from django_filters.fields import Lookup
from django.db.models import Q


class ListFilter(Filter):
    def filter(self, qs, value):
        return super(ListFilter, self).filter(qs, Lookup(value.split(u","), "in"))


class MultipleFieldListFilter(Filter):
    def filter(self, qs, value):
        value = value.split(u",")
        if not value:
            return qs
        q = Q()
        for name in self.name.split(','):
            for v in value:
                q |= Q(**{name: v})
        return qs.filter(q).distinct()