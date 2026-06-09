from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

from apps.accounts.repositories import AddressRepository
from apps.cart.repositories import CartRepository
from apps.cart.services import CartService
from apps.common.exceptions import InsufficientStockError
from apps.common.utils import apply_percentage_discount, calculate_tax, generate_order_number
from apps.notifications.tasks import send_order_confirmation, send_shipping_update

from .models import CouponType, OrderItem, OrderStatus
from .repositories import CouponRepository, OrderItemRepository, OrderRepository


class CouponService:
    @staticmethod
    def validate_coupon(code: str, subtotal: Decimal) -> tuple:
        coupon = CouponRepository.get_by_code(code)
        if not coupon:
            raise ValidationError({'code': 'Invalid coupon code.'})
        if not coupon.is_valid():
            raise ValidationError({'code': 'Coupon has expired or is no longer valid.'})
        if subtotal < coupon.min_order_amount:
            raise ValidationError({
                'code': f'Minimum order amount of ₹{coupon.min_order_amount} required.'
            })
        if coupon.coupon_type == CouponType.PERCENTAGE:
            discount = apply_percentage_discount(subtotal, coupon.value)
            if coupon.max_discount:
                discount = min(discount, coupon.max_discount)
        else:
            discount = min(coupon.value, subtotal)
        return coupon, discount.quantize(Decimal('0.01'))

    @staticmethod
    def apply_coupon(user, code: str) -> dict:
        cart = CartService.get_cart(user)
        coupon, discount = CouponService.validate_coupon(code, cart['subtotal'])
        tax = calculate_tax(cart['subtotal'], settings.TAX_RATE)
        total = cart['subtotal'] + tax - discount
        return {
            'coupon': coupon,
            'discount': discount,
            'subtotal': cart['subtotal'],
            'tax': tax,
            'total': max(total, Decimal('0')).quantize(Decimal('0.01')),
        }


class OrderService:
    @staticmethod
    @transaction.atomic
    def place_order(user, data: dict):
        cart_items = list(CartRepository.get_user_cart(user, saved_for_later=False))
        if not cart_items:
            raise ValidationError({'detail': 'Cart is empty.'})

        shipping_address = AddressRepository.get_by_id(data['shipping_address_id'], user)
        if not shipping_address:
            raise ValidationError({'shipping_address_id': 'Invalid shipping address.'})

        billing_address_id = data.get('billing_address_id') or data['shipping_address_id']
        billing_address = AddressRepository.get_by_id(billing_address_id, user)
        if not billing_address:
            raise ValidationError({'billing_address_id': 'Invalid billing address.'})

        subtotal = Decimal('0')
        order_items_data = []

        for item in cart_items:
            product = item.product
            if product.stock < item.quantity:
                raise InsufficientStockError(
                    detail=f'Insufficient stock for {product.name}.'
                )
            unit_price = product.effective_price
            total_price = unit_price * item.quantity
            subtotal += total_price
            order_items_data.append({
                'product': product,
                'product_name': product.name,
                'product_sku': product.sku,
                'quantity': item.quantity,
                'unit_price': unit_price,
                'total_price': total_price,
            })

        discount = Decimal('0')
        coupon = None
        coupon_code = data.get('coupon_code', '').strip()
        if coupon_code:
            coupon, discount = CouponService.validate_coupon(coupon_code, subtotal)

        tax = calculate_tax(subtotal, settings.TAX_RATE)
        total = subtotal + tax - discount

        order = OrderRepository.create(
            order_number=generate_order_number(),
            user=user,
            shipping_address=shipping_address,
            billing_address=billing_address,
            coupon=coupon,
            subtotal=subtotal,
            tax=tax,
            discount=discount,
            total=max(total, Decimal('0')),
            notes=data.get('notes', ''),
        )

        items = [
            OrderItem(order=order, **item_data) for item_data in order_items_data
        ]
        OrderItemRepository.bulk_create(items)

        for item_data in order_items_data:
            product = item_data['product']
            product.stock -= item_data['quantity']
            product.sales_count += item_data['quantity']
            product.save(update_fields=['stock', 'sales_count'])

        if coupon:
            coupon.used_count += 1
            coupon.save(update_fields=['used_count'])

        OrderRepository.update_status(order, OrderStatus.PENDING, 'Order placed')
        CartRepository.clear(user)
        send_order_confirmation.delay(str(order.id))

        return order

    @staticmethod
    def cancel_order(user, order_id):
        order = OrderRepository.get_by_id(order_id, user)
        if not order:
            raise ValidationError({'detail': 'Order not found.'})
        if order.status not in (OrderStatus.PENDING, OrderStatus.PROCESSING):
            raise ValidationError({'detail': 'Order cannot be cancelled at this stage.'})
        with transaction.atomic():
            for item in order.items.select_related('product'):
                item.product.stock += item.quantity
                item.product.save(update_fields=['stock'])
            OrderRepository.update_status(order, OrderStatus.CANCELLED, 'Cancelled by customer')
        return order

    @staticmethod
    def update_order_status(order, status, note='', tracking_number=''):
        if tracking_number:
            order.tracking_number = tracking_number
            order.save(update_fields=['tracking_number'])
        OrderRepository.update_status(order, status, note)
        if status == OrderStatus.SHIPPED:
            send_shipping_update.delay(str(order.id))
        return order

    @staticmethod
    def generate_invoice(order) -> str:
        context = {
            'order': order,
            'items': order.items.all(),
            'shipping': order.shipping_address,
            'billing': order.billing_address,
        }
        return render_to_string('orders/invoice.html', context)
