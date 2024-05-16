from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    AdvertViewSet,
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, 'categories')
router.register(r'adverts', AdvertViewSet, 'adverts')


urlpatterns = [
    path('', include(router.urls)),
]