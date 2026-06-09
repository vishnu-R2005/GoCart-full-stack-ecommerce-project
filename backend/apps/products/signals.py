from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Category, Product, Review
from .services import ProductService, ReviewService


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def invalidate_product_cache(sender, **kwargs):
    ProductService.invalidate_cache()


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def invalidate_category_cache(sender, **kwargs):
    ProductService.invalidate_cache()


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    ReviewService.update_product_ratings(instance.product)
