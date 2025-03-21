from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Node, Edge, Type, Content_type, Object_house, Link

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
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ("type", "type_description")
class Content_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content_type
        fields = ("content_type_link", "content_type", "content_type_description")
class Object_houseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object_house
        fields = (
            "id",
            "build",
            "object_type",
            "object_name",
            "object_date",
            "object_description",
        )

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = (
            "id",
            "connection",
            "specific",
            "link_name",
            "link_description",
        )

