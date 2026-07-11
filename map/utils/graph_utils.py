import networkx as nx
import geopandas as gpd
import math
from community import community_louvain
from map.models import Node, Edge, Link, Object_house

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

# -----------------------------------------------------------------------------

def build_combined_graph():
    """
    Создаёт граф домов на основе существующих связей (Edge), общих типов и характеристик связей (Link).
    """
    graph = nx.Graph()

    # Добавляем вершины (дома)
    nodes = Node.objects.all()
    for node in nodes:
        graph.add_node(node.id, pos=(node.geom.centroid.x, node.geom.centroid.y))

    # Создаём словарь для хранения типов каждого дома
    house_types = {}
    for obj in Object_house.objects.all():
        if obj.build.id not in house_types:
            house_types[obj.build.id] = set()
        house_types[obj.build.id].add(obj.object_type.type)

    # Добавляем рёбра на основе существующих связей (Edge)
    for edge in Edge.objects.all():
        source_id = edge.source.id
        target_id = edge.target.id

        # Вычисляем вес ребра на основе характеристик связей (Link)
        link_weight = Link.objects.filter(connection=edge).count()  # Количество характеристик связи

        # Вычисляем вес ребра на основе общих типов
        common_types = house_types.get(source_id, set()) & house_types.get(target_id, set())
        type_weight = len(common_types)

        # Общий вес ребра
        weight = link_weight + type_weight

        # Добавляем ребро в граф
        graph.add_edge(source_id, target_id, weight=weight)

    return graph

def detect_communities(graph):
    """
    Выполняет кластеризацию графа с использованием алгоритма Лувена.
    Возвращает словарь, где ключи — это узлы, а значения — их кластеры.
    """
    partition = community_louvain.best_partition(graph)
    return partition

#----------------------------------------------------------------------------------------

def build_graph():
    """
    Создаёт граф домов с весами рёбер на основе количества связей и общих характеристик.
    """
    # Инициализируем граф
    graph = nx.Graph()

    # Добавляем узлы (дома)
    for node in Node.objects.all():
        graph.add_node(node.id, name=node.name)

    # Создаём словарь для хранения типов объектов каждого дома
    house_types = {}
    for obj in Object_house.objects.all():
        if obj.build.id not in house_types:
            house_types[obj.build.id] = set()
        house_types[obj.build.id].add(obj.object_type.type)

    # Добавляем рёбра (связи между домами) с весами
    for edge in Edge.objects.all():
        source_id = edge.source.id
        target_id = edge.target.id

        # 1. Вес на основе количества характеристик связи (Link)
        link_weight = Link.objects.filter(connection=edge).count()

        # 2. Вес на основе общих типов объектов (Object_house)
        common_types = house_types.get(source_id, set()) & house_types.get(target_id, set())
        type_weight = len(common_types)

        # Общий вес ребра (можно настроить формулу)
        weight = link_weight + type_weight

        # Добавляем ребро в граф
        graph.add_edge(source_id, target_id, weight=weight)

    return graph

def calculate_pagerank(graph):
    pagerank_scores = nx.pagerank(graph, weight='weight')  # Учитываем вес рёбер
    return pagerank_scores

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