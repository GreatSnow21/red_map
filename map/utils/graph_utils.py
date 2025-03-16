import networkx as nx
import geopandas as gpd
import math
from map.models import Node, Edge

def create_road_graph(roads_geojson):
    # Загружаем данные о дорогах
    roads = gpd.read_file('map/utils/roads_drive_spb.geojson')

    # Создаём граф
    graph = nx.Graph()

    # Добавляем вершины и рёбра
    for _, road in roads.iterrows():
        coords = list(road.geometry.coords)
        for i in range(len(coords) - 1):
            start = coords[i]
            end = coords[i + 1]
            distance = ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5  # Евклидово расстояние
            graph.add_edge(start, end, weight=distance)

    return graph

def find_shortest_path(graph, start, end):
    try:
        path = nx.astar_path(graph, start, end, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None


def find_nearest_node(graph, point):
    """
    Находит ближайшую вершину графа к заданной точке.
    """
    nearest_node = None
    min_distance = float('inf')

    for node in graph.nodes:
        distance = math.sqrt((node[0] - point[0]) ** 2 + (node[1] - point[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            nearest_node = node

    return nearest_node

# def build_graph():
#     # Создаём граф
#     graph = nx.Graph()
#
#     # Добавляем вершины (Nodes)
#     nodes = Node.objects.all()
#     for node in nodes:
#         graph.add_node(node.id, pos=(node.geom.centroid.x, node.geom.centroid.y))  # Используем центр полигона как координаты
#
#     # Добавляем рёбра (Edges)
#     edges = Edge.objects.all()
#     for edge in edges:
#         # Вычисляем вес ребра (например, расстояние между source и target)
#         source_node = Node.objects.get(id=edge.source.id)
#         target_node = Node.objects.get(id=edge.target.id)
#         weight = source_node.geom.distance(target_node.geom)  # Расстояние между объектами
#         graph.add_edge(edge.source.id, edge.target.id, weight=weight)
#
#     return graph

# def find_shortest_path(graph, start_node_id, end_node_id):
#     try:
#         path = nx.astar_path(graph, start_node_id, end_node_id, weight='weight')
#         print("Найден путь:", path)  # Отладочная информация
#         return path
#     except nx.NetworkXNoPath:
#         print("Путь не найден")  # Отладочная информация
#         return None