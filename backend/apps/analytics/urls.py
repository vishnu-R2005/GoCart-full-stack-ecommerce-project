from django.urls import path

from .views import (
    DashboardView,
    MonthlySalesView,
    RecentOrdersView,
    SalesByStatusView,
    TopCategoriesView,
    TopProductsView,
)

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='analytics-dashboard'),
    path('monthly-sales/', MonthlySalesView.as_view(), name='analytics-monthly-sales'),
    path('top-products/', TopProductsView.as_view(), name='analytics-top-products'),
    path('top-categories/', TopCategoriesView.as_view(), name='analytics-top-categories'),
    path('recent-orders/', RecentOrdersView.as_view(), name='analytics-recent-orders'),
    path('sales-by-status/', SalesByStatusView.as_view(), name='analytics-sales-by-status'),
]
