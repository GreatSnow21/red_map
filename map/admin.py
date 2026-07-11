from django.contrib import admin
from .models import Node, Edge, Type, Content_type, Link, Object_house
from django.contrib import admin
from django.contrib.gis import forms
from leaflet.admin import LeafletGeoAdmin


class NodeAdmin(LeafletGeoAdmin):  # Используем Leaflet
    pass

class EdgeAdmin(LeafletGeoAdmin):  # Используем Leaflet
    pass

class TypeAdmin(LeafletGeoAdmin):  # Используем Leaflet
    pass

class Content_typeAdmin(LeafletGeoAdmin):  # Используем Leaflet
    pass

class LinkAdmin(LeafletGeoAdmin):  # Используем Leaflet
    pass

class Object_houseAdmin(LeafletGeoAdmin):  # Используем Leaflet
    pass

admin.site.register(Node, NodeAdmin)
admin.site.register(Edge, EdgeAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Content_type, Content_typeAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Object_house, Object_houseAdmin)
