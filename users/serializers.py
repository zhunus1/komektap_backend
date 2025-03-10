from .models import AppUser
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from profiles.models import Profile

class PhoneSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length = 128,
    )


class VerificationCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    verification_code = serializers.CharField(
        max_length = 4,
    )

    def validate_verification_code(self, value):
        if not value.isdigit() or len(value) != 4:
            raise serializers.ValidationError("Invalid verification code")
        return value


class AuthorizationSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    class Meta:
        model = AppUser
        fields = (
            'phone_number', 
            'password',
        )


class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    class Meta:
        model = AppUser
        fields = (
            'first_name',
            'last_name',
            'phone_number', 
            'password',
        )
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegistrationSerializer, self).create(validated_data)
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        
        user = AppUser.objects.create(**validated_data)
        
        profile = Profile.objects.get_or_create(
            user = user,
        ) 
        
        return user
