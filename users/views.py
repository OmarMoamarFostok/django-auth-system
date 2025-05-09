from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer, LoginSerializer
from .services import UserService
from drf_yasg import openapi

class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Render the register page as HTML.",
        responses={200: openapi.Response('Register page', content={'text/html': {}})}
    )
    def get(self, request):
        return render(request,'register.html')
    @swagger_auto_schema(
        operation_description="Register a new user.",
        responses={201: 'User registered successfully.', 400: 'Bad Request'},
        request_body=RegisterSerializer,
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = UserService.register_user(**serializer.validated_data)
                return Response({'msg': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Render the login page as HTML.",
        responses={200: openapi.Response('Login page', content={'text/html': {}})}
    )
    def get(self,request):
        return render(request,"login.html")
    @swagger_auto_schema(
        operation_description="Login and authenticate user.",
        responses={200: 'Tokens returned successfully.', 401: 'Unauthorized'},
        request_body=LoginSerializer,
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = UserService.authenticate_user(**serializer.validated_data)
                tokens = UserService.generate_tokens(user)
                return Response(tokens)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve user profile information.",
        responses={200: 'Profile data', 401: 'Unauthorized'},
    )
    def get(self, request):
        return Response({
            'name': request.user.name,
            'email': request.user.email,
        })
