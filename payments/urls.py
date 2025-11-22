from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('stripe/create-payment-intent/', views.create_stripe_payment_intent, name='stripe_create_payment_intent'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('paypal/create-order/', views.create_paypal_order, name='paypal_create_order'),
    path('paypal/capture-order/', views.capture_paypal_order, name='paypal_capture_order'),
    path('refund/<int:payment_id>/', views.create_refund, name='create_refund'),
]
