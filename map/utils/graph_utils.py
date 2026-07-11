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

#--------------------------------------------------------------------------------------------

def find_shortest_routes_by_type(graph, type_name, type_content):
    """
    Находит кратчайшие маршруты между зданиями, которые соответствуют выбранному Type и Object name.
    """
    # Находим все здания, которые соответствуют выбранному Type и Object name

    print(type_name)
    print(type_content)


    link_objects = Link.objects.filter(specific=type_name, link_name=type_content)

    edge_ids = link_objects.values_list('connection', flat=True)

    unique_nodes = set()

    for edge in Edge.objects.filter(id__in=edge_ids):
        unique_nodes.add(edge.source_id)  # Добавляем source
        unique_nodes.add(edge.target_id)  # Добавляем target

    # Преобразуем множество в список
    node_ids = list(unique_nodes)

    roads_geojson = 'map/utils/roads_drive_spb.geojson'  # Путь к GeoJSON с дорогами
    road_graph = create_road_graph(roads_geojson)

    # Получаем координаты домов
    nodes = Node.objects.filter(id__in=node_ids)

    # Сопоставляем дома с ближайшими вершинами графа
    node_to_graph_node = {}
    for node in nodes:
        if node.geom:
            point = (node.geom.centroid.x, node.geom.centroid.y)  # Центр полигона здания
            nearest_node = find_nearest_node(road_graph, point)
            node_to_graph_node[node.id] = nearest_node

    # Находим кратчайшие маршруты между всеми парами домов
    routes = []
    node_object = []
    if len(node_ids) > 1:
        for i in range(1, len(node_ids)):
            source_id = node_ids[i-1]
            target_id = node_ids[i]

            # Получаем ближайшие вершины графа для source и target
            source_node = node_to_graph_node.get(source_id)
            target_node = node_to_graph_node.get(target_id)

            if source_node and target_node:
                # Находим кратчайший путь
                path = find_shortest_path(road_graph, source_node, target_node)
                if path:
                    routes.append({
                        'source': source_id,
                        'target': target_id,
                        'path': path,
                    })

    elif len(node_ids) == 0:
        node_object = Object_house.objects.get(object_type=type_name, object_name=type_content).build
        print(node_object)

    else:
        source_id = node_ids[0]
        target_id = node_ids[0]

        source_node = node_to_graph_node.get(source_id)
        target_node = node_to_graph_node.get(target_id)

        if source_node and target_node:
            # Находим кратчайший путь
            path = find_shortest_path(road_graph, source_node, target_node)
            if path:
                routes.append({
                    'source': source_id,
                    'target': target_id,
                    'path': path,
                })

    return node_object, node_ids, routes