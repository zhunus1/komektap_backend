from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from ..paginations import StandardSetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from ..models import (
    Category,
    Advert,
)
from ..serializers.public import (
    CategorySerializer, 
    AdvertDetailSerializer,
    AdvertListSerializer,
)
from ..filters import AdvertFilter


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    pagination_class = StandardSetPagination


class AdvertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Advert.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandardSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = (
        'title',
    )
    filterset_class = AdvertFilter

    def get_queryset(self):
        return Advert.objects.filter(
            is_active = True,
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return AdvertListSerializer
        return AdvertDetailSerializer
