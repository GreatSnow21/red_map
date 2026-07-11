from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString
from django.core.validators import MinValueValidator, MaxValueValidator

class Node(models.Model):
    """ Вершина графа, представляет здание с его границами """
    name = models.CharField(max_length=255, null=False, default="Unnamed Node")
    geom = models.PolygonField(srid=4326)  # Хранение контура здания
    status_active = models.BooleanField(default=True)  # Активен ли объект
    date_build = models.IntegerField("Год", validators=[
        MinValueValidator(1500),  # Минимальный год
        MaxValueValidator(2100)   # Максимальный год
    ], blank=True, null=True) # Дата постройки
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
    type = models.CharField(max_length=255, primary_key=True)
    type_description = models.TextField(default="Описание отсутствует")
    def __str__(self):
        return f"{self.type}"

class Content_type(models.Model):
    """Содержание отдельного типа"""
    content_type_link = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type_from')
    content_type = models.CharField(max_length=255, primary_key=True)
    content_type_description = models.TextField(default="Описание отсутствует")

    def __str__(self):
        return f"{self.content_type}"


class Object_house(models.Model):
    """ Карточка объекта, принадлежащего зданию """
    build = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='house')
    object_type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='object_types')
    object_name = models.ForeignKey(Content_type, on_delete=models.CASCADE, related_name='object_content_type')
    object_date = models.IntegerField("Год", validators=[
        MinValueValidator(1500),  # Минимальный год
        MaxValueValidator(2100)   # Максимальный год
    ], blank=True, null=True)
    object_description = models.TextField(default="Описание отсутствует")
    def __str__(self):
        return f"{self.build.name} ({self.object_type.type} - {self.object_name})"

class Link(models.Model):
    """ Связь на дуге (возможно, избыточная таблица) """
    connection = models.ForeignKey(Edge, on_delete=models.CASCADE, related_name='links')
    specific = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='specific_links')
    link_name = models.ForeignKey(Content_type, on_delete=models.CASCADE, related_name='links_name')
    link_description = models.TextField(default="Описание отсутствует")

    def __str__(self):
        return f"{self.connection.source.name} -> {self.connection.target.name} ({self.specific.type})"



