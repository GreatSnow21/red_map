from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString

class Node(models.Model):
    """ Вершина графа, представляет здание с его границами """
    name = models.CharField(max_length=255, null=False, default="Unnamed Node")
    geom = models.PolygonField(srid=4326)  # Хранение контура здания
    status_active = models.BooleanField(default=True)  # Активен ли объект
    date_build = models.DateField(null=True, blank=True)  # Дата постройки
    description = models.TextField(default="Описание отсутствует")  # Описание здания
    def __str__(self):
        return self.name

class Edge(models.Model):
    """ Дуга графа, соединяет здания """
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='edges_from')
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='edges_to')
    geom_way = models.LineStringField(srid=4326, default=LineString())  # Геометрия линии связи

    def __str__(self):
        return f"{self.source.name} <-> {self.target.name}"


class Type(models.Model):
    """ Типы объектов, связанных с домами """
    type = models.CharField(max_length=255, primary_key=True)  # Уникальный тип связи
    type_description = models.TextField(default="Описание отсутствует")
    def __str__(self):
        return f"{self.type}"

class Object_house(models.Model):
    """ Карточка объекта, принадлежащего зданию """
    build = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='house')
    object_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='object_types')
    object_name = models.CharField(max_length=255)
    object_date = models.DateField(null=True, blank=True)
    object_description = models.TextField(default="Описание отсутствует")
    def __str__(self):
        return f"{self.build.name} ({self.object_type.type} - {self.object_name})"

class Link(models.Model):
    """ Связь на дуге (возможно, избыточная таблица) """
    connection = models.ForeignKey(Edge, on_delete=models.CASCADE, related_name='links')
    specific = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='specific_links')
    link_name = models.ForeignKey(Object_house, on_delete=models.SET_NULL, null=True,  blank=True)
    link_description = models.TextField(default="Описание отсутствует")

    def __str__(self):
        return f"{self.connection.source.name} -> {self.connection.target.name} ({self.specific.type_name})"



