from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Node, Edge, Type, Content_type, Object_house, Link
from .serializers import NodeSerializer, EdgeSerializer, TypeSerializer, Content_typeSerializer, Object_houseSerializer, LinkSerializer

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
class EdgeViewSet(viewsets.ModelViewSet):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer
class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
class Content_typeViewSet(viewsets.ModelViewSet):
    queryset = Content_type.objects.all()
    serializer_class = Content_typeSerializer
class Object_houseViewSet(viewsets.ModelViewSet):
    queryset = Object_house.objects.all()
    serializer_class = Object_houseSerializer
class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
