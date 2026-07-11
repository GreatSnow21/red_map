from django.shortcuts import render
from .models import Node, Edge

def index(request):
    context = {}
    return render(request, 'index.html', context)

'''
def index(request):
    content_node = Node.objects.all()
    content_edge = Edge.objects.all()
    return render(request, "index.html", {'content_node': content_node, 'content_edge': content_edge})
'''

#
# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponse
# from django.core.serializers import serialize
# from django.contrib.gis.geos import Point
# from django.contrib.gis.db.models.functions import Distance
# from .models import Node, Edge
# from django.db import connection
#
# def map_view(request):
#     """ Главная страница с картой """
#     return render(request, "map.html")
#
# def get_nodes(request):
#     """ API: Получить вершины графа в формате GeoJSON """
#     nodes = Node.objects.all()
#     data = serialize("geojson", nodes, geometry_field="geom", fields=("id", "name"))
#     return HttpResponse(data, content_type="application/json")
#
# def get_edges(request):
#     """ API: Получить связи (рёбра) графа в формате GeoJSON """
#     edges = Edge.objects.all()
#     data = serialize("geojson", edges, geometry_field="geom", fields=("id", "source", "target", "cost"))
#     return HttpResponse(data, content_type="application/json")
#
# def find_nearest_node(lat, lon):
#     """ Найти ближайшую вершину графа к указанным координатам """
#     point = Point(lon, lat, srid=4326)  # Создаём точку
#     nearest_node = Node.objects.annotate(distance=Distance("geom", point)).order_by("distance").first()
#     return nearest_node.id if nearest_node else None
#
# def get_route(request):
#     """ API: Рассчитать маршрут между двумя точками с использованием pgRouting """
#     try:
#         lat1, lon1 = float(request.GET["lat1"]), float(request.GET["lon1"])
#         lat2, lon2 = float(request.GET["lat2"]), float(request.GET["lon2"])
#     except (KeyError, ValueError):
#         return JsonResponse({"error": "Invalid coordinates"}, status=400)
#
#     # Находим ближайшие узлы к старту и финишу
#     source_id = find_nearest_node(lat1, lon1)
#     target_id = find_nearest_node(lat2, lon2)
#
#     if not source_id or not target_id:
#         return JsonResponse({"error": "No nodes found"}, status=400)
#
#     # SQL-запрос к pgRouting (алгоритм Dijkstra)
#     query = f"""
#         SELECT route.seq, node.geom AS geom
#         FROM pgr_dijkstra(
#             'SELECT id, source, target, cost FROM graph_edges',
#             {source_id}, {target_id}, directed := false
#         ) AS route
#         JOIN graph_nodes AS node ON route.node = node.id
#         ORDER BY route.seq;
#     """
#
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         route_data = cursor.fetchall()
#
#     if not route_data:
#         return JsonResponse({"error": "No route found"}, status=400)
#
#     # Формируем GeoJSON-массив маршрута
#     route_geojson = {
#         "type": "FeatureCollection",
#         "features": [
#             {
#                 "type": "Feature",
#                 "geometry": {"type": "Point", "coordinates": [float(row[1].x), float(row[1].y)]},
#                 "properties": {"seq": row[0]},
#             }
#             for row in route_data
#         ],
#     }
#
#     return JsonResponse(route_geojson)
