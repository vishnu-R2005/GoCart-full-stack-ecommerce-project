from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.common.permissions import IsOwnerOrAdmin

from .models import Address
from .serializers import (
    AddressSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    UserRegistrationSerializer,
)
from .services import AddressService, AuthService, ProfileService


class AuthThrottle(AnonRateThrottle):
    scope = 'auth'


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    # throttle_classes = [AuthThrottle]

    @extend_schema(tags=['Authentication'], summary='Register a new customer account')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        user = AuthService.register(validated)
        tokens = AuthService.login(validated['email'], validated['password'])
        return Response({
            'success': True,
            'message': 'Registration successful. Please verify your email.',
            'user': UserProfileSerializer(user).data,
            'tokens': tokens['tokens'],
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    throttle_classes = [AuthThrottle]

    @extend_schema(tags=['Authentication'], summary='Login with email and password')
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = AuthService.login(**serializer.validated_data)
        return Response({
            'success': True,
            'user': UserProfileSerializer(result['user']).data,
            'tokens': result['tokens'],
        })


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Authentication'], summary='Logout and blacklist refresh token')
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return Response({'success': True, 'message': 'Logged out successfully.'})


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['Authentication'], summary='Verify email address')
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'success': False, 'error': 'Token is required.'}, status=400)
        user = AuthService.verify_email(token)
        return Response({
            'success': True,
            'message': 'Email verified successfully.',
            'user': UserProfileSerializer(user).data,
        })


class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer
    throttle_classes = [AuthThrottle]

    @extend_schema(tags=['Authentication'], summary='Request password reset email')
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuthService.forgot_password(serializer.validated_data['email'])
        return Response({
            'success': True,
            'message': 'If the email exists, a reset link has been sent.',
        })


class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer
    throttle_classes = [AuthThrottle]

    @extend_schema(tags=['Authentication'], summary='Reset password with token')
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuthService.reset_password(
            str(serializer.validated_data['token']),
            serializer.validated_data['new_password'],
        )
        return Response({'success': True, 'message': 'Password reset successfully.'})


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserProfileUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        return self.request.user

    @extend_schema(tags=['Profile'], summary='Get user profile')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=['Profile'], summary='Update user profile')
    def patch(self, request, *args, **kwargs):
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = ProfileService.update_profile(request.user, serializer.validated_data)
        return Response({
            'success': True,
            'user': UserProfileSerializer(user).data,
        })


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @extend_schema(tags=['Profile'], summary='Change password')
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuthService.change_password(
            request.user,
            serializer.validated_data['old_password'],
            serializer.validated_data['new_password'],
        )
        return Response({'success': True, 'message': 'Password changed successfully.'})


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    @extend_schema(tags=['Addresses'])
    def list(self, request, *args, **kwargs):
        addresses = AddressService.list_addresses(request.user)
        serializer = self.get_serializer(addresses, many=True)
        return Response({'success': True, 'results': serializer.data})

    @extend_schema(tags=['Addresses'])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = AddressService.create_address(request.user, serializer.validated_data)
        return Response({
            'success': True,
            'address': AddressSerializer(address).data,
        }, status=status.HTTP_201_CREATED)

    @extend_schema(tags=['Addresses'])
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        address = AddressService.update_address(
            request.user, kwargs['pk'], serializer.validated_data
        )
        return Response({
            'success': True,
            'address': AddressSerializer(address).data,
        })

    @extend_schema(tags=['Addresses'])
    def destroy(self, request, *args, **kwargs):
        AddressService.delete_address(request.user, kwargs['pk'])
        return Response({'success': True, 'message': 'Address deleted.'}, status=status.HTTP_204_NO_CONTENT)
