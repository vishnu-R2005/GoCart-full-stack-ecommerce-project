import hashlib
import hmac
import logging
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.common.exceptions import PaymentError
from apps.orders.models import OrderStatus
from apps.orders.repositories import OrderRepository

from .models import Payment, PaymentStatus, Refund

logger = logging.getLogger('gocart')


class RazorpayService:
    def __init__(self):
        import razorpay
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

    def create_order(self, order, user) -> Payment:
        amount_paise = int(order.total * 100)
        razorpay_order = self.client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': order.order_number,
            'notes': {
                'order_id': str(order.id),
                'user_id': str(user.id),
            },
        })
        payment, _ = Payment.objects.update_or_create(
            order=order,
            defaults={
                'user': user,
                'razorpay_order_id': razorpay_order['id'],
                'amount': order.total,
                'status': PaymentStatus.CREATED,
            },
        )
        return payment, razorpay_order

    def verify_signature(self, razorpay_order_id: str, razorpay_payment_id: str, signature: str) -> bool:
        message = f'{razorpay_order_id}|{razorpay_payment_id}'
        expected = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def verify_webhook_signature(self, body: bytes, signature: str) -> bool:
        expected = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    @transaction.atomic
    def capture_payment(self, razorpay_order_id: str, razorpay_payment_id: str, signature: str) -> Payment:
        if not self.verify_signature(razorpay_order_id, razorpay_payment_id, signature):
            raise PaymentError(detail='Invalid payment signature.')

        payment = Payment.objects.select_for_update().filter(
            razorpay_order_id=razorpay_order_id
        ).first()
        if not payment:
            raise ValidationError({'detail': 'Payment record not found.'})
        if payment.status == PaymentStatus.CAPTURED:
            return payment

        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = signature
        payment.status = PaymentStatus.CAPTURED
        payment.save()

        OrderRepository.update_status(payment.order, OrderStatus.PROCESSING, 'Payment captured')
        return payment

    def create_refund(self, payment: Payment, amount: Decimal = None, reason: str = '') -> Refund:
        if payment.status != PaymentStatus.CAPTURED:
            raise ValidationError({'detail': 'Only captured payments can be refunded.'})
        refund_amount = amount or payment.amount
        amount_paise = int(refund_amount * 100)
        razorpay_refund = self.client.payment.refund(
            payment.razorpay_payment_id,
            {'amount': amount_paise, 'notes': {'reason': reason}},
        )
        refund = Refund.objects.create(
            payment=payment,
            razorpay_refund_id=razorpay_refund['id'],
            amount=refund_amount,
            reason=reason,
            status=razorpay_refund.get('status', 'processed'),
        )
        if refund_amount >= payment.amount:
            payment.status = PaymentStatus.REFUNDED
        else:
            payment.status = PaymentStatus.PARTIALLY_REFUNDED
        payment.save(update_fields=['status', 'updated_at'])
        OrderRepository.update_status(payment.order, OrderStatus.RETURNED, f'Refund: {reason}')
        return refund

    def handle_webhook(self, event: str, payload: dict):
        logger.info(f'Razorpay webhook: {event}')
        if event == 'payment.captured':
            payment_entity = payload.get('payment', {}).get('entity', {})
            order_id = payment_entity.get('order_id')
            payment_id = payment_entity.get('id')
            if order_id and payment_id:
                payment = Payment.objects.filter(razorpay_order_id=order_id).first()
                if payment and payment.status != PaymentStatus.CAPTURED:
                    payment.razorpay_payment_id = payment_id
                    payment.status = PaymentStatus.CAPTURED
                    payment.save()
                    OrderRepository.update_status(
                        payment.order, OrderStatus.PROCESSING, 'Payment captured via webhook'
                    )
        elif event == 'payment.failed':
            payment_entity = payload.get('payment', {}).get('entity', {})
            order_id = payment_entity.get('order_id')
            if order_id:
                Payment.objects.filter(razorpay_order_id=order_id).update(
                    status=PaymentStatus.FAILED,
                    failure_reason=payment_entity.get('error_description', 'Payment failed'),
                )
