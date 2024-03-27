from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    AdvertViewSet,
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'adverts', AdvertViewSet)


urlpatterns = [
    path('', include(router.urls)),
]