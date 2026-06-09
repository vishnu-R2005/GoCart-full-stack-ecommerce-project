import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger('gocart')


def _create_notification(user_id, notification_type, title, message, metadata=None):
    from apps.accounts.models import User
    from .models import Notification

    user = User.objects.filter(id=user_id).first()
    if user:
        Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            metadata=metadata or {},
        )


@shared_task(bind=True, max_retries=3)
def send_verification_email(self, user_id, token):
    from apps.accounts.models import User
    user = User.objects.filter(id=user_id).first()
    if not user:
        return
    verify_url = f'{settings.FRONTEND_URL}/verify-email?token={token}'
    html = render_to_string('emails/verify_email.html', {'user': user, 'verify_url': verify_url})
    try:
        send_mail(
            subject='Verify your GoCart account',
            message=f'Click to verify: {verify_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html,
            fail_silently=False,
        )
    except Exception as exc:
        logger.error(f'Failed to send verification email: {exc}')
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_id):
    from apps.accounts.models import User
    user = User.objects.filter(id=user_id).first()
    if not user:
        return
    html = render_to_string('emails/welcome.html', {'user': user})
    try:
        send_mail(
            subject='Welcome to GoCart!',
            message=f'Welcome to GoCart, {user.first_name}!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html,
        )
        _create_notification(user_id, 'system', 'Welcome!', 'Welcome to GoCart. Shop Smarter. Shop Faster.')
    except Exception as exc:
        logger.error(f'Failed to send welcome email: {exc}')
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_password_reset_email(self, user_id, token):
    from apps.accounts.models import User
    user = User.objects.filter(id=user_id).first()
    if not user:
        return
    reset_url = f'{settings.FRONTEND_URL}/reset-password?token={token}'
    html = render_to_string('emails/password_reset.html', {'user': user, 'reset_url': reset_url})
    try:
        send_mail(
            subject='Reset your GoCart password',
            message=f'Reset password: {reset_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html,
        )
    except Exception as exc:
        logger.error(f'Failed to send password reset email: {exc}')
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_order_confirmation(self, order_id):
    from apps.orders.models import Order
    order = Order.objects.select_related('user').prefetch_related('items').filter(id=order_id).first()
    if not order:
        return
    html = render_to_string('emails/order_confirmation.html', {'order': order})
    try:
        send_mail(
            subject=f'Order Confirmed - {order.order_number}',
            message=f'Your order {order.order_number} has been placed.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html,
        )
        _create_notification(
            str(order.user.id), 'order',
            'Order Confirmed',
            f'Your order {order.order_number} has been placed successfully.',
            {'order_id': str(order.id)},
        )
    except Exception as exc:
        logger.error(f'Failed to send order confirmation: {exc}')
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_shipping_update(self, order_id):
    from apps.orders.models import Order
    order = Order.objects.select_related('user').filter(id=order_id).first()
    if not order:
        return
    html = render_to_string('emails/shipping_update.html', {'order': order})
    try:
        send_mail(
            subject=f'Order Shipped - {order.order_number}',
            message=f'Your order {order.order_number} has been shipped.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html,
        )
        _create_notification(
            str(order.user.id), 'shipping',
            'Order Shipped',
            f'Your order {order.order_number} is on its way! Tracking: {order.tracking_number}',
            {'order_id': str(order.id), 'tracking': order.tracking_number},
        )
    except Exception as exc:
        logger.error(f'Failed to send shipping update: {exc}')
        raise self.retry(exc=exc, countdown=60)
