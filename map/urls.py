from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import NodeViewSet, EdgeViewSet
from django.views.generic import TemplateView
from .views import index

router = DefaultRouter()
router.register(r'nodes', NodeViewSet)
router.register(r'edges', EdgeViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),  # Маршрут для карты
    path('api/', include(router.urls)),
]
    # path('', index, name='index'),


