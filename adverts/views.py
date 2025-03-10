from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .paginations import StandardSetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Category, Advert
from .serializers import (
    CategorySerializer, 
    AdvertSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class AdvertViewSet(viewsets.ModelViewSet):
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardSetPagination

    def get_queryset(self):
        user = self.request.user

        queryset = Advert.objects.filter(
            profile__user = user, 
            is_active = True,
        )
        return queryset

    def perform_create(self, serializer):
        user = self.request.user

        if hasattr(user, "profile"):
            serializer.save(profile = user.profile)
        else:
            raise PermissionDenied("User does not have a profile.")

    def perform_update(self, serializer):
        advert = self.get_object()

        if advert.profile.user != self.request.user:
            raise PermissionDenied("You can only edit your own adverts.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.profile.user != self.request.user:
            raise PermissionDenied("You can only delete your own adverts.")
        instance.delete()

