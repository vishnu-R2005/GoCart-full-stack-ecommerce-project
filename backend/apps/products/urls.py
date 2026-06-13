from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, ReviewViewSet, WishlistViewSet
from .views import (
    CategoryViewSet,
    ProductViewSet,
    ReviewViewSet,
    WishlistViewSet,
    ProductImageViewSet,
)
router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('reviews', ReviewViewSet, basename='review')
router.register('wishlist', WishlistViewSet, basename='wishlist')

router.register('images',ProductImageViewSet,basename='product-image')
router.register('', ProductViewSet, basename='product')
urlpatterns = [
    path('', include(router.urls)),
    
]
