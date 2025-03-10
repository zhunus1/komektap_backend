from rest_framework import serializers
from djmoney.contrib.django_rest_framework.fields import MoneyField
from django.contrib.gis.geos import Point
from .models import Category, Images, Advert

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "icon"]

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ["id", "image"]

class AdvertSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["profile"]

    def get_location(self, obj):
        if isinstance(obj.location, Point):
            return {"latitude": obj.location.y, "longitude": obj.location.x}
        return None

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist("images")
        categories_data = validated_data.pop("category")
        advert = Advert.objects.create(**validated_data)

        for category in categories_data:
            advert.category.add(category)

        for image in images_data:
            Images.objects.create(advert=advert, image=image)

        return advert

    def update(self, instance, validated_data):
        if "category" in validated_data:
            categories_data = validated_data.pop("category")
            instance.category.set(categories_data)

        return super().update(instance, validated_data)
