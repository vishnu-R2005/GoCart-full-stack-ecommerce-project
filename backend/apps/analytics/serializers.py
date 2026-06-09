from rest_framework import serializers

from apps.orders.serializers import OrderListSerializer


class DashboardStatsSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)
    monthly_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_orders = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    total_products = serializers.IntegerField()


class MonthlySalesSerializer(serializers.Serializer):
    month = serializers.DateTimeField()
    revenue = serializers.DecimalField(max_digits=14, decimal_places=2)
    orders = serializers.IntegerField()


class TopProductSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    product__id = serializers.IntegerField(allow_null=True)
    total_sold = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=14, decimal_places=2)


class RecentOrdersSerializer(serializers.Serializer):
    orders = OrderListSerializer(many=True)
