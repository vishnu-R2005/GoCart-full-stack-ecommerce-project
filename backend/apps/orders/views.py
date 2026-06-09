from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsAdmin, IsOwnerOrAdmin

from .models import Coupon, Order, OrderStatus
from .serializers import (
    ApplyCouponSerializer,
    CouponSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    PlaceOrderSerializer,
    UpdateOrderStatusSerializer,
)
from .services import CouponService, OrderService


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Order.objects.all().prefetch_related('items__product')
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderListSerializer

    @extend_schema(tags=['Orders'])
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'success': True, **response.data}
        return response

    @extend_schema(tags=['Orders'])
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({'success': True, 'order': response.data})

    @extend_schema(tags=['Orders'], request=PlaceOrderSerializer)
    @action(detail=False, methods=['post'])
    def place(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = OrderService.place_order(request.user, serializer.validated_data)
        return Response({
            'success': True,
            'order': OrderDetailSerializer(order).data,
        }, status=status.HTTP_201_CREATED)

    @extend_schema(tags=['Orders'])
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = OrderService.cancel_order(request.user, pk)
        return Response({
            'success': True,
            'order': OrderDetailSerializer(order).data,
        })

    @extend_schema(tags=['Orders'])
    @action(detail=True, methods=['get'])
    def tracking(self, request, pk=None):
        order = self.get_object()
        return Response({
            'success': True,
            'order_number': order.order_number,
            'status': order.status,
            'tracking_number': order.tracking_number,
            'history': [
                {'status': h.status, 'note': h.note, 'created_at': h.created_at}
                for h in order.status_history.all()
            ],
        })

    @extend_schema(tags=['Orders'])
    @action(detail=True, methods=['get'])
    def invoice(self, request, pk=None):
        order = self.get_object()
        html = OrderService.generate_invoice(order)
        return HttpResponse(html, content_type='text/html')

    @extend_schema(tags=['Orders'])
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsAdmin])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = UpdateOrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_statuses = [s.value for s in OrderStatus]
        status_val = serializer.validated_data['status']
        if status_val not in valid_statuses:
            return Response({'success': False, 'error': 'Invalid status.'}, status=400)
        order = OrderService.update_order_status(
            order,
            status_val,
            serializer.validated_data.get('note', ''),
            serializer.validated_data.get('tracking_number', ''),
        )
        return Response({
            'success': True,
            'order': OrderDetailSerializer(order).data,
        })


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'apply'):
            return [IsAuthenticated()]
        return [IsAdmin()]

    @extend_schema(tags=['Coupons'])
    @action(detail=False, methods=['post'])
    def apply(self, request):
        serializer = ApplyCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = CouponService.apply_coupon(request.user, serializer.validated_data['code'])
        return Response({
            'success': True,
            'discount': result['discount'],
            'subtotal': result['subtotal'],
            'tax': result['tax'],
            'total': result['total'],
            'coupon': CouponSerializer(result['coupon']).data,
        })

    @extend_schema(tags=['Coupons'])
    @action(detail=False, methods=['post'])
    def remove(self, request):
        cart = __import__('apps.cart.services', fromlist=['CartService']).CartService.get_cart(request.user)
        return Response({
            'success': True,
            'subtotal': cart['subtotal'],
            'tax': cart['tax'],
            'discount': 0,
            'total': cart['subtotal'] + cart['tax'],
        })
