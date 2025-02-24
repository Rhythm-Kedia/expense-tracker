from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from banking_app.models import Account
from banking_app.serializers import AccountSerializer

User = get_user_model()

# SignupView to handle user signup, also return token
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """Handle user creation and return tokens upon successful signup"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)  # Generate JWT tokens

        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

# LoginView to handle user login, and return tokens
class LoginView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            accounts = Account.objects.filter(user=user)
            account_serializer = AccountSerializer(accounts, many=True)
            profile_image_url = user.profile_image.url if user.profile_image else None

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'full_name': user.full_name,
                    'profile_image': request.build_absolute_uri(profile_image_url) if profile_image_url else None,
                },
                'accounts': account_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

# Creating a view to handle profile image management

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser
from .serializers import ProfileImageSerializer

class ProfileImageView(generics.UpdateAPIView):
    serializer_class = ProfileImageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        # Handle image upload/update
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Handle image deletion
        user = self.get_object()
        user.delete_profile_image()
        return Response(status=status.HTTP_204_NO_CONTENT)