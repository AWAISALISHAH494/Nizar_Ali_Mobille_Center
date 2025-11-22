from django.contrib import admin
from .models import SiteSettings, Newsletter, ContactMessage, Banner


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Site settings admin."""
    list_display = ('site_name', 'email', 'phone', 'is_active', 'updated_at')
    list_filter = ('maintenance_mode', 'allow_registration', 'require_email_verification')
    search_fields = ('site_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    def is_active(self, obj):
        return not obj.maintenance_mode
    is_active.boolean = True
    is_active.short_description = 'Active'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Newsletter admin."""
    list_display = ('email', 'is_active', 'subscribed_at', 'unsubscribed_at')
    list_filter = ('is_active', 'subscribed_at', 'unsubscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at', 'unsubscribed_at')
    ordering = ('-subscribed_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Contact message admin."""
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """Banner admin."""
    list_display = ('title', 'position', 'is_active', 'sort_order', 'created_at')
    list_filter = ('position', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    ordering = ('sort_order', '-created_at')
