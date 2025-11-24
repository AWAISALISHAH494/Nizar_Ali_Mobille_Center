// Main JavaScript for Ecommerce Store

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 80
            }, 1000);
        }
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Add to cart functionality
    $('.add-to-cart').on('click', function(e) {
        e.preventDefault();
        var productId = $(this).data('product-id');
        var quantity = $(this).closest('.product-actions').find('.quantity-input').val() || 1;
        
        addToCart(productId, quantity);
    });

    // Add to wishlist functionality
    $('.add-to-wishlist').on('click', function(e) {
        e.preventDefault();
        var productId = $(this).data('product-id');
        
        addToWishlist(productId);
    });

    // Quantity controls
    $('.quantity-btn').on('click', function() {
        var input = $(this).siblings('.quantity-input');
        var currentVal = parseInt(input.val());
        
        if ($(this).hasClass('quantity-plus')) {
            input.val(currentVal + 1);
        } else if ($(this).hasClass('quantity-minus') && currentVal > 1) {
            input.val(currentVal - 1);
        }
    });

    // Search functionality
    $('#search-form').on('submit', function(e) {
        var query = $(this).find('input[name="q"]').val().trim();
        if (query.length < 2) {
            e.preventDefault();
            showAlert('Please enter at least 2 characters to search.', 'warning');
        }
    });

    // Newsletter subscription
    $('#newsletter-form').on('submit', function(e) {
        e.preventDefault();
        var email = $(this).find('input[name="email"]').val();
        
        if (isValidEmail(email)) {
            subscribeNewsletter(email);
        } else {
            showAlert('Please enter a valid email address.', 'warning');
        }
    });

    // Product image zoom
    $('.product-image').on('mouseenter', function() {
        $(this).addClass('zoom-in');
    }).on('mouseleave', function() {
        $(this).removeClass('zoom-in');
    });

    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Reveal-on-scroll animations for sections and footer
    if ('IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
        // Auto-apply to footer columns
        document.querySelectorAll('.footer-premium .row > [class^="col"], .footer-premium .row > [class*=" col"]').forEach(el => {
            el.classList.add('reveal');
            revealObserver.observe(el);
        });
    }
});

// Add to cart function
function addToCart(productId, quantity = 1) {
    $.ajax({
        url: '/cart/add/',
        method: 'POST',
        data: {
            'product_id': productId,
            'quantity': quantity,
            'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            if (response.success) {
                updateCartCount(response.cart_items_count);
                showAlert('Product added to cart!', 'success');
            } else {
                if (response.redirect) {
                    showAlert(response.message, 'warning');
                    setTimeout(() => {
                        window.location.href = response.redirect;
                    }, 2000);
                } else {
                    showAlert(response.message || 'Error adding product to cart', 'error');
                }
            }
        },
        error: function() {
            showAlert('Error adding product to cart', 'error');
        }
    });
}

// Add to wishlist function
function addToWishlist(productId) {
    $.ajax({
        url: '/wishlist/add/',
        method: 'POST',
        data: {
            'product_id': productId,
            'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            if (response.success) {
                showAlert('Product added to wishlist!', 'success');
            } else {
                showAlert(response.message || 'Error adding product to wishlist', 'error');
            }
        },
        error: function() {
            showAlert('Error adding product to wishlist', 'error');
        }
    });
}

// Update cart count
function updateCartCount(count) {
    $('.cart-count').text(count);
    $('.badge').text(count);
}

// Show alert function
function showAlert(message, type) {
    var alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    var alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('.container').first().prepend(alertHtml);
    
    // Auto-dismiss after 3 seconds
    setTimeout(function() {
        $('.alert').fadeOut();
    }, 3000);
}

// Email validation
function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Newsletter subscription
function subscribeNewsletter(email) {
    $.ajax({
        url: '/newsletter/subscribe/',
        method: 'POST',
        data: {
            'email': email,
            'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            showAlert('Successfully subscribed to newsletter!', 'success');
            $('#newsletter-form')[0].reset();
        },
        error: function() {
            showAlert('Error subscribing to newsletter', 'error');
        }
    });
}

