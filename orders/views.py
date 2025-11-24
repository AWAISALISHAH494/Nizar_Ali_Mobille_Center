import json
import logging
import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, TemplateView

from .models import Order, OrderItem, ShippingMethod, TaxRate
from .utils import calculate_delivery_charges, get_pakistan_cities
from cart.models import Cart, CartItem
from accounts.models import Address

logger = logging.getLogger(__name__)


class CheckoutView(TemplateView):
    """Checkout view."""
    template_name = 'orders/checkout.html'

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
        
        # Calculate delivery charges (default to 0 if no city selected)
        delivery_charges = Decimal('0.00')
        total_with_delivery = cart.total_price
        
        context['cart'] = cart
        context['delivery_charges'] = delivery_charges
        context['total_with_delivery'] = total_with_delivery
        context['pakistan_cities'] = get_pakistan_cities()
        context['free_delivery_threshold'] = Decimal('5000.00')
        return context

    def post(self, request, *args, **kwargs):
        """Process checkout form."""
        try:
            with transaction.atomic():
                # Get cart
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
                
                if not cart.items.exists():
                    messages.error(request, 'Your cart is empty')
                    return redirect('cart:cart')
                
                # Get city values from hidden fields (handled by JavaScript)
                billing_city_value = request.POST.get('billing_city', '').strip()
                shipping_city_value = request.POST.get('shipping_city', '').strip()
                billing_email = request.POST.get('billing_email', '').strip()
                
                if not billing_city_value:
                    messages.error(request, 'Please select or enter a billing city')
                    return redirect('orders:checkout')
                
                if not shipping_city_value:
                    messages.error(request, 'Please select or enter a shipping city')
                    return redirect('orders:checkout')
                
                # Create addresses
                billing_address = Address.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    address_type='billing',
                    first_name=request.POST.get('billing_first_name'),
                    last_name=request.POST.get('billing_last_name'),
                    address_line_1=request.POST.get('billing_address_line_1'),
                    address_line_2=request.POST.get('billing_address_line_2'),
                    city=billing_city_value,
                    state=request.POST.get('billing_state'),
                    postal_code=request.POST.get('billing_postal_code'),
                    country=request.POST.get('billing_country'),
                    phone_number=request.POST.get('billing_phone'),
                )
                
                shipping_address = Address.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    address_type='shipping',
                    first_name=request.POST.get('shipping_first_name'),
                    last_name=request.POST.get('shipping_last_name'),
                    address_line_1=request.POST.get('shipping_address_line_1'),
                    address_line_2=request.POST.get('shipping_address_line_2'),
                    city=shipping_city_value,
                    state=request.POST.get('shipping_state'),
                    postal_code=request.POST.get('shipping_postal_code'),
                    country=request.POST.get('shipping_country'),
                )
                
                # Calculate delivery charges based on shipping city
                delivery_charges = calculate_delivery_charges(shipping_city_value, cart.total_price)
                
                # Calculate total amount including delivery charges
                total_amount = cart.total_price + delivery_charges
                
                # Create order
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    order_number=str(uuid.uuid4())[:8].upper(),
                    billing_address=billing_address,
                    shipping_address=shipping_address,
                    subtotal=cart.total_price,
                    shipping_amount=delivery_charges,
                    total_amount=total_amount,
                    payment_status='pending',  # COD orders start as pending
                )
                
                # Create order items
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        variant=cart_item.variant,
                        quantity=cart_item.quantity,
                        unit_price=cart_item.unit_price,
                        total_price=cart_item.total_price,
                    )
                
                # Clear cart
                cart.items.all().delete()

                # Email customer about delivery charge payment
                customer_email = billing_email or (request.user.email if request.user.is_authenticated else '')
                customer_name = billing_address.first_name or billing_address.last_name
                transaction.on_commit(lambda: self._send_delivery_charge_email(
                    order=order,
                    customer_email=customer_email,
                    customer_name=customer_name,
                    delivery_charges=delivery_charges,
                    total_amount=total_amount
                ))
                
                messages.success(request, 'Order placed successfully!')
                # Pass order number to success page via session
                request.session['order_number'] = order.order_number
                return redirect('orders:checkout_success')
                
        except Exception as e:
            messages.error(request, f'Error processing order: {str(e)}')
            return redirect('cart:cart')

    def _send_delivery_charge_email(self, order, customer_email, customer_name, delivery_charges, total_amount):
        """Send COD delivery charge instructions to the customer."""
        if not customer_email:
            return

        site_name = getattr(settings, 'SITE_BRAND_NAME', 'LUNDKHWAR MOBILE CENTER')
        easypaisa_number = getattr(settings, 'EASYPAISA_NUMBER', '03129151970')
        jazzcash_number = getattr(settings, 'JAZZCASH_NUMBER', '03489278571')

        subject = f"{site_name} Order {order.order_number} - Delivery Charges"
        delivery_amount = f"{delivery_charges:.2f}"
        total_amount_display = f"{total_amount:.2f}"

        message_lines = [
            f"Assalam-o-Alaikum {customer_name or 'Customer'},",
            "",
            f"Thank you for placing order {order.order_number} at {site_name}.",
            f"To confirm your delivery we require an advance payment of Rs. {delivery_amount} for delivery charges.",
            "",
            "Please send the delivery charges using one of the following options:",
            f"- Easypaisa: {easypaisa_number}",
            f"- JazzCash: {jazzcash_number}",
            "",
            f"Total order amount: Rs. {total_amount_display}",
            "",
            "Once paid, reply to this email or WhatsApp us with the payment screenshot so we can dispatch your parcel promptly.",
            "",
            f"Shukriya,",
            f"{site_name} Team",
        ]

        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')

        try:
            send_mail(
                subject=subject,
                message="\n".join(message_lines),
                from_email=from_email,
                recipient_list=[customer_email],
                fail_silently=False,
            )
        except Exception as email_error:
            logger.warning("Failed to send delivery charge email for order %s: %s", order.order_number, email_error)


class CheckoutSuccessView(TemplateView):
    """Checkout success view."""
    template_name = 'orders/checkout_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get order number from session if available
        order_number = self.request.session.pop('order_number', None)
        context['order_number'] = order_number
        
        # Get the most recent order if user is authenticated
        if self.request.user.is_authenticated and order_number:
            try:
                from .models import Order
                order = Order.objects.get(order_number=order_number, user=self.request.user)
                context['order'] = order
            except Order.DoesNotExist:
                pass
        
        return context


class OrderDetailView(DetailView):
    """Order detail view."""
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()


@login_required
@require_POST
def cancel_order(request, pk):
    """Cancel order."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    
    if order.status in ['pending', 'processing']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully')
    else:
        messages.error(request, 'Cannot cancel this order')
    
    return redirect('orders:order_detail', pk=pk)


class OrderTrackView(DetailView):
    """Order tracking view."""
    model = Order
    template_name = 'orders/order_track.html'
    context_object_name = 'order'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()


@require_POST
def get_delivery_charges(request):
    """API endpoint to get delivery charges based on city and cart total."""
    try:
        data = json.loads(request.body)
        city = data.get('city', '')
        cart_total = Decimal(str(data.get('cart_total', '0.00')))
        
        delivery_charges = calculate_delivery_charges(city, cart_total)
        total_with_delivery = cart_total + delivery_charges
        
        return JsonResponse({
            'success': True,
            'delivery_charges': str(delivery_charges),
            'total_with_delivery': str(total_with_delivery),
            'is_free_delivery': delivery_charges == Decimal('0.00')
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
