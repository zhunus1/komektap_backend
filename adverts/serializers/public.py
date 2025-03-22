from rest_framework import serializers
from djmoney.contrib.django_rest_framework.fields import MoneyField
from django.contrib.gis.geos import Point
from ..models import (
    Category, 
    Images, 
    Advert,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id", 
            "title", 
            "icon"
        )


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = (
            "id", 
            "image",
        )


class AdvertDetailSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(
        many = True, 
        read_only = True,
    )

    category = serializers.PrimaryKeyRelatedField(
        many = True, 
        queryset = Category.objects.all(),
    )

    price = MoneyField(
        max_digits = 10,
        decimal_places = 0, 
        default_currency = "KZT",
    )
    
    location = serializers.SerializerMethodField()

    class Meta:
        model = Advert
        fields = (
            "id", 
            "title", 
            "profile", 
            "category", 
            "description",
            "price", 
            "location", 
            "is_active",
            "images",
        )


    def get_location(self, obj):
        if isinstance(obj.location, Point):
            return {"latitude": obj.location.y, "longitude": obj.location.x}
        return None


class AdvertListSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(
        many = True, 
        read_only = True,
    )

    category = serializers.PrimaryKeyRelatedField(
        many = True, 
        queryset = Category.objects.all(),
    )

    price = MoneyField(
        max_digits = 10,
        decimal_places = 0, 
        default_currency = "KZT",
    )
    
    location = serializers.SerializerMethodField()

    phone_number = serializers.CharField(
        source = 'profile.user.phone_number', 
        read_only = True,
    )

    class Meta:
        model = Advert
        fields = (
            "id", 
            "title", 
            "category", 
            "price", 
            "location", 
            "images",
            "phone_number",
        )


    def get_location(self, obj):
        if isinstance(obj.location, Point):
            return {"latitude": obj.location.y, "longitude": obj.location.x}
        return None