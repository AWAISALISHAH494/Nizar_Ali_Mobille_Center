from django.contrib import admin
from .models import Wishlist, WishlistItem


class WishlistItemInline(admin.TabularInline):
    """Wishlist item inline."""
    model = WishlistItem
    extra = 0


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Wishlist admin."""
    list_display = ('user', 'name', 'is_public', 'total_items', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('user__email', 'name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [WishlistItemInline]
    ordering = ('-created_at',)


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    """Wishlist item admin."""
    list_display = ('wishlist', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('wishlist__user__email', 'product__name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
