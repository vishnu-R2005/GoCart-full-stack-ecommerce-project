from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser
from apps.common.permissions import IsAdmin, IsAdminOrReadOnly

from .filters import ProductFilter
from .models import Category, Product, Review
from .repositories import ProductRepository
from .serializers import (
    CategoryListSerializer,
    CategorySerializer,
    ProductCreateUpdateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ReviewCreateSerializer,
    ReviewSerializer,
    WishlistItemSerializer,
)
from .services import CategoryService, ProductService, ReviewService, WishlistService

from .models import ProductImage
from .serializers import ProductImageSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' and self.request.query_params.get('tree'):
            return CategorySerializer
        return CategoryListSerializer

    @extend_schema(tags=['Categories'])
    def list(self, request, *args, **kwargs):
        if request.query_params.get('tree'):
            data = CategoryService.get_category_tree()
            return Response({'success': True, 'results': data})
        return super().list(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'brand', 'sku']
    ordering_fields = ['price', 'created_at', 'avg_rating', 'sales_count', 'name']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_queryset(self):
        qs = ProductRepository.get_base_queryset()
        if not self.request.user.is_authenticated or self.request.user.role != 'admin':
            qs = qs.filter(is_active=True)
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return ProductCreateUpdateSerializer
        return ProductListSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdmin()]
        return [AllowAny()]

    @extend_schema(tags=['Products'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=['Products'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=['Products'], summary='Get featured products')
    @action(detail=False, methods=['get'])
    def featured(self, request):
        data = ProductService.get_featured()
        return Response({'success': True, 'results': data})

    @extend_schema(tags=['Products'], summary='Get best selling products')
    @action(detail=False, methods=['get'])
    def best_sellers(self, request):
        data = ProductService.get_best_sellers()
        return Response({'success': True, 'results': data})

    @extend_schema(tags=['Products'], summary='Get related products')
    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        product = self.get_object()
        data = ProductService.get_related(product)
        return Response({'success': True, 'results': data})

    def perform_create(self, serializer):
        serializer.save()
        ProductService.invalidate_cache()

    def perform_update(self, serializer):
        serializer.save()
        ProductService.invalidate_cache()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        ProductService.invalidate_cache()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Review.objects.select_related('user', 'product')
        product_id = self.request.query_params.get('product')
        if product_id:
            qs = qs.filter(product_id=product_id)
        if self.request.user.role != 'admin':
            qs = qs.filter(user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer

    @extend_schema(tags=['Reviews'])
    def create(self, request, *args, **kwargs):
        serializer = ReviewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = ReviewService.create_review(request.user, serializer.validated_data)
        return Response({
            'success': True,
            'review': ReviewSerializer(review).data,
        }, status=status.HTTP_201_CREATED)

    @extend_schema(tags=['Reviews'])
    def update(self, request, *args, **kwargs):
        serializer = ReviewCreateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        review = ReviewService.update_review(request.user, kwargs['pk'], serializer.validated_data)
        return Response({'success': True, 'review': ReviewSerializer(review).data})

    @extend_schema(tags=['Reviews'])
    def destroy(self, request, *args, **kwargs):
        ReviewService.delete_review(request.user, kwargs['pk'])
        return Response({'success': True, 'message': 'Review deleted.'}, status=status.HTTP_204_NO_CONTENT)


class WishlistViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Wishlist'])
    def list(self, request):
        items = WishlistService.get_wishlist(request.user)
        serializer = WishlistItemSerializer(items, many=True, context={'request': request})
        return Response({'success': True, 'results': serializer.data})

    @extend_schema(tags=['Wishlist'])
    @action(detail=False, methods=['post'], url_path='add/(?P<product_id>[^/.]+)')
    def add(self, request, product_id=None):
        item, created = WishlistService.add_to_wishlist(request.user, product_id)
        return Response({
            'success': True,
            'message': 'Added to wishlist.' if created else 'Already in wishlist.',
            'item': WishlistItemSerializer(item, context={'request': request}).data,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @extend_schema(tags=['Wishlist'])
    @action(detail=False, methods=['delete'], url_path='remove/(?P<product_id>[^/.]+)')
    def remove(self, request, product_id=None):
        WishlistService.remove_from_wishlist(request.user, product_id)
        return Response({'success': True, 'message': 'Removed from wishlist.'})

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdmin]

    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(tags=['Product Images'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(tags=['Product Images'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)