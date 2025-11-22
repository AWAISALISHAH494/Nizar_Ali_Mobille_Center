from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product, ProductVariant

User = get_user_model()


class Cart(models.Model):
    """Shopping cart model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(user__isnull=False),
                name='unique_user_cart'
            ),
            models.UniqueConstraint(
                fields=['session_key'],
                condition=models.Q(session_key__isnull=False),
                name='unique_session_cart'
            ),
        ]

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.email}"
        return f"Cart {self.id}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def is_empty(self):
        return self.items.count() == 0


class CartItem(models.Model):
    """Cart item model."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['cart', 'product', 'variant']

    def __str__(self):
        variant_text = f" - {self.variant.name}" if self.variant else ""
        return f"{self.product.name}{variant_text} x {self.quantity}"

    @property
    def unit_price(self):
        if self.variant:
            return self.variant.final_price
        return self.product.price

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.variant and self.variant.product != self.product:
            raise ValidationError("Variant must belong to the selected product.")
