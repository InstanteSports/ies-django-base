from django.db import models
from django.db.models.fields.related import ManyToOneRel, AutoField


# Create your models here.
class ManualUpdateModel(models.Model):
    class Meta:
        abstract = True

    def auto_save(self):
        updated_fields = []
        for field in type(self)._meta.get_fields():
            if (not field.name.startswith("m_") and
                    not isinstance(field, ManyToOneRel) and
                    not isinstance(field, AutoField)):
                try:
                    if not getattr(self, "m_" + field.name):
                        updated_fields.append(field.name)
                except AttributeError:
                    updated_fields.append(field.name)
        try:
            return self.save(update_fields=updated_fields)
        except ValueError:
            return self.save()


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

    NONE = 0
    LEAGUE_OF_LEGENDS = 1
    DOTA2 = 2


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