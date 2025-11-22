from django.contrib import admin
from .models import Order, OrderItem, ShippingMethod, TaxRate, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    """Order item inline."""
    model = OrderItem
    readonly_fields = ('unit_price', 'total_price')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin."""
    list_display = ('order_number', 'user', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'user__email')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Order item admin."""
    list_display = ('order', 'product', 'variant', 'quantity', 'unit_price', 'total_price')
    list_filter = ('created_at',)
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    """Shipping method admin."""
    list_display = ('name', 'price', 'free_shipping_threshold', 'estimated_delivery', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    """Tax rate admin."""
    list_display = ('name', 'rate', 'country', 'state', 'is_active')
    list_filter = ('is_active', 'country')
    search_fields = ('name', 'country', 'state')
    ordering = ('country', 'state')


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    """Order status history admin."""
    list_display = ('order', 'status', 'created_at', 'created_by')
    list_filter = ('status', 'created_at')
    search_fields = ('order__order_number',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
