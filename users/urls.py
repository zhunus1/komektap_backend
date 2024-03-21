from django.urls import path
from .views import (
    AuthorizationView,
    RegistrationView,
    VerificationView,
)


urlpatterns = [
    path('authorize/', AuthorizationView.as_view(), name = 'authorize'),
    path('register/', RegistrationView.as_view(), name = 'register'),
    path('verify/', VerificationView.as_view(), name = 'verify'),
]

