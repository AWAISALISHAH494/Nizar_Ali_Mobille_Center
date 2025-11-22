from django.core.cache import cache
from .models import SiteSettings
from products.models import Category
from cart.models import Cart
from django.contrib.sessions.models import Session
from wishlist.models import Wishlist


def cart(request):
    """Add cart information to context."""
    cart = None
    cart_items = 0
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if session_key:
            cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    if cart:
        cart_items = cart.total_items
    
    return {
        'cart': cart,
        'cart_items_count': cart_items,
    }


def categories(request):
    """Add categories to context."""
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.filter(is_active=True, parent__isnull=True)
        cache.set('categories', categories, 300)  # Cache for 5 minutes
    
    return {
        'categories': categories,
    }


def site_settings(request):
    """Add site settings to context."""
    settings = cache.get('site_settings')
    if not settings:
        settings = SiteSettings.objects.first()
        if settings:
            cache.set('site_settings', settings, 3600)  # Cache for 1 hour
    
    return {
        'site_settings': settings,
    }


def wishlist_product_ids(request):
    """Expose a set of product IDs that are in the current user's wishlist."""
    product_ids = set()
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        wishlist, _ = Wishlist.objects.get_or_create(user=user)
        product_ids = set(wishlist.items.values_list('product_id', flat=True))
    return {
        'wishlist_product_ids': product_ids,
    }
