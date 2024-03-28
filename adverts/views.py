from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CategorySerializer,
    AdvertDetailSerializer,
    AdvertListSerializer,
    AdvertUpdateSerializer,
    AdvertCreateSerializer,
)
from .models import (
    Category,
    Advert,
)
from .paginations import (
    StandardSetPagination,
)

# Create your views here.
#TO-DO: Add pagination

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = StandardSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title',]


class AdvertViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardSetPagination

    def get_queryset(self):
        queryset = Advert.objects.filter(
            is_active = True,
        )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return AdvertListSerializer
        elif self.action in 'retrieve':
            return AdvertDetailSerializer
        elif self.action in [ 'update', 'partial_update']:
            return AdvertUpdateSerializer
        return AdvertCreateSerializer
    

    @action(
        detail = True, 
        methods = ['post'],
    )
    def mark_favorite(self, request, pk = None):
        advert = self.get_object()
        user = request.user

        if user.profile.favorites.filter(
                pk = advert.pk,
            ).exists():
            user.profile.favorites.remove(advert)
            return Response(
                {'detail': 'Advert removed from favorites'}, 
                status = status.HTTP_200_OK,
            )
        else:
            user.profile.favorites.add(advert)
            return Response(
                {'detail': 'Advert added to favorites'}, 
                status = status.HTTP_200_OK,
            )