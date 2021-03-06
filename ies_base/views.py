from rest_framework.views import APIView
from rest_framework.response import Response
from models import TaggableModel, FollowableModel
from django.contrib.contenttypes.models import ContentType
from serializers import TagSerializer, FollowableSerializer


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
                for item in model.objects.filter(taggable=True):
                    t = TagSerializer(data=item.get_tags())
                    if t.is_valid():
                        out_list.append(t.save())
                    else:
                        print t.errors
        return Response(TagSerializer(out_list, many=True).data)


class AllFollowablesView(APIView):
    """
    Returns a list of all followables in this project
    """
    def get(self, request, *args, **kwargs):
        out_list = []
        for ct in ContentType.objects.all():
            model = ct.model_class()
            if model and isinstance(model(), FollowableModel):
                for item in model.objects.filter(followable=True):
                    f = FollowableSerializer(data=item.get_following_information())
                    if f.is_valid():
                        out_list.append(f.save())
                    else:
                        print f.errors
        return Response(FollowableSerializer(out_list, many=True).data)
