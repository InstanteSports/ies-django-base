from rest_framework import serializers


class Tag(object):
    def __init__(self, name, related_tags, equivalent_names):
        self.name = name
        self.related_tags = related_tags
        self.equivalent_names = equivalent_names


class TagSerializer(serializers.Serializer):
    name = serializers.CharField()
    related_tags = serializers.ListField(child=serializers.CharField(), allow_null=True)
    equivalent_names = serializers.ListField(child=serializers.CharField(), allow_null=True)

    def create(self, validated_data):
        return Tag(**validated_data)


class Followable(object):
    def __init__(self, name, type, game, object_id, thumbnail_url="", **kwargs):
        self.name = name
        self.type = type
        self.game = game
        self.object_id = object_id
        self.thumbnail_url = thumbnail_url
        for field, value in kwargs.items():
            setattr(self, field, value)


class FollowableSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.IntegerField()
    game = serializers.IntegerField()
    object_id = serializers.IntegerField()
    default_color = serializers.CharField(allow_null=True, allow_blank=True)
    thumbnail_url = serializers.CharField(allow_blank=True, allow_null=True)

    def create(self, validated_data):
        return Followable(**validated_data)
