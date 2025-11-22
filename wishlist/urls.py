from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.WishlistView.as_view(), name='wishlist'),
    path('add/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('remove/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
    path('move-to-cart/', views.MoveToCartView.as_view(), name='move_to_cart'),
]
