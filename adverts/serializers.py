from rest_framework import serializers
from .models import (
    Location,
    Category,
    Advert,
)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'address',
            'latitude',
            'longitude',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'icon',
            'title',
        )


class AdvertDetailSerializer(serializers.ModelSerializer):
    profile = None
    location = None
    class Meta:
        model = Advert
        fields = (
            'id',
            'profile',
            'title',
            'category',
            'images',
            'description',
            'price',
            'location',
            'created'
        )


class AdvertListSerializer(serializers.ModelSerializer):
    phone_number = None
    category = None
    class Meta:
        model = Advert
        fields = (
            'id',
            'title',
            'phone_number',
            'price',
            'images',
            'category'
        )


class AdvertUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = (
            'id',
            'profile',
            'title',
            'category',
            'images',
            'description',
            'price',
            'location',
            'is_active'
        )


class AdvertCreateSerializer(serializers.ModelSerializer):
    location = None
    class Meta:
        model = Advert
        fields = (
            'id',
            'profile',
            'title',
            'category',
            'images',
            'description',
            'price',
            'location',
        )