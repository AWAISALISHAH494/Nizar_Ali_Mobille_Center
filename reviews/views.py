from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import Review, ReviewImage
from products.models import Product


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')

        product = get_object_or_404(Product, id=product_id)
        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                'rating': rating,
                'title': title,
                'content': content,
                'is_verified_purchase': False,
                'is_approved': True,
            }
        )
        return JsonResponse({'success': True})


class MarkHelpfulView(LoginRequiredMixin, View):
    def post(self, request, review_id, *args, **kwargs):
        review = get_object_or_404(Review, id=review_id)
        review.helpful_votes += 1
        review.save(update_fields=['helpful_votes'])
        return JsonResponse({'success': True, 'helpful_votes': review.helpful_votes})


class AddReviewImageView(LoginRequiredMixin, View):
    def post(self, request, review_id, *args, **kwargs):
        review = get_object_or_404(Review, id=review_id, user=request.user)
        image_file = request.FILES.get('image')
        if not image_file:
            return JsonResponse({'success': False, 'message': 'Image file required'}, status=400)
        ReviewImage.objects.create(review=review, image=image_file)
        return JsonResponse({'success': True})


