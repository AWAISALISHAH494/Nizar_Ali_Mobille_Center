from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import User, Address, UserProfile
from orders.models import Order


class ProfileView(LoginRequiredMixin, DetailView):
    """User profile view."""
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit user profile."""
    model = User
    template_name = 'accounts/profile_edit.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'avatar']
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


class AddressListView(LoginRequiredMixin, ListView):
    """User addresses list."""
    model = Address
    template_name = 'accounts/address_list.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    """Create new address."""
    model = Address
    template_name = 'accounts/address_form.html'
    fields = ['address_type', 'first_name', 'last_name', 'company', 'address_line_1', 
              'address_line_2', 'city', 'state', 'postal_code', 'country', 'phone_number', 'is_default']
    success_url = reverse_lazy('accounts:address_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Address added successfully!')
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    """Update address."""
    model = Address
    template_name = 'accounts/address_form.html'
    fields = ['address_type', 'first_name', 'last_name', 'company', 'address_line_1', 
              'address_line_2', 'city', 'state', 'postal_code', 'country', 'phone_number', 'is_default']
    success_url = reverse_lazy('accounts:address_list')

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Address updated successfully!')
        return super().form_valid(form)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    """Delete address."""
    model = Address
    template_name = 'accounts/address_confirm_delete.html'
    success_url = reverse_lazy('accounts:address_list')

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Address deleted successfully!')
        return super().delete(request, *args, **kwargs)


class OrderListView(LoginRequiredMixin, ListView):
    """User orders list."""
    model = Order
    template_name = 'accounts/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    """Order detail view."""
    model = Order
    template_name = 'accounts/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
