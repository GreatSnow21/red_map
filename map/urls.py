from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import NodeViewSet, EdgeViewSet
from django.views.generic import TemplateView
# from .views import ShortestPathView
from .views import map_view, routes_view

router = DefaultRouter()
router.register(r'nodes', NodeViewSet)
router.register(r'edges', EdgeViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='map'),  # Маршрут для карты
    path('api/', include(router.urls)),
    path('assistant/', map_view, name='assistant'),
    path('assistant/routes', routes_view, name='routes')
]
    # path('', index, name='index'),


