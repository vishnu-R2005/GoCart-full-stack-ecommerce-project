import json

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin
from apps.orders.repositories import OrderRepository

from .models import Payment
from .serializers import (
    CreatePaymentSerializer,
    PaymentSerializer,
    RefundDetailSerializer,
    RefundSerializer,
    VerifyPaymentSerializer,
)
from .services import RazorpayService


class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Payments'], request=CreatePaymentSerializer)
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = OrderRepository.get_by_id(serializer.validated_data['order_id'], request.user)
        if not order:
            return Response({'success': False, 'error': 'Order not found.'}, status=404)
        service = RazorpayService()
        payment, razorpay_order = service.create_order(order, request.user)
        return Response({
            'success': True,
            'payment': PaymentSerializer(payment).data,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency'],
        })

    @extend_schema(tags=['Payments'], request=VerifyPaymentSerializer)
    @action(detail=False, methods=['post'])
    def verify(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = RazorpayService()
        payment = service.capture_payment(**serializer.validated_data)
        return Response({
            'success': True,
            'payment': PaymentSerializer(payment).data,
        })

    @extend_schema(tags=['Payments'])
    def list(self, request):
        payments = Payment.objects.filter(user=request.user)
        return Response({
            'success': True,
            'results': PaymentSerializer(payments, many=True).data,
        })

    @extend_schema(tags=['Payments'])
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
    def refund(self, request):
        serializer = RefundSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = Payment.objects.filter(id=serializer.validated_data['payment_id']).first()
        if not payment:
            return Response({'success': False, 'error': 'Payment not found.'}, status=404)
        service = RazorpayService()
        refund = service.create_refund(
            payment,
            serializer.validated_data.get('amount'),
            serializer.validated_data.get('reason', ''),
        )
        return Response({
            'success': True,
            'refund': RefundDetailSerializer(refund).data,
        })


class RazorpayWebhookView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=['Payments'], exclude=True)
    def post(self, request):
        signature = request.headers.get('X-Razorpay-Signature', '')
        body = request.body
        service = RazorpayService()
        if settings.RAZORPAY_WEBHOOK_SECRET and not service.verify_webhook_signature(body, signature):
            return Response({'error': 'Invalid signature'}, status=400)
        payload = json.loads(body)
        event = payload.get('event', '')
        service.handle_webhook(event, payload.get('payload', {}))
        return Response({'status': 'ok'})
