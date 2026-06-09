import uuid

from django.conf import settings
from django.db import models


class NotificationType(models.TextChoices):
    ORDER = 'order', 'Order'
    SHIPPING = 'shipping', 'Shipping'
    PAYMENT = 'payment', 'Payment'
    PROMO = 'promo', 'Promotion'
    SYSTEM = 'system', 'System'


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.title}'
