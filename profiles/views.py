from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Advert
from .serializers import AdvertSerializer
from adverts.paginations import StandardSetPagination

# Create your views here.
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardSetPagination

    def get_queryset(self):
        # Retrieve the user from the request
        user = self.request.user

        # Filter adverts where the user is the profile owner and is_active=True
        queryset = Advert.objects.filter(profile__user=user, is_active=True)

        return queryset