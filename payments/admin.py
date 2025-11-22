from django.contrib import admin
from .models import Payment, Refund


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Payment admin."""
    list_display = ('id', 'order', 'payment_method', 'status', 'amount', 'currency', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('order__order_number', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at', 'processed_at')
    ordering = ('-created_at',)


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """Refund admin."""
    list_display = ('id', 'payment', 'amount', 'status', 'reason', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment__order__order_number', 'gateway_refund_id')
    readonly_fields = ('created_at', 'updated_at', 'processed_at')
    ordering = ('-created_at',)
