from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    path('sales/', views.SalesAnalyticsView.as_view(), name='sales'),
    path('products/', views.ProductAnalyticsView.as_view(), name='products'),
    path('customers/', views.CustomerAnalyticsView.as_view(), name='customers'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
]
