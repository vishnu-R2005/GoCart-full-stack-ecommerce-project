from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.notifications.tasks import send_password_reset_email, send_verification_email, send_welcome_email

from .models import User
from .repositories import AddressRepository, TokenRepository, UserRepository


class AuthService:
    @staticmethod
    def register(data: dict) -> User:
        if UserRepository.get_by_email(data['email']):
            raise ValidationError({'email': 'A user with this email already exists.'})
        user = UserRepository.create(
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            phone=data.get('phone', ''),
        )
        expires_at = timezone.now() + timedelta(hours=24)
        token_obj = TokenRepository.create_verification_token(user, expires_at)
        send_verification_email.delay(str(user.id), str(token_obj.token))
        return user

    @staticmethod
    def login(email: str, password: str) -> dict:
        user = authenticate(email=email, password=password)
        if not user:
            raise ValidationError({'detail': 'Invalid email or password.'})
        if not user.is_active:
            raise ValidationError({'detail': 'Account is deactivated.'})
        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
        }

    @staticmethod
    def verify_email(token: str) -> User:
        token_obj = TokenRepository.get_valid_verification_token(token)
        if not token_obj:
            raise ValidationError({'detail': 'Invalid or expired verification token.'})
        user = token_obj.user
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        token_obj.is_used = True
        token_obj.save(update_fields=['is_used'])
        send_welcome_email.delay(str(user.id))
        return user

    @staticmethod
    def forgot_password(email: str):
        user = UserRepository.get_by_email(email)
        if user:
            expires_at = timezone.now() + timedelta(hours=1)
            token_obj = TokenRepository.create_reset_token(user, expires_at)
            send_password_reset_email.delay(str(user.id), str(token_obj.token))

    @staticmethod
    def reset_password(token: str, new_password: str) -> User:
        token_obj = TokenRepository.get_valid_reset_token(token)
        if not token_obj:
            raise ValidationError({'detail': 'Invalid or expired reset token.'})
        user = token_obj.user
        user.set_password(new_password)
        user.save()
        token_obj.is_used = True
        token_obj.save(update_fields=['is_used'])
        return user

    @staticmethod
    def change_password(user: User, old_password: str, new_password: str):
        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'Current password is incorrect.'})
        user.set_password(new_password)
        user.save()


class ProfileService:
    @staticmethod
    def update_profile(user: User, data: dict) -> User:
        return UserRepository.update(user, **data)


class AddressService:
    @staticmethod
    def list_addresses(user):
        return AddressRepository.get_user_addresses(user)

    @staticmethod
    def create_address(user, data: dict):
        if data.get('is_default'):
            AddressRepository.get_user_addresses(user).update(is_default=False)
        return AddressRepository.create(user, **data)

    @staticmethod
    def update_address(user, address_id, data: dict):
        address = AddressRepository.get_by_id(address_id, user)
        if not address:
            raise ValidationError({'detail': 'Address not found.'})
        if data.get('is_default'):
            AddressRepository.get_user_addresses(user).exclude(id=address_id).update(is_default=False)
        return AddressRepository.update(address, **data)

    @staticmethod
    def delete_address(user, address_id):
        address = AddressRepository.get_by_id(address_id, user)
        if not address:
            raise ValidationError({'detail': 'Address not found.'})
        AddressRepository.delete(address)
