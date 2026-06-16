from django.db.models import Avg, Count

from apps.common.cache import CACHE_TTL, get_cached, invalidate_pattern, make_cache_key, set_cached
from apps.orders.models import OrderItem, OrderStatus

from .models import Product, Review
from .repositories import CategoryRepository, ProductRepository, ReviewRepository, WishlistRepository
from .models import WishlistItem


class CategoryService:
    @staticmethod
    def get_category_tree():
        cache_key = make_cache_key('categories:tree')
        cached = get_cached(cache_key)
        if cached:
            return cached
        from .serializers import CategorySerializer
        categories = CategoryRepository.get_root_categories()
        data = CategorySerializer(categories, many=True).data
        set_cached(cache_key, data, CACHE_TTL['categories_tree'])
        return data


class ProductService:
    @staticmethod
    def get_featured():
        cache_key = make_cache_key('products:featured')
        cached = get_cached(cache_key)
        if cached:
            return cached
        from .serializers import ProductListSerializer
        products = ProductRepository.get_featured()
        data = ProductListSerializer(products, many=True).data
        set_cached(cache_key, data, CACHE_TTL['products_featured'])
        return data

    @staticmethod
    def get_best_sellers():
        from .serializers import ProductListSerializer
        products = ProductRepository.get_best_sellers()
        return ProductListSerializer(products, many=True).data

    @staticmethod
    def get_related(product):
        from .serializers import ProductListSerializer
        products = ProductRepository.get_related(product)
        return ProductListSerializer(products, many=True).data

    @staticmethod
    def invalidate_cache():
        invalidate_pattern('products:')
        invalidate_pattern('categories:')


class ReviewService:
    @staticmethod
    def _check_verified_purchase(user, product) -> bool:
        return OrderItem.objects.filter(
            order__user=user,
            order__status__in=[OrderStatus.DELIVERED, OrderStatus.SHIPPED, OrderStatus.PROCESSING],
            product=product,
        ).exists()

    @staticmethod
    def create_review(user, data: dict) -> Review:
        product = data['product']
        existing = ReviewRepository.get_user_review(user, product)
        if existing:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'detail': 'You have already reviewed this product.'})
        is_verified = ReviewService._check_verified_purchase(user, product)
        return ReviewRepository.create(user=user, is_verified_purchase=is_verified, **data)

    @staticmethod
    def update_review(user, review_id, data: dict) -> Review:
        review = Review.objects.filter(id=review_id, user=user).first()
        if not review:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'detail': 'Review not found.'})
        return ReviewRepository.update(review, **data)

    @staticmethod
    def delete_review(user, review_id):
        review = Review.objects.filter(id=review_id, user=user).first()
        if not review:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'detail': 'Review not found.'})
        ReviewRepository.delete(review)

    @staticmethod
    def update_product_ratings(product: Product):
        stats = Review.objects.filter(product=product).aggregate(
            avg=Avg('rating'), count=Count('id')
        )
        product.avg_rating = round(stats['avg'] or 0, 1)
        product.reviews_count = stats['count'] or 0
        product.save(update_fields=['avg_rating', 'reviews_count'])


class WishlistService:
    @staticmethod
    def get_wishlist(user):
        return WishlistRepository.get_user_wishlist(user)

    @staticmethod
    def add_to_wishlist(user, product_id):
        product = ProductRepository.get_by_id(product_id)
        if not product:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'detail': 'Product not found.'})
        return WishlistRepository.add(user, product)
        

    @staticmethod
    def remove_from_wishlist(user, product_id):
        WishlistItem.objects.filter(
            user=user,
            product_id=product_id
        ).delete()