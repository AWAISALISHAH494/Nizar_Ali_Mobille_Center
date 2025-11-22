from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product, ProductVariant


class CartView(TemplateView):
    """Shopping cart view."""
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # Get the most recent cart for the user
            cart = Cart.objects.filter(user=self.request.user).order_by('-created_at').first()
            if not cart:
                cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            # Get the most recent cart for the session
            cart = Cart.objects.filter(session_key=session_key).order_by('-created_at').first()
            if not cart:
                cart, created = Cart.objects.get_or_create(session_key=session_key)
        
        context['cart'] = cart
        return context


@require_POST
def add_to_cart(request):
    """Add product to cart."""
    try:
        # Check if user is authenticated or has session
        if not request.user.is_authenticated and not request.session.session_key:
            return JsonResponse({
                'success': False,
                'message': 'Please log in to add items to cart',
                'redirect': '/accounts/login/'
            })
        
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        variant_id = request.POST.get('variant_id')
        
        product = get_object_or_404(Product, id=product_id)
        variant = None
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
        
        # Get or create cart
        if request.user.is_authenticated:
            # Get the most recent cart for the user
            cart = Cart.objects.filter(user=request.user).order_by('-created_at').first()
            if not cart:
                cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            # Get the most recent cart for the session
            cart = Cart.objects.filter(session_key=session_key).order_by('-created_at').first()
            if not cart:
                cart, created = Cart.objects.get_or_create(session_key=session_key)
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_items_count': cart.total_items
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@require_POST
def update_cart(request):
    """Update cart item quantity."""
    try:
        # Check if user is authenticated or has session
        if not request.user.is_authenticated and not request.session.session_key:
            return JsonResponse({
                'success': False,
                'message': 'Please log in to update cart',
                'redirect': '/accounts/login/'
            })
        
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        # Verify cart ownership
        if request.user.is_authenticated:
            if cart_item.cart.user != request.user:
                return JsonResponse({
                    'success': False,
                    'message': 'Unauthorized access'
                })
        else:
            if cart_item.cart.session_key != request.session.session_key:
                return JsonResponse({
                    'success': False,
                    'message': 'Unauthorized access'
                })
        
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@require_POST
def remove_from_cart(request):
    """Remove item from cart."""
    try:
        # Check if user is authenticated or has session
        if not request.user.is_authenticated and not request.session.session_key:
            return JsonResponse({
                'success': False,
                'message': 'Please log in to remove items from cart',
                'redirect': '/accounts/login/'
            })
        
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        # Verify cart ownership
        if request.user.is_authenticated:
            if cart_item.cart.user != request.user:
                return JsonResponse({
                    'success': False,
                    'message': 'Unauthorized access'
                })
        else:
            if cart_item.cart.session_key != request.session.session_key:
                return JsonResponse({
                    'success': False,
                    'message': 'Unauthorized access'
                })
        
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@require_POST
def clear_cart(request):
    """Clear entire cart."""
    try:
        if request.user.is_authenticated:
            # Get the most recent cart for the user
            cart = Cart.objects.filter(user=request.user).order_by('-created_at').first()
            if not cart:
                return JsonResponse({
                    'success': False,
                    'message': 'Cart not found'
                })
        else:
            session_key = request.session.session_key
            if not session_key:
                return JsonResponse({
                    'success': False,
                    'message': 'Session not found'
                })
            # Get the most recent cart for the session
            cart = Cart.objects.filter(session_key=session_key).order_by('-created_at').first()
            if not cart:
                return JsonResponse({
                    'success': False,
                    'message': 'Cart not found'
                })
        
        cart.items.all().delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart cleared'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
