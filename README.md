IES Django Base
=============

IES Django base is a set of helper functions that can be implemented in a
project to add certain functionality to your app.

Quick start
-----------

1. Add "ies-base" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'ies_base',
    )
    
Utility Models
--------------

###ManualUpdateModel

Manual Update models allow for a custom "Auto save" function for parsers that
allows for custom field updating by parsers. Below is an example

```python
from ies_base.models import ManualUpdateModel
class Player(ManualUpdateModel):
    ign = models.CharField(max_length=40)
    m_ign = models.BooleanField(default=False)
def parse_player(ign):
    player, created = Player.objects.get_or_create(ign=ign)
    player.auto_save()
```

This will create a player, with a single ign field, and a "manual ign" boolean
flag. When running an automatic parse, use the auto_save() function rather than
the save function.

###ListFilter

The ListFilter allows you to filter a field using comma-separated arguments, 
for example ?tags=TSM,CLG. This performs a SQL "IN" query

```python
from ies_base.filters import ListFilter
import django_filters
class NewsEntryFiterSet(django_filters.FilterSet):
    tag = ListFilter(name="tags__name")
```

###MultipleFieldListFilter

The MultipleFieldListFilter allows you to filter multiple fields with the same 
arguments (comma-separated), syntax is same as ListFilter. This performs a SQL 
"OR" query

```
from ies_base.filters import MultipleFieldListFilter
import django_filters
class MatchFilter(django_filters.FilterSet):
    team = MultipleFieldListFilter(name="blue_team__tag,red_team__tag")
```