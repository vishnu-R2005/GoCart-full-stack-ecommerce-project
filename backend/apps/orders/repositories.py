from .models import Coupon, Order, OrderItem, OrderStatusHistory


class OrderRepository:
    @staticmethod
    def get_user_orders(user):
        return Order.objects.filter(user=user).prefetch_related('items__product')

    @staticmethod
    def get_by_id(order_id, user=None):
        qs = Order.objects.prefetch_related('items__product', 'status_history')
        if user:
            qs = qs.filter(user=user)
        return qs.filter(id=order_id).first()

    @staticmethod
    def get_by_order_number(order_number):
        return Order.objects.filter(order_number=order_number).first()

    @staticmethod
    def create(**kwargs):
        return Order.objects.create(**kwargs)

    @staticmethod
    def update_status(order, status, note=''):
        order.status = status
        order.save(update_fields=['status', 'updated_at'])
        OrderStatusHistory.objects.create(order=order, status=status, note=note)
        return order


class CouponRepository:
    @staticmethod
    def get_by_code(code):
        return Coupon.objects.filter(code__iexact=code).first()


class OrderItemRepository:
    @staticmethod
    def bulk_create(items):
        return OrderItem.objects.bulk_create(items)
