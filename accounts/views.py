from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer
)
from notifications.tasks import send_welcome_email


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    POST /api/accounts/register/
    Anyone can access this — no auth required.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # ✅ Send welcome email with account details (no password)
        send_welcome_email.delay(
            email=user.email,
            username=user.username,
            role=user.role,
            phone=user.phone,
            company_name=user.company_name,
            skills=user.skills,
        )

        # Generate JWT tokens for the new user immediately after register
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Registration successful.",
            "user": UserProfileSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    API endpoint for user login.
    POST /api/accounts/login/
    Returns JWT tokens on success.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                "error": "Email and password are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        print(user)

        if user is None:
            return Response({
                "error": "Invalid email or password."
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({
                "error": "Account is disabled."
            }, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful.",
            "user": UserProfileSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/accounts/logout/
    Blacklists the refresh token so it can't be used again.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "message": "Logout successful."
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "error": "Invalid token."
            }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/accounts/profile/ — view your profile
    PUT  /api/accounts/profile/ — update your profile
    Only authenticated users can access this.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """
    POST /api/accounts/change-password/
    Allows logged in users to change their password.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                "error": "Old password is incorrect."
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            "message": "Password changed successfully."
        }, status=status.HTTP_200_OK)