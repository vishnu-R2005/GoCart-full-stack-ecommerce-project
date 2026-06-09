from django.utils import timezone

from .models import Address, EmailVerificationToken, PasswordResetToken, User


class UserRepository:
    @staticmethod
    def get_by_email(email: str):
        return User.objects.filter(email__iexact=email).first()

    @staticmethod
    def get_by_id(user_id):
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def create(**kwargs):
        return User.objects.create_user(**kwargs)

    @staticmethod
    def update(user, **kwargs):
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user


class AddressRepository:
    @staticmethod
    def get_user_addresses(user):
        return Address.objects.filter(user=user)

    @staticmethod
    def get_by_id(address_id, user):
        return Address.objects.filter(id=address_id, user=user).first()

    @staticmethod
    def create(user, **kwargs):
        return Address.objects.create(user=user, **kwargs)

    @staticmethod
    def update(address, **kwargs):
        for key, value in kwargs.items():
            setattr(address, key, value)
        address.save()
        return address

    @staticmethod
    def delete(address):
        address.delete()


class TokenRepository:
    @staticmethod
    def create_verification_token(user, expires_at):
        return EmailVerificationToken.objects.create(user=user, expires_at=expires_at)

    @staticmethod
    def get_valid_verification_token(token):
        return EmailVerificationToken.objects.filter(
            token=token, is_used=False, expires_at__gt=timezone.now()
        ).select_related('user').first()

    @staticmethod
    def create_reset_token(user, expires_at):
        return PasswordResetToken.objects.create(user=user, expires_at=expires_at)

    @staticmethod
    def get_valid_reset_token(token):
        return PasswordResetToken.objects.filter(
            token=token, is_used=False, expires_at__gt=timezone.now()
        ).select_related('user').first()
