from django.contrib import admin
from .models import Review, ReviewImage, ReviewHelpful


class ReviewImageInline(admin.TabularInline):
    """Review image inline."""
    model = ReviewImage
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review admin."""
    list_display = ('product', 'user', 'rating', 'title', 'is_approved', 'helpful_votes', 'created_at')
    list_filter = ('rating', 'is_approved', 'is_verified_purchase', 'created_at')
    search_fields = ('product__name', 'user__email', 'title', 'content')
    readonly_fields = ('created_at', 'updated_at', 'helpful_votes')
    inlines = [ReviewImageInline]
    ordering = ('-created_at',)


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    """Review image admin."""
    list_display = ('review', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('review__product__name', 'review__user__email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(ReviewHelpful)
class ReviewHelpfulAdmin(admin.ModelAdmin):
    """Review helpful admin."""
    list_display = ('review', 'user', 'is_helpful', 'created_at')
    list_filter = ('is_helpful', 'created_at')
    search_fields = ('review__product__name', 'user__email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
