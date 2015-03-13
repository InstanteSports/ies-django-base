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
        Takes a model, and returns its tags. MUST be implemented to take advantage of automatic tagging
        :return: Tuple with 2 elements, Element 0 is the name of the tag and Element 1 is a List/Tuple with strings of
        possible tags
        """
        raise NotImplementedError
