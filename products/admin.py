from django.contrib import admin
from .models import (
    Category, Brand, Product, ProductImage, ProductVariant, 
    ProductAttribute, ProductAttributeValue, Inventory
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin."""
    list_display = ('name', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Brand admin."""
    list_display = ('name', 'website', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    """Product image inline."""
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    """Product variant inline."""
    model = ProductVariant
    extra = 1


class ProductAttributeValueInline(admin.TabularInline):
    """Product attribute value inline."""
    model = ProductAttributeValue
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin."""
    list_display = ('name', 'sku', 'price', 'category', 'brand', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'is_featured', 'is_digital', 'category', 'brand')
    search_fields = ('name', 'sku', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline, ProductAttributeValueInline]
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'short_description', 'sku')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_price', 'cost_price')
        }),
        ('Categorization', {
            'fields': ('category', 'brand')
        }),
        ('Physical Properties', {
            'fields': ('weight', 'dimensions')
        }),
        ('Status & Features', {
            'fields': ('status', 'is_featured', 'is_digital', 'track_inventory', 'allow_backorder')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Product image admin."""
    list_display = ('product', 'is_primary', 'sort_order', 'created_at')
    list_filter = ('is_primary',)
    ordering = ('product', 'sort_order')


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """Product variant admin."""
    list_display = ('product', 'name', 'sku', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'product__category')
    search_fields = ('product__name', 'name', 'sku')
    ordering = ('product', 'name')


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """Product attribute admin."""
    list_display = ('name', 'is_required', 'is_filterable', 'created_at')
    list_filter = ('is_required', 'is_filterable')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    """Product attribute value admin."""
    list_display = ('product', 'attribute', 'value', 'created_at')
    list_filter = ('attribute', 'product__category')
    search_fields = ('product__name', 'value')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    """Inventory admin."""
    list_display = ('product', 'variant', 'quantity', 'reserved_quantity', 'available_quantity', 'is_low_stock')
    list_filter = ('is_tracked', 'product__category')
    search_fields = ('product__name', 'variant__name')
    readonly_fields = ('available_quantity', 'is_low_stock', 'is_out_of_stock')
    
    def available_quantity(self, obj):
        return obj.available_quantity
    available_quantity.short_description = 'Available'
    
    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'
