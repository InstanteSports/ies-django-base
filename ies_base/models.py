from django.db import models
from django.db.models.fields.related import ManyToOneRel, AutoField, ManyToManyField, RelatedField
from django import VERSION


# Create your models here.
class ManualUpdateModel(models.Model):
    class Meta:
        abstract = True

    def auto_save(self, force_insert=False, force_update=False):
        updated_fields = []

        if VERSION >= (1, 8 ,0, '', 0):
            for field in type(self)._meta.get_fields():
                if (not field.name.startswith("m_") and
                        not isinstance(field, ManyToOneRel) and
                        not isinstance(field, AutoField) and
                        not isinstance(field, ManyToManyField)):
                    try:
                        if not getattr(self, "m_" + field.name):
                            updated_fields.append(field.name)
                    except AttributeError:
                        updated_fields.append(field.name)
        else:
            for field in type(self)._meta.fields:
                if (not field.name.startswith("m_") and
                        not isinstance(field, models.ManyToManyField) and
                        not isinstance(field, models.AutoField)):
                    try:
                        if not getattr(self, "m_" + field.name):
                            updated_fields.append(field.name)
                    except AttributeError as e:
                        updated_fields.append(field.name)
        try:
            return self.save(update_fields=updated_fields, force_insert=force_insert, force_update=force_update)
        except ValueError as e:
            return self.save(force_insert=force_insert, force_update=force_update)


class TaggableModel(models.Model):
    taggable = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def get_tags(self):
        """
        Takes an object, and returns its tags. MUST be implemented to take advantage of automatic tagging
        :return:
        {
            "name": Name of the tag
            "related_tags": Related things to tag
            "equivalent_names": Names that are the same (TSM = Team Solo Mid)
        }
        """
        raise NotImplementedError


class FollowableModel(models.Model):
    PLAYER = 0
    TEAM = 1
    ORGANIZATION = 2
    SERIES = 3
    TOURNAMENT = 4
    GAME_CHARACTER = 5
    REGION = 6

    NONE = 0
    LEAGUE_OF_LEGENDS = 1
    DOTA2 = 2
    HEARTHSTONE = 3
    CSGO = 4

    TYPE_CHOICES = (
        (PLAYER, "PLAYER"),
        (TEAM, "TEAM"),
        (ORGANIZATION, "ORGANIZATION"),
        (SERIES, "SERIES"),
        (TOURNAMENT, "TOURNAMENT"),
        (GAME_CHARACTER, "GAME_CHARACTER"),
        (REGION, "REGION"),
    )

    GAME_CHOICES = (
        (NONE, "NONE"),
        (LEAGUE_OF_LEGENDS, "LEAGUE OF LEGENDS"),
        (DOTA2, "DOTA2"),
        (HEARTHSTONE, "HEARTHSTONE"),
        (CSGO, "CS:GO")
    )

    followable = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def get_following_information(self):
        """
        Takes an object and returns the information for following that item

        GAME_ENUM:
            NONE = 0
            LEAGUE_OF_LEGENDS = 1
            DOTA2 = 2

        TYPE_ENUM:
            PLAYER = 0
            TEAM = 1
            ORGANIZATION = 2
            SERIES = 3
            TOURNAMENT = 4

        :return:
        {
            "game": INTEGER based on ENUM above
            "type": Integer based on ENUM above
            "name": Display name
            "object_id": ID of the object on the other end
            "thumbnail_url": Absolute URL of the thumbnail for this followable
        }
        """
        raise NotImplementedError
