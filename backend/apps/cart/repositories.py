from .models import CartItem


class CartRepository:
    @staticmethod
    def get_user_cart(user, saved_for_later=False):
        return CartItem.objects.filter(
            user=user, saved_for_later=saved_for_later
        ).select_related('product__category').prefetch_related('product__images')

    @staticmethod
    def get_item(user, product):
        return CartItem.objects.filter(user=user, product=product).first()

    @staticmethod
    def add_or_update(user, product, quantity):
        item, created = CartItem.objects.get_or_create(
            user=user, product=product, defaults={'quantity': quantity}
        )
        if not created:
            item.quantity = quantity
            item.save(update_fields=['quantity', 'updated_at'])
        return item

    @staticmethod
    def remove(user, product):
        CartItem.objects.filter(user=user, product=product).delete()

    @staticmethod
    def clear(user):
        CartItem.objects.filter(user=user, saved_for_later=False).delete()

    @staticmethod
    def update_quantity(item, quantity):
        item.quantity = quantity
        item.save(update_fields=['quantity', 'updated_at'])
        return item

    @staticmethod
    def toggle_save_for_later(item, saved):
        item.saved_for_later = saved
        item.save(update_fields=['saved_for_later', 'updated_at'])
        return item
