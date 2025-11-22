from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms_of_service'),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('newsletter/unsubscribe/', views.NewsletterUnsubscribeView.as_view(), name='newsletter_unsubscribe'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('test-account/', views.TestAccountView.as_view(), name='test_account'),
    path('datepicker-demo/', views.DatePickerDemoView.as_view(), name='datepicker_demo'),
    path('calendar-demo/', views.CalendarDemoView.as_view(), name='calendar_demo'),
]
