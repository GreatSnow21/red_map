from django.shortcuts import render
from .forms import RouteForm
from .utils.graph_utils import create_road_graph, find_shortest_path, find_nearest_node, build_combined_graph, detect_communities
from .serializers import NodeSerializer
from .models import Node

ROADS_GEOJSON = "roads_drive_spb.geojson"


def map_view(request):
    path = None
    path_coordinates = []
    start_geometry = None
    end_geometry = None
    communities = None
    nodes_data = []

    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            if 'find_route' in request.POST:
                start_node = form.cleaned_data['start_node']
                end_node = form.cleaned_data['end_node']

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


            elif 'detect_communities' in request.POST:  # Если нажата кнопка "Кластеризация Лувена"

                # Логика для кластеризации

                graph = build_combined_graph()

                communities = detect_communities(graph)

                # Получаем данные о зданиях (узлах) для визуализации

                nodes_data = []

                for node in Node.objects.all():

                    # Преобразуем координаты из кортежей в списки

                    geom_coords = [[y, x] for x, y in node.geom.coords[0]]

                    nodes_data.append({

                        'id': node.id,

                        'name': node.name,

                        'geom': geom_coords,  # Координаты полигона здания (уже в формате [[lat, lon], ...])

                        'community': communities.get(node.id, -1)  # Номер сообщества

                    })

    else:
        form = RouteForm()

    return render(request, 'shortest_path.html', {
        'form': form,
        'path': path,
        'path_coordinates': path_coordinates,
        'start_geometry': start_geometry,
        'end_geometry': end_geometry,
        'communities': communities,
        'nodes_data': nodes_data
    })

'''
from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'index.html', context)
'''
