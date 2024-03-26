from django.shortcuts import render
from .models import AppUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from django.contrib.auth.hashers import make_password


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
class AuthorizationView(GenericAPIView):
    serializer_class = AuthorizationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data = request.data,
        )

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            
            # Authenticate the user
            user = authenticate(
                phone_number = phone_number, 
                password = password
            )

            #Authorize only active users          
            if user is not None:
                if user.is_active:
                    token, created = Token.objects.get_or_create(
                        user = user,
                    )
                                    
                    return Response(
                        {
                            'detail': 'User authenticated successfully.', 
                            'token': token.key
                        }, 
                        status = status.HTTP_200_OK
                    )
                return Response(
                    {'detail': 'Phone number is not verified.'}, 
                    status = status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'detail': 'Invalid phone number or password.'}, 
                status = status.HTTP_401_UNAUTHORIZED
            )
        

        return Response(
            serializer.errors, 
            status = status.HTTP_400_BAD_REQUEST
        )


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
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
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
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
    

class RequestCallView(GenericAPIView):
    serializer_class = PhoneSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data = request.data,
        )

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # Check if a user exists
            if not AppUser.objects.filter(phone_number = phone_number).exists():
                return Response(
                    {'detail': 'Пользователь с данным номером не существует.'}, 
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
    

class PasswordResetView(GenericAPIView):
    serializer_class = AuthorizationSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data = request.data,
        )

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            # Check if a user exists
            try:
                user = AppUser.objects.get(
                    phone_number = phone_number,
                )
            except AppUser.DoesNotExist:
                return Response(
                    {'detail': 'Пользователь с данным номером не существует.'}, 
                    status = status.HTTP_400_BAD_REQUEST
                )

            # Update user's password
            user.password = make_password(password)
            user.save()

            return Response(
                {'detail': 'Пароль успешно изменен.'},
                status = status.HTTP_200_OK
            )

        return Response(
            serializer.errors, 
            status = status.HTTP_400_BAD_REQUEST
        )