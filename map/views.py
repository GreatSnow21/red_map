from django.shortcuts import render
from .forms import RouteForm
from .utils.graph_utils import create_road_graph, find_shortest_path, find_nearest_node
from .serializers import NodeSerializer

ROADS_GEOJSON = "roads_drive_spb.geojson"


def map_view(request):
    path = None
    path_coordinates = []
    start_geometry = None
    end_geometry = None

    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
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
                print("Найден путь:", path)  # Отладочная информация
                print("Координаты пути:", path_coordinates)  # Отладочная информация

            # Используем NodeSerializer для получения GeoJSON
            print(start_node)
            print(end_node)
            # Преобразуем координаты в GeoJSON-полигон
            start_geometry = NodeSerializer(start_node).data['geometry']
            end_geometry = NodeSerializer(end_node).data['geometry']
            print(start_geometry)
            print(end_geometry)
    else:
        form = RouteForm()

    return render(request, 'shortest_path.html', {
        'form': form,
        'path': path,
        'path_coordinates': path_coordinates,
        'start_geometry': start_geometry,
        'end_geometry': end_geometry})

'''
from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'index.html', context)
'''
