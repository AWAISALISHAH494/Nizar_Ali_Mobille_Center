from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Coupon


class ApplyCouponView(View):
    def post(self, request, *args, **kwargs):
        code = request.POST.get('coupon_code', '').strip()
        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid coupon code'}, status=400)

        if not coupon.is_valid():
            return JsonResponse({'success': False, 'message': 'Coupon is not valid'}, status=400)

        request.session['active_coupon'] = code
        return JsonResponse({'success': True, 'message': 'Coupon applied'})


class RemoveCouponView(View):
    def post(self, request, *args, **kwargs):
        request.session.pop('active_coupon', None)
        return JsonResponse({'success': True, 'message': 'Coupon removed'})


class ValidateCouponView(View):
    def post(self, request, *args, **kwargs):
        code = request.POST.get('coupon_code', '').strip()
        exists = Coupon.objects.filter(code__iexact=code, is_active=True).exists()
        return JsonResponse({'valid': exists})


