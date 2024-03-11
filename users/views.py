from django.shortcuts import render
from .models import AppUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from .utils import (
    generate_code,
    validate_code,
    make_call
)
from .serializers import (
    PhoneSerializer,
    PasswordSerializer,
    VerificationCodeSerializer,
    AuthorizationSerializer,
    RegistrationSerializer
)


# Create your views here.

class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer
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
            
            try:
                # Attempt to generate code and save user
                verification_code = generate_code(phone_number)
            except Exception as e:
                return Response(
                    {'detail': 'Ошибка генерации кода. Попробуйте позже.'},
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            # Make a call to the users phone
            result = make_call(phone_number, verification_code)
            if result:
                serializer.save()
                return Response(
                    data = serializer.data,
                    status = status.HTTP_201_CREATED
                )
            return Response(
                {'detail': 'Ошибка верификации номера телефона. Попробуйте позже.'},
                status = status.HTTP_400_BAD_REQUEST
            )

        return Response(
            serializer.errors, 
            status = status.HTTP_400_BAD_REQUEST
        )
    


class VerificationView(GenericAPIView):
    serializer_class = VerificationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerificationCodeSerializer(
            data = request.data,
        )

        if serializer.is_valid():
            verification_code = serializer.validated_data['verification_code']
            phone_number = serializer.validated_data['phone_number']
            
            result = validate_code(phone_number, verification_code)
            if result:
                # Get the user from the database using the phone_number
                user = AppUser.objects.get(
                    phone_number = phone_number,
                )
                
                # Update the user's is_active status to True
                user.is_active = True
                user.save()

                return Response(
                    {'detail': 'Верификация прошла успешно.'},
                    status = status.HTTP_200_OK
                )
            return Response(
                {'detail': 'Неверный код верификации.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.errors, 
            status = status.HTTP_400_BAD_REQUEST
        )
    
