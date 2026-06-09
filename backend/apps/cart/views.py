from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import AddToCartSerializer, CartItemSerializer, CartSummarySerializer, UpdateCartSerializer
from .services import CartService


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Cart'], responses=CartSummarySerializer)
    def list(self, request):
        cart = CartService.get_cart(request.user)
        return Response({
            'success': True,
            'items': CartItemSerializer(cart['items'], many=True, context={'request': request}).data,
            'subtotal': cart['subtotal'],
            'tax': cart['tax'],
            'discount': cart['discount'],
            'total': cart['total'],
            'item_count': cart['item_count'],
        })

    @extend_schema(tags=['Cart'])
    @action(detail=False, methods=['post'])
    def add(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = CartService.add_to_cart(
            request.user,
            serializer.validated_data['product_id'],
            serializer.validated_data.get('quantity', 1),
        )
        return Response({
            'success': True,
            'item': CartItemSerializer(item, context={'request': request}).data,
        }, status=status.HTTP_201_CREATED)

    @extend_schema(tags=['Cart'])
    @action(detail=False, methods=['patch'], url_path='update/(?P<product_id>[^/.]+)')
    def update_item(self, request, product_id=None):
        serializer = UpdateCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = CartService.update_quantity(request.user, int(product_id), serializer.validated_data['quantity'])
        return Response({
            'success': True,
            'item': CartItemSerializer(item, context={'request': request}).data,
        })

    @extend_schema(tags=['Cart'])
    @action(detail=False, methods=['delete'], url_path='remove/(?P<product_id>[^/.]+)')
    def remove(self, request, product_id=None):
        CartService.remove_from_cart(request.user, int(product_id))
        return Response({'success': True, 'message': 'Item removed from cart.'})

    @extend_schema(tags=['Cart'])
    @action(detail=False, methods=['post'], url_path='save-for-later/(?P<product_id>[^/.]+)')
    def save_for_later(self, request, product_id=None):
        item = CartService.save_for_later(request.user, int(product_id))
        return Response({
            'success': True,
            'item': CartItemSerializer(item, context={'request': request}).data,
        })

    @extend_schema(tags=['Cart'])
    @action(detail=False, methods=['post'], url_path='move-to-cart/(?P<product_id>[^/.]+)')
    def move_to_cart(self, request, product_id=None):
        item = CartService.move_to_cart(request.user, int(product_id))
        return Response({
            'success': True,
            'item': CartItemSerializer(item, context={'request': request}).data,
        })

    @extend_schema(tags=['Cart'])
    @action(detail=False, methods=['get'])
    def saved(self, request):
        items = CartService.get_saved_for_later(request.user)
        return Response({
            'success': True,
            'results': CartItemSerializer(items, many=True, context={'request': request}).data,
        })

    @extend_schema(tags=['Cart'])
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        CartService.clear_cart(request.user)
        return Response({'success': True, 'message': 'Cart cleared.'})
