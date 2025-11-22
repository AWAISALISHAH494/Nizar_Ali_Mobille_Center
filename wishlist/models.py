from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Wishlist(models.Model):
    """User wishlist model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    name = models.CharField(max_length=100, default='My Wishlist')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.name}"

    @property
    def total_items(self):
        return self.items.count()


class WishlistItem(models.Model):
    """Wishlist item model."""
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['wishlist', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.wishlist.name} - {self.product.name}"
