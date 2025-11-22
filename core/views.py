from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import SiteSettings, Newsletter, ContactMessage
from .forms import ContactForm, NewsletterForm
from products.models import Product, Category
from cart.models import Cart


class HomeView(TemplateView):
    """Home page view."""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(
            is_featured=True, status='published'
        )[:8]
        context['latest_products'] = Product.objects.filter(
            status='published'
        ).order_by('-created_at')[:8]
        return context


class AboutView(TemplateView):
    """About page view."""
    template_name = 'core/about.html'


class ContactView(FormView):
    """Contact page view."""
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)


class PrivacyPolicyView(TemplateView):
    """Privacy policy page view."""
    template_name = 'core/privacy_policy.html'


class TermsOfServiceView(TemplateView):
    """Terms of service page view."""
    template_name = 'core/terms_of_service.html'


class NewsletterSubscribeView(FormView):
    """Newsletter subscription view."""
    form_class = NewsletterForm
    success_url = '/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        newsletter, created = Newsletter.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )
        if created:
            messages.success(self.request, 'Successfully subscribed to newsletter!')
        else:
            messages.info(self.request, 'You are already subscribed to our newsletter!')
        return super().form_valid(form)


class NewsletterUnsubscribeView(TemplateView):
    """Newsletter unsubscribe view."""
    template_name = 'core/newsletter_unsubscribe.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if email:
            try:
                newsletter = Newsletter.objects.get(email=email)
                newsletter.is_active = False
                newsletter.save()
                messages.success(request, 'Successfully unsubscribed from newsletter!')
            except Newsletter.DoesNotExist:
                messages.error(request, 'Email not found in our newsletter list!')
        return redirect('core:newsletter_unsubscribe')


class SearchView(TemplateView):
    """Search results view."""
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        category = self.request.GET.get('category', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        sort_by = self.request.GET.get('sort', 'relevance')

        products = Product.objects.filter(status='published')

        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(short_description__icontains=query) |
                Q(sku__icontains=query)
            )

        if category:
            products = products.filter(category__slug=category)

        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)

        # Sorting
        if sort_by == 'price_low':
            products = products.order_by('price')
        elif sort_by == 'price_high':
            products = products.order_by('-price')
        elif sort_by == 'newest':
            products = products.order_by('-created_at')
        elif sort_by == 'popular':
            products = products.order_by('-reviews__count')

        # Pagination
        paginator = Paginator(products, 12)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'products': page_obj,
            'query': query,
            'category': category,
            'min_price': min_price,
            'max_price': max_price,
            'sort_by': sort_by,
            'categories': Category.objects.filter(is_active=True),
        })
        return context


class TestAccountView(TemplateView):
    """Test account styling view."""
    template_name = 'account/test.html'


class DatePickerDemoView(TemplateView):
    """Date picker demo view."""
    template_name = 'core/datepicker_demo.html'


class CalendarDemoView(TemplateView):
    """Calendar dropdown demo view."""
    template_name = 'core/calendar_demo.html'
