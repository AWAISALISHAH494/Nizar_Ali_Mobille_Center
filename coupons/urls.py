from django.urls import path
from . import views

app_name = 'coupons'

urlpatterns = [
    path('apply/', views.ApplyCouponView.as_view(), name='apply_coupon'),
    path('remove/', views.RemoveCouponView.as_view(), name='remove_coupon'),
    path('validate/', views.ValidateCouponView.as_view(), name='validate_coupon'),
]
