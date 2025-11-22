from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
import paypalrestsdk

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Configure PayPal
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


@require_POST
def create_stripe_payment_intent(request):
    """Create Stripe payment intent."""
    try:
        # Get cart total
        if request.user.is_authenticated:
            from cart.models import Cart
            cart = Cart.objects.get(user=request.user)
            amount = int(cart.total_price * 100)  # Convert to cents
        else:
            amount = 10000  # Default amount for testing
        
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            metadata={
                'user_id': request.user.id if request.user.is_authenticated else None,
            }
        )
        
        return JsonResponse({
            'success': True,
            'client_secret': intent.client_secret
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Handle successful payment
        print(f"Payment succeeded: {payment_intent['id']}")
    
    return JsonResponse({'status': 'success'})


@require_POST
def create_paypal_order(request):
    """Create PayPal order."""
    try:
        # Get cart total
        if request.user.is_authenticated:
            from cart.models import Cart
            cart = Cart.objects.get(user=request.user)
            amount = cart.total_price
        else:
            amount = 100.00  # Default amount for testing
        
        # Create PayPal payment
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/payments/paypal/capture-order/'),
                "cancel_url": request.build_absolute_uri('/cart/')
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Order Total",
                        "sku": "order-total",
                        "price": str(amount),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(amount),
                    "currency": "USD"
                },
                "description": "Ecommerce order payment"
            }]
        })
        
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return JsonResponse({
                        'success': True,
                        'approval_url': approval_url
                    })
        
        return JsonResponse({
            'success': False,
            'message': 'Failed to create PayPal payment'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@require_POST
def capture_paypal_order(request):
    """Capture PayPal order."""
    try:
        payment_id = request.POST.get('paymentId')
        payer_id = request.POST.get('PayerID')
        
        payment = paypalrestsdk.Payment.find(payment_id)
        
        if payment.execute({"payer_id": payer_id}):
            # Payment successful
            return JsonResponse({
                'success': True,
                'message': 'Payment captured successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Payment execution failed'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@login_required
@require_POST
def create_refund(request, payment_id):
    """Create refund for payment."""
    try:
        # This would integrate with the actual payment system
        # For now, just return success
        return JsonResponse({
            'success': True,
            'message': 'Refund processed successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
