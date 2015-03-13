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