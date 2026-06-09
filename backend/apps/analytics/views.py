from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin
from apps.orders.serializers import OrderListSerializer

from .services import AnalyticsService


class DashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(tags=['Analytics'], summary='Admin dashboard statistics')
    def get(self, request):
        stats = AnalyticsService.get_dashboard_stats()
        return Response({'success': True, 'stats': stats})


class MonthlySalesView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(tags=['Analytics'])
    def get(self, request):
        months = int(request.query_params.get('months', 12))
        data = AnalyticsService.get_monthly_sales(months)
        return Response({'success': True, 'results': data})


class TopProductsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(tags=['Analytics'])
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        data = AnalyticsService.get_top_products(limit)
        return Response({'success': True, 'results': data})


class TopCategoriesView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(tags=['Analytics'])
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        data = AnalyticsService.get_top_categories(limit)
        return Response({'success': True, 'results': data})


class RecentOrdersView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(tags=['Analytics'])
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        orders = AnalyticsService.get_recent_orders(limit)
        return Response({
            'success': True,
            'results': OrderListSerializer(orders, many=True).data,
        })


class SalesByStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(tags=['Analytics'])
    def get(self, request):
        data = AnalyticsService.get_sales_by_status()
        return Response({'success': True, 'results': data})
