from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from apps.accounts.models import User
from apps.orders.models import Order, OrderItem, OrderStatus
from apps.payments.models import Payment, PaymentStatus
from apps.products.models import Category, Product


class AnalyticsService:
    @staticmethod
    def get_dashboard_stats():
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)

        total_revenue = Payment.objects.filter(
            status=PaymentStatus.CAPTURED
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        monthly_revenue = Payment.objects.filter(
            status=PaymentStatus.CAPTURED,
            created_at__gte=thirty_days_ago,
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status=OrderStatus.PENDING).count()
        total_customers = User.objects.filter(role='customer').count()
        total_products = Product.objects.filter(is_active=True).count()

        return {
            'total_revenue': total_revenue,
            'monthly_revenue': monthly_revenue,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'total_customers': total_customers,
            'total_products': total_products,
        }

    @staticmethod
    def get_monthly_sales(months=12):
        cutoff = timezone.now() - timedelta(days=months * 30)
        return list(
            Payment.objects.filter(
                status=PaymentStatus.CAPTURED,
                created_at__gte=cutoff,
            )
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(revenue=Sum('amount'), orders=Count('id'))
            .order_by('month')
        )

    @staticmethod
    def get_top_products(limit=10):
        return list(
            OrderItem.objects.values('product_name', 'product__id')
            .annotate(total_sold=Sum('quantity'), revenue=Sum('total_price'))
            .order_by('-total_sold')[:limit]
        )

    @staticmethod
    def get_top_categories(limit=10):
        return list(
            OrderItem.objects.values('product__category__name')
            .annotate(total_sold=Sum('quantity'), revenue=Sum('total_price'))
            .order_by('-revenue')[:limit]
        )

    @staticmethod
    def get_recent_orders(limit=10):
        return Order.objects.select_related('user').order_by('-created_at')[:limit]

    @staticmethod
    def get_sales_by_status():
        return list(
            Order.objects.values('status')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
