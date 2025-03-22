from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.public import CategoryViewSet, AdvertViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename = 'categories')
router.register(r'', AdvertViewSet, basename = 'adverts')

urlpatterns = [
    path('', include(router.urls)),
]