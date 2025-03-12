from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .paginations import StandardSetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Category, Advert
from .serializers import (
    CategorySerializer, 
    AdvertDetailSerializer,
    AdvertListSerializer,
    AdvertCreateSerializer,
    AdvertUpdateSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class AdvertViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardSetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return AdvertListSerializer
        elif self.action == 'retrieve':
            return AdvertDetailSerializer
        elif self.action == 'create':
            return AdvertCreateSerializer
        else:
            return AdvertUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        return Advert.objects.filter(profile__user = user, is_active = True)

