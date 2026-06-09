from decimal import Decimal

from django.conf import settings
from rest_framework.exceptions import ValidationError

from apps.common.exceptions import InsufficientStockError
from apps.common.utils import calculate_tax
from apps.products.repositories import ProductRepository

from .repositories import CartRepository


class CartService:
    @staticmethod
    def _calculate_totals(items, discount: Decimal = Decimal('0')):
        subtotal = sum((item.subtotal for item in items), Decimal('0'))
        tax = calculate_tax(subtotal, settings.TAX_RATE)
        total = subtotal + tax - discount
        return {
            'subtotal': subtotal.quantize(Decimal('0.01')),
            'tax': tax,
            'discount': discount.quantize(Decimal('0.01')),
            'total': max(total, Decimal('0')).quantize(Decimal('0.01')),
            'item_count': sum(item.quantity for item in items),
        }

    @staticmethod
    def get_cart(user):
        items = list(CartRepository.get_user_cart(user, saved_for_later=False))
        totals = CartService._calculate_totals(items)
        return {'items': items, **totals}

    @staticmethod
    def get_saved_for_later(user):
        return CartRepository.get_user_cart(user, saved_for_later=True)

    @staticmethod
    def add_to_cart(user, product_id: int, quantity: int = 1):
        product = ProductRepository.get_by_id(product_id)
        if not product or not product.is_active:
            raise ValidationError({'detail': 'Product not found.'})
        if product.stock < quantity:
            raise InsufficientStockError()
        existing = CartRepository.get_item(user, product)
        new_qty = (existing.quantity + quantity) if existing else quantity
        if product.stock < new_qty:
            raise InsufficientStockError()
        return CartRepository.add_or_update(user, product, new_qty)

    @staticmethod
    def update_quantity(user, product_id: int, quantity: int):
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ValidationError({'detail': 'Product not found.'})
        if product.stock < quantity:
            raise InsufficientStockError()
        item = CartRepository.get_item(user, product)
        if not item:
            raise ValidationError({'detail': 'Item not in cart.'})
        return CartRepository.update_quantity(item, quantity)

    @staticmethod
    def remove_from_cart(user, product_id: int):
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ValidationError({'detail': 'Product not found.'})
        CartRepository.remove(user, product)

    @staticmethod
    def save_for_later(user, product_id: int):
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ValidationError({'detail': 'Product not found.'})
        item = CartRepository.get_item(user, product)
        if not item:
            raise ValidationError({'detail': 'Item not in cart.'})
        return CartRepository.toggle_save_for_later(item, True)

    @staticmethod
    def move_to_cart(user, product_id: int):
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ValidationError({'detail': 'Product not found.'})
        item = CartRepository.get_item(user, product)
        if not item:
            raise ValidationError({'detail': 'Item not found.'})
        return CartRepository.toggle_save_for_later(item, False)

    @staticmethod
    def clear_cart(user):
        CartRepository.clear(user)
