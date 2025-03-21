from django.shortcuts import render
from .forms import RouteForm, RouteByTypeForm
from .utils.graph_utils import create_road_graph, find_shortest_path, find_nearest_node, build_combined_graph, detect_communities, build_graph, calculate_pagerank, find_shortest_routes_by_type
from .serializers import NodeSerializer, TypeSerializer
from .models import Node, Type, Object_house
from django.http import JsonResponse
import json

ROADS_GEOJSON = "roads_drive_spb.geojson"


def map_view(request):
    communities = None
    nodes_data = []
    nodes_data_pr = []
    pagerank_scores = None

    if request.method == 'POST':
        if 'detect_communities' in request.POST:  # Если нажата кнопка "Кластеризация Лувена"

                # Логика для кластеризации

                graph = build_combined_graph()
                communities = detect_communities(graph)

                # Получаем данные о зданиях (узлах) для визуализации

                for node in Node.objects.all():

                    # Преобразуем координаты из кортежей в списки
                    geom_coords = [[y, x] for x, y in node.geom.coords[0]]
                    nodes_data.append({
                        'id': node.id,
                        'name': node.name,
                        'geom': geom_coords,
                        'community': communities.get(node.id, -1)  # Номер сообщества
                    })

        elif 'calculate_pagerank' in request.POST:  # Если нажата кнопка "PageRank"
            # Логика для вычисления PageRank
            graph = build_graph()
            pagerank_scores = calculate_pagerank(graph)
            print("Результат PageRank:", pagerank_scores)

            # Получаем данные о зданиях (узлах) для визуализации

            for node in Node.objects.all():
                # Преобразуем координаты из кортежей в списки
                geom_coords = [[y, x] for x, y in node.geom.coords[0]]
                nodes_data_pr.append({
                    'id': node.id,
                    'name': node.name,
                    'geom': geom_coords,  # Координаты полигона здания (уже в формате [[lat, lon], ...])
                    'pagerank': pagerank_scores.get(node.id, 0)  # Рейтинг PageRank
                })
            print(nodes_data_pr)


    return render(request, 'assistant.html', {
        'communities': communities,
        'nodes_data': nodes_data,
        'nodes_data_pr': nodes_data_pr,
        'pagerank_scores': pagerank_scores
    })

def routes_view(request):
    path = None
    path_coordinates = []
    start_geometry = None
    end_geometry = None
    routes = None
    nodes_data = None

    # Создаём экземпляры форм
    route_form = RouteForm(request.POST or None)
    route_by_type_form = RouteByTypeForm(request.POST or None)

    if request.method == 'POST':
        if 'find_route' in request.POST:
            if route_form.is_valid():
                start_node = route_form.cleaned_data['start_node']
                end_node = route_form.cleaned_data['end_node']

                # Получаем координаты начальной и конечной точек
                start_coords = (start_node.geom.centroid.x, start_node.geom.centroid.y)
                end_coords = (end_node.geom.centroid.x, end_node.geom.centroid.y)

                # Создаём граф дорог
                graph = create_road_graph(ROADS_GEOJSON)

                # Находим ближайшие вершины графа
                start_nearest = find_nearest_node(graph, start_coords)
                end_nearest = find_nearest_node(graph, end_coords)

                # Находим кратчайший путь
                path = find_shortest_path(graph, start_nearest, end_nearest)

                # Получаем координаты для пути
                if path:
                    path_coordinates = [[y, x] for x, y in path]  # Преобразуем в [широта, долгота]

                # Используем NodeSerializer для получения GeoJSON

                start_geometry = NodeSerializer(start_node).data['geometry']
                end_geometry = NodeSerializer(end_node).data['geometry']



        elif 'find_routes_by_type' in request.POST:  # Если нажата кнопка "Найти маршруты по типу"
            print(request.POST)
            if route_by_type_form.is_valid():
                type_name = request.POST['type']
                type_content = request.POST['content_type']

                # Создаём граф
                graph = build_graph()

                # Находим кратчайшие маршруты
                node_object, node_ids, routes = find_shortest_routes_by_type(graph, type_name, type_content)

                # Получаем данные о зданиях для визуализации
                nodes_data = []

                if len(node_ids) != 0:
                    for node in Node.objects.filter(id__in=node_ids):
                        if node.geom:
                            geom_coords = [[y, x] for x, y in node.geom.coords[0]]
                            nodes_data.append({
                                'id': node.id,
                                'name': node.name,
                                'geom': geom_coords,
                            })

                else:
                    for node in Node.objects.filter(name=node_object):
                        if node.geom:
                            geom_coords = [[y, x] for x, y in node.geom.coords[0]]
                            nodes_data.append({
                                'id': node.id,
                                'name': node.name,
                                'geom': geom_coords,
                            })

        else:
            print('Не считывается форма')


    return render(request, 'routes.html', {
        'path': path,
        'path_coordinates': path_coordinates,
        'start_geometry': start_geometry,
        'end_geometry': end_geometry,
        'route_form': route_form,
        'route_by_type_form': route_by_type_form,
        'routes': routes,
        'nodes_data': nodes_data,
    })



'''
from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'index.html', context)
'''