// Product comparison
var compareProducts = [];

function addToCompare(productId) {
    if (compareProducts.length >= 4) {
        showAlert('You can compare maximum 4 products', 'warning');
        return;
    }
    
    if (compareProducts.includes(productId)) {
        showAlert('Product is already in comparison list', 'info');
        return;
    }
    
    compareProducts.push(productId);
    updateCompareButton();
    showAlert('Product added to comparison', 'success');
}

function removeFromCompare(productId) {
    compareProducts = compareProducts.filter(id => id !== productId);
    updateCompareButton();
    showAlert('Product removed from comparison', 'info');
}

function updateCompareButton() {
    $('.compare-btn').each(function() {
        var productId = $(this).data('product-id');
        if (compareProducts.includes(productId)) {
            $(this).addClass('btn-success').removeClass('btn-outline-primary');
            $(this).html('<i class="fas fa-check me-1"></i>Added');
        } else {
            $(this).addClass('btn-outline-primary').removeClass('btn-success');
            $(this).html('<i class="fas fa-balance-scale me-1"></i>Compare');
        }
    });
}

// Quick view modal
function showQuickView(productId) {
    const modal = document.getElementById('quickViewModal');
    if (!modal) return;
    modal.querySelector('.modal-body').innerHTML = '<div class="text-center py-5 text-muted">Loading...</div>';

    fetch(`/products/${productId}/quick-view/`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(res => res.text())
      .then(html => {
        modal.querySelector('.modal-body').innerHTML = html;
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
      })
      .catch(() => {
        showAlert('Error loading product details', 'error');
      });
}

// Price filter
function filterByPrice() {
    var minPrice = $('#min-price').val();
    var maxPrice = $('#max-price').val();
    
    if (minPrice && maxPrice && parseFloat(minPrice) > parseFloat(maxPrice)) {
        showAlert('Minimum price cannot be greater than maximum price', 'warning');
        return;
    }
    
    // Reload page with price filters
    var url = new URL(window.location);
    if (minPrice) url.searchParams.set('min_price', minPrice);
    if (maxPrice) url.searchParams.set('max_price', maxPrice);
    window.location.href = url.toString();
}

// Sort products
function sortProducts(sortBy) {
    var url = new URL(window.location);
    url.searchParams.set('sort', sortBy);
    window.location.href = url.toString();
}

// Pagination
function goToPage(page) {
    var url = new URL(window.location);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}

// Mobile menu toggle
function toggleMobileMenu() {
    $('.mobile-menu').toggleClass('active');
    $('body').toggleClass('menu-open');
}

// Back to top button
$(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
        $('.back-to-top').fadeIn();
    } else {
        $('.back-to-top').fadeOut();
    }
});

$('.back-to-top').click(function() {
    $('html, body').animate({scrollTop: 0}, 800);
    return false;
});

// Form validation
function validateForm(formId) {
    var form = document.getElementById(formId);
    if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
    }
    form.classList.add('was-validated');
}

// Loading states
function showLoading(element) {
    $(element).prop('disabled', true);
    $(element).html('<span class="spinner-border spinner-border-sm me-2"></span>Loading...');
}

function hideLoading(element, originalText) {
    $(element).prop('disabled', false);
    $(element).html(originalText);
}

// Cookie consent
function acceptCookies() {
    localStorage.setItem('cookieConsent', 'accepted');
    $('.cookie-consent').fadeOut();
}

function checkCookieConsent() {
    if (!localStorage.getItem('cookieConsent')) {
        $('.cookie-consent').fadeIn();
    }
}

// Initialize cookie consent
$(document).ready(function() {
    checkCookieConsent();
});

// Export functions for global use
window.addToCart = addToCart;
window.addToWishlist = addToWishlist;
window.showAlert = showAlert;
window.addToCompare = addToCompare;
window.removeFromCompare = removeFromCompare;
window.showQuickView = showQuickView;
window.filterByPrice = filterByPrice;
window.sortProducts = sortProducts;
window.acceptCookies = acceptCookies;
