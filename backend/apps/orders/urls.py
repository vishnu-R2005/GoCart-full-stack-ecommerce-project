from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CouponViewSet, OrderViewSet

router = DefaultRouter()
router.register('', OrderViewSet, basename='order')
router.register('coupons', CouponViewSet, basename='coupon')

urlpatterns = [
    path('', include(router.urls)),
]
