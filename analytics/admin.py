from django.contrib import admin
from .models import PageView, ProductView, SearchQuery, ConversionEvent, UserActivity


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    """Page view admin."""
    list_display = ('url', 'user', 'ip_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('url', 'user__email', 'ip_address')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    """Product view admin."""
    list_display = ('product', 'user', 'ip_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'user__email', 'ip_address')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    """Search query admin."""
    list_display = ('query', 'user', 'results_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('query', 'user__email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(ConversionEvent)
class ConversionEventAdmin(admin.ModelAdmin):
    """Conversion event admin."""
    list_display = ('event_type', 'user', 'product', 'value', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('user__email', 'product__name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """User activity admin."""
    list_display = ('user', 'activity_type', 'description', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__email', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
