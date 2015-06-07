from django_filters import Filter
from django_filters.fields import Lookup
from django.db.models import Q


class ListFilter(Filter):
    def filter(self, qs, value):
        return super(ListFilter, self).filter(qs, Lookup(value.split(u","), "in"))


class MultipleFieldListFilter(Filter):
    def __init__(self, combiner="OR", *args, **kwargs):
        self.combiner = combiner
        super(MultipleFieldListFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        value = value.split(u",")
        if not value:
            return qs
        q = Q()
        for name in self.name.split(','):
            for v in value:
                if self.combiner == "OR":
                    q |= Q(**{name: v})
                else:
                    q &= Q(**{name: v})
        return qs.filter(q).distinct()