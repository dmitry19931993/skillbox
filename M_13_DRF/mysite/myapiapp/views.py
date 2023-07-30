from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from .serializers import GroupSelializer

@api_view()
def hello_world_view(request: Request)-> Response:
    return Response({"message": "Hello World"})

class GroupsListView(ListModelMixin, GenericAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSelializer
    def get(self, request: Request) -> Response:
        return self.list(request)