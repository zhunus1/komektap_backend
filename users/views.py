import requests
from django.shortcuts import render
from .models import AppUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import generate_code
from .serializers import (
    PhoneSerializer,
    PasswordSerializer,
    VerificationCodeSerializer,
    AuthorizationSerializer,
    RegistrationSerializer
)


# Create your views here.

class RegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(
            data = request.data,
        )

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # Check if a user already exists
            if AppUser.objects.filter(phone_number = phone_number).exists():
                return Response(
                    {'detail': 'Пользователь с данным номером телефона уже существует.'}, 
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            verification_code = generate_code()

            # Make a call to the service
            flashcall_data = {
                'msisdn': phone_number,
                'verification_code': verification_code,
            }

            flashcall_url = 'https://authenticalls.com/api/flashcall/'
            flashcall_response = requests.post(
                flashcall_url, 
                flashcall_data
            )

            if flashcall_response.status_code == 200:
                user = serializer.save()
                return Response(
                    {'detail': 'Пользователь успешно зарегистрирован.'},
                    status = status.HTTP_201_CREATED
                )
            return Response(
                {'detail': 'Ошибка валидации номера телефона. Попробуйте снова.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.errors, 
            status = status.HTTP_400_BAD_REQUEST
        )

