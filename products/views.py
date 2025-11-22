from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Brand
from django.http import HttpResponse


class ProductListView(ListView):
    """Product list view with filtering and search."""
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(status='published').select_related('category', 'brand')
        
        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(sku__icontains=search_query)
            )
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Price filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Brand filter (allow multiple)
        brands = self.request.GET.getlist('brand') or ([] if not self.request.GET.get('brand') else [self.request.GET.get('brand')])
        if brands:
            queryset = queryset.filter(brand__slug__in=brands)

        # Rating filter (minimum stars)
        rating_min = self.request.GET.get('rating')
        if rating_min:
            try:
                rating_val = int(rating_min)
                queryset = queryset.filter(reviews__rating__gte=rating_val).distinct()
            except ValueError:
                pass
        
        # Sorting
        sort_by = self.request.GET.get('sort', 'relevance')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'popular':
            queryset = queryset.order_by('-reviews__count')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True, parent__isnull=True)
        context['brands'] = Brand.objects.filter(is_active=True)
        context['selected_brands'] = self.request.GET.getlist('brand')
        context['selected_rating'] = self.request.GET.get('rating', '')
        return context


class ProductDetailView(DetailView):
    """Product detail view."""
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Get related products
        related_products = Product.objects.filter(
            category=product.category,
            status='published'
        ).exclude(id=product.id)[:4]
        
        context['related_products'] = related_products
        return context


class CategoryDetailView(ListView):
    """Category detail view."""
    model = Product
    template_name = 'products/category_detail.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(
            category=self.category,
            status='published'
        ).select_related('brand')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProductSearchView(ListView):
    """Product search view."""
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(sku__icontains=query),
                status='published'
            ).select_related('category', 'brand')
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class ProductCompareView(ListView):
    """Product comparison view."""
    model = Product
    template_name = 'products/compare.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Get products from session
        compare_products = self.request.session.get('compare_products', [])
        return Product.objects.filter(id__in=compare_products)


def add_to_compare(request, product_id):
    """Add product to comparison list."""
    if 'compare_products' not in request.session:
        request.session['compare_products'] = []
    
    compare_products = request.session['compare_products']
    if len(compare_products) >= 4:
        return JsonResponse({'success': False, 'message': 'Maximum 4 products can be compared'})
    
    if product_id not in compare_products:
        compare_products.append(product_id)
        request.session['compare_products'] = compare_products
        request.session.modified = True
    
    return JsonResponse({'success': True, 'message': 'Product added to comparison'})


def remove_from_compare(request, product_id):
    """Remove product from comparison list."""
    compare_products = request.session.get('compare_products', [])
    if product_id in compare_products:
        compare_products.remove(product_id)
        request.session['compare_products'] = compare_products
        request.session.modified = True
    
    return JsonResponse({'success': True, 'message': 'Product removed from comparison'})


def product_quick_view(request, pk: int):
    """Return minimal HTML snippet for quick view modal."""
    product = get_object_or_404(Product, pk=pk)
    # Minimal, inline HTML. In a real app, render a template.
    first_image = product.images.first()
    image_url = first_image.image.url if first_image else ''
    html = f"""
    <div class=\"row g-3\">
      <div class=\"col-md-6\">
        {'<img src="' + image_url + '" class="img-fluid rounded" />' if image_url else '<div class=\"bg-light rounded d-flex align-items-center justify-content-center\" style=\"height:260px;\"><i class=\"fas fa-image fa-2x text-muted\"></i></div>'}
      </div>
      <div class=\"col-md-6\">
        <h5 class=\"mb-2\">{product.name}</h5>
        <div class=\"mb-2\"><span class=\"h5 text-primary\">${product.price}</span>{' <small class=\\"text-muted text-decoration-line-through ms-2\\">$' + str(product.compare_price) + '</small>' if product.compare_price else ''}</div>
        <p class=\"text-muted\">{product.short_description}</p>
        <a href=\"{product.get_absolute_url()}\" class=\"btn btn-primary\">View Details</a>
      </div>
    </div>
    """
    return HttpResponse(html)
