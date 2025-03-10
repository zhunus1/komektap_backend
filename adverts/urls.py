from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, AdvertViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename = 'category')
router.register(r'', AdvertViewSet, basename = 'advert')

urlpatterns = [
    path('', include(router.urls)),
]
