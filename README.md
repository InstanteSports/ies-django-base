IES Django Base
=============

IES Django base is a set of helper functions that can be implemented in a
project to add certain functionality to your app.

Quick start
-----------

1. Install ies-base from pip with this line
    ```
    pip install -e git+https://github.com/InstanteSports/ies-django-base.git#egg=ies_django_base-master
    ```
2. Add "ies-base" to your INSTALLED_APPS setting like this

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
flag. If this flag is True, then the auto_save function will avoid overwriting 
the content of the field.
When running an automatic parse, use the auto_save() function rather than
the save function.


###FollowableModel

Followable models allow you to create "followables" for your project. To use 
followables, you must subclass your model with FollowableModel, and override 
the abstract method get_following_information().

get_following_information -
Takes an object and returns the information for following that item

GAME_ENUM:
- NONE = 0
- LEAGUE_OF_LEGENDS = 1
- DOTA2 = 2

TYPE_ENUM:
- PLAYER = 0
- TEAM = 1
- ORGANIZATION = 2
- SERIES = 3
- TOURNAMENT = 4

:return:  
{  
    "game": INTEGER based on ENUM above  
    "type": Integer based on ENUM above  
    "name": Display name  
    "object_id": ID of the object on the other end  
    "thumbnail_url": Absolute URL of the thumbnail for this followable  
}  


```python
from django.db import models
from ies_base.models import FollowableModel
class Player(FollowableModel):
    ign = models.CharField(max_length=40)
    player_id = models.IntegerField(unique=True)
    def get_following_information(self):
        return {
            "game": 1,
            "type": 0,
            "name": self.ign,
            "object_id": self.player_id,
            "thumbnail_url": "http://ies-cdn.net/static/player/player" + str(self.player_id) + ".jpg"
        }
```

To output the followables in a URL format, add the AllFollowablesView to your urls.
```python
from ies_base.views import AllFollowablesView
url(r'^followables/$', AllFollowablesView.as_view())
```

###TaggableModel

Taggable models allow you to create news tags for your project. To use 
tags, you must subclass your model with TaggableModel, and override 
the abstract method get_tags().

get_tags -
Takes an object, and returns its tags. MUST be implemented to take advantage of automatic tagging
:return:
{
    "name": Name of the tag
    "related_tags": Related things to tag (list)
    "equivalent_names": Names that are the same (TSM = Team Solo Mid) (list)
}


```python
from django.db import models
from ies_base.models import Taggable 
class Player(TaggableModel):
    ign = models.CharField(max_length=40)
    name = models.CharField(max_length=200)
    team = models.ForeignKey(null=True, blank=True)
    def get_tags(self):
        return {
            "name" : self.ign,
            "related_tags" : [self.team, ],
            "equivalent_names" : [self.name, ],
        }
```

To output the followables in a URL format, add the AllTagsView to your urls.
```python
from ies_base.views import AllTagsView
url(r'^followables/$', AllTagsView.as_view())
```

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