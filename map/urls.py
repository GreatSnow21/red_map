from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import NodeViewSet, EdgeViewSet
from . import views

router = DefaultRouter()
router.register(r'nodes', NodeViewSet)
router.register(r'edges', EdgeViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),  # REST API
]
