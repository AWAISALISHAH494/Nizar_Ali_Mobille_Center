from django.views.generic import TemplateView


class AnalyticsDashboardView(TemplateView):
    template_name = 'analytics/dashboard.html'


class SalesAnalyticsView(TemplateView):
    template_name = 'analytics/sales.html'


class ProductAnalyticsView(TemplateView):
    template_name = 'analytics/products.html'


class CustomerAnalyticsView(TemplateView):
    template_name = 'analytics/customers.html'


class ReportsView(TemplateView):
    template_name = 'analytics/reports.html'


