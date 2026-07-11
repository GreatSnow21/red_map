from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import NodeViewSet, EdgeViewSet, TypeViewSet, Content_typeViewSet, Object_houseViewSet, LinkViewSet
from django.views.generic import TemplateView
from .views import map_view, routes_view

router = DefaultRouter()
router.register(r'nodes', NodeViewSet)
router.register(r'edges', EdgeViewSet)
router.register(r'type', TypeViewSet)
router.register(r'content_type', Content_typeViewSet)
router.register(r'object_house', Object_houseViewSet)
router.register(r'link', LinkViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='map'),  # Маршрут для карты
    path('api/', include(router.urls)),
    path('assistant/', map_view, name='assistant'),
    path('assistant/routes', routes_view, name='routes'),
]
    # path('', index, name='index'),


