from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart admin."""
    list_display = ('id', 'user', 'session_key', 'total_items', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'session_key')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Cart item admin."""
    list_display = ('id', 'cart', 'product', 'variant', 'quantity', 'unit_price', 'total_price')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'cart__user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
