from rest_framework import serializers
from djmoney.contrib.django_rest_framework.fields import MoneyField
from django.contrib.gis.geos import Point
from .models import Category, Images, Advert


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


class AdvertCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )
    price = MoneyField(max_digits=10, decimal_places=0, default_currency='KZT')

    class Meta:
        model = Advert
        fields = (
            'id', 
            'title', 
            'profile', 
            'category', 
            'description', 
            'price', 
            'location', 
            'images'
        )

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        advert = Advert.objects.create(**validated_data)

        for image in images_data:
            Images.objects.create(advert=advert, image=image)

        return advert
    

class AdvertUpdateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, required=False
    )
    price = MoneyField(max_digits=10, decimal_places=0, default_currency='KZT')

    class Meta:
        model = Advert
        fields = (
            'id', 
            'title', 
            'category', 
            'description', 
            'price', 
            'location', 
            'images', 
            'is_active'
        )

        def update(self, instance, validated_data):
            images_data = validated_data.pop('images', None)
            category_data = validated_data.pop('category', None)

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if category_data is not None:
                instance.category.set(category_data)

            if images_data:
                instance.images.all().delete()
                for image in images_data:
                    Images.objects.create(advert=instance, image=image)

            instance.save()
            return instance