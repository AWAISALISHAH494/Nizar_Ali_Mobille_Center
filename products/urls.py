from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    # Removed undefined ProductReviewsView route
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
    path('compare/', views.ProductCompareView.as_view(), name='product_compare'),
    # Wire to existing function-based views instead of undefined CBVs
    path('compare/add/<int:product_id>/', views.add_to_compare, name='add_to_compare'),
    path('compare/remove/<int:product_id>/', views.remove_from_compare, name='remove_from_compare'),
    path('<int:pk>/quick-view/', views.product_quick_view, name='product_quick_view'),
]
