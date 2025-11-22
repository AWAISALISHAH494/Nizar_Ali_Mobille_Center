from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product, Category

User = get_user_model()


class PageView(models.Model):
    """Page view analytics model."""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40)
    url = models.URLField()
    referrer = models.URLField(blank=True)
    user_agent = models.TextField()
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Page view: {self.url} at {self.created_at}"


class ProductView(models.Model):
    """Product view analytics model."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Product view: {self.product.name} at {self.created_at}"


class SearchQuery(models.Model):
    """Search query analytics model."""
    query = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40)
    results_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Search: '{self.query}' ({self.results_count} results)"


class ConversionEvent(models.Model):
    """Conversion event analytics model."""
    EVENT_TYPES = [
        ('add_to_cart', 'Add to Cart'),
        ('remove_from_cart', 'Remove from Cart'),
        ('checkout_started', 'Checkout Started'),
        ('checkout_completed', 'Checkout Completed'),
        ('purchase', 'Purchase'),
        ('newsletter_signup', 'Newsletter Signup'),
    ]

    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_type} - {self.created_at}"


class UserActivity(models.Model):
    """User activity tracking model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50)
    description = models.TextField()
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.activity_type}"
