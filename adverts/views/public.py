from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from ..paginations import StandardSetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from ..models import (
    Category,
    Advert,
)
from ..serializers.public import (
    CategorySerializer, 
    AdvertDetailSerializer,
    AdvertListSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer


class AdvertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Advert.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandardSetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return AdvertListSerializer
        return AdvertDetailSerializer
