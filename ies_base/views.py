from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from models import TaggableModel
from django.contrib.contenttypes.models import ContentType
from serializers import TagSerializer

# Create your views here.
class AllTagsView(APIView):
    """
    Returns a list of all tags in this project
    """
    def get(self, request, *args, **kwargs):
        out_list = []
        for ct in ContentType.objects.all():
            model = ct.model_class()
            if model and isinstance(model(), TaggableModel):
                for item in model.objects.all():
                    t = TagSerializer(data=item.get_tags())
                    if t.is_valid():
                        out_list.append(t.save())
                    else:
                        print t.errors
        return Response(TagSerializer(out_list, many=True).data)