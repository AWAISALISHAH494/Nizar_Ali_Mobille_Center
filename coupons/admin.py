from django.contrib import admin
from .models import Coupon, CouponUsage, DiscountCampaign


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Coupon admin."""
    list_display = ('code', 'discount_type', 'discount_value', 'usage_count', 'usage_limit', 'is_active', 'valid_from', 'valid_until')
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_until')
    search_fields = ('code', 'description')
    readonly_fields = ('usage_count', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    """Coupon usage admin."""
    list_display = ('coupon', 'user', 'order', 'discount_amount', 'used_at')
    list_filter = ('used_at',)
    search_fields = ('coupon__code', 'user__email', 'order__order_number')
    readonly_fields = ('used_at',)
    ordering = ('-used_at',)


@admin.register(DiscountCampaign)
class DiscountCampaignAdmin(admin.ModelAdmin):
    """Discount campaign admin."""
    list_display = ('name', 'is_active', 'valid_from', 'valid_until', 'created_at')
    list_filter = ('is_active', 'valid_from', 'valid_until')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
