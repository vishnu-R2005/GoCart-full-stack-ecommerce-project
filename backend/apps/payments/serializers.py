from rest_framework import serializers

from .models import Payment, Refund


class CreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()


class VerifyPaymentSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField()
    razorpay_payment_id = serializers.CharField()
    razorpay_signature = serializers.CharField()


class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_number', 'razorpay_order_id', 'razorpay_payment_id',
            'amount', 'currency', 'status', 'created_at',
        ]


class RefundSerializer(serializers.Serializer):
    payment_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    reason = serializers.CharField(required=False, allow_blank=True)


class RefundDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'payment', 'razorpay_refund_id', 'amount', 'reason', 'status', 'created_at']
