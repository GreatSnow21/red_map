from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Node, Edge

class NodeSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Node
        geo_field = "geom"
        fields = ("id", "name", "status_active", "date_build", "description")

class EdgeSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Edge
        geo_field = "geom_way"
        fields = ("id", "source", "target")
