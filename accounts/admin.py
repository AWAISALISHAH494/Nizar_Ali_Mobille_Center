from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin."""
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Address admin."""
    list_display = ('user', 'first_name', 'last_name', 'city', 'state', 'is_default', 'address_type')
    list_filter = ('address_type', 'is_default', 'country')
    search_fields = ('user__email', 'first_name', 'last_name', 'city')
    ordering = ('-created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User profile admin."""
    list_display = ('user', 'newsletter_subscription', 'email_notifications')
    list_filter = ('newsletter_subscription', 'email_notifications', 'sms_notifications')
    search_fields = ('user__email',)
