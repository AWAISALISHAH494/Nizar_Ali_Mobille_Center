from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/success/', views.CheckoutSuccessView.as_view(), name='checkout_success'),
    path('checkout/get-delivery-charges/', views.get_delivery_charges, name='get_delivery_charges'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/cancel/', views.cancel_order, name='order_cancel'),
    path('<int:pk>/track/', views.OrderTrackView.as_view(), name='order_track'),
]
