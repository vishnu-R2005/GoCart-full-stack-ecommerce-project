import re

from django.core.exceptions import ValidationError


def validate_phone(value):
    pattern = r'^\+?1?\d{9,15}$'
    if not re.match(pattern, value):
        raise ValidationError('Enter a valid phone number.')


def validate_positive_decimal(value):
    if value < 0:
        raise ValidationError('Value must be positive.')
