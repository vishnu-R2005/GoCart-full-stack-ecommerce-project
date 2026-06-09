from django.db.models import Prefetch, Q

from .models import Category, Product, ProductImage, Review, WishlistItem


class CategoryRepository:
    @staticmethod
    def get_all_active():
        return Category.objects.filter(is_active=True).select_related('parent')

    @staticmethod
    def get_root_categories():
        return Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related('children')

    @staticmethod
    def get_by_slug(slug):
        return Category.objects.filter(slug=slug, is_active=True).first()

    @staticmethod
    def get_by_id(category_id):
        return Category.objects.filter(id=category_id).first()


class ProductRepository:
    @staticmethod
    def get_base_queryset():
        return Product.objects.filter(is_active=True).select_related('category').prefetch_related(
            Prefetch('images', queryset=ProductImage.objects.order_by('order'))
        )

    @staticmethod
    def get_by_slug(slug):
        return ProductRepository.get_base_queryset().filter(slug=slug).first()

    @staticmethod
    def get_by_id(product_id):
        return ProductRepository.get_base_queryset().filter(id=product_id).first()

    @staticmethod
    def get_featured(limit=8):
        return ProductRepository.get_base_queryset().filter(is_featured=True)[:limit]

    @staticmethod
    def get_best_sellers(limit=8):
        return ProductRepository.get_base_queryset().order_by('-sales_count')[:limit]

    @staticmethod
    def get_related(product, limit=4):
        return ProductRepository.get_base_queryset().filter(
            category=product.category
        ).exclude(id=product.id)[:limit]

    @staticmethod
    def search(query):
        return ProductRepository.get_base_queryset().filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query)
        )

    @staticmethod
    def create(**kwargs):
        return Product.objects.create(**kwargs)

    @staticmethod
    def update(product, **kwargs):
        for key, value in kwargs.items():
            setattr(product, key, value)
        product.save()
        return product


class ReviewRepository:
    @staticmethod
    def get_product_reviews(product):
        return Review.objects.filter(product=product).select_related('user')

    @staticmethod
    def get_user_review(user, product):
        return Review.objects.filter(user=user, product=product).first()

    @staticmethod
    def create(**kwargs):
        return Review.objects.create(**kwargs)

    @staticmethod
    def update(review, **kwargs):
        for key, value in kwargs.items():
            setattr(review, key, value)
        review.save()
        return review

    @staticmethod
    def delete(review):
        review.delete()


class WishlistRepository:
    @staticmethod
    def get_user_wishlist(user):
        return WishlistItem.objects.filter(user=user).select_related('product__category').prefetch_related(
            'product__images'
        )

    @staticmethod
    def add(user, product):
        item, created = WishlistItem.objects.get_or_create(user=user, product=product)
        return item, created

    @staticmethod
    def remove(user, product):
        WishlistItem.objects.filter(user=user, product=product).delete()

    @staticmethod
    def exists(user, product):
        return WishlistItem.objects.filter(user=user, product=product).exists()
