from django.core.mail import send_mail
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
class UserService:
    @staticmethod
    def register_user(name, email, password):
        if User.objects.filter(email=email).exists():
            raise ValueError("Email already exists")
        user = User.objects.create_user(name=name, email=email, password=password)
        send_mail(
            'Welcome!',
            f'Hi {user.name}, welcome to our site!',
            'noreply@example.com',
            [user.email],
        )
        return user

    @staticmethod
    def authenticate_user(email, password):
        user = authenticate(email=email, password=password)
        if not user:
            raise ValueError("Invalid credentials")
        return user

    @staticmethod
    def generate_tokens(user):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(hours=1))
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
